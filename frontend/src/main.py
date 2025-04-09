import flet as ft
from pages.Login import LoginPage
from pages.Signup import SignUpPage

def main(page: ft.Page):
    page.title='Market studies'
    page.theme_mode=ft.ThemeMode.DARK
    
    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(LoginPage(page))
        elif page.route=="/signup":
            page.views.append(SignUpPage(page))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main)
