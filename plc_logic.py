from pymodbus.client import ModbusTcpClient
import logging
from scada_db import get_or_create_card, has_access, record_rfid_event


logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.WARNING)


class PLCManager:
    """
    Manages the connection and data exchange with the PLC via Modbus TCP.
    This version is optimized for bulk read/write operations and includes RFID handling.
    """

    def __init__(self, ip: str, port: int):
        """Initializes the PLC manager and defines memory mappings."""
        self.client = ModbusTcpClient(ip, port=port)
        self.ip = ip
        self.port = port
        self._define_mappings()
        self._last_written_controls = {}

    def _define_mappings(self):
        """
        Defines mappings from application state attributes to PLC addresses
        and groups them into efficient, contiguous blocks for bulk reading.
        """
        self.read_coils_map = {
            'l_mvmnt': 212, 'l_smoke': 221, 'l_light': 234, 'l_door_open': 202,
            'l_rfid_ok': 226, 'l_security': 215,
            'o1_mvmnt': 214, 'o1_smoke': 218, 'o1_door_open': 203, 'o1_rfid_ok': 227,
            'o2_mvmnt': 214, 'o2_smoke': 219, 'o2_door_open': 204, 'o2_rfid_ok': 228,
            'o3_mvmnt': 214, 'o3_smoke': 220, 'o3_door_open': 205, 'o3_rfid_ok': 229,
            'o3_heating': 232, 'o3_cooling': 233,
            'c1_mvmnt': 213, 'c1_smoke': 222, 'c1_light': 235,
            'c2_mvmnt': 213, 'c2_smoke': 223, 'c2_light': 235,
            'p_inside_cycle': 13, 'p_outside_cycle': 14,
            'p_gate_closed': 207, 'p_obj_det': 208,
            'p_gate_open': 230, 'p_gate_close': 231,
            'p_full_bulb': 239,
            'call_fire_dept': 238, 'call_security': 237, 'fire_sprinklers_on': 236,
            'warn_config_altered': 495, 'warn_auto_security_impossible': 496,
            'warn_fire_det': 497, 'warn_pgate_open': 498, 'warn_pspot_miscount': 499,
            'err_light_config': 505, 'err_pgate_force': 506, 'err_pspot_config': 507,
            'err_temp_config': 508, 'err_work_day_config': 509,
            'err_cold_month_config': 510, 'emergency': 511,
        }
        self.read_registers_map = {
            'p_spots_taken': 9, 'p_spots_total': 8,
            'o3_temp': 200, 'measured_light': 201,
        }

        self.coil_read_blocks = [
            (13, 2),  # Coils from M13 to M14
            (202, 38),  # Coils from M202 to M239
            (495, 17)  # Coils from M495 to M511
        ]
        self.register_read_blocks = [
            (8, 2),  # Registers from MW8 to MW9
            (200, 2)  # Registers from MW200 to MW201
        ]

    def connect(self):
        """Establishes a connection to the PLC if not already open."""
        if not self.client.is_socket_open():
            return self.client.connect()
        return True

    @staticmethod
    def _scale_temp_for_write(deg_c: float) -> int:
        """Scales Celsius temperature for PLC register (e.g., 23.5°C -> 735)."""
        return int((float(deg_c) + 50.0) * 10.0)

    @staticmethod
    def _scale_temp_for_read(raw: int) -> float:
        """Scales PLC register value back to Celsius."""
        return raw / 10.0 - 50.0

    @staticmethod
    def _scale_temp_tol_for_write(raw: str) -> int:
        """Scales PLC register value back to Celsius."""
        return int(float(raw)) * 10

    @staticmethod
    def _scale_lux_for_write(lux: float) -> int:
        """Scales lux value (0-100000) for PLC register (0-1000)."""
        lux = max(0.0, min(100000.0, float(lux)))
        return int(lux / 100.0)

    @staticmethod
    def _scale_lux_for_read(raw: int) -> float:
        """Scales PLC register value back to lux."""
        return raw * 100.0

    def update(self, state):
        """
        Reads data from and writes data to the PLC in a single, optimized update cycle.
        """
        if not self.connect():
            if state.plc_connected:
                state.plc_connected = False
                state.reset_to_defaults()
            return

        if not state.plc_connected:
            state.plc_connected = True
            state.config_altered = True

        try:
            self._write_to_plc(state)
            self._read_from_plc(state)
        except Exception as e:
            print(f"PLC Communication Error: {e}")
            self.client.close()
            state.plc_connected = False
            state.reset_to_defaults()

    def _read_from_plc(self, state):
        """Reads all required data points from the PLC using optimized block requests."""
        for start_addr, count in self.coil_read_blocks:
            response = self.client.read_coils(start_addr, count=count)
            if not response.isError():
                bits = response.bits
                for attr, addr in self.read_coils_map.items():
                    if start_addr <= addr < start_addr + count:
                        index = addr - start_addr
                        if 0 <= index < len(bits):
                            setattr(state, attr, bits[index])

        for start_addr, count in self.register_read_blocks:
            response = self.client.read_holding_registers(start_addr, count=count)
            if not response.isError():
                regs = response.registers
                for attr, addr in self.read_registers_map.items():
                    if start_addr <= addr < start_addr + count:
                        index = addr - start_addr
                        if 0 <= index < len(regs):
                            setattr(state, attr, regs[index])

    def _process_rfid_request(self, req_coil, regs_req, resp_coil, regs_resp, location):
        """
        If the PLC has raised req_coil, read the card number from regs_req,
        look up access rights in the DB, write a response to regs_resp,
        raise resp_coil, log the event, and clear the request coil.
        """
        req_bit_resp = self.client.read_coils(req_coil, count=1)
        if req_bit_resp.isError() or not req_bit_resp.bits[0]:
            return

        card_regs_resp = self.client.read_holding_registers(regs_req[0], count=3)
        if card_regs_resp.isError():
            return

        x, y, z = card_regs_resp.registers
        full_card_value = (x << 32) | (y << 16) | z
        card_str = f"{full_card_value:010d}"

        card_id = get_or_create_card(card_str)
        has_permission = has_access(card_id, location) if card_id is not None else False
        if card_id is not None:
            record_rfid_event(location, card_id, has_permission)

        if has_permission:
            resp_vals = [x, y, z]
        else:
            resp_vals = [0, 0, 0]
        self.client.write_registers(regs_resp[0], resp_vals)

        self.client.write_coil(resp_coil, True)

        self.client.write_coil(req_coil, False)

    def _write_to_plc(self, state):
        """
        Writes data to the PLC, handling RFID, immediate controls, and configuration.
        """

        self._process_rfid_request(
            req_coil=100, regs_req=(100, 101, 102),
            resp_coil=101, regs_resp=(103, 104, 105),
            location="Lobby",
        )
        self._process_rfid_request(
            req_coil=106, regs_req=(106, 107, 108),
            resp_coil=107, regs_resp=(109, 110, 111),
            location="Office 1",
        )
        self._process_rfid_request(
            req_coil=112, regs_req=(112, 113, 114),
            resp_coil=113, regs_resp=(115, 116, 117),
            location="Office 2",
        )
        self._process_rfid_request(
            req_coil=118, regs_req=(118, 119, 120),
            resp_coil=119, regs_resp=(121, 122, 123),
            location="Office 3",
        )
        self._process_rfid_request(
            req_coil=124, regs_req=(124, 125, 126),
            resp_coil=125, regs_resp=(127, 128, 129),
            location="Parking lot",
        )

        control_coils = {
            128: state.force_park_open,
            129: state.force_park_close,
            226: state.force_lobby_door,
        }
        for addr, value in control_coils.items():
            if self._last_written_controls.get(addr) != value:
                self.client.write_coil(addr, value)
                self._last_written_controls[addr] = value

        spots_taken_value = int(state.p_spots_taken)
        if self._last_written_controls.get(9) != spots_taken_value:
            self.client.write_register(9, spots_taken_value)
            self._last_written_controls[9] = spots_taken_value

        if not state.config_altered:
            return

        work_day_vals = [state.cfg_heat_off_days] + state.cfg_work_days
        self.client.write_coils(0, work_day_vals)

        test_mode_vals = [state.cfg_test_fire, state.cfg_test_security]
        self.client.write_coils(26, test_mode_vals)

        self.client.write_coil(28, state.cfg_auto_lights_lobby)
        self.client.write_coil(29, state.cfg_wdonly_lights_l)
        self.client.write_coil(32, state.cfg_lobby_lights_mode == 'movement')
        self.client.write_coil(35, state.cfg_auto_lights_bldg)
        self.client.write_coil(36, state.cfg_wdonly_lights_b)
        self.client.write_coil(39, state.cfg_bldg_lights_mode == 'movement')

        self.client.write_coil(199, state.cfg_sim_io)

        temp_config_vals = [
            self._scale_temp_for_write(state.cfg_work_temp),
            self._scale_temp_tol_for_write(state.cfg_work_temp_tol),
            self._scale_temp_for_write(state.cfg_non_work_temp),
            int(state.cfg_work_start),
            int(state.cfg_work_end),
            int(state.cfg_cold_start),
            int(state.cfg_cold_end)
        ]

        self.client.write_registers(0, temp_config_vals)

        self.client.write_registers(14, [
            self._scale_lux_for_write(state.cfg_light_thresh),
            self._scale_lux_for_write(state.cfg_light_tol),
        ])

        self.client.write_register(8, int(state.cfg_park_spots))
        self.client.write_register(10, int(state.cfg_max_park_spots))

        self.client.write_coil(495, True)

        state.config_altered = False
