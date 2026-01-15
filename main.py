import flet as ft
import sqlite3
from database.init_db import init_db

# Initialize database on startup
init_db()

class LexApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Lex - Teacher Lesson Diary System"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window_width = 1200
        self.page.window_height = 800
        
        self.current_teacher_id = 1 # Default for now
        self.ensure_default_teacher()

        self.setup_ui()

    def ensure_default_teacher(self):
        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM teachers LIMIT 1")
        row = cursor.fetchone()
        if not row:
            cursor.execute("INSERT INTO teachers (name) VALUES (?)", ("Default Teacher",))
            self.current_teacher_id = cursor.lastrowid
        else:
            self.current_teacher_id = row[0]
        conn.commit()
        conn.close()

    def setup_ui(self):
        self.nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            leading=ft.Icon(ft.Icons.AUTO_STORIES),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.DASHBOARD_OUTLINED,
                    selected_icon=ft.Icons.DASHBOARD,
                    label="Dashboard",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.BOOK_OUTLINED,
                    selected_icon=ft.Icons.BOOK,
                    label="Syllabus",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.EDIT_NOTE_OUTLINED,
                    selected_icon=ft.Icons.EDIT_NOTE,
                    label="Diary",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.GROUPS_OUTLINED,
                    selected_icon=ft.Icons.GROUPS,
                    label="Cohorts",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS,
                    label="Settings",
                ),
            ],
            on_change=self.nav_change,
        )

        self.content_area = ft.Container(
            content=ft.Text("Welcome to Lex", size=30, weight=ft.FontWeight.BOLD),
            expand=True,
            padding=20,
        )

        self.page.add(
            ft.Row(
                [
                    self.nav_rail,
                    ft.VerticalDivider(width=1),
                    self.content_area,
                ],
                expand=True,
            )
        )

    def nav_change(self, e):
        index = e.control.selected_index
        if index == 0:
            self.show_dashboard()
        elif index == 1:
            self.show_syllabus()
        elif index == 2:
            self.show_diary()
        elif index == 3:
            self.show_cohorts()
        elif index == 4:
            self.show_settings()
        self.page.update()

    def show_dashboard(self):
        self.content_area.content = ft.Column([
            ft.Text("Dashboard", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Quick stats and recent entries will appear here."),
        ])

    def show_syllabus(self):
        from ui.syllabus_view import SyllabusView
        self.content_area.content = SyllabusView(self.page, self.current_teacher_id)

    def show_diary(self):
        from ui.diary_view import DiaryView
        self.content_area.content = DiaryView(self.page, self.current_teacher_id)

    def show_cohorts(self):
        from ui.cohort_view import CohortView
        self.content_area.content = CohortView(self.page, self.current_teacher_id)

    def show_settings(self):
        from ui.settings_view import SettingsView
        self.content_area.content = SettingsView(self.page, self.current_teacher_id)

def main(page: ft.Page):
    LexApp(page)

if __name__ == "__main__":
    ft.run(main)
