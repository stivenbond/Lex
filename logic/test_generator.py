from logic.ai_engine import AIEngine
import re

class TestGenerator:
    def __init__(self):
        self.ai = AIEngine()

    def generate_assessment(self, content_text, num_questions=5, difficulty="Medium"):
        prompt = f"""
        Generate a {num_questions}-question multiple choice test based on the following text.
        Difficulty: {difficulty}.
        
        Text:
        {content_text}
        
        Format your response purely as a JSON object with this structure:
        {{
            "questions": [
                {{
                    "question": "Question text here",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "A"
                }}
            ]
        }}
        Do NOT include any markdown formatting or extra text.
        """
        
        response = self.ai.generate(prompt)
        return self._parse_json_response(response)

    def _parse_json_response(self, response_text):
        # Attempt to clean and parse JSON
        try:
            # Simple regex to find the first { and last }
            import json
            match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if match:
                json_str = match.group(0)
                return json.loads(json_str)
            else:
                # Fallback mock if parsing fails or AI returns garbage in dev mode
                return {
                    "questions": [
                        {
                            "question": "Could not parse AI response. See raw output.",
                            "options": ["Raw Output"],
                            "correct_answer": response_text
                        }
                    ]
                }
        except Exception as e:
            return {"error": str(e), "raw_response": response_text}
