import flet as ft
import sqlite3

class CohortView(ft.Column):
    def __init__(self, page: ft.Page, teacher_id: int):
        super().__init__(expand=True)
        self.main_page = page
        self.teacher_id = teacher_id
        
        self.cohort_name_field = ft.TextField(label="Cohort Name", expand=True)
        self.cohorts_list = ft.ListView(expand=True, spacing=10)
        
        self.load_data()
        self.build_ui()

    def load_data(self):
        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM cohorts WHERE teacher_id = ?", (self.teacher_id,))
        self.cohorts = cursor.fetchall()
        conn.close()

    def build_ui(self):
        self.controls = [
            ft.Text("Cohorts", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Manage your student groups/cohorts.", italic=True),
            ft.Row([
                self.cohort_name_field,
                ft.ElevatedButton("Add Cohort", icon=ft.Icons.ADD, on_click=self.add_cohort)
            ]),
            ft.Divider(),
            self.cohorts_list
        ]
        self.refresh_list()

    def refresh_list(self):
        self.cohorts_list.controls.clear()
        for c in self.cohorts:
            self.cohorts_list.controls.append(
                ft.ListTile(
                    title=ft.Text(c[1]),
                    trailing=ft.Row([
                        ft.IconButton(ft.Icons.EDIT_OUTLINED, tooltip="Rename Cohort", on_click=lambda e, cohort=c: self.edit_cohort_dialog(cohort)),
                        ft.IconButton(ft.Icons.DELETE_OUTLINE, tooltip="Delete Cohort", icon_color=ft.Colors.RED_400, on_click=lambda e, cid=c[0]: self.delete_cohort(cid))
                    ], tight=True)
                )
            )
        try:
            self.update()
        except Exception:
            pass

    def edit_cohort_dialog(self, cohort):
        name_inp = ft.TextField(label="Cohort Name", value=cohort[1])
        def confirm_edit(ev):
            if not name_inp.value: return
            conn = sqlite3.connect("lex_database.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE cohorts SET name = ? WHERE id = ?", (name_inp.value, cohort[0]))
            conn.commit()
            conn.close()
            self.load_data()
            self.refresh_list()
            dialog.open = False
            self.main_page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Rename Cohort"),
            content=name_inp,
            actions=[ft.ElevatedButton("Save", on_click=confirm_edit)]
        )
        self.main_page.dialog = dialog
        dialog.open = True
        self.main_page.update()

    def add_cohort(self, e):
        if not self.cohort_name_field.value: return
        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cohorts (teacher_id, name) VALUES (?, ?)", (self.teacher_id, self.cohort_name_field.value))
        conn.commit()
        conn.close()
        self.cohort_name_field.value = ""
        self.load_data()
        self.refresh_list()

    def delete_cohort(self, cid):
        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cohorts WHERE id = ?", (cid,))
        conn.commit()
        conn.close()
        self.load_data()
        self.refresh_list()
