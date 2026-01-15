from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime

class DiaryExporter:
    @staticmethod
    def export_to_pdf(filename, title, content, cohorts):
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        
        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(72, height - 72, f"Diary Entry: {title}")
        
        # Meta info
        c.setFont("Helvetica", 10)
        c.drawString(72, height - 90, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        c.drawString(72, height - 105, f"Cohorts: {', '.join(cohorts)}")
        
        # Content
        c.setFont("Helvetica", 12)
        text_object = c.beginText(72, height - 140)
        
        # Simple text wrapping (this is very basic)
        max_width = 80
        words = content.split()
        current_line = []
        
        for word in words:
            if len(" ".join(current_line + [word])) < max_width:
                current_line.append(word)
            else:
                text_object.textLine(" ".join(current_line))
                current_line = [word]
        if current_line:
            text_object.textLine(" ".join(current_line))
            
        c.drawText(text_object)
        c.save()
        return filename
