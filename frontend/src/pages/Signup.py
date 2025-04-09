import flet as ft

class SignUp(ft.View):
    def __init__(self,page:ft.Page):
        super().__init__(route="/signup")
        self.page=page