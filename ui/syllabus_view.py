import flet as ft
import sqlite3
from services.import_service import parse_docx_table, parse_xlsx_table, import_syllabus

class SyllabusView(ft.Column):
    def __init__(self, page: ft.Page, teacher_id: int):
        super().__init__(expand=True)
        self.main_page = page
        self.teacher_id = teacher_id
        
        self.syllabuses = []
        self.selected_syllabus_id = None
        
        self.syllabus_dropdown = ft.Dropdown(label="Select Syllabus", on_select=self.on_syllabus_select, expand=True)
        self.topics_list = ft.ListView(expand=True, spacing=10)
        
        self.load_syllabuses()
        self.build_ui()

    def load_syllabuses(self):
        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM syllabuses WHERE teacher_id = ?", (self.teacher_id,))
        self.syllabuses = cursor.fetchall()
        conn.close()
        
        self.syllabus_dropdown.options = [ft.dropdown.Option(str(s[0]), s[1]) for s in self.syllabuses]
        if self.syllabuses:
            if not self.selected_syllabus_id or self.selected_syllabus_id not in [s[0] for s in self.syllabuses]:
                self.selected_syllabus_id = self.syllabuses[0][0]
            self.syllabus_dropdown.value = str(self.selected_syllabus_id)
        else:
            self.selected_syllabus_id = None
            self.syllabus_dropdown.value = None

    def on_syllabus_select(self, e):
        self.selected_syllabus_id = int(self.syllabus_dropdown.value)
        self.refresh_topics()

    def refresh_topics(self):
        if not self.selected_syllabus_id: return
        
        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, topic_id_string, name FROM topics WHERE syllabus_id = ? ORDER BY order_index", (self.selected_syllabus_id,))
        topics = cursor.fetchall()
        conn.close()
        
        self.topics_list.controls.clear()
        for t in topics:
            self.topics_list.controls.append(
                ft.ListTile(
                    leading=ft.Text(t[1], weight=ft.FontWeight.BOLD),
                    title=ft.Text(t[2]),
                    subtitle=ft.Text("Click to view content", size=12),
                    on_click=lambda e, tid=t[0]: self.show_lesson_content(tid),
                    trailing=ft.Row([
                        ft.IconButton(ft.Icons.EDIT_OUTLINED, tooltip="Edit Topic", on_click=lambda e, topic=t: self.edit_topic_dialog(topic)),
                        ft.IconButton(ft.Icons.DELETE_OUTLINE, tooltip="Delete Topic", icon_color=ft.Colors.RED_400, on_click=lambda e, tid=t[0]: self.delete_topic(tid))
                    ], tight=True)
                )
            )
        try:
            self.update()
        except:
            pass

    def build_ui(self):
        self.controls = [
            ft.Row([
                ft.Text("Syllabus & Topics", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(expand=True),
                ft.ElevatedButton("New Syllabus", icon=ft.Icons.ADD, on_click=self.add_syllabus_dialog),
                ft.ElevatedButton("Import", icon=ft.Icons.UPLOAD_FILE, on_click=self.pick_file)
            ]),
            ft.Row([
                self.syllabus_dropdown,
                ft.IconButton(ft.Icons.EDIT_NOTE, tooltip="Rename Syllabus", on_click=self.rename_syllabus_dialog),
                ft.IconButton(ft.Icons.DELETE, tooltip="Delete Syllabus", on_click=self.delete_syllabus, icon_color=ft.Colors.RED_400)
            ]),
            ft.Divider(),
            ft.Row([
                ft.Text("Topics", size=20, weight=ft.FontWeight.W_500),
                ft.Container(expand=True),
                ft.ElevatedButton("Add Topic", icon=ft.Icons.ADD_CIRCLE_OUTLINE, on_click=self.add_topic_dialog, visible=self.selected_syllabus_id is not None)
            ]),
            ft.Text("Click a topic to view or upload lesson content.", italic=True),
            self.topics_list
        ]
        if not self.syllabuses:
            self.topics_list.controls = [ft.Text("No syllabuses found. Create one or import to start.", italic=True)]
        elif self.selected_syllabus_id:
            self.refresh_topics()

    def add_syllabus_dialog(self, e):
        name_inp = ft.TextField(label="Syllabus Name")
        def confirm_add(ev):
            if not name_inp.value: return
            conn = sqlite3.connect("lex_database.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO syllabuses (teacher_id, name) VALUES (?, ?)", (self.teacher_id, name_inp.value))
            conn.commit()
            conn.close()
            self.load_syllabuses()
            self.build_ui()
            dialog.open = False
            self.main_page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Create New Syllabus"),
            content=name_inp,
            actions=[ft.ElevatedButton("Create", on_click=confirm_add)]
        )
        self.main_page.dialog = dialog
        dialog.open = True
        self.main_page.update()

    def delete_syllabus(self, e):
        if not self.selected_syllabus_id: return
        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM syllabuses WHERE id = ?", (self.selected_syllabus_id,))
        cursor.execute("DELETE FROM topics WHERE syllabus_id = ?", (self.selected_syllabus_id,))
        conn.commit()
        conn.close()
        self.selected_syllabus_id = None
        self.load_syllabuses()
        self.build_ui()
        self.main_page.update()

    def rename_syllabus_dialog(self, e):
        if not self.selected_syllabus_id: return
        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM syllabuses WHERE id = ?", (self.selected_syllabus_id,))
        current_name = cursor.fetchone()[0]
        conn.close()

        name_inp = ft.TextField(label="Syllabus Name", value=current_name)
        def confirm_rename(ev):
            if not name_inp.value: return
            conn = sqlite3.connect("lex_database.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE syllabuses SET name = ? WHERE id = ?", (name_inp.value, self.selected_syllabus_id))
            conn.commit()
            conn.close()
            self.load_syllabuses()
            self.build_ui()
            dialog.open = False
            self.main_page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Rename Syllabus"),
            content=name_inp,
            actions=[ft.ElevatedButton("Save", on_click=confirm_rename)]
        )
        self.main_page.dialog = dialog
        dialog.open = True
        self.main_page.update()

    def add_topic_dialog(self, e):
        id_inp = ft.TextField(label="Topic No (e.g. 1.1)")
        name_inp = ft.TextField(label="Topic Name")
        def confirm_add(ev):
            if not id_inp.value or not name_inp.value: return
            conn = sqlite3.connect("lex_database.db")
            cursor = conn.cursor()
            # Calculate next order index
            cursor.execute("SELECT MAX(order_index) FROM topics WHERE syllabus_id = ?", (self.selected_syllabus_id,))
            max_idx = cursor.fetchone()[0]
            next_idx = (max_idx + 1) if max_idx is not None else 0
            
            cursor.execute("INSERT INTO topics (syllabus_id, topic_id_string, name, order_index) VALUES (?, ?, ?, ?)",
                           (self.selected_syllabus_id, id_inp.value, name_inp.value, next_idx))
            conn.commit()
            conn.close()
            self.refresh_topics()
            dialog.open = False
            self.main_page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Add Topic"),
            content=ft.Column([id_inp, name_inp], tight=True),
            actions=[ft.ElevatedButton("Add", on_click=confirm_add)]
        )
        self.main_page.dialog = dialog
        dialog.open = True
        self.main_page.update()

    def edit_topic_dialog(self, topic):
        id_inp = ft.TextField(label="Topic No", value=topic[1])
        name_inp = ft.TextField(label="Topic Name", value=topic[2])
        def confirm_edit(ev):
            if not id_inp.value or not name_inp.value: return
            conn = sqlite3.connect("lex_database.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE topics SET topic_id_string = ?, name = ? WHERE id = ?",
                           (id_inp.value, name_inp.value, topic[0]))
            conn.commit()
            conn.close()
            self.refresh_topics()
            dialog.open = False
            self.main_page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Edit Topic"),
            content=ft.Column([id_inp, name_inp], tight=True),
            actions=[ft.ElevatedButton("Save", on_click=confirm_edit)]
        )
        self.main_page.dialog = dialog
        dialog.open = True
        self.main_page.update()

    def delete_topic(self, topic_id):
        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM topics WHERE id = ?", (topic_id,))
        cursor.execute("DELETE FROM text_blocks WHERE topic_id = ?", (topic_id,))
        conn.commit()
        conn.close()
        self.refresh_topics()
        self.main_page.update()

    def pick_file(self, e):
        def on_file_result(e):
            if e.files:
                file_path = e.files[0].path
                if file_path.endswith('.docx'):
                    data = parse_docx_table(file_path)
                elif file_path.endswith('.xlsx'):
                    data = parse_xlsx_table(file_path)
                else:
                    return
                
                # Simple dialog for name
                name_inp = ft.TextField(label="Syllabus Name")
                def confirm_import(ev):
                    import_syllabus(self.teacher_id, name_inp.value, data)
                    self.load_syllabuses()
                    try:
                        self.update()
                    except Exception:
                        pass
                    import_dialog.open = False
                    self.main_page.update()

                import_dialog = ft.AlertDialog(
                    title=ft.Text("Import Syllabus"),
                    content=name_inp,
                    actions=[ft.ElevatedButton("Import", on_click=confirm_import)]
                )
                self.main_page.dialog = import_dialog
                import_dialog.open = True
                self.main_page.update()

        picker = ft.FilePicker(on_result=on_file_result)
        self.main_page.overlay.append(picker)
        self.main_page.update()
        picker.pick_files(allowed_extensions=['docx', 'xlsx'])

    def show_lesson_content(self, topic_id):
        from ui.lesson_content_view import LessonContentView
        # Replace the current content with LessonContentView
        # This is a bit tricky since we are in a sub-component. 
        # In a real app we'd use routing. For now, let's just swap controls in the parent.
        self.controls = [LessonContentView(self.main_page, self.teacher_id, topic_id, on_back=self.back_to_syllabus)]
        try:
            self.update()
        except Exception:
            pass

    def back_to_syllabus(self, e):
        self.build_ui()
        try:
            self.update()
        except Exception:
            pass
