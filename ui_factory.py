import flet as ft
import scada_db as db


def grid_cell(content):
    return ft.Container(content=content, padding=6 if isinstance(content, ft.Text) else 4, expand=True,
                        alignment=ft.alignment.center)


def icon_btn(get_text, tooltip_key, default_icon):
    return ft.IconButton(icon=default_icon, icon_size=24, tooltip=get_text(tooltip_key),
                         mouse_cursor=ft.MouseCursor.HELP,
                         padding=0, hover_color=ft.Colors.TRANSPARENT, highlight_color=ft.Colors.TRANSPARENT,
                         style=ft.ButtonStyle(padding=0, shape=ft.CircleBorder(),
                                              overlay_color=ft.Colors.with_opacity(0, ft.Colors.BLACK),
                                              elevation=0))


def create_appbar(page, state, get_text, toggle_lang_handler, logout_handler):
    plc_icon = ft.IconButton(
        icon=ft.Icons.PHONELINK_OFF, icon_color=ft.Colors.RED,
        tooltip=get_text("plc_disconnected"),
        mouse_cursor=ft.MouseCursor.HELP, hover_color=ft.Colors.TRANSPARENT, highlight_color=ft.Colors.TRANSPARENT
    )
    state.ui_refs["plc_status_icon"] = plc_icon

    dash_btn = ft.TextButton(get_text("dashboard"), on_click=lambda _: page.go("/dashboard"))
    lang_btn = ft.TextButton(
        text=state.lang.upper(),
        on_click=toggle_lang_handler,
        tooltip="Change language / Смяна на език",
        style=ft.ButtonStyle(color=ft.Colors.ON_PRIMARY_CONTAINER)
    )
    logout_btn = ft.IconButton(ft.Icons.LOGOUT, tooltip=get_text("logout"), on_click=logout_handler,
                               icon_color=ft.Colors.ON_PRIMARY_CONTAINER)
    actions = [dash_btn]
    if page.session.get("user_role") == "administrator":
        actions.append(ft.TextButton(get_text("config_panel"), on_click=lambda _: page.go("/config")))
    actions.append(lang_btn)
    actions.append(logout_btn)
    return ft.AppBar(leading=plc_icon, leading_width=60, title=None, center_title=False, adaptive=True,
                     bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.ON_SURFACE), actions=actions)


