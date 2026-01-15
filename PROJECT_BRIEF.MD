Project Specification: EduCanvas Desktop
1. Project Vision
A cross-platform desktop application for educators that automates administrative "diary" logging and transforms static lesson content into interactive, node-based mind maps.

2. Technical Stack
Framework: Python 3.10+ with Flet (Desktop Target).
AI Engine: Ollama (Local Inference) or llama-cpp-python.
Database: SQLite with JSON1 extension for dynamic diary schemas.
Document Processing: python-docx, python-pptx, pandas.

3. System Architecture
A. UI Layer (Flet)
Reactive State: Use Flet’s page.session and page.client_storage to manage user preferences and multi-language keys.
Navigation: A sidebar-based navigation (Diary, Lesson Lab, Whiteboard, Exams, Settings).
B. Logic Layer
The Parser: A module to break down .docx or .pptx into a list of "Content Blocks" (Paragraphs, Tables, Images).
The Generator: A prompt-engineering module that talks to the local LLM to generate 30 distinct versions of a test from the parsed blocks.

4. Feature Specifications
F1: Multilingual UI Manager
Requirement: Support switching between English, Spanish, etc., without restarting.
F2: Smart Diary Management
Requirement: Dynamic templates that support table formats.
Functionality: Teachers fill a "Master Diary." The system allows them to select multiple cohorts (e.g., "Class 10A", "Class 10B") to auto-populate separate logs.
Export: Use reportlab (PDF) and python-docx to generate files based on the diary entries.
F3: Whiteboard Mode (Logic Mapping)
Requirement: Not a free-draw canvas, but a Node-Link Diagram.
Workflow:
Teacher opens a Lesson Document.
The Sidebar lists all paragraphs as draggable "Text Blocks."
Teacher drags a block onto the Flet Stack container.
The block becomes a Container with a GestureDetector for moving.
Tangible Interface: Ability to click two blocks to create a connecting line (using Flet's cv.Canvas).

5. Data Schema (SQLite)
Table	Key Fields
Lessons	id, title, raw_content (JSON blocks), metadata
Diaries	id, lesson_id, cohort_name, schema_id, data (JSON)
Templates	id, name, structure_definition (JSON)
Assessments	id, lesson_id, variants (JSON list), active_status