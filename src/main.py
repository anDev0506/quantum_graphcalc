import flet as ft
from scripts import newinputfunc as ev
from utils import *
import asyncio

async def main(page: ft.Page):
    sub_div: int = 25
    page.theme_mode = ft.ThemeMode.DARK
    
    def change_theme(k):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            color_theme_button.icon = ft.Icons.DARK_MODE
            page.update()
        else:
            page.theme_mode = ft.ThemeMode.DARK
            color_theme_button.icon = ft.Icons.LIGHT_MODE
            page.update()
    
    def add(k: ft.ControlEvent, value: int = 1):
        nonlocal sub_div
        sub_div += value
        change_subdivs.value = sub_div
        page.update()
    
    old_expression: str = ''
    old_limit_a: int = 0
    old_limit_b: int = 0
    old_subdiv: int = 25
    expression: ft.TextField = ft.TextField(
        value="sin(x)",
        width=256,
        label="Expression",
        hint_text="Write here the mathematical expression to plot"
    )
    
    limit_a: Limit = Limit(value=-6, label="X\u2081", page=page)
    limit_b: Limit = Limit(value=6, label="X\u2082", page=page)
    color_theme_button: ft.IconButton = ft.IconButton(on_click=change_theme, icon=ft.Icons.LIGHT_MODE)
    settings_button: ft.IconButton = ft.IconButton(
        icon=ft.Icons.SETTINGS,
        on_click=lambda k: page.open(settings_screen)
    )
    
    change_subdivs: ft.TextField = ft.TextField(
        label="Subdivisions",
        hint_text="This value represents the subdivisions of a inteval",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=128,
        value=sub_div,
        input_filter=ft.NumbersOnlyInputFilter())
    
    plus_1_sub: ft.IconButton = ft.IconButton(
        icon=ft.Icons.ADD,
        on_click=lambda k: add(k))
    
    minus_1_sub: ft.IconButton = ft.IconButton(
        icon=ft.Icons.REMOVE,
        on_click=lambda k: add(k, -1))

    interval_settings: ft.AlertDialog = ft.AlertDialog(
        title=ft.Text("Interval"),
        content=ft.Column([
            ft.Text("Here you can change the interval of plotting by modifying X\u2081 and X\u2082.", text_align=ft.TextAlign.CENTER),
            ft.Row([limit_a, limit_b], alignment=ft.MainAxisAlignment.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        actions=[ft.TextButton("Close", on_click=lambda k: page.close(interval_settings))]
    )

    open_interval_button: ft.ElevatedButton = ft.ElevatedButton(
        text="Interval",
        on_click=lambda k: page.open(interval_settings),
    )

    subdivs_settings: ft.AlertDialog = ft.AlertDialog(
        title=ft.Text("Subdivisions"),
        content=ft.Column([
            ft.Text("Here you can change the subdivisions per interval\nBigger values implies better accuracy but less performance.", text_align=ft.TextAlign.CENTER),
            ft.Row([plus_1_sub, change_subdivs, minus_1_sub], alignment=ft.MainAxisAlignment.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        actions=[ft.TextButton("Close", on_click=lambda k: page.close(subdivs_settings))]
    )

    open_subdivs_button: ft.ElevatedButton = ft.ElevatedButton(
        text="Subdivisions",
        on_click=lambda k: page.open(subdivs_settings),
    )

    settings_screen: ft.AlertDialog = ft.AlertDialog(
        title=ft.Text("Settings"),
        content=ft.Row([
                open_interval_button,
                open_subdivs_button,
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        actions=[ft.TextButton("Close", on_click=lambda k: page.close(settings_screen)), color_theme_button]
    )
    
    axis: Axis = Axis(
        max_y=1,
        min_y=-1,
        page=page
    )
    
    show_info_distribution_1: ft.Container = ft.Container(
        content=ft.Column([expression, ft.Row([limit_a, limit_b])], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        height=150,
        border_radius=8,
        alignment=ft.alignment.top_left,
        padding=2,
        blur=2,
        bgcolor=ft.Colors.with_opacity(0.5, color=ft.Colors.SECONDARY_CONTAINER)
    )
    
    distribution_1: ft.Stack = ft.Stack([
        axis,
        show_info_distribution_1,
        ft.Row([settings_button], alignment=ft.MainAxisAlignment.END, vertical_alignment=ft.CrossAxisAlignment.END)
    ])
        
    if (sub_div < 10):
        sub_div = 10
        change_subdivs.value = sub_div
        page.update()
    
    if (page.width) > 1000:
        show_info_distribution_1.width = page.width * 3/10
    else:
        show_info_distribution_1.width = page.width * 1/2
    
    axis.height = page.height - 3
    axis.width = page.width - 3
    if (page.height < page.width):
        page.add(distribution_1)
    else:
        axis.left_axis_labels_size = 0
        page.bottom_appbar = ft.BottomAppBar(
            content=ft.Row([expression, settings_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            shape=ft.NotchShape.AUTO,
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.INVERSE_PRIMARY)
        )
        page.add(ft.SafeArea(axis))
        
    page.on_media_change = lambda k: when_change_window(k, axis, distribution_1, expression, settings_button)
    page.window.on_resized = lambda k: when_change_window(k, axis, distribution_1, expression, settings_button)
    page.on_resized = lambda k: when_change_window(k, axis, distribution_1, expression, settings_button)

    while (True):
        if (expression.value != old_expression or old_limit_a != limit_a.value or old_limit_b != limit_b.value or old_subdiv != sub_div):
            axis.graph_data(limit_a, limit_b, sub_div, expression)
        old_expression = expression.value
        old_limit_a = limit_a.value
        old_limit_b = limit_b.value
        old_subdiv = sub_div
        await asyncio.sleep(0.5)
    
    
ft.app(main)