def create_dashboard_view(page, state, get_text, handlers):
    state.ui_refs.clear()

    l_label_cell = grid_cell(ft.Text(get_text("lobby"), weight=ft.FontWeight.BOLD, text_align=ft.alignment.center,
                                     style=ft.TextStyle(italic=True)))
    l_mvmnt_cell = grid_cell(icon_btn(get_text, "movement", ft.Icons.PERSON_OUTLINE))
    l_smoke_cell = grid_cell(icon_btn(get_text, "smoke", ft.Icons.LOCAL_FIRE_DEPARTMENT_OUTLINED))
    l_light_cell = grid_cell(icon_btn(get_text, "light", ft.Icons.LIGHTBULB_OUTLINE))
    l_door_cell = grid_cell(icon_btn(get_text, "door", ft.Icons.DOOR_FRONT_DOOR_OUTLINED))
    l_rfid_cell = grid_cell(icon_btn(get_text, "rfid", ft.Icons.LOCK_PERSON_OUTLINED))
    l_sec_cell = grid_cell(icon_btn(get_text, "security", ft.Icons.SHIELD_OUTLINED))
    l_empty_cell1, l_empty_cell2, l_empty_cell3 = grid_cell(ft.Text("")), grid_cell(ft.Text("")), grid_cell(ft.Text(""))
    state.ui_refs['l_mvmnt_icon'] = l_mvmnt_cell.content
    state.ui_refs['l_smoke_icon'] = l_smoke_cell.content
    state.ui_refs['l_light_icon'] = l_light_cell.content
    state.ui_refs['l_door_icon'] = l_door_cell.content
    state.ui_refs['l_rfid_icon'] = l_rfid_cell.content
    state.ui_refs['l_sec_icon'] = l_sec_cell.content
    state.ui_refs['lobby_container'] = [l_label_cell, l_empty_cell1, l_empty_cell2, l_empty_cell3, l_mvmnt_cell,
                                        l_smoke_cell, l_light_cell, l_door_cell, l_rfid_cell, l_sec_cell]

    o1_label_cell = grid_cell(ft.Text(get_text("office_1"), weight=ft.FontWeight.BOLD, text_align=ft.alignment.center,
                                      style=ft.TextStyle(italic=True)))
    o1_mvmnt_cell = grid_cell(icon_btn(get_text, "movement", ft.Icons.PERSON_OUTLINE))
    o1_smoke_cell = grid_cell(icon_btn(get_text, "smoke", ft.Icons.LOCAL_FIRE_DEPARTMENT_OUTLINED))
    o1_door_cell = grid_cell(icon_btn(get_text, "door", ft.Icons.DOOR_FRONT_DOOR_OUTLINED))
    o1_rfid_cell = grid_cell(icon_btn(get_text, "rfid", ft.Icons.LOCK_PERSON_OUTLINED))
    state.ui_refs['o1_mvmnt_icon'] = o1_mvmnt_cell.content
    state.ui_refs['o1_smoke_icon'] = o1_smoke_cell.content
    state.ui_refs['o1_door_icon'] = o1_door_cell.content
    state.ui_refs['o1_rfid_icon'] = o1_rfid_cell.content
    state.ui_refs['o1_container'] = [o1_label_cell, o1_mvmnt_cell, o1_smoke_cell, o1_door_cell, o1_rfid_cell]
    o2_label_cell = grid_cell(ft.Text(get_text("office_2"), weight=ft.FontWeight.BOLD, text_align=ft.alignment.center,
                                      style=ft.TextStyle(italic=True)))
    o2_mvmnt_cell = grid_cell(icon_btn(get_text, "movement", ft.Icons.PERSON_OUTLINE))
    o2_smoke_cell = grid_cell(icon_btn(get_text, "smoke", ft.Icons.LOCAL_FIRE_DEPARTMENT_OUTLINED))
    o2_door_cell = grid_cell(icon_btn(get_text, "door", ft.Icons.DOOR_FRONT_DOOR_OUTLINED))
    o2_rfid_cell = grid_cell(icon_btn(get_text, "rfid", ft.Icons.LOCK_PERSON_OUTLINED))
    state.ui_refs['o2_mvmnt_icon'] = o2_mvmnt_cell.content
    state.ui_refs['o2_smoke_icon'] = o2_smoke_cell.content
    state.ui_refs['o2_door_icon'] = o2_door_cell.content
    state.ui_refs['o2_rfid_icon'] = o2_rfid_cell.content
    state.ui_refs['o2_container'] = [o2_label_cell, o2_mvmnt_cell, o2_smoke_cell, o2_door_cell, o2_rfid_cell]
    c1_label_cell = grid_cell(ft.Text(get_text("corridor_1"), weight=ft.FontWeight.BOLD, text_align=ft.alignment.center,
                                      style=ft.TextStyle(italic=True)))
    c1_mvmnt_cell = grid_cell(icon_btn(get_text, "movement", ft.Icons.PERSON_OUTLINE))
    c1_smoke_cell = grid_cell(icon_btn(get_text, "smoke", ft.Icons.LOCAL_FIRE_DEPARTMENT_OUTLINED))
    c1_light_cell = grid_cell(icon_btn(get_text, "light", ft.Icons.LIGHTBULB_OUTLINE))
    c1_empty_cell = grid_cell(ft.Text(""))
    state.ui_refs['c1_mvmnt_icon'] = c1_mvmnt_cell.content
    state.ui_refs['c1_smoke_icon'] = c1_smoke_cell.content
    state.ui_refs['c1_light_icon'] = c1_light_cell.content
    state.ui_refs['c1_container'] = [c1_label_cell, c1_mvmnt_cell, c1_smoke_cell, c1_light_cell, c1_empty_cell]
    o3_label_cell = grid_cell(ft.Text(get_text("office_3"), weight=ft.FontWeight.BOLD, text_align=ft.alignment.center,
                                      style=ft.TextStyle(italic=True)))
    o3_mvmnt_cell = grid_cell(icon_btn(get_text, "movement", ft.Icons.PERSON_OUTLINE))
    o3_smoke_cell = grid_cell(icon_btn(get_text, "smoke", ft.Icons.LOCAL_FIRE_DEPARTMENT_OUTLINED))
    o3_door_cell = grid_cell(icon_btn(get_text, "door", ft.Icons.DOOR_FRONT_DOOR_OUTLINED))
    o3_rfid_cell = grid_cell(icon_btn(get_text, "rfid", ft.Icons.LOCK_PERSON_OUTLINED))
    o3_heat_cell = grid_cell(icon_btn(get_text, "heating", ft.Icons.WB_SUNNY_OUTLINED))
    o3_cool_cell = grid_cell(icon_btn(get_text, "cooling", ft.Icons.AC_UNIT_OUTLINED))
    o3_temp_text = ft.Text("0.0°C", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    o3_temp_cell = grid_cell(o3_temp_text)
    o3_empty_cell1, o3_empty_cell2 = grid_cell(ft.Text("")), grid_cell(ft.Text(""))
    state.ui_refs['o3_mvmnt_icon'] = o3_mvmnt_cell.content
    state.ui_refs['o3_smoke_icon'] = o3_smoke_cell.content
    state.ui_refs['o3_door_icon'] = o3_door_cell.content
    state.ui_refs['o3_rfid_icon'] = o3_rfid_cell.content
    state.ui_refs['o3_heating_icon'] = o3_heat_cell.content
    state.ui_refs['o3_cooling_icon'] = o3_cool_cell.content
    state.ui_refs['o3_temp_text'] = o3_temp_text
    state.ui_refs['o3_container'] = [o3_label_cell, o3_mvmnt_cell, o3_smoke_cell, o3_door_cell, o3_rfid_cell,
                                     o3_heat_cell, o3_cool_cell, o3_temp_cell, o3_empty_cell1, o3_empty_cell2]
    c2_label_cell = grid_cell(ft.Text(get_text("corridor_2"), weight=ft.FontWeight.BOLD, text_align=ft.alignment.center,
                                      style=ft.TextStyle(italic=True)))
    c2_mvmnt_cell = grid_cell(icon_btn(get_text, "movement", ft.Icons.PERSON_OUTLINE))
    c2_smoke_cell = grid_cell(icon_btn(get_text, "smoke", ft.Icons.LOCAL_FIRE_DEPARTMENT_OUTLINED))
    c2_light_cell = grid_cell(icon_btn(get_text, "light", ft.Icons.LIGHTBULB_OUTLINE))
    c2_empty_cell = grid_cell(ft.Text(""))
    state.ui_refs['c2_mvmnt_icon'] = c2_mvmnt_cell.content
    state.ui_refs['c2_smoke_icon'] = c2_smoke_cell.content
    state.ui_refs['c2_light_icon'] = c2_light_cell.content
    state.ui_refs['c2_container'] = [c2_label_cell, c2_mvmnt_cell, c2_smoke_cell, c2_light_cell, c2_empty_cell]
    pspots_text = ft.Text(f"0/{state.p_spots_total}", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    p_spots_cell = grid_cell(pspots_text)
    p_obj_cell = grid_cell(icon_btn(get_text, "object_detected", ft.Icons.CAR_CRASH_OUTLINED))
    p_open_cell = grid_cell(icon_btn(get_text, "gate_opening", ft.Icons.ARROW_CIRCLE_LEFT_OUTLINED))
    p_closed_cell = grid_cell(icon_btn(get_text, "gate_closed", ft.Icons.GARAGE_OUTLINED))
    p_close_cell = grid_cell(icon_btn(get_text, "gate_closing", ft.Icons.ARROW_CIRCLE_RIGHT_OUTLINED))
    p_inside_btn_cell = grid_cell(icon_btn(get_text, "outside_rfid", ft.Icons.LOCK_PERSON_OUTLINED))
    p_rfid_cell = grid_cell(icon_btn(get_text, "inside_button", ft.Icons.RADIO_BUTTON_OFF))
    p_empty_cell1, p_empty_cell2 = grid_cell(ft.Text("")), grid_cell(ft.Text(""))
    state.ui_refs['p_spots_text'] = pspots_text
    state.ui_refs['p_obj_icon'] = p_obj_cell.content
    state.ui_refs['p_open_icon'] = p_open_cell.content
    state.ui_refs['p_closed_icon'] = p_closed_cell.content
    state.ui_refs['p_close_icon'] = p_close_cell.content
    state.ui_refs['p_inside_btn_icon'] = p_inside_btn_cell.content
    state.ui_refs['p_rfid_icon'] = p_rfid_cell.content

    lobby_door_switch_ctrl = ft.Switch(on_change=handlers['on_keep_lobby_door_open'], value=state.force_lobby_door,
                                       scale=0.75, )
    parking_open_switch_ctrl = ft.Switch(on_change=handlers['on_keep_parking_open'], value=state.force_park_open,
                                         scale=0.75)
    parking_closed_switch_ctrl = ft.Switch(on_change=handlers['on_keep_parking_closed'], value=state.force_park_close,
                                           scale=0.75)
    pspots_taken_field = ft.TextField(value=str(state.p_spots_taken), width=50, text_align=ft.TextAlign.CENTER,
                                      on_submit=handlers['on_update_pspots'], scale=0.85)
    state.ui_refs['force_open_switch'] = parking_open_switch_ctrl
    state.ui_refs['force_close_switch'] = parking_closed_switch_ctrl
    state.ui_refs['pspots_taken_field'] = pspots_taken_field

    alerts_list_col = ft.Column(
        controls=[ft.Text(get_text("no_alerts"), italic=True, color=ft.Colors.GREY, size=14)],
        spacing=5, scroll=ft.ScrollMode.AUTO)
    state.ui_refs['alerts_container'] = alerts_list_col

    negative_spacing = -0.55
    floor0_cont = ft.Container(ft.Column([
        ft.Row([l_label_cell], spacing=negative_spacing, tight=True),
        ft.Row([l_empty_cell1], spacing=negative_spacing, tight=True),
        ft.Row([l_mvmnt_cell, l_smoke_cell], spacing=negative_spacing, tight=True),
        ft.Row([l_light_cell, l_sec_cell], spacing=negative_spacing, tight=True),
        ft.Row([l_door_cell, l_rfid_cell], spacing=negative_spacing, tight=True),
        ft.Row([l_empty_cell2], spacing=negative_spacing, tight=True)
    ], spacing=negative_spacing, tight=True), border_radius=ft.border_radius.all(30), alignment=ft.alignment.center,
        bgcolor=ft.Colors.with_opacity(0.07, ft.Colors.ON_SURFACE))
    state.ui_refs['floor0_main_container'] = floor0_cont
    floor1_cont = ft.Container(ft.Column([
        ft.Row([o1_label_cell, o2_label_cell], spacing=negative_spacing, tight=True),
        ft.Row([o1_mvmnt_cell, o1_smoke_cell, o2_mvmnt_cell, o2_smoke_cell], spacing=negative_spacing, tight=True),
        ft.Row([o1_door_cell, o1_rfid_cell, o2_door_cell, o2_rfid_cell], spacing=negative_spacing, tight=True),
        ft.Row([c1_label_cell], spacing=negative_spacing, tight=True),
        ft.Row([c1_mvmnt_cell, c1_smoke_cell, c1_light_cell], spacing=negative_spacing, tight=True),
        ft.Row([c1_empty_cell], spacing=negative_spacing, tight=True),
    ], spacing=negative_spacing, tight=True), border_radius=ft.border_radius.all(30), alignment=ft.alignment.center,
        bgcolor=ft.Colors.with_opacity(0.07, ft.Colors.ON_SURFACE))
    state.ui_refs['floor1_main_container'] = floor1_cont
    floor2_cont = ft.Container(ft.Column([
        ft.Row([o3_label_cell, o3_temp_cell], spacing=negative_spacing, tight=True),
        ft.Row([o3_mvmnt_cell, o3_smoke_cell, o3_heat_cell, o3_cool_cell], spacing=negative_spacing, tight=True),
        ft.Row([o3_door_cell, o3_rfid_cell], spacing=negative_spacing, tight=True),
        ft.Row([c2_label_cell], spacing=negative_spacing, tight=True),
        ft.Row([c2_mvmnt_cell, c2_smoke_cell, c2_light_cell], spacing=negative_spacing, tight=True),
        ft.Row([c2_empty_cell], spacing=negative_spacing, tight=True),
    ], spacing=negative_spacing, tight=True), border_radius=ft.border_radius.all(30), alignment=ft.alignment.center,
        bgcolor=ft.Colors.with_opacity(0.07, ft.Colors.ON_SURFACE))
    state.ui_refs['floor2_main_container'] = floor2_cont
    parking_cont = ft.Container(ft.Column([
        ft.Row([p_spots_cell], spacing=negative_spacing, tight=True),
        ft.Row([p_empty_cell1], spacing=negative_spacing, tight=True),
        ft.Row([p_open_cell, p_close_cell], spacing=negative_spacing, tight=True),
        ft.Row([p_inside_btn_cell, p_rfid_cell], spacing=negative_spacing, tight=True),
        ft.Row([p_closed_cell, p_obj_cell], spacing=negative_spacing, tight=True),
        ft.Row([p_empty_cell2], spacing=negative_spacing, tight=True),
    ], spacing=negative_spacing, tight=True), border_radius=ft.border_radius.all(30), alignment=ft.alignment.center,
        bgcolor=ft.Colors.with_opacity(0.07, ft.Colors.ON_SURFACE))
    quick_controls_cont = ft.Container(ft.Column(controls=[
        ft.Row([lobby_door_switch_ctrl,
                ft.Text(get_text("keep_lobby_door_open"), weight=ft.FontWeight.BOLD, style=ft.TextStyle(italic=True))]),
        ft.Row([parking_open_switch_ctrl,
                ft.Text(get_text("keep_parking_open"), weight=ft.FontWeight.BOLD, style=ft.TextStyle(italic=True))]),
        ft.Row([parking_closed_switch_ctrl,
                ft.Text(get_text("keep_parking_closed"), weight=ft.FontWeight.BOLD, style=ft.TextStyle(italic=True))]),
        ft.Row(controls=[
            ft.Text(get_text("set_parking_spots"), weight=ft.FontWeight.BOLD, style=ft.TextStyle(italic=True)),
            pspots_taken_field, ]),
    ], spacing=5, ), border_radius=ft.border_radius.all(30), expand=True,
        bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.ON_SURFACE), padding=12)
    alerts_main_cont = ft.Container(content=alerts_list_col, border_radius=ft.border_radius.all(30),
                                    alignment=ft.alignment.top_left,
                                    bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.ON_SURFACE), padding=15, expand=True)
    dashboard_grid = ft.ResponsiveRow([
        ft.Column(controls=[
            ft.Container(ft.Text(get_text("floor_0"), weight=ft.FontWeight.BOLD, style=ft.TextThemeStyle.TITLE_MEDIUM),
                         margin=ft.Margin(10, 0, 0, 0)), floor0_cont,
            ft.Container(ft.Text(get_text("floor_1"), weight=ft.FontWeight.BOLD, style=ft.TextThemeStyle.TITLE_MEDIUM),
                         margin=ft.Margin(10, 0, 0, 0)), floor1_cont, ], col={"xs": 12, "sm": 6, "md": 4}, ),
        ft.Column(controls=[
            ft.Container(ft.Text(get_text("floor_2"), weight=ft.FontWeight.BOLD, style=ft.TextThemeStyle.TITLE_MEDIUM),
                         margin=ft.Margin(10, 0, 0, 0)), floor2_cont, ft.Container(
                ft.Text(get_text("parking_lot"), weight=ft.FontWeight.BOLD, style=ft.TextThemeStyle.TITLE_MEDIUM),
                margin=ft.Margin(10, 0, 0, 0)), parking_cont, ], col={"xs": 12, "sm": 6, "md": 4}, ),
        ft.Column(controls=[ft.Container(
            ft.Text(get_text("quick_controls"), weight=ft.FontWeight.BOLD, style=ft.TextThemeStyle.TITLE_MEDIUM),
            margin=ft.Margin(10, 0, 0, 0)), quick_controls_cont, ft.Container(
            ft.Text(get_text("alerts"), weight=ft.FontWeight.BOLD, style=ft.TextThemeStyle.TITLE_MEDIUM),
            margin=ft.Margin(10, 0, 0, 0)), alerts_main_cont, ], col={"xs": 12, "sm": 12, "md": 4}, ),
    ])

    return ft.View(
        "/dashboard",
        [ft.Column([dashboard_grid], expand=True, scroll=ft.ScrollMode.AUTO,
                   horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)],
        appbar=create_appbar(page, state, get_text, handlers['toggle_lang'], handlers['logout']),
        vertical_alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, padding=20
    )


