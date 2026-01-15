import flet as ft
from ui.language_manager import LanguageManager

class SettingsView(ft.Column):
    def __init__(self, page: ft.Page, lang_manager: LanguageManager, on_lang_change):
        super().__init__()
        self.page = page
        self.lang_manager = lang_manager
        self.on_lang_change = on_lang_change
        
        self.init_ui()

    def init_ui(self):
        self.controls = [
            ft.Text(self.lang_manager.get_string("settings_title"), size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text(self.lang_manager.get_string("select_language"), size=16),
            ft.Dropdown(
                width=200,
                value=self.lang_manager.current_lang,
                options=[
                    ft.dropdown.Option("en", "English"),
                    ft.dropdown.Option("sq", "Shqip (Albanian)"),
                ],
                on_change=self.change_language
            ),
        ]

    def change_language(self, e):
        new_lang = e.control.value
        self.lang_manager.set_language(new_lang)
        self.on_lang_change()
        
        snack = ft.SnackBar(ft.Text(self.lang_manager.get_string("settings_saved")))
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()
