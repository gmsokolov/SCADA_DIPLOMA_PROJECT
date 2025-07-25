# app_state.py

class AppState:
    def __init__(self):
        self.lang = 'en'
        self.ui_refs = {}
        self.plc_connected = False
        self.config_altered = False
        self.l_mvmnt = False
        self.l_smoke = False
        self.l_light = False
        self.l_door_open = False
        self.l_rfid_ok = False
        self.l_security = False
        self.o1_smoke = False
        self.o1_mvmnt = False
        self.o1_door_open = False
        self.o1_rfid_ok = False
        self.o2_smoke = False
        self.o2_mvmnt = False
        self.o2_door_open = False
        self.o2_rfid_ok = False
        self.c1_smoke = False
        self.c1_mvmnt = False
        self.c1_light = False
        self.o3_smoke = False
        self.o3_mvmnt = False
        self.o3_door_open = False
        self.o3_rfid_ok = False
        self.o3_heating = False
        self.o3_cooling = False
        self.o3_temp = 0
        self.c2_smoke = False
        self.c2_mvmnt = False
        self.c2_light = False
        self.p_spots_total = 0
        self.p_spots_taken = 0
        self.p_obj_det = False
        self.p_gate_open = False
        self.p_gate_closed = True
        self.p_gate_close = False
        self.p_inside_cycle = False
        self.p_outside_cycle = False
        self.p_full_bulb = False
        self.force_lobby_door = False
        self.force_park_open = False
        self.force_park_close = False
        self.warn_config_altered = False
        self.warn_auto_security_impossible = False
        self.warn_fire_det = False
        self.warn_pgate_open = False
        self.warn_pspot_miscount = False
        self.err_light_config = False
        self.err_pgate_force = False
        self.err_pspot_config = False
        self.err_temp_config = False
        self.err_work_day_config = False
        self.err_cold_month_config = False
        self.call_security = False
        self.call_fire_dept = False
        self.fire_sprinklers_on = False
        self.emergency = False
        self.cfg_work_days = [False] * 7
        self.cfg_work_start = "0"
        self.cfg_work_end = "0"
        self.cfg_heat_off_days = False
        self.cfg_cold_start = "0"
        self.cfg_cold_end = "0"
        self.cfg_work_temp = "0.0"
        self.cfg_work_temp_tol = "0.0"
        self.cfg_non_work_temp = "0.0"
        self.cfg_park_spots = "0"
        self.cfg_max_park_spots = "0"
        self.cfg_light_thresh = "0"
        self.cfg_light_tol = "0"
        self.cfg_auto_lights_lobby = False
        self.cfg_wdonly_lights_l = False
        self.cfg_lobby_lights_mode = "dark"
        self.cfg_auto_lights_bldg = False
        self.cfg_wdonly_lights_b = False
        self.cfg_bldg_lights_mode = "dark"
        self.cfg_sim_io = False
        self.cfg_test_fire = False
        self.cfg_test_security = False
        self.measured_light = 0

    def get_snapshot(self):
        """Creates a copy of the current state data."""
        snapshot = AppState()
        for attr, value in self.__dict__.items():
            if attr != 'ui_refs':
                if isinstance(value, list):
                    setattr(snapshot, attr, value[:])
                else:
                    setattr(snapshot, attr, value)
        return snapshot

    def reset_to_defaults(self):
        """Resets dynamic values to their default state, typically on PLC disconnect."""
        self.plc_connected = False
        self.l_mvmnt = False
        self.l_smoke = False
        self.l_light = False
        self.l_door_open = False
        self.l_rfid_ok = False
        self.l_security = False
        self.o1_smoke = False
        self.o1_mvmnt = False
        self.o1_door_open = False
        self.o1_rfid_ok = False
        self.o2_smoke = False
        self.o2_mvmnt = False
        self.o2_door_open = False
        self.o2_rfid_ok = False
        self.c1_smoke = False
        self.c1_mvmnt = False
        self.c1_light = False
        self.o3_smoke = False
        self.o3_mvmnt = False
        self.o3_door_open = False
        self.o3_rfid_ok = False
        self.o3_heating = False
        self.o3_cooling = False
        self.o3_temp = 0
        self.c2_smoke = False
        self.c2_mvmnt = False
        self.c2_light = False
        self.p_spots_total = int(self.cfg_park_spots) if self.cfg_park_spots.isdigit() else 0
        self.p_spots_taken = 0
        self.p_obj_det = False
        self.p_gate_open = False
        self.p_gate_closed = True
        self.p_gate_close = False
        self.p_inside_cycle = False
        self.p_outside_cycle = False
        self.p_full_bulb = False
        self.measured_light = 0
        self.warn_config_altered = False
        self.warn_auto_security_impossible = False
        self.warn_fire_det = False
        self.warn_pgate_open = False
        self.warn_pspot_miscount = False
        self.err_light_config = False
        self.err_pgate_force = False
        self.err_pspot_config = False
        self.err_temp_config = False
        self.err_work_day_config = False
        self.err_cold_month_config = False
        self.call_security = False
        self.call_fire_dept = False
        self.fire_sprinklers_on = False
        self.emergency = False
