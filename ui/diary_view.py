import flet as ft
import sqlite3
import datetime

class DiaryView(ft.Column):
    def __init__(self, page: ft.Page, teacher_id: int):
        super().__init__(expand=True)
        self.main_page = page
        self.teacher_id = teacher_id
        
        self.selected_cohort_id = None
        self.selected_topic_id = None
        
        self.cohort_dropdown = ft.Dropdown(label="Cohort", on_select=self.on_selection_change)
        self.syllabus_dropdown = ft.Dropdown(label="Syllabus", on_select=self.load_topics)
        self.topic_dropdown = ft.Dropdown(label="Topic", on_select=self.on_selection_change)
        
        self.form_container = ft.Column(spacing=15)
        self.entries_list = ft.Column(spacing=10, scroll=ft.ScrollMode.ALWAYS, expand=True)
        
        self.load_initial_data()
        self.build_ui()
        self.load_entries()

    def load_initial_data(self):
        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        
        # Load cohorts
        cursor.execute("SELECT id, name FROM cohorts WHERE teacher_id = ?", (self.teacher_id,))
        self.cohorts = cursor.fetchall()
        self.cohort_dropdown.options = [ft.dropdown.Option(str(c[0]), c[1]) for c in self.cohorts]
        
        # Load syllabuses
        cursor.execute("SELECT id, name FROM syllabuses WHERE teacher_id = ?", (self.teacher_id,))
        self.syllabuses = cursor.fetchall()
        self.syllabus_dropdown.options = [ft.dropdown.Option(str(s[0]), s[1]) for s in self.syllabuses]
        
        conn.close()

    def load_topics(self, e):
        syllabus_id = self.syllabus_dropdown.value
        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM topics WHERE syllabus_id = ? ORDER BY order_index", (syllabus_id,))
        topics = cursor.fetchall()
        conn.close()
        
        self.topic_dropdown.options = [ft.dropdown.Option(str(t[0]), t[1]) for t in topics]
        self.topic_dropdown.value = None
        try:
            self.update()
        except:
            pass

    def on_selection_change(self, e):
        self.refresh_form()

    def refresh_form(self):
        self.form_container.controls.clear()
        
        cohort_id = self.cohort_dropdown.value
        topic_id = self.topic_dropdown.value
        
        if not cohort_id or not topic_id:
            self.form_container.controls.append(
                ft.Text("Select a cohort and a topic from the dropdowns above to start a diary entry.", italic=True)
            )
            try:
                self.update()
            except Exception:
                pass
            return

        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        
        # Check if this topic has been taught before by this teacher
        cursor.execute("""
            SELECT id, teaching_date, cohort_id 
            FROM diary_entries 
            WHERE teacher_id = ? AND topic_id = ? AND is_reference = 0
            LIMIT 1
        """, (self.teacher_id, topic_id))
        primary_entry = cursor.fetchone()
        
        if primary_entry:
            # Show Reference Entry UI
            cursor.execute("SELECT name FROM cohorts WHERE id = ?", (primary_entry[2],))
            primary_cohort_name = cursor.fetchone()[0]
            
            self.form_container.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text("Reference Entry", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER),
                        ft.Text(f"This topic was already taught on {primary_entry[1]} in cohort {primary_cohort_name}."),
                        ft.Text("A reference will be created to avoid duplication."),
                        ft.ElevatedButton("Create Reference Entry", on_click=lambda e: self.save_entry(is_reference=True, ref_id=primary_entry[0]))
                    ]),
                    padding=20,
                    bgcolor=ft.Colors.GREY_900,
                    border_radius=10
                )
            )
        else:
            # Show Full Entry UI
            self.form_container.controls.append(ft.Text("New Diary Entry", size=20, weight=ft.FontWeight.BOLD))
            
            # Load schema fields
            cursor.execute("SELECT id, label, stability FROM diary_fields WHERE teacher_id = ?", (self.teacher_id,))
            fields = cursor.fetchall()
            
            self.field_inputs = {}
            for f in fields:
                input_field = ft.TextField(label=f[1], multiline=True, min_lines=2)
                self.field_inputs[f[0]] = input_field
                self.form_container.controls.append(input_field)
            
            self.form_container.controls.append(
                ft.ElevatedButton("Save Diary Entry", on_click=lambda e: self.save_entry(is_reference=False))
            )
            
        conn.close()
        try:
            self.update()
        except Exception:
            pass

    def save_entry(self, is_reference, ref_id=None):
        cohort_id = self.cohort_dropdown.value
        topic_id = self.topic_dropdown.value
        date_str = datetime.date.today().isoformat()
        
        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO diary_entries (teacher_id, topic_id, cohort_id, teaching_date, is_reference, reference_entry_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.teacher_id, topic_id, cohort_id, date_str, 1 if is_reference else 0, ref_id))
        
        entry_id = cursor.lastrowid
        
        if not is_reference:
            for field_id, inp in self.field_inputs.items():
                cursor.execute("""
                    INSERT INTO diary_values (entry_id, field_id, value)
                    VALUES (?, ?, ?)
                """, (entry_id, field_id, inp.value))
        
        conn.commit()
        conn.close()
        
        self.main_page.snack_bar = ft.SnackBar(ft.Text("Diary entry saved!"))
        self.main_page.snack_bar.open = True
        self.refresh_form()
        self.load_entries()
        self.main_page.update()

    def edit_entry_dialog(self, entry_id, topic_name):
        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        
        # Load current values
        cursor.execute("""
            SELECT f.id, f.label, v.value
            FROM diary_fields f
            LEFT JOIN diary_values v ON f.id = v.field_id AND v.entry_id = ?
            WHERE f.teacher_id = ?
        """, (entry_id, self.teacher_id))
        fields_data = cursor.fetchall()
        
        edit_inputs = {}
        controls = []
        for fid, label, val in fields_data:
            inp = ft.TextField(label=label, value=val if val else "", multiline=True, min_lines=2)
            edit_inputs[fid] = inp
            controls.append(inp)
            
        def confirm_edit(e):
            conn = sqlite3.connect("lex_database.db")
            cursor = conn.cursor()
            for fid, inp in edit_inputs.items():
                # Check if value exists to UPDATE or INSERT
                cursor.execute("SELECT id FROM diary_values WHERE entry_id = ? AND field_id = ?", (entry_id, fid))
                val_row = cursor.fetchone()
                if val_row:
                    cursor.execute("UPDATE diary_values SET value = ? WHERE id = ?", (inp.value, val_row[0]))
                else:
                    cursor.execute("INSERT INTO diary_values (entry_id, field_id, value) VALUES (?, ?, ?)", (entry_id, fid, inp.value))
            conn.commit()
            conn.close()
            self.load_entries()
            dialog.open = False
            self.main_page.update()

        dialog = ft.AlertDialog(
            title=ft.Text(f"Edit Entry: {topic_name}"),
            content=ft.Column(controls, tight=True, scroll=ft.ScrollMode.ALWAYS),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: setattr(dialog, "open", False)),
                ft.ElevatedButton("Save Changes", on_click=confirm_edit)
            ]
        )
        self.main_page.dialog = dialog
        dialog.open = True
        self.main_page.update()
        conn.close()

    def delete_entry(self, entry_id):
        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM diary_entries WHERE id = ?", (entry_id,))
        cursor.execute("DELETE FROM diary_values WHERE entry_id = ?", (entry_id,))
        conn.commit()
        conn.close()
        self.load_entries()
        self.main_page.update()

    def load_entries(self):
        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.id, e.teaching_date, t.name, c.name, e.is_reference
            FROM diary_entries e
            JOIN topics t ON e.topic_id = t.id
            JOIN cohorts c ON e.cohort_id = c.id
            WHERE e.teacher_id = ?
            ORDER BY e.teaching_date DESC, e.id DESC
        """, (self.teacher_id,))
        entries = cursor.fetchall()
        conn.close()

        self.entries_list.controls.clear()
        for ent in entries:
            self.entries_list.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{ent[2]} ({ent[3]})"),
                    subtitle=ft.Text(f"{ent[1]} {'(Ref)' if ent[4] else ''}"),
                    trailing=ft.Row([
                        ft.IconButton(ft.Icons.EDIT_OUTLINED, tooltip="Edit Entry", on_click=lambda e, eid=ent[0], tname=ent[2]: self.edit_entry_dialog(eid, tname), visible=ent[4]==0),
                        ft.IconButton(ft.Icons.PICTURE_AS_PDF, tooltip="Export PDF", on_click=lambda e, eid=ent[0]: self.export_entry(eid, 'pdf')),
                        ft.IconButton(ft.Icons.DESCRIPTION, tooltip="Export Word", on_click=lambda e, eid=ent[0]: self.export_entry(eid, 'docx')),
                        ft.IconButton(ft.Icons.DELETE_OUTLINE, tooltip="Delete Entry", icon_color=ft.Colors.RED_400, on_click=lambda e, eid=ent[0]: self.delete_entry(eid)),
                    ], tight=True)
                )
            )
        if not entries:
            self.entries_list.controls.append(ft.Text("No entries found yet.", italic=True))
        try:
            self.update()
        except:
            pass

    def export_entry(self, entry_id, format):
        from services.export_service import ExportService
        import os
        
        filename = f"diary_entry_{entry_id}.{format}"
        # For simplicity, save in current dir
        if format == 'pdf':
            ExportService.export_to_pdf(entry_id, filename)
        else:
            ExportService.export_to_docx(entry_id, filename)
            
        self.main_page.snack_bar = ft.SnackBar(ft.Text(f"Exported to {filename}"))
        self.main_page.snack_bar.open = True
        self.main_page.update()

    def build_ui(self):
        self.controls = [
            ft.Text("Diary Management", size=30, weight=ft.FontWeight.BOLD),
            ft.Row([
                self.cohort_dropdown,
                self.syllabus_dropdown,
                self.topic_dropdown,
            ]),
            ft.Divider(),
            ft.Row([
                ft.Column([
                    ft.Text("New/Reference Entry Form", size=20, weight=ft.FontWeight.W_500),
                    self.form_container
                ], expand=True),
                ft.VerticalDivider(),
                ft.Column([
                    ft.Text("Recent Entries", size=20, weight=ft.FontWeight.W_500),
                    self.entries_list
                ], expand=True)
            ], expand=True)
        ]