def create_config_view(page, state, get_text, handlers):
    state.ui_refs.clear()
    small_text_size, query_text_size = 17, 14
    db_output_cont = ft.Container(padding=10)
    sql_query_field = ft.TextField(label=get_text("sql_query"), multiline=True, min_lines=1, text_size=query_text_size,
                                   label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True))

    def update_db_results_table(columns, data, error=None):
        db_output_cont.content = None
        if error:
            content = ft.Column(
                [ft.Text(f"{get_text('error_executing_query')}", color=ft.Colors.RED, weight=ft.FontWeight.BOLD),
                 ft.Text(error)])
        elif not data:
            content = ft.Text(get_text("no_results"))
        else:
            table = ft.DataTable(
                columns=[ft.DataColumn(ft.Text(col, weight=ft.FontWeight.BOLD, size=13)) for col in columns],
                rows=[ft.DataRow(
                    cells=[ft.DataCell(ft.Text(str(item) if item is not None else "", size=12)) for item in row]) for
                      row in data],
                data_row_min_height=28, heading_row_height=32, column_spacing=20
            )
            table_container = ft.Row(controls=[table], scroll=ft.ScrollMode.ALWAYS)
            content = ft.Column(
                [ft.Text(get_text("db_results"), style=ft.TextThemeStyle.TITLE_MEDIUM), ft.Divider(), table_container],
                scroll=ft.ScrollMode.ADAPTIVE, expand=True)
        db_output_cont.content = content
        db_output_cont.visible = True
        page.update()

    def handle_db_query(e, query_func=None, query_str=None):
        db_output_cont.visible = True
        page.update()
        columns, data, error = query_func() if query_func else db.execute_query(
            query_str) if query_str and query_str.strip() else (None, None, "No query specified")
        update_db_results_table(columns, data, error)

    def show_db_form(e, action: str):
        form_fields, title_text = {}, get_text(action)

        def submit_form(e, error=None):
            try:
                required_map = {'add_person': ['fname', 'lname'], 'add_card': ['card_number', 'person_id'],
                                'add_access': ['card_id', 'location_id'], 'remove_person': ['person_id'],
                                'remove_card': ['card_id'], 'remove_access': ['access_id']}
                if action in required_map:
                    for field_key in required_map[action]:
                        if not form_fields[field_key].value:
                            raise ValueError(
                                get_text('form_error_required').format(field_name=form_fields[field_key].label))
                db_output_cont.content = ft.ProgressRing()
                page.update()
                if action == 'add_person':
                    _, _, error = db.add_person(form_fields['fname'].value, form_fields['mname'].value,
                                                form_fields['lname'].value)
                    handle_db_query(None, query_func=db.get_people)
                elif action == 'add_card':
                    if not (len(form_fields['card_number'].value) == 10 and form_fields['card_number'].value.isdigit()):
                        raise ValueError(get_text('add_card_error_format'))
                    _, _, error = db.add_card(form_fields['card_number'].value, form_fields['person_id'].value)
                    handle_db_query(None, query_func=db.get_cards)
                elif action == 'add_access':
                    _, _, error = db.add_access(form_fields['card_id'].value, form_fields['location_id'].value)
                    handle_db_query(None, query_func=db.get_accesses)
                elif action == 'remove_person':
                    _, _, error = db.remove_person(form_fields['person_id'].value)
                    handle_db_query(None, query_func=db.get_people)
                elif action == 'remove_card':
                    _, _, error = db.remove_card(form_fields['card_id'].value)
                    handle_db_query(None, query_func=db.get_cards)
                elif action == 'remove_access':
                    _, _, error = db.remove_access(form_fields['access_id'].value)
                    handle_db_query(None, query_func=db.get_accesses)
                if error:
                    raise Exception(error)
            except (ValueError, Exception) as ex:
                show_db_form(None, action)

        if action == 'add_person':
            form_fields.update({'fname': ft.TextField(label=get_text('add_person_fname'),
                                                      label_style=ft.TextStyle(weight=ft.FontWeight.BOLD,
                                                                               italic=True)),
                                'mname': ft.TextField(label=get_text('add_person_mname'),
                                                      label_style=ft.TextStyle(weight=ft.FontWeight.BOLD,
                                                                               italic=True)),
                                'lname': ft.TextField(label=get_text('add_person_lname'),
                                                      label_style=ft.TextStyle(weight=ft.FontWeight.BOLD,
                                                                               italic=True))})
        elif action == 'add_card':
            form_fields.update(
                {'card_number': ft.TextField(label=get_text('add_card_number'), max_length=10,
                                             label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
                                             keyboard_type=ft.KeyboardType.NUMBER),
                 'person_id': ft.TextField(label=get_text('add_card_person_id'),
                                           label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
                                           keyboard_type=ft.KeyboardType.NUMBER)})
        elif action == 'add_access':
            form_fields.update(
                {'card_id': ft.TextField(label=get_text('add_access_card_id'),
                                         label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
                                         keyboard_type=ft.KeyboardType.NUMBER),
                 'location_id': ft.TextField(label=get_text('add_access_location_id'),
                                             label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
                                             keyboard_type=ft.KeyboardType.NUMBER)})
        elif action == 'remove_person':
            form_fields.update(
                {'person_id': ft.TextField(label=get_text('remove_person_id'),
                                           label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
                                           keyboard_type=ft.KeyboardType.NUMBER)})
        elif action == 'remove_card':
            form_fields.update(
                {'card_id': ft.TextField(label=get_text('remove_card_id'),
                                         label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
                                         keyboard_type=ft.KeyboardType.NUMBER)})
        elif action == 'remove_access':
            form_fields.update(
                {'access_id': ft.TextField(label=get_text('remove_access_id'),
                                           label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
                                           keyboard_type=ft.KeyboardType.NUMBER)})

        submit_btn = ft.ElevatedButton(get_text('form_submit'), icon=ft.Icons.PLAY_ARROW, on_click=submit_form,
                                       style=ft.ButtonStyle(color=ft.Colors.GREEN))
        db_output_cont.content = ft.Column(
            controls=[ft.Text(title_text, style=ft.TextThemeStyle.TITLE_MEDIUM), ft.Divider()] + list(
                form_fields.values()) + [ft.Row([submit_btn], alignment=ft.MainAxisAlignment.CENTER)], spacing=10)
        db_output_cont.visible = True
        page.update()

    def validate_temp(field: ft.TextField) -> str:
        try:
            val = float(field.value)
            if val > 50:
                val = 50
            if val < -50:
                val = -50
            field.value = f"{val:.1f}"
            return field.value
        except (ValueError, TypeError):
            field.value = "0.0"
            return "0.0"

    def validate_temp_tol(field: ft.TextField) -> str:
        try:
            val = float(field.value)
            if val < 0:
                val = 0
            if val > 50:
                val = 50
            field.value = f"{val:.1f}"
            return field.value
        except (ValueError, TypeError):
            field.value = "0.0"
            return "0.0"

    def validate_lux(field: ft.TextField) -> str:
        try:
            val = int(field.value)
            if val > 100000:
                val = 100000
            if val < 0:
                val = 0
            field.value = str(val)
            return field.value
        except (ValueError, TypeError):
            field.value = "0"
            return "0"

    def validate_sensor_number(field: ft.TextField):
        field.value = str(max(0, int(field.value or '0')))
        return field.value

    work_start_field, work_end_field = ft.TextField(label=get_text("work_hours_start"),
                                                    label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
                                                    expand=True,
                                                    disabled=not any(state.cfg_work_days),
                                                    text_size=small_text_size,
                                                    value=state.cfg_work_start), ft.TextField(
        label=get_text("work_hours_end"), label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True), expand=True,
        disabled=not state.cfg_heat_off_days, text_size=small_text_size, value=state.cfg_work_end)
    cold_start_field, cold_end_field = ft.TextField(label=get_text("cold_months_begin"),
                                                    label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
                                                    expand=True,
                                                    disabled=not state.cfg_heat_off_days,
                                                    text_size=small_text_size,
                                                    value=state.cfg_cold_start), ft.TextField(
        label=get_text("cold_months_end"), label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
        expand=True, disabled=not state.cfg_heat_off_days,
        text_size=small_text_size, value=state.cfg_cold_end)

    work_temp_field = ft.TextField(
        label=get_text("desired_work_temp"), label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
        expand=True,
        text_size=small_text_size, value=state.cfg_work_temp
    )
    non_work_temp_field = ft.TextField(
        label=get_text("desired_non_work_temp"), label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
        expand=True, disabled=not state.cfg_heat_off_days,
        text_size=small_text_size, value=state.cfg_non_work_temp
    )
    temp_tol_field = ft.TextField(
        label=get_text("work_temp_tolerance"), label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
        expand=True,
        text_size=small_text_size, value=state.cfg_work_temp_tol,
    )

    park_spots_field, max_spots_field = ft.TextField(label=get_text("num_spots"),
                                                     label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
                                                     text_size=small_text_size,
                                                     value=state.cfg_park_spots), ft.TextField(
        label=get_text("max_spots"), label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
        text_size=small_text_size, value=state.cfg_max_park_spots)
    light_thresh_field, light_tol_field = ft.TextField(label=get_text("threshold_lux"),
                                                       label_style=ft.TextStyle(weight=ft.FontWeight.BOLD,
                                                                                italic=True), expand=True,
                                                       text_size=small_text_size,
                                                       value=state.cfg_light_thresh), ft.TextField(
        label=get_text("tolerance_lux"), label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
        expand=True, text_size=small_text_size, value=state.cfg_light_tol)
    measured_light_text = ft.Text(f"{get_text('measured_light')} {state.measured_light}", weight=ft.FontWeight.BOLD)
    state.ui_refs['measured_light_text'] = measured_light_text

    work_days_keys = ["mo", "tu", "we", "th", "fr", "sa", "su"]
    work_days_controls = [ft.Checkbox(expand=True, label=get_text(day_key),
                                      label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
                                      value=state.cfg_work_days[i],
                                      on_change=lambda e: (setattr(work_start_field, 'disabled',
                                                                   not any(cb.value for cb in work_days_controls)),
                                                           setattr(work_end_field, 'disabled',
                                                                   not any(cb.value for cb in work_days_controls)),
                                                           page.update())) for i, day_key in enumerate(work_days_keys)]
    heating_off_days_switch = ft.Switch(label=get_text("enable_heating_off_days"),
                                        label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
                                        value=state.cfg_heat_off_days,
                                        on_change=lambda e: (setattr(cold_start_field, 'disabled', not e.control.value),
                                                             setattr(cold_end_field, 'disabled', not e.control.value),
                                                             setattr(non_work_temp_field, 'disabled',
                                                                     not e.control.value), page.update()))
    wd_only_lobby_switch, wd_only_bldg_switch = ft.Switch(label=get_text("wd_only_lights"),
                                                          label_style=ft.TextStyle(weight=ft.FontWeight.BOLD,
                                                                                   italic=True),
                                                          value=state.cfg_wdonly_lights_l,
                                                          disabled=not state.cfg_auto_lights_lobby), ft.Switch(
        label=get_text("wd_only_lights"), label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
        value=state.cfg_wdonly_lights_b, disabled=not state.cfg_auto_lights_bldg)
    lobby_lights_radiogroup, building_lights_radiogroup = ft.RadioGroup(content=ft.Row(
        [ft.Radio(value="dark", label=get_text("keep_on_dark"),
                  label_style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
         ft.Radio(value="movement", label=get_text("activate_on_movement"),
                  label_style=ft.TextStyle(weight=ft.FontWeight.BOLD))]),
        value=state.cfg_lobby_lights_mode,
        disabled=not state.cfg_auto_lights_lobby), ft.RadioGroup(
        content=ft.Row([ft.Radio(value="dark", label=get_text("keep_on_dark"),
                                 label_style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                        ft.Radio(value="movement", label=get_text("activate_on_movement"),
                                 label_style=ft.TextStyle(weight=ft.FontWeight.BOLD))]),
        value=state.cfg_bldg_lights_mode, disabled=not state.cfg_auto_lights_bldg)
    lobby_auto_switch = ft.Switch(label=get_text("enable_auto_lights_lobby"),
                                  label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
                                  value=state.cfg_auto_lights_lobby,
                                  on_change=lambda e: (
                                      setattr(lobby_lights_radiogroup, 'disabled', not e.control.value),
                                      setattr(wd_only_lobby_switch, 'disabled', not e.control.value), page.update()))
    building_auto_switch = ft.Switch(label=get_text("enable_auto_lights_building"),
                                     label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
                                     value=state.cfg_auto_lights_bldg,
                                     on_change=lambda e: (
                                         setattr(building_lights_radiogroup, 'disabled', not e.control.value),
                                         setattr(wd_only_bldg_switch, 'disabled', not e.control.value),
                                         page.update()))
    sim_io_switch, test_fire_switch, test_security_switch = (
        ft.Switch(label=get_text("enable_sim_io"), label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
                  value=state.cfg_sim_io),
        ft.Switch(label=get_text("test_fire"), label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True), value=state.cfg_test_fire),
        ft.Switch(label=get_text("test_security"), label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True), value=state.cfg_test_security))
    cfg_pspots_taken_field, cfg_parking_open_switch, cfg_parking_closed_switch = ft.TextField(
        label=get_text("num_spots_taken"), label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
        value=str(state.p_spots_taken),
        text_size=small_text_size), ft.Switch(label=get_text("keep_parking_open"),
                                              label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
                                              value=state.force_park_open,
                                              on_change=handlers['on_keep_parking_open']), ft.Switch(
        label=get_text("keep_parking_closed"), label_style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
        value=state.force_park_close,
        on_change=handlers['on_keep_parking_closed'])
    state.ui_refs.update(
        {'cfg_pspots_taken_field': cfg_pspots_taken_field, 'cfg_force_open_switch': cfg_parking_open_switch,
         'cfg_force_close_switch': cfg_parking_closed_switch})

    def on_submit_plc_config(e):
        state.cfg_work_start, state.cfg_work_end = validate_sensor_number(work_start_field), validate_sensor_number(
            work_end_field)
        state.cfg_cold_start, state.cfg_cold_end = validate_sensor_number(cold_start_field), validate_sensor_number(
            cold_end_field)

        state.cfg_work_temp = validate_temp(work_temp_field)
        state.cfg_non_work_temp = validate_temp(non_work_temp_field)
        tolerance_value = validate_temp_tol(temp_tol_field)
        state.cfg_work_temp_tol = tolerance_value
        state.cfg_non_work_temp_tol = tolerance_value
        state.p_spots_taken = int(validate_sensor_number(cfg_pspots_taken_field))
        state.cfg_park_spots, state.p_spots_total = validate_sensor_number(park_spots_field), int(
            validate_sensor_number(park_spots_field))
        state.cfg_max_park_spots = validate_sensor_number(max_spots_field)
        state.cfg_light_thresh, state.cfg_light_tol = validate_lux(light_thresh_field), validate_lux(light_tol_field)
        state.cfg_work_days = [cb.value for cb in work_days_controls]
        state.cfg_heat_off_days, state.cfg_auto_lights_lobby, state.cfg_wdonly_lights_l = heating_off_days_switch.value, lobby_auto_switch.value, wd_only_lobby_switch.value
        state.cfg_lobby_lights_mode, state.cfg_auto_lights_bldg, state.cfg_wdonly_lights_b = lobby_lights_radiogroup.value, building_auto_switch.value, wd_only_bldg_switch.value
        state.cfg_bldg_lights_mode, state.cfg_sim_io, state.cfg_test_fire, state.cfg_test_security = building_lights_radiogroup.value, sim_io_switch.value, test_fire_switch.value, test_security_switch.value
        state.config_altered = True

    submit_button = ft.ElevatedButton(get_text("submit_changes"), icon=ft.Icons.SAVE, on_click=on_submit_plc_config,
                                      width=300, style=ft.ButtonStyle(color=ft.Colors.GREEN))
    plc_config_container = ft.Container(content=ft.Column(controls=[
        ft.Text(get_text("plc_config"), style=ft.TextThemeStyle.HEADLINE_SMALL), ft.Divider(),
        ft.Column([ft.Text(get_text("work_schedule"), style=ft.TextThemeStyle.TITLE_MEDIUM,
                           weight=ft.FontWeight.BOLD), ft.Row(work_days_controls),
                   ft.Row([work_start_field, work_end_field])]), ft.Divider(thickness=0.2),
        ft.Column(
            [ft.Text(get_text("heating_cooling"), style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
             heating_off_days_switch,
             ft.Row([cold_start_field, cold_end_field]),
             ft.Row([work_temp_field, non_work_temp_field], spacing=10),
             ft.Row([temp_tol_field], spacing=10)]), ft.Divider(thickness=0.2),
        ft.Column([ft.Text(get_text("config_parking_lot"), style=ft.TextThemeStyle.TITLE_MEDIUM,
                           weight=ft.FontWeight.BOLD), park_spots_field,
                   max_spots_field, cfg_pspots_taken_field, cfg_parking_open_switch, cfg_parking_closed_switch]),
        ft.Divider(thickness=0.2),
        ft.Column([ft.Text(get_text("lights_control"), style=ft.TextThemeStyle.TITLE_MEDIUM,
                           weight=ft.FontWeight.BOLD),
                   ft.Row([light_thresh_field, light_tol_field]), measured_light_text,
                   ft.Divider(height=5, color="transparent"),
                   ft.Text(get_text("config_lobby"), style=ft.TextThemeStyle.TITLE_SMALL, weight=ft.FontWeight.BOLD,
                           italic=True), lobby_auto_switch,
                   wd_only_lobby_switch, lobby_lights_radiogroup,
                   ft.Text(get_text("config_building"), style=ft.TextThemeStyle.TITLE_SMALL, weight=ft.FontWeight.BOLD,
                           italic=True), building_auto_switch,
                   wd_only_bldg_switch, building_lights_radiogroup]), ft.Divider(thickness=0.2),
        ft.Column(
            [ft.Text(get_text("system_testing"), style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
             sim_io_switch, test_fire_switch,
             test_security_switch]), ft.Divider(thickness=0.2),
        ft.Row([submit_button], alignment=ft.MainAxisAlignment.CENTER)
    ], spacing=15), padding=20, border_radius=ft.border_radius.all(30),
        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.ON_SURFACE))

    db_management_container = ft.Container(content=ft.Column([
        ft.Text(get_text("db_management"), style=ft.TextThemeStyle.HEADLINE_SMALL), ft.Divider(), sql_query_field,
        ft.Row([ft.ElevatedButton(get_text("exec_query"), icon=ft.Icons.PLAY_ARROW,
                                  style=ft.ButtonStyle(color=ft.Colors.GREEN), expand=True,
                                  on_click=lambda e: handle_db_query(e, query_str=sql_query_field.value)),
                ft.ElevatedButton(get_text("view_log"), icon=ft.Icons.TABLE_CHART, expand=True,
                                  on_click=lambda e: handle_db_query(e, query_func=db.get_logs))]),
        ft.Row([ft.ElevatedButton(get_text("view_people"), icon=ft.Icons.PEOPLE, expand=True,
                                  on_click=lambda e: handle_db_query(e, query_func=db.get_people)),
                ft.ElevatedButton(get_text("view_cards"), icon=ft.Icons.CREDIT_CARD, expand=True,
                                  on_click=lambda e: handle_db_query(e, query_func=db.get_cards)),
                ft.ElevatedButton(get_text("view_access"), icon=ft.Icons.DATASET, expand=True,
                                  on_click=lambda e: handle_db_query(e, query_func=db.get_accesses))]),
        ft.Row([ft.ElevatedButton(get_text("add_person"), icon=ft.Icons.PERSON_ADD,
                                  style=ft.ButtonStyle(color=ft.Colors.GREEN), expand=True,
                                  on_click=lambda e: show_db_form(e, 'add_person')),
                ft.ElevatedButton(get_text("add_card"), icon=ft.Icons.ADD_CARD,
                                  style=ft.ButtonStyle(color=ft.Colors.GREEN), expand=True,
                                  on_click=lambda e: show_db_form(e, 'add_card')),
                ft.ElevatedButton(get_text("add_access"), icon=ft.Icons.VERIFIED_USER,
                                  style=ft.ButtonStyle(color=ft.Colors.GREEN), expand=True,
                                  on_click=lambda e: show_db_form(e, 'add_access'))]),
        ft.Row([ft.ElevatedButton(get_text("remove_person"), icon=ft.Icons.PERSON_REMOVE,
                                  style=ft.ButtonStyle(color=ft.Colors.RED_ACCENT), expand=True,
                                  on_click=lambda e: show_db_form(e, 'remove_person')),
                ft.ElevatedButton(get_text("remove_card"), icon=ft.Icons.REMOVE_MODERATOR,
                                  style=ft.ButtonStyle(color=ft.Colors.RED_ACCENT), expand=True,
                                  on_click=lambda e: show_db_form(e, 'remove_card')),
                ft.ElevatedButton(get_text("remove_access"), icon=ft.Icons.GPP_BAD,
                                  style=ft.ButtonStyle(color=ft.Colors.RED_ACCENT), expand=True,
                                  on_click=lambda e: show_db_form(e, 'remove_access'))]),
        db_output_cont,
    ], spacing=15), padding=20, border_radius=ft.border_radius.all(30),
        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.ON_SURFACE))

    return ft.View(
        "/config",
        [ft.ResponsiveRow([ft.Column(col={"xs": 12, "lg": 6}, controls=[plc_config_container]),
                           ft.Column(col={"xs": 12, "lg": 6}, controls=[db_management_container])], spacing=20,
                          run_spacing=20)],
        appbar=create_appbar(page, state, get_text, handlers['toggle_lang'], handlers['logout']),
        vertical_alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, padding=20,
        scroll=ft.ScrollMode.AUTO
    )
