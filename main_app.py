import flet as ft
import time
import threading
import scada_db as db
from plc_logic import PLCManager
from definitions import TEXTS, USERS
from app_state import AppState
from ui_factory import create_dashboard_view, create_config_view
from ui_updater import update_dashboard_ui, update_config_ui, update_app_bar


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO_ACCENT_400, scaffold_bgcolor="#FaFaFf")
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO_600)
    page.window_min_width = 600
    db.create_tables()

    state = AppState()

    def get_text(key):
        return TEXTS.get(state.lang, TEXTS['en']).get(key, key)

    page.title = get_text("app_title")

    def check_and_log_events(current, previous):
        """Compares current and previous states to log significant events."""
        if not previous:
            return

        event_definitions = {
            'l_smoke': ('fire_detected', None, 'Lobby', False),
            'o1_smoke': ('fire_detected', None, 'Office 1', False),
            'o2_smoke': ('fire_detected', None, 'Office 2', False),
            'o3_smoke': ('fire_detected', None, 'Office 3', False),
            'c1_smoke': ('fire_detected', None, 'Corridor 1', False),
            'c2_smoke': ('fire_detected', None, 'Corridor 2', False),
            'l_security': ('alarm_was_activated', 'alarm_was_deactivated', 'Lobby', False),
            'emergency': ('emergency_happened', None, 'System', True),
            'call_fire_dept': ('fire_dept_was_called', None, 'System', True),
            'call_security': ('security_was_called', None, 'System', True),
            'warn_config_altered': ('config_altered', None, 'System', False),
            'warn_auto_security_impossible': ('auto_security_impossible', None, 'System', False),
            'warn_fire_det': ('fire_detected', None, 'System', False),
            'warn_pgate_open': ('parking_gate_open_warning', None, 'Parking lot', False),
            'warn_pspot_miscount': ('parking_spot_miscount', None, 'Parking lot', False),
            'err_light_config': ('light_config_error', None, 'System', False),
            'err_pgate_force': ('parking_gate_forced_error', None, 'Parking lot', False),
            'err_pspot_config': ('parking_spot_config_error', None, 'Parking lot', False),
            'err_temp_config': ('temp_config_error', None, 'System', False),
            'err_work_day_config': ('work_day_config_error', None, 'System', False),
            'err_cold_month_config': ('cold_month_config_error', None, 'System', False),
        }

        for attr, (event_on, event_off, location, is_momentary) in event_definitions.items():
            if getattr(current, attr) and not getattr(previous, attr):
                db.log_event(event_name=event_on, location_name=location, is_resolved=is_momentary)
            elif not getattr(current, attr) and getattr(previous, attr):
                if event_off:
                    db.log_event(event_name=event_off, location_name=location, is_resolved=True)
                db.resolve_event(event_name=event_on, location_name=location)

        if current.force_park_open and not previous.force_park_open:
            db.log_event('parking_lot_was_forced_open', 'Parking lot', is_resolved=False)
        elif not current.force_park_open and previous.force_park_open:
            db.resolve_event('parking_lot_was_forced_open', 'Parking lot')

        if current.force_park_close and not previous.force_park_close:
            db.log_event('parking_lot_was_forced_closed', 'Parking lot', is_resolved=False)
        elif not current.force_park_close and previous.force_park_close:
            db.resolve_event('parking_lot_was_forced_closed', 'Parking lot')

        if current.l_security:
            trigger_locations = {
                'Lobby': (current.l_mvmnt and not previous.l_mvmnt) or (
                            current.l_door_open and not previous.l_door_open),
                'Office 1': (current.o1_mvmnt and not previous.o1_mvmnt) or (
                            current.o1_door_open and not previous.o1_door_open),
                'Office 2': (current.o2_mvmnt and not previous.o2_mvmnt) or (
                            current.o2_door_open and not previous.o2_door_open),
                'Office 3': (current.o3_mvmnt and not previous.o3_mvmnt) or (
                            current.o3_door_open and not previous.o3_door_open),
                'Corridor 1': current.c1_mvmnt and not previous.c1_mvmnt,
                'Corridor 2': current.c2_mvmnt and not previous.c2_mvmnt,
            }
            for location, triggered in trigger_locations.items():
                if triggered:
                    db.log_event('alarm_was_triggered', location, is_resolved=True)

    def on_keep_lobby_door_open(e):
        state.force_lobby_door = e.control.value

    def on_keep_parking_open(e):
        state.force_park_open = e.control.value
        if state.force_park_open:
            state.force_park_close = False

    def on_keep_parking_closed(e):
        state.force_park_close = e.control.value
        if state.force_park_close:
            state.force_park_open = False

    def on_update_pspots(e):
        try:
            state.p_spots_taken = int(e.control.value)
        except (ValueError, TypeError):
            pass

    def toggle_lang(e):
        next_lang = "bg" if state.lang == "en" else "en"
        state.lang = next_lang
        route_change(page.route, is_lang_toggle=True)

    def login(e):
        username, password = user_field.value, pass_field.value
        user = USERS.get(username)
        if user and user["password"] == password:
            page.session.set("user_role", user["role"])
            page.go("/dashboard")
        else:
            login_error_text.value = get_text("invalid_credentials")
            page.update()

    def logout(e):
        page.session.clear()
        user_field.value, pass_field.value, login_error_text.value = "", "", ""
        page.go("/")
        page.update()

    def update_state_on_interval():
        plc_manager = PLCManager('127.0.0.1', 502)
        previous_state = None
        while True:
            previous_state = state.get_snapshot()
            plc_manager.update(state)
            check_and_log_events(state, previous_state)
            update_app_bar(state, get_text)
            if page.route == "/dashboard":
                update_dashboard_ui(state, get_text)
            elif page.route == "/config":
                update_config_ui(state, get_text)
            page.update()
            time.sleep(0.7)

    handlers = {
        "on_keep_lobby_door_open": on_keep_lobby_door_open,
        "on_keep_parking_open": on_keep_parking_open,
        "on_keep_parking_closed": on_keep_parking_closed,
        "on_update_pspots": on_update_pspots,
        "toggle_lang": toggle_lang,
        "logout": logout,
    }

    def route_change(route, is_lang_toggle=False):
        page.views.clear()

        page.title = get_text("login_title")
        page.views.append(
            ft.View(
                "/",
                [
                    ft.Column(
                        controls=[
                            ft.Text(get_text("login"), size=32),
                            user_field,
                            pass_field,
                            login_btn,
                            login_error_text,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                    )
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

        if page.route == "/dashboard":
            user_role = page.session.get("user_role")
            if not user_role:
                page.go("/")
                return
            page.title = get_text("dashboard_title")
            page.views.append(
                create_dashboard_view(page, state, get_text, handlers)
            )

        elif page.route == "/config":
            if page.session.get("user_role") != "administrator":
                page.go("/")
                return
            page.title = get_text("config_title")
            page.views.append(
                create_config_view(page, state, get_text, handlers)
            )

        update_dashboard_ui(state, get_text)
        update_app_bar(state, get_text)
        page.update()

    user_field = ft.TextField(label=get_text("username"), on_submit=login, width=330, autofocus=True)
    pass_field = ft.TextField(label=get_text("password"), on_submit=login, password=True, can_reveal_password=True,
                              width=330)
    login_error_text = ft.Text("", color="red")
    login_btn = ft.ElevatedButton(get_text("login"), on_click=login, width=300)

    page.on_route_change = route_change
    update_thread = threading.Thread(target=update_state_on_interval, daemon=True)
    update_thread.start()
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main, view=ft.FLET_APP)