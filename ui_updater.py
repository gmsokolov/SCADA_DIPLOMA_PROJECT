import flet as ft
from definitions import ALERT_TEXTS, ALERT_DEFS


def update_icon(key, state, status, on_icon, off_icon, on_color, on_tooltip, off_tooltip):
    icon_ctrl = state.ui_refs.get(key)
    if icon_ctrl:
        if status:
            icon_ctrl.icon, icon_ctrl.icon_color, icon_ctrl.tooltip = on_icon, ft.Colors.ON_SECONDARY_CONTAINER, on_tooltip
            icon_ctrl.style = ft.ButtonStyle(elevation=0.5, shadow_color=on_color,
                                             padding=0, shape=ft.CircleBorder(),
                                             overlay_color=None)
        else:
            icon_ctrl.icon, icon_ctrl.icon_color, icon_ctrl.tooltip = off_icon, ft.Colors.GREY, off_tooltip
            icon_ctrl.style = ft.ButtonStyle(elevation=0, padding=0, shape=ft.CircleBorder(),
                                             overlay_color=ft.Colors.TRANSPARENT)


def update_app_bar(state, get_text):
    """Updates the PLC status icon in the AppBar."""
    plc_icon = state.ui_refs.get("plc_status_icon")
    if plc_icon:
        is_connected = state.plc_connected
        plc_icon.icon = ft.Icons.PHONELINK if is_connected else ft.Icons.PHONELINK_OFF
        plc_icon.icon_color = ft.Colors.GREEN_ACCENT_700 if is_connected else ft.Colors.RED_ACCENT
        plc_icon.tooltip = get_text("plc_connected") if is_connected else get_text("plc_disconnected")


