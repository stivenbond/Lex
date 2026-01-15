# PROJECT BRIEF

## Teacher Lesson Diary & Lesson Structuring System

---

## 1. Purpose & Core Problem

Teachers are required to fill out **lesson diary entries after every lecture**, following a **predefined format**.
However:

* Each teacher may have **their own diary format**
* Some diary fields are **stable across academic years** (as long as syllabus doesn’t change)
* Some diary fields are **lesson-specific**
* Teachers teach the **same lesson to multiple cohorts** at different times
* Repeating full diary entries for each cohort is inefficient and error-prone

This system must:

* **Normalize lesson diaries**
* **Avoid redundant data entry**
* **Track cohort-specific teaching progress**
* **Support structured lesson content storage**
* **Support professional exports (PDF, Word, Image)**

---

## 2. High-Level Conceptual Model (Mental Model for Agents)

Think in terms of **four orthogonal domains**:

```
Teacher
 ├── Diary Templates (field definitions)
 ├── Syllabus (topics + metadata)
 ├── Lessons (content blocks)
 └── Diary Entries (execution records)

Lesson ≠ Diary Entry
Diary Entry ≠ Cohort
```

**Key principle:**

> A *lesson* is an abstract teaching unit.
> A *diary entry* is a record of teaching that lesson **at a specific time**, possibly reused across cohorts.

---

## 3. Core Entities & Responsibilities

### 3.1 Teacher

* Owns:

  * Diary field definitions
  * Lessons
  * Syllabus imports
* Isolation:

  * No data is shared between teachers

---

### 3.2 Syllabus

**Purpose:** Defines the teaching structure and sequencing.

**Source formats:**

* Word (.docx)
* Excel (.xlsx)

**Representation:**

* Table-based
* Contains:

  * Topic ID / Topic Name
  * Optional metadata (hours, objectives, etc.)

**System responsibility:**

* Parse syllabus table
* Convert each row into a **Topic entity**
* Preserve ordering

---

### 3.3 Topic

A **teachable unit**, reused across cohorts.

Attributes:

* Topic ID
* Topic Name
* Linked Lesson Content
* Linked Diary Entries (via references)

---

## 4. Diary System (Critical Section)

### 4.1 Diary Field Definitions (Template System)

Each teacher defines **their own diary schema**.

Properties:

* All fields are **text fields**
* Fields have:

  * Field ID
  * Label
  * Description (optional)
  * Stability flag:

    * `STATIC` → same across years
    * `DYNAMIC` → lesson-specific

Templates are:

* Versioned implicitly by syllabus year
* Reusable as long as syllabus doesn’t change

---

### 4.2 Diary Entry (Primary Record)

A diary entry represents:

> “This topic was taught on this date, following this structure.”

Attributes:

* Teacher
* Topic
* Teaching Date
* Diary Template Version
* Field Values (key → text)
* **Primary Cohort** (see below)

---

### 4.3 Cohort Handling (Anti-Redundancy Rule)

A teacher may teach the **same topic** to multiple cohorts at different times.

**Rule:**

* The **first cohort taught** creates a **FULL diary entry**
* All subsequent cohorts:

  * DO NOT duplicate diary content
  * Instead create a **Reference Entry**

#### Reference Entry contains:

* Cohort Name
* Reference:

  * Original Diary Entry Date
  * Original Cohort Name

This guarantees:

* Zero content duplication
* Traceability
* Auditability

---

### 4.4 Cohort

Attributes:

* Cohort Name (e.g., “10A”, “CS-2025”)
* Teaching Progress:

  * Last taught topic
  * Dates per topic (direct or referenced)

---

## 5. Export System

### 5.1 Export Targets

Each diary entry (full or reference) must be exportable as:

* PDF
* Word (.docx)

---

### 5.2 Formatting Modes

Teacher-defined preference:

* **Table layout**
* **Plain text layout**

Formatting must:

* Respect field order
* Include:

  * Topic
  * Date
  * Cohort
  * Reference info (if applicable)

---

## 6. Lesson Content System (Separate but Linked)

### 6.1 Lesson Content Storage

Each Topic may have **Lesson Content**, independent of diary entries.

Lesson content is composed of **Text Blocks**.

Sources:

* Word documents
* PowerPoint slides

Parsing rule:

* Each paragraph → one Text Block
* Order preserved

---

### 6.2 Text Block Entity

Attributes:

* Block ID
* Text Content
* Optional metadata (position, tags)

---

## 7. Lesson Visualization Modes

### 7.1 Document Mode

* Linear reading
* Blocks shown sequentially
* Equivalent to a document

---

### 7.2 Whiteboard Mode (Conceptual Mapping)

Whiteboard characteristics:

* Canvas-based
* Each Text Block becomes a draggable node
* Teacher can:

  * Reposition blocks
  * Cluster ideas
  * Create implicit diagrams / mind maps

This is **layout-only**:

* Does NOT modify text content
* Stores positions and relationships

---

### 7.3 Whiteboard Export

Export formats:

* PDF
* PNG / Image

Export includes:

* Block text
* Spatial layout
* Visual grouping

---

## 8. Import Capabilities (Mandatory)

### 8.1 Supported Imports

* Syllabus:

  * Word table
  * Excel table
* Lessons:

  * Word (.docx)
  * PowerPoint (.pptx)

### 8.2 Parsing Rules

* No AI inference
* Deterministic parsing only
* Preserve original text exactly

---

## 9. Non-Functional Requirements (For Agents)

### Determinism

* No guessing
* No inferred fields
* No auto-generated content unless explicitly asked

### Data Integrity

* Reference entries must never duplicate content
* Deleting a primary diary entry must invalidate references

### Extensibility

* Diary fields must be schema-driven
* No hardcoded field names

---

## 10. Explicit Non-Goals (To Prevent Scope Creep)

* No grading
* No student data
* No LMS integration
* No AI content generation
* No real-time collaboration

---

## 11. Recommended Implementation Strategy (Agent Guidance)

**Architecture pattern:**

* Strong domain separation
* Schema-driven forms
* Export layer isolated from data layer

**Critical pitfalls to avoid:**

* Treating cohorts as copies instead of references
* Mixing lesson content with diary entries
* Hardcoding diary formats

---

## 12. Validation Checklist (Agent Self-Test)

Before declaring completion, the system must support:

* [ ] Custom diary fields per teacher
* [ ] Syllabus import from Word/Excel
* [ ] Full diary entry for first cohort
* [ ] Reference diary entries for later cohorts
* [ ] PDF + Word export with formatting choice
* [ ] Lesson import from Word/PowerPoint
* [ ] Document mode view
* [ ] Whiteboard mode with export
