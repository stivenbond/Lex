import flet as ft
from ui.app_layout import AppLayout

def main(page: ft.Page):
    page.title = "EduCanvas Desktop"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    
    app = AppLayout(page)
    page.add(app)

if __name__ == "__main__":
    ft.app(target=main)
