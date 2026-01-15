from database.db_manager import DBManager
import flet as ft
import json
from ui.language_manager import LanguageManager

class DiaryView(ft.Column):
    def __init__(self, page: ft.Page, lang_manager: LanguageManager):
        super().__init__()
        self.page = page
        self.lang_manager = lang_manager
        self.db = DBManager() # Initialize DB Manager
        self.expand = True
        self.scroll = ft.ScrollMode.AUTO
        
        self.init_ui()

# ... (init_ui remains same) ...

    def save_entry(self, e):
        title = self.topic_field.value
        content = self.content_field.value

        if not title or not content:
             self.page.snack_bar = ft.SnackBar(ft.Text("Please fill in Topic and Content."))
             self.page.snack_bar.open = True
             self.page.update()
             return

        # Validate selection
        selected_cohorts = [c.label for c in self.cohort_checks if c.value]
        if not selected_cohorts:
            self.page.snack_bar = ft.SnackBar(ft.Text(self.lang_manager.get_string("diary_no_cohort_msg")))
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Save to database
        try:
            # 1. Create Lesson (Source of Truth)
            # In a real app we might check if lesson exists, but for now we create new
            lesson_id = self.db.create_lesson(title, {"text": content})
            
            # 2. Create Diary Entries for each cohort
            for cohort in selected_cohorts:
                self.db.create_diary_entry(
                    lesson_id=lesson_id, 
                    cohort_name=cohort, 
                    data_json={"notes": "Auto-generated from Master Diary"}
                )
            
            self.page.snack_bar = ft.SnackBar(ft.Text(self.lang_manager.get_string("diary_saved_msg")))
            self.topic_field.value = ""
            self.content_field.value = ""
            # Reset checkboxes
            for c in self.cohort_checks:
                c.value = False
            self.update() # Update the view to clear fields

        except Exception as ex:
             print(f"Error saving: {ex}")
             self.page.snack_bar = ft.SnackBar(ft.Text(f"Error saving entry: {str(ex)}"))
        
        self.page.snack_bar.open = True
        self.page.update()

    def export_entry(self, e):
        title = self.topic_field.value
        content = self.content_field.value
        selected_cohorts = [c.label for c in self.cohort_checks if c.value]

        if not title or not content:
            self.page.snack_bar = ft.SnackBar(ft.Text("Nothing to export. Fill in details first."))
            self.page.snack_bar.open = True
            self.page.update()
            return

        from logic.exporter import DiaryExporter
        import os
        
        # Save to Downloads or similar (for now just project root/exports)
        export_dir = "exports"
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
            
        filename = os.path.join(export_dir, f"diary_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        
        try:
            DiaryExporter.export_to_pdf(filename, title, content, selected_cohorts)
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Exported to {filename}"))
        except Exception as ex:
             self.page.snack_bar = ft.SnackBar(ft.Text(f"Export failed: {ex}"))
             
        self.page.snack_bar.open = True
        self.page.update()
