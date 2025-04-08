import flet as ft

class Button(ft.ElevatedButton):
    def __init__(self, page: ft.Page, text: str, icon: str = None, on_click=None,width: float = None,height: float = None):
        super().__init__(text=text, icon=icon, on_click=on_click)
        self.page = page
        self.icon = icon
        self.text = text
        self.on_click = on_click
        self.width = width
        self.height = height
        self.bgcolor=ft.Colors.BLUE_600