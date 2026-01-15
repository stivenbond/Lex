import flet as ft
import sqlite3

class SettingsView(ft.Column):
    def __init__(self, page: ft.Page, teacher_id: int):
        super().__init__(expand=True)
        self.main_page = page
        self.teacher_id = teacher_id
        
        self.teacher_name_field = ft.TextField(label="Teacher Name", expand=True)
        self.fields_list = ft.Column(spacing=10)
        
        self.load_data()
        self.build_ui()

    def load_data(self):
        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        
        # Load teacher name
        cursor.execute("SELECT name FROM teachers WHERE id = ?", (self.teacher_id,))
        self.teacher_name_field.value = cursor.fetchone()[0]
        
        # Load diary fields
        cursor.execute("SELECT id, label, description, stability FROM diary_fields WHERE teacher_id = ?", (self.teacher_id,))
        self.fields = cursor.fetchall()
        
        conn.close()

    def build_ui(self):
        self.controls = [
            ft.Text("Settings", size=30, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text("Teacher Information", size=20, weight=ft.FontWeight.W_500),
            ft.Row([
                self.teacher_name_field,
                ft.ElevatedButton("Save Name", on_click=self.save_teacher_name)
            ]),
            ft.Divider(),
            ft.Row([
                ft.Text("Diary Schema Definition", size=20, weight=ft.FontWeight.W_500),
                ft.IconButton(ft.Icons.ADD, on_click=self.add_field_dialog)
            ]),
            ft.Text("Define the fields that appear in your diary entries.", italic=True),
            self.fields_list
        ]
        self.refresh_fields_list()

    def refresh_fields_list(self):
        self.fields_list.controls.clear()
        for field in self.fields:
            self.fields_list.controls.append(
                ft.ListTile(
                    title=ft.Text(field[1]),
                    subtitle=ft.Text(f"{field[3]} - {field[2] if field[2] else 'No description'}"),
                    trailing=ft.Row([
                        ft.IconButton(ft.Icons.EDIT_OUTLINED, tooltip="Edit Field", on_click=lambda e, field=field: self.edit_field_dialog(field)),
                        ft.IconButton(ft.Icons.DELETE_OUTLINE, tooltip="Delete Field", icon_color=ft.Colors.RED_400, on_click=lambda e, fid=field[0]: self.delete_field(fid))
                    ], tight=True)
                )
            )
        try:
            self.update()
        except Exception:
            pass

    def save_teacher_name(self, e):
        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE teachers SET name = ? WHERE id = ?", (self.teacher_name_field.value, self.teacher_id))
        conn.commit()
        conn.close()
        self.main_page.snack_bar = ft.SnackBar(ft.Text("Teacher name saved!"))
        self.main_page.snack_bar.open = True
        self.main_page.update()

    def add_field_dialog(self, e):
        label_inp = ft.TextField(label="Field Label (e.g., Homework, Goal)")
        desc_inp = ft.TextField(label="Description (optional)")
        stability_drop = ft.Dropdown(
            label="Stability",
            options=[
                ft.dropdown.Option("STATIC", "Static (Same across years)"),
                ft.dropdown.Option("DYNAMIC", "Dynamic (Lesson-specific)"),
            ],
            value="DYNAMIC"
        )

        def save_new_field(e):
            if not label_inp.value: return
            conn = sqlite3.connect("lex_database.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO diary_fields (teacher_id, label, description, stability) VALUES (?, ?, ?, ?)",
                           (self.teacher_id, label_inp.value, desc_inp.value, stability_drop.value))
            conn.commit()
            conn.close()
            self.load_data()
            self.refresh_fields_list()
            dialog.open = False
            self.main_page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Add Diary Field"),
            content=ft.Column([label_inp, desc_inp, stability_drop], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: setattr(dialog, "open", False)),
                ft.ElevatedButton("Save", on_click=save_new_field)
            ]
        )
        self.main_page.dialog = dialog
        dialog.open = True
        self.main_page.update()

    def edit_field_dialog(self, field):
        label_inp = ft.TextField(label="Field Label", value=field[1])
        desc_inp = ft.TextField(label="Description", value=field[2])
        stability_drop = ft.Dropdown(
            label="Stability",
            options=[
                ft.dropdown.Option("STATIC", "Static (Same across years)"),
                ft.dropdown.Option("DYNAMIC", "Dynamic (Lesson-specific)"),
            ],
            value=field[3]
        )

        def confirm_edit(e):
            if not label_inp.value: return
            conn = sqlite3.connect("lex_database.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE diary_fields SET label = ?, description = ?, stability = ? WHERE id = ?",
                           (label_inp.value, desc_inp.value, stability_drop.value, field[0]))
            conn.commit()
            conn.close()
            self.load_data()
            self.refresh_fields_list()
            dialog.open = False
            self.main_page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Edit Diary Field"),
            content=ft.Column([label_inp, desc_inp, stability_drop], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: setattr(dialog, "open", False)),
                ft.ElevatedButton("Save", on_click=confirm_edit)
            ]
        )
        self.main_page.dialog = dialog
        dialog.open = True
        self.main_page.update()

    def delete_field(self, field_id):
        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM diary_fields WHERE id = ?", (field_id,))
        conn.commit()
        conn.close()
        self.load_data()
        self.refresh_fields_list()
