import flet as ft

class LanguageManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_lang = self.page.client_storage.get("language") or "en"
        
        self.translations = {
            "en": {
                "app_title": "EduCanvas Desktop",
                "nav_diary": "Diary",
                "nav_lesson_lab": "Lesson Lab",
                "nav_whiteboard": "Whiteboard",
                "nav_exams": "Exams",
                "nav_settings": "Settings",
                "welcome_message": "Welcome to EduCanvas! Select an option from the sidebar.",
                "settings_title": "Settings",
                "select_language": "Select Language",
                "save_settings": "Save Settings",
                "settings_saved": "Settings saved successfully!",
                "coming_soon": "Coming Soon",
                "diary_master_title": "Master Diary Entry",
                "diary_topic": "Topic / Lesson Title",
                "diary_content": "Content / Activities",
                "diary_date": "Date",
                "diary_cohorts": "Select Cohorts",
                "diary_save": "Save Entry",
                "diary_export": "Export to PDF",
                "diary_saved_msg": "Diary entry saved for selected cohorts!",
                "diary_no_cohort_msg": "Please select at least one cohort."
            },
            "sq": {
                "app_title": "EduCanvas Desktop",
                "nav_diary": "Ditari",
                "nav_lesson_lab": "Laboratori i Mësimit",
                "nav_whiteboard": "Tabela e Bardhë",
                "nav_exams": "Provimet",
                "nav_settings": "Cilësimet",
                "welcome_message": "Mirësevini në EduCanvas! Zgjidhni një opsion nga shiriti anësor.",
                "settings_title": "Cilësimet",
                "select_language": "Zgjidhni Gjuhën",
                "save_settings": "Ruaj Cilësimet",
                "settings_saved": "Cilësimet u ruajtën me sukses!",
                "coming_soon": "Së Shpejti",
                "diary_master_title": "Hyrja në Ditarin Kryesor",
                "diary_topic": "Tema / Titulli i Mësimit",
                "diary_content": "Përmbajtja / Aktivitetet",
                "diary_date": "Data",
                "diary_cohorts": "Zgjidhni Klasat",
                "diary_save": "Ruaj Hyrjen",
                "diary_export": "Eksporto në PDF",
                "diary_saved_msg": "Hyrja në ditar u ruajt për klasat e zgjedhura!",
                "diary_no_cohort_msg": "Ju lutemi zgjidhni të paktën një klasë."
            }
        }

    def get_string(self, key):
        return self.translations.get(self.current_lang, self.translations["en"]).get(key, key)

    def set_language(self, lang_code):
        if lang_code in self.translations:
            self.current_lang = lang_code
            self.page.client_storage.set("language", lang_code)
            return True
        return False
