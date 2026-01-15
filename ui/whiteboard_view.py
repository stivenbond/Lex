import flet as ft
import flet.canvas as cv
from logic.document_parser import DocumentParser
import os

class DraggableBlock(ft.GestureDetector):
    def __init__(self, content_text, x, y, on_pan_update, on_select, block_id):
        super().__init__()
        self.x = x
        self.y = y
        self.block_id = block_id
        self.on_pan_update = on_pan_update
        self.on_select = on_select
        self.content_text = content_text
        
        self.container = ft.Container(
            content=ft.Text(content_text, size=12),
            padding=10,
            bgcolor=ft.colors.BLUE_50,
            border=ft.border.all(1, ft.colors.BLUE_200),
            border_radius=5,
            width=200,
            on_click=lambda e: self.on_select(self.block_id)
        )
        self.content = self.container
        self.left = x
        self.top = y
        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.left = self.x
        self.top = self.y

class WhiteboardView(ft.Row):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.blocks = [] # List of DraggableBlock controls
        self.connections = [] # List of (id1, id2) tuples
        self.selected_block_id = None
        
        self.init_ui()

    def init_ui(self):
        # Sidebar for file uploading and unplaced items
        self.sidebar_content = ft.Column(scroll=ft.ScrollMode.AUTO)
        self.sidebar = ft.Container(
            width=250,
            padding=10,
            bgcolor=ft.colors.GREY_100,
            content=ft.Column([
                ft.Text("Lesson Content", weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Import .docx/pptx", on_click=self.pick_file),
                ft.Divider(),
                self.sidebar_content
            ])
        )

        # Canvas Area
        self.canvas_layer = cv.Canvas(
            expand=True,
            shapes=[]
        )
        
        # Stack for draggable items (overlaying the canvas)
        self.stack = ft.Stack(
            expand=True,
            controls=[
                # Canvas layer at the bottom for lines
                ft.Container(content=self.canvas_layer, expand=True),
            ]
        )

        self.file_picker = ft.FilePicker(on_result=self.on_file_picked)
        self.page.overlay.append(self.file_picker)

        self.controls = [
            self.sidebar,
            ft.VerticalDivider(width=1),
            ft.Container(content=self.stack, expand=True, bgcolor=ft.colors.WHITE)
        ]

    def pick_file(self, e):
        self.file_picker.pick_files(allow_multiple=False, allowed_extensions=["docx", "pptx"])

    def on_file_picked(self, e: ft.FilePickerResultEvent):
        if not e.files:
            return
            
        file_path = e.files[0].path
        try:
            parsed_data = DocumentParser.parse_file(file_path)
            self.populate_sidebar(parsed_data)
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error parsing file: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def populate_sidebar(self, data):
        self.sidebar_content.controls.clear()
        for i, item in enumerate(data):
            # Create a clickable item in sidebar to add to canvas
            self.sidebar_content.controls.append(
                ft.Container(
                    content=ft.Text(item["content"][:50] + "...", size=12),
                    padding=5,
                    bgcolor=ft.colors.WHITE,
                    border=ft.border.all(1, ft.colors.GREY_300),
                    on_click=lambda e, txt=item["content"]: self.add_block_to_canvas(txt)
                )
            )
        self.sidebar.update()

    def add_block_to_canvas(self, text):
        block_id = len(self.blocks)
        # Position slightly offset
        x, y = 100 + (block_id * 20), 100 + (block_id * 20)
        
        block = DraggableBlock(
            text, x, y, 
            on_pan_update=self.on_block_drag, 
            on_select=self.on_block_click,
            block_id=block_id
        )
        
        self.blocks.append(block)
        self.stack.controls.append(block)
        self.stack.update()

    def on_block_drag(self, e: ft.DragUpdateEvent):
        block = e.control
        block.move(e.delta_x, e.delta_y)
        block.update()
        self.redraw_lines()

    def on_block_click(self, block_id):
        if self.selected_block_id is None:
            self.selected_block_id = block_id
            # Highlight block
            self.blocks[block_id].container.border = ft.border.all(2, ft.colors.BLUE_700)
            self.blocks[block_id].update()
            
            self.page.snack_bar = ft.SnackBar(ft.Text("Block selected. Click another to connect."))
            self.page.snack_bar.open = True
            self.page.update()
        else:
            if self.selected_block_id != block_id:
                # Create connection
                self.connections.append((self.selected_block_id, block_id))
                self.redraw_lines()
                self.page.snack_bar = ft.SnackBar(ft.Text("Blocks connected!"))
                self.page.snack_bar.open = True
                self.page.update()
            
            # Deselect
            prev_block = self.blocks[self.selected_block_id]
            prev_block.container.border = ft.border.all(1, ft.colors.BLUE_200)
            prev_block.update()
            self.selected_block_id = None

    def redraw_lines(self):
        self.canvas_layer.shapes.clear()
        
        for id1, id2 in self.connections:
            b1 = self.blocks[id1]
            b2 = self.blocks[id2]
            
            # Center points
            x1 = b1.x + 100 # Half width
            y1 = b1.y + 20  # Approx half height
            x2 = b2.x + 100
            y2 = b2.y + 20
            
            self.canvas_layer.shapes.append(
                cv.Line(x1, y1, x2, y2, paint=ft.Paint(stroke_width=2, color=ft.colors.GREY_500))
            )
            
        self.canvas_layer.update()
