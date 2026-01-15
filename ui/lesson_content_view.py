import flet as ft
import sqlite3
from services.lesson_service import parse_docx_lessons, parse_pptx_lessons, save_lesson_content

class LessonContentView(ft.Column):
    def __init__(self, page: ft.Page, teacher_id: int, topic_id: int, on_back):
        super().__init__(expand=True)
        self.main_page = page
        self.teacher_id = teacher_id
        self.topic_id = topic_id
        self.on_back = on_back
        
        self.view_mode = "DOCUMENT" # DOCUMENT or WHITEBOARD
        self.blocks = []
        
        self.load_blocks()
        self.build_ui()

    def load_blocks(self):
        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, content, order_index, x, y FROM text_blocks WHERE topic_id = ? ORDER BY order_index", (self.topic_id,))
        self.blocks = cursor.fetchall()
        
        cursor.execute("SELECT name FROM topics WHERE id = ?", (self.topic_id,))
        self.topic_name = cursor.fetchone()[0]
        conn.close()

    def build_ui(self):
        mode_toggle = ft.SegmentedButton(
            selected={"DOCUMENT" if self.view_mode == "DOCUMENT" else "WHITEBOARD"},
            on_change=self.handle_mode_change,
            segments=[
                ft.Segment("DOCUMENT", label=ft.Text("Document Mode"), icon=ft.Icon(ft.Icons.DESCRIPTION)),
                ft.Segment("WHITEBOARD", label=ft.Text("Whiteboard Mode"), icon=ft.Icon(ft.Icons.BRUSH)),
            ],
        )

        header = ft.Row([
            ft.IconButton(ft.Icons.ARROW_BACK, on_click=self.on_back),
            ft.Text(f"Lesson: {self.topic_name}", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(expand=True),
            mode_toggle,
            ft.ElevatedButton("Export WB", icon=ft.Icons.PICTURE_AS_PDF, on_click=self.export_whiteboard, visible=self.view_mode=="WHITEBOARD"),
            ft.ElevatedButton("Add Text", icon=ft.Icons.ADD, on_click=self.add_block_dialog),
            ft.ElevatedButton("Import", icon=ft.Icons.UPLOAD, on_click=self.pick_lesson_file)
        ])

        if self.view_mode == "DOCUMENT":
            content = self.build_document_view()
        else:
            content = self.build_whiteboard_view()

        self.controls = [header, ft.Divider(), content]
        try:
            self.update()
        except Exception:
            pass

    def handle_mode_change(self, e):
        self.view_mode = list(e.selection)[0] if e.selection else "DOCUMENT"
        self.build_ui()

    def build_document_view(self):
        return ft.ListView(
            expand=True,
            spacing=10,
            controls=[
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(b[1], size=16),
                            ft.Row([
                                ft.TextButton("Edit", icon=ft.Icons.EDIT, on_click=lambda e, block=b: self.edit_block_dialog(block)),
                                ft.TextButton("Delete", icon=ft.Icons.DELETE, icon_color=ft.Colors.RED_400, on_click=lambda e, bid=b[0]: self.delete_block(bid)),
                            ], alignment=ft.MainAxisAlignment.END)
                        ]),
                        padding=15
                    )
                ) for b in self.blocks
            ]
        )

    def build_whiteboard_view(self):
        stack_controls = []
        for i, b in enumerate(self.blocks):
            def on_pan_update(e: ft.DragUpdateEvent, block_index=i):
                block = self.blocks[block_index]
                # Update local state
                new_list = list(self.blocks)
                item = list(new_list[block_index])
                item[3] = (item[3] if item[3] else 20) + e.delta_x
                item[4] = (item[4] if item[4] else 50 + (block_index * 100)) + e.delta_y
                new_list[block_index] = tuple(item)
                self.blocks = new_list
                
                # Update DB (could be debounced in a real app)
                conn = sqlite3.connect("lex_database.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE text_blocks SET x = ?, y = ? WHERE id = ?", (item[3], item[4], item[0]))
                conn.commit()
                conn.close()
                self.build_ui()

            stack_controls.append(
                ft.GestureDetector(
                    mouse_cursor=ft.MouseCursor.MOVE,
                    on_pan_update=on_pan_update,
                    content=ft.Container(
                        content=ft.Text(b[1], size=14),
                        bgcolor=ft.Colors.BLUE_GREY_900,
                        padding=15,
                        border_radius=10,
                        width=250,
                        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK),
                    ),
                    left=b[3] if b[3] else 20,
                    top=b[4] if b[4] else 50 + (i * 100),
                )
            )

        if not stack_controls:
            return ft.Container(content=ft.Text("No content blocks. Add some or import to see them on the whiteboard.", italic=True), padding=20)
            
        return ft.Stack(
            controls=stack_controls,
            expand=True,
        )

    def edit_block_dialog(self, block):
        content_inp = ft.TextField(label="Content", multiline=True, min_lines=3, value=block[1])
        def confirm_edit(ev):
            if not content_inp.value: return
            conn = sqlite3.connect("lex_database.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE text_blocks SET content = ? WHERE id = ?", (content_inp.value, block[0]))
            conn.commit()
            conn.close()
            self.load_blocks()
            self.build_ui()
            dialog.open = False
            self.main_page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Edit Text Block"),
            content=content_inp,
            actions=[ft.ElevatedButton("Save", on_click=confirm_edit)]
        )
        self.main_page.dialog = dialog
        dialog.open = True
        self.main_page.update()

    def delete_block(self, block_id):
        conn = sqlite3.connect("lex_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM text_blocks WHERE id = ?", (block_id,))
        conn.commit()
        conn.close()
        self.load_blocks()
        self.build_ui()
        self.main_page.update()

    def add_block_dialog(self, e):
        content_inp = ft.TextField(label="Content", multiline=True, min_lines=3)
        def confirm_add(ev):
            if not content_inp.value: return
            conn = sqlite3.connect("lex_database.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO text_blocks (topic_id, content, order_index, x, y) VALUES (?, ?, 0, 50, 50)",
                           (self.topic_id, content_inp.value))
            conn.commit()
            conn.close()
            self.load_blocks()
            self.build_ui()
            dialog.open = False
            self.main_page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Add Text Block"),
            content=content_inp,
            actions=[ft.ElevatedButton("Add", on_click=confirm_add)]
        )
        self.main_page.dialog = dialog
        dialog.open = True
        self.main_page.update()

    def pick_lesson_file(self, e):
        def on_file_result(e):
            if e.files:
                file_path = e.files[0].path
                if file_path.endswith('.docx'):
                    blocks = parse_docx_lessons(file_path)
                elif file_path.endswith('.pptx'):
                    blocks = parse_pptx_lessons(file_path)
                else:
                    return
                
                save_lesson_content(self.topic_id, blocks)
                self.load_blocks()
                self.build_ui()

        picker = ft.FilePicker(on_result=on_file_result)
        self.main_page.overlay.append(picker)
        self.main_page.update()
        picker.pick_files(allowed_extensions=['docx', 'pptx'])

    def export_whiteboard(self, e):
        from services.export_service import ExportService
        filename = f"whiteboard_{self.topic_id}.pdf"
        ExportService.export_whiteboard_to_pdf(self.topic_id, filename)
        self.main_page.snack_bar = ft.SnackBar(ft.Text(f"Whiteboard exported to {filename}"))
        self.main_page.snack_bar.open = True
        self.main_page.update()
