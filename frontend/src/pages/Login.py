import flet as ft
from components.Button import Button

class LoginPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/")

        self.label=ft.Text("Login",size=30,weight=ft.FontWeight.BOLD,color=ft.Colors.WHITE,text_align=ft.TextAlign.CENTER)
        self.page = page
        self.email = ft.TextField(label="Email", width=400)
        self.password = ft.TextField(label="Mot de passe", password=True, width=400)
        self.passwordtrigger=ft.IconButton(icon=ft.Icons.VERIFIED_USER,on_click=self.show_password)
        
        content_row=ft.Row(
            controls=[
                self.password,
                self.passwordtrigger
            ],
            alignment=ft.MainAxisAlignment.CENTER,  
            spacing=-50,  
        )

        login_button = Button(
            page,
            text="Se connecter",
            icon=ft.Icons.LOGIN,
            width=400,
            height=40,
        )
        
        content_column = ft.Column(
            controls=[
                self.label,
                ft.Container(height=50),
                self.email,
                ft.Container(height=50),  
                content_row,
                ft.Container(height=75),  
                login_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,  
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
            spacing=0,  
        )
        
        self.controls = [
            ft.Container(
                content=content_column,
                alignment=ft.alignment.center,  
                margin=ft.margin.only(top=50),
                expand=True  
            )
        ]

    def show_password(self,e):
        if self.password.password:
            self.password.password=False
            self.passwordtrigger.icon=ft.Icons.VERIFIED_USER
            LoginPage.update(self)
        else:
            self.password.password=True
            self.passwordtrigger.icon=ft.Icons.VERIFIED_USER_OUTLINED
            LoginPage.update(self)