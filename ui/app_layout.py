import flet as ft

from ui.language_manager import LanguageManager
from ui.settings_view import SettingsView
from ui.diary_view import DiaryView
from ui.whiteboard_view import WhiteboardView
from ui.exams_view import ExamsView

class AppLayout(ft.Row):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.spacing = 0
        self.lang_manager = LanguageManager(page)

        self.init_ui()

    def init_ui(self):
        self.rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200, # Reduced width for cleaner look
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.BOOK, 
                    selected_icon=ft.icons.BOOK, 
                    label=self.lang_manager.get_string("nav_diary")
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.EDIT_DOCUMENT, 
                    selected_icon=ft.icons.EDIT_DOC, 
                    label=self.lang_manager.get_string("nav_lesson_lab")
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.GESTURE, 
                    selected_icon=ft.icons.GESTURE_OUTLINED, 
                    label=self.lang_manager.get_string("nav_whiteboard")
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.ASSIGNMENT, 
                    selected_icon=ft.icons.ASSIGNMENT_IND, 
                    label=self.lang_manager.get_string("nav_exams")
                ),
                 ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS, 
                    selected_icon=ft.icons.SETTINGS_OUTLINED, 
                    label=self.lang_manager.get_string("nav_settings")
                ),
            ],
            on_change=self.nav_change,
        )

        self.content_area = ft.Container(
            expand=True,
            padding=20,
            content=ft.Text(self.lang_manager.get_string("welcome_message")),
        )

        self.controls = [
            self.rail,
            ft.VerticalDivider(width=1),
            self.content_area,
        ]

    def refresh_ui(self):
        # Re-initialize UI to update strings
        self.controls.clear()
        self.init_ui()
        self.page.update()

    def nav_change(self, e):
        index = e.control.selected_index
        
        if index == 0: # Diary
            self.content_area.content = DiaryView(self.page, self.lang_manager)
        elif index == 2: # Whiteboard
            self.content_area.content = WhiteboardView(self.page)
        elif index == 3: # Exams
            self.content_area.content = ExamsView(self.page)
        elif index == 4: # Settings
            self.content_area.content = SettingsView(
                self.page, 
                self.lang_manager, 
                self.refresh_ui
            )
        else:
            labels = ["Diary", "Lesson Lab", "Whiteboard", "Exams"]
            # For now just showing a placeholder, but using the localized "Coming Soon"
            self.content_area.content = ft.Text(f"{labels[index]} - {self.lang_manager.get_string('coming_soon')}")
        
        self.content_area.update()
