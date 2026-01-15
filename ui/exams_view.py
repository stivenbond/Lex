import flet as ft
from logic.test_generator import TestGenerator

class ExamsView(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.generator = TestGenerator()
        self.expand = True
        self.scroll = ft.ScrollMode.AUTO
        
        self.init_ui()

    def init_ui(self):
        self.source_text = ft.TextField(
            label="Paste Lesson Content or Summary",
            multiline=True,
            min_lines=5,
            max_lines=10
        )
        
        self.results_area = ft.Column()
        
        self.controls = [
            ft.Text("Exam Generator", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Generate multiple variations of tests from your content."),
            ft.Divider(),
            
            self.source_text,
            
            ft.Row([
                ft.Dropdown(
                    label="Difficulty",
                    options=[
                        ft.dropdown.Option("Easy"),
                        ft.dropdown.Option("Medium"),
                        ft.dropdown.Option("Hard"),
                    ],
                    value="Medium"
                ),
                ft.Dropdown(
                    label="Questions",
                    options=[
                        ft.dropdown.Option("3"),
                        ft.dropdown.Option("5"),
                        ft.dropdown.Option("10"),
                    ],
                    value="5"
                ),
                ft.ElevatedButton(
                    "Generate Test", 
                    icon=ft.icons.AUTO_AWESOME,
                    on_click=self.run_generation
                )
            ]),
            
            ft.Divider(),
            ft.Text("Generated Assessment:", size=16, weight=ft.FontWeight.BOLD),
            self.results_area
        ]

    def run_generation(self, e):
        content = self.source_text.value
        if not content:
            self.page.snack_bar = ft.SnackBar(ft.Text("Please enter some content first."))
            self.page.snack_bar.open = True
            self.page.update()
            return
            
        self.results_area.controls = [ft.ProgressBar()]
        self.results_area.update()
        
        # In a real app, run this in a thread to avoid blocking UI
        # For this prototype, we'll run synchronously or use Flet's async support if configured
        
        # Get settings
        difficulty = self.controls[4].controls[0].value
        num_q = int(self.controls[4].controls[1].value)
        
        result = self.generator.generate_assessment(content, num_q, difficulty)
        
        self.render_results(result)

    def render_results(self, result):
        self.results_area.controls.clear()
        
        if "error" in result:
             self.results_area.controls.append(ft.Text(f"Error: {result['error']}", color="red"))
             self.results_area.update()
             return

        questions = result.get("questions", [])
        
        for i, q in enumerate(questions):
            q_card = ft.Card(
                content=ft.Container(
                    padding=10,
                    content=ft.Column([
                        ft.Text(f"Q{i+1}: {q.get('question', 'Unknown Question')}", weight=ft.FontWeight.BOLD),
                        ft.Column([
                            ft.RadioGroup(
                                content=ft.Column([
                                    ft.Radio(value=opt, label=opt) for opt in q.get('options', [])
                                ])
                            )
                        ])
                    ])
                )
            )
            self.results_area.controls.append(q_card)
        
        if not questions:
            self.results_area.controls.append(ft.Text("No questions generated. Check AI response."))

        self.results_area.update()