def update_dashboard_ui(state, get_text):
    """Updates all dynamic controls on the dashboard view."""
    if not state.ui_refs:
        return

    if 'force_open_switch' in state.ui_refs:
        state.ui_refs['force_open_switch'].value = state.force_park_open
    if 'force_close_switch' in state.ui_refs:
        state.ui_refs['force_close_switch'].value = state.force_park_close

    alarm_on = state.l_security
    l_color = ft.Colors.RED_600 if state.l_smoke or ((state.l_mvmnt or state.l_door_open) and alarm_on) else ft.Colors.TRANSPARENT
    o1_color = ft.Colors.RED_600 if state.o1_smoke or ((state.o1_mvmnt or state.o1_door_open) and alarm_on) else ft.Colors.TRANSPARENT
    o2_color = ft.Colors.RED_600 if state.o2_smoke or ((state.o2_mvmnt or state.o2_door_open) and alarm_on) else ft.Colors.with_opacity(0.13, ft.Colors.INVERSE_PRIMARY)
    c1_color = ft.Colors.RED_600 if state.c1_smoke or (state.c2_mvmnt and alarm_on) else ft.Colors.ON_INVERSE_SURFACE
    o3_color = ft.Colors.RED_600 if state.o3_smoke or ((state.o2_mvmnt or state.o2_door_open) and alarm_on) else ft.Colors.TRANSPARENT
    c2_color = ft.Colors.RED_600 if state.c2_smoke or (state.c2_mvmnt and alarm_on) else ft.Colors.ON_INVERSE_SURFACE

    for key, color in [('o1_container', o1_color), ('o2_container', o2_color), ('c1_container', c1_color),
                       ('lobby_container', l_color), ('o3_container', o3_color), ('c2_container', c2_color)]:
        if key in state.ui_refs:
            for ctrl in state.ui_refs[key]:
                ctrl.bgcolor = color

    update_icon('l_mvmnt_icon', state, state.l_mvmnt, ft.Icons.PERSON, ft.Icons.PERSON_OUTLINE,
                ft.Colors.BLUE_ACCENT, get_text("movement_detected"), get_text("no_movement"))
    update_icon('l_smoke_icon', state, state.l_smoke, ft.Icons.LOCAL_FIRE_DEPARTMENT,
                ft.Icons.LOCAL_FIRE_DEPARTMENT_OUTLINED, ft.Colors.ORANGE_ACCENT, get_text("smoke_detected"),
                get_text("no_smoke"))
    update_icon('l_light_icon', state, state.l_light, ft.Icons.LIGHTBULB, ft.Icons.LIGHTBULB_OUTLINE,
                ft.Colors.YELLOW, get_text("light_on"), get_text("light_off"))
    update_icon('l_door_icon', state, state.l_door_open, ft.Icons.DOOR_FRONT_DOOR, ft.Icons.DOOR_FRONT_DOOR_OUTLINED,
                ft.Colors.RED_ACCENT, get_text("door_open"), get_text("door_closed_tooltip"))
    update_icon('l_rfid_icon', state, state.l_rfid_ok, ft.Icons.LOCK_PERSON, ft.Icons.LOCK_PERSON_OUTLINED,
                ft.Colors.GREEN_ACCENT, get_text("rfid_accepted"), get_text("no_card"))
    update_icon('l_sec_icon', state, state.l_security, ft.Icons.SHIELD, ft.Icons.SHIELD_OUTLINED,
                ft.Colors.BLUE_ACCENT, get_text("security_active"), get_text("security_inactive"))
    update_icon('o1_mvmnt_icon', state, state.o1_mvmnt, ft.Icons.PERSON, ft.Icons.PERSON_OUTLINE,
                ft.Colors.BLUE_ACCENT, get_text("movement_detected"), get_text("no_movement"))
    update_icon('o1_smoke_icon', state, state.o1_smoke, ft.Icons.LOCAL_FIRE_DEPARTMENT,
                ft.Icons.LOCAL_FIRE_DEPARTMENT_OUTLINED, ft.Colors.ORANGE, get_text("smoke_detected"),
                get_text("no_smoke"))
    update_icon('o1_door_icon', state, state.o1_door_open, ft.Icons.DOOR_FRONT_DOOR, ft.Icons.DOOR_FRONT_DOOR_OUTLINED,
                ft.Colors.RED_ACCENT, get_text("door_open"), get_text("door_closed_tooltip"))
    update_icon('o1_rfid_icon', state, state.o1_rfid_ok, ft.Icons.LOCK_PERSON, ft.Icons.LOCK_PERSON_OUTLINED,
                ft.Colors.GREEN_ACCENT, get_text("rfid_accepted"), get_text("no_card"))
    update_icon('o2_mvmnt_icon', state, state.o2_mvmnt, ft.Icons.PERSON, ft.Icons.PERSON_OUTLINE,
                ft.Colors.BLUE_ACCENT, get_text("movement_detected"), get_text("no_movement"))
    update_icon('o2_smoke_icon', state, state.o2_smoke, ft.Icons.LOCAL_FIRE_DEPARTMENT,
                ft.Icons.LOCAL_FIRE_DEPARTMENT_OUTLINED, ft.Colors.ORANGE, get_text("smoke_detected"),
                get_text("no_smoke"))
    update_icon('o2_door_icon', state, state.o2_door_open, ft.Icons.DOOR_FRONT_DOOR, ft.Icons.DOOR_FRONT_DOOR_OUTLINED,
                ft.Colors.RED_ACCENT, get_text("door_open"), get_text("door_closed_tooltip"))
    update_icon('o2_rfid_icon', state, state.o2_rfid_ok, ft.Icons.LOCK_PERSON, ft.Icons.LOCK_PERSON_OUTLINED,
                ft.Colors.GREEN_ACCENT, get_text("rfid_accepted"), get_text("no_card"))
    update_icon('c1_mvmnt_icon', state, state.c1_mvmnt, ft.Icons.PERSON, ft.Icons.PERSON_OUTLINE,
                ft.Colors.BLUE_ACCENT, get_text("movement_detected"), get_text("no_movement"))
    update_icon('c1_smoke_icon', state, state.c1_smoke, ft.Icons.LOCAL_FIRE_DEPARTMENT,
                ft.Icons.LOCAL_FIRE_DEPARTMENT_OUTLINED, ft.Colors.ORANGE, get_text("smoke_detected"),
                get_text("no_smoke"))
    update_icon('c1_light_icon', state, state.c1_light, ft.Icons.LIGHTBULB, ft.Icons.LIGHTBULB_OUTLINE,
                ft.Colors.YELLOW_ACCENT, get_text("light_on"), get_text("light_off"))
    update_icon('o3_mvmnt_icon', state, state.o3_mvmnt, ft.Icons.PERSON, ft.Icons.PERSON_OUTLINE,
                ft.Colors.BLUE_ACCENT, get_text("movement_detected"), get_text("no_movement"))
    update_icon('o3_smoke_icon', state, state.o3_smoke, ft.Icons.LOCAL_FIRE_DEPARTMENT,
                ft.Icons.LOCAL_FIRE_DEPARTMENT_OUTLINED, ft.Colors.ORANGE, get_text("smoke_detected"),
                get_text("no_smoke"))
    update_icon('o3_door_icon', state, state.o3_door_open, ft.Icons.DOOR_FRONT_DOOR, ft.Icons.DOOR_FRONT_DOOR_OUTLINED,
                ft.Colors.RED_ACCENT, get_text("door_open"), get_text("door_closed_tooltip"))
    update_icon('o3_rfid_icon', state, state.o3_rfid_ok, ft.Icons.LOCK_PERSON, ft.Icons.LOCK_PERSON_OUTLINED,
                ft.Colors.GREEN_ACCENT, get_text("rfid_accepted"), get_text("no_card"))
    update_icon('o3_heating_icon', state, state.o3_heating, ft.Icons.WB_SUNNY_ROUNDED, ft.Icons.WB_SUNNY_OUTLINED,
                ft.Colors.YELLOW_700, get_text("heating_on"), get_text("heating_off"))
    update_icon('o3_cooling_icon', state, state.o3_cooling, ft.Icons.AC_UNIT, ft.Icons.AC_UNIT_OUTLINED,
                ft.Colors.LIGHT_BLUE_ACCENT_400, get_text("cooling_on"), get_text("cooling_off"))
    temp_text_ctrl = state.ui_refs.get('o3_temp_text')
    if temp_text_ctrl:
        celsius_temp = (state.o3_temp / 10.0) - 50.0
        temp_text_ctrl.value = f"{celsius_temp:.1f}°C"
    update_icon('c2_mvmnt_icon', state, state.c2_mvmnt, ft.Icons.PERSON, ft.Icons.PERSON_OUTLINE,
                ft.Colors.BLUE_ACCENT, get_text("movement_detected"), get_text("no_movement"))
    update_icon('c2_smoke_icon', state, state.c2_smoke, ft.Icons.LOCAL_FIRE_DEPARTMENT,
                ft.Icons.LOCAL_FIRE_DEPARTMENT_OUTLINED, ft.Colors.ORANGE, get_text("smoke_detected"),
                get_text("no_smoke"))
    update_icon('c2_light_icon', state, state.c2_light, ft.Icons.LIGHTBULB, ft.Icons.LIGHTBULB_OUTLINE,
                ft.Colors.YELLOW, get_text("light_on"), get_text("light_off"))
    spots_text_ctrl = state.ui_refs.get('p_spots_text')
    if spots_text_ctrl:
        spots_text_ctrl.value = f"{state.p_spots_taken}/{state.p_spots_total}"
        spots_text_ctrl.color = ft.Colors.RED_ACCENT if state.p_full_bulb else ft.Colors.ON_SURFACE
    spots_textfield_ctrl = state.ui_refs.get('pspots_taken_field')
    if spots_textfield_ctrl and not spots_textfield_ctrl.focus:
        spots_textfield_ctrl.value = str(state.p_spots_taken)
    update_icon('p_obj_icon', state, state.p_obj_det, ft.Icons.CAR_CRASH, ft.Icons.CAR_CRASH_OUTLINED,
                ft.Colors.YELLOW, get_text("object_in_front"), get_text("no_object"))
    update_icon('p_open_icon', state, state.p_gate_open, ft.Icons.ARROW_CIRCLE_LEFT,
                ft.Icons.ARROW_CIRCLE_LEFT_OUTLINED, ft.Colors.GREEN_ACCENT, get_text("opening_gate"),
                get_text("gate_not_opening"))
    update_icon('p_closed_icon', state, not state.p_gate_closed, ft.Icons.GARAGE, ft.Icons.GARAGE_OUTLINED,
                ft.Colors.RED_ACCENT, get_text("gate_not_closed"), get_text("gate_closed_tooltip"))
    update_icon('p_close_icon', state, state.p_gate_close, ft.Icons.ARROW_CIRCLE_RIGHT,
                ft.Icons.ARROW_CIRCLE_RIGHT_OUTLINED, ft.Colors.RED_ACCENT, get_text("closing_gate"),
                get_text("gate_not_closing"))
    update_icon('p_inside_btn_icon', state, state.p_outside_cycle, ft.Icons.LOCK_PERSON,
                ft.Icons.LOCK_PERSON_OUTLINED, ft.Colors.GREEN_ACCENT, get_text("rfid_accepted_outside"),
                get_text("no_card_outside"))
    update_icon('p_rfid_icon', state, state.p_inside_cycle, ft.Icons.RADIO_BUTTON_CHECKED,
                ft.Icons.RADIO_BUTTON_OFF, ft.Colors.GREEN_ACCENT, get_text("button_pressed_inside"),
                get_text("button_not_pressed_inside"))
    alerts_cont = state.ui_refs.get('alerts_container')
    if alerts_cont:
        alert_texts = ALERT_TEXTS[state.lang]
        alerts_definition = [
            (p, state_key, alert_texts[text_key], i, c)
            for p, state_key, text_key, i, c in ALERT_DEFS
        ]
        active_alerts = sorted([{"priority": p, "msg": m, "icon": i, "color": c}
                                for p, k, m, i, c in alerts_definition if getattr(state, k, False)],
                               key=lambda x: x['priority'], reverse=True)
        alerts_cont.controls.clear()
        if not active_alerts:
            alerts_cont.controls.append(
                ft.Text(get_text("no_alerts"), italic=True, color=ft.Colors.GREY, size=13.5))
        else:
            for alert in active_alerts:
                alerts_cont.controls.append(
                    ft.Row([ft.Icon(name=alert['icon'], color=alert['color'], size=20),
                            ft.Text(alert['msg'], color=alert['color'], weight=ft.FontWeight.BOLD, size=13.5)],
                           alignment=ft.MainAxisAlignment.START, spacing=10))


def update_config_ui(state, get_text):
    """Updates fields on the config screen that reflect PLC state."""
    if not state.ui_refs:
        return  # Don't update if UI not built

    if 'cfg_force_open_switch' in state.ui_refs:
        state.ui_refs['cfg_force_open_switch'].value = state.force_park_open
    if 'cfg_force_close_switch' in state.ui_refs:
        state.ui_refs['cfg_force_close_switch'].value = state.force_park_close
    if 'cfg_pspots_taken_field' in state.ui_refs:
        state.ui_refs['cfg_pspots_taken_field'].value = str(state.p_spots_taken)
    if 'measured_light_text' in state.ui_refs:
        state.ui_refs['measured_light_text'].value = f"{get_text('measured_light')} {state.measured_light}"
