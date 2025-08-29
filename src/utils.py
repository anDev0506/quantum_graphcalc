import flet as ft
from typing import List
from scripts import newinputfunc as ev

number_filter = ft.InputFilter([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "+-"])

class Limit(ft.Row):
    def __init__(self, value: int, label: str, page: ft.Page = None):
        super().__init__()
        
        self.label: str = label
        self.value: int = value
        self.page: ft.Page = page
        
        def add(k:ft.ControlEvent, num: int = 1):
            self.value += num
            input_field.value = self.value
            self.page.update()
        
        input_field: ft.TextField = ft.TextField(
            width=64,
            value=self.value,
            input_filter=number_filter,
            label=self.label,
        )

        add_1_button: ft.IconButton = ft.IconButton(
            icon=ft.Icons.ADD,
            on_click=add)
        less_1_button: ft.IconButton = ft.IconButton(
            icon=ft.Icons.REMOVE,
            on_click=lambda k: add(k, -1))
        
        self.aligment: ft.Alignment = ft.MainAxisAlignment.CENTER
        self.controls: List[ft.Control] = [add_1_button, input_field, less_1_button]

class Axis(ft.LineChart):
    def __init__(self, max_y: float, min_y: float, page: ft.Page):
        super().__init__()
        self.max_y: float = max_y
        self.min_y: float = min_y
        self.page: ft.Page = page
        self.bottom_axis: ft.ChartAxis = ft.ChartAxis(labels_size=64)
        self.left_axis: ft.ChartAxis = ft.ChartAxis(labels_size=64)
        self.data_points: List[ft.LineChartDataPoint] = list()
        self.width: int = self.page.width
        self.height: int = self.page.height
        
        self.data_series: List[ft.LineChartData] = [ft.LineChartData(
            data_points=self.data_points,
            color=ft.Colors.ON_PRIMARY_CONTAINER,
            curved=True,
            stroke_width=5,
            stroke_cap_round=True)]
        
        self.border: ft.Border = ft.border.all(5, color=ft.Colors.PRIMARY_CONTAINER)
        self.horizontal_grid_lines: ft.ChartGridLines = ft.ChartGridLines(
            interval=1, color=ft.Colors.PRIMARY_CONTAINER, width=1)
        
        self.vertical_grid_lines: ft.ChartGridLines = ft.ChartGridLines(
            interval=1, color=ft.Colors.PRIMARY_CONTAINER, width=1)
        
        
    def graph_data(self, x_1: Limit, x_2: Limit, subdivisions: int, expression: ft.TextField) -> None:
        aux_x: float
        aux_float: float
        aux_point: ft.LineChartDataPoint
        self.data_points.clear()
        for x in range(x_1.value * subdivisions, x_2.value * subdivisions):
            try:
                aux_x = x/subdivisions
                aux_float = ev.custom_eval(func=expression.value, x=aux_x)
                aux_point = ft.LineChartDataPoint(
                    x=aux_x,
                    y=aux_float,
                    tooltip=f"({aux_x},{aux_float})"
                )
                self.data_points.append(aux_point)
            except ValueError:
                continue
        try:
            self.max_y = max((point.y for point in self.data_points))
            self.min_y = min((point.y for point in self.data_points))
        except:
            pass
        self.page.update()

def when_change_window(k: ft.ControlEvent, axis: Axis, distribution_1: ft.Stack, expression: ft.TextField, settings_button: ft.IconButton):
    axis.page.clean()
    if (axis.page.height < axis.page.width):
        axis.page.bottom_appbar = ft.BottomAppBar(
            shape=ft.NotchShape.AUTO,
            bgcolor=ft.Colors.TRANSPARENT
        )
        axis.page.add(distribution_1)
    else:
        axis.left_axis_labels_size = 0
        axis.page.bottom_appbar = ft.BottomAppBar(
            content=ft.Row([expression, settings_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            shape=ft.NotchShape.AUTO,
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.INVERSE_PRIMARY)
        )
        axis.page.add(ft.SafeArea(axis))