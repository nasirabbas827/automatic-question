# automatic_question_final  

**Automated Question Paper Generator** – a Django‑based web application that lets educators create, store, and distribute exam papers. The project also demonstrates a simple blockchain‑style audit trail for vote‑based paper approval.

---

## Overview  

`automatic_question_final` is a **Python/Django** project that:

* Generates question papers from a predefined question bank.  
* Stores papers, candidates, and election data in a relational database.  
* Provides an admin interface for managing users, courses, and submissions.  
* Records paper‑submission events on a lightweight blockchain model to ensure tamper‑evidence.  

The core documentation lives in `Automated Question Paper Generator.docx`.  

---

## Features  

| ✅ | Feature |
|---|---------|
| **Paper Generation** | Create custom question papers based on selected courses, degree programs, and difficulty levels. |
| **User & Profile Management** | Register voters, candidates, and administrators with profile fields (photo, address, DOB, etc.). |
| **Election Workflow** | Conduct paper‑approval elections; votes are stored in `myapp/models.py` and reflected in the blockchain. |
| **Blockchain Audit Trail** | Each vote generates a hash‑linked block (`blockchain.py`) guaranteeing integrity. |
| **Admin Dashboard** | Full CRUD via Django admin (`myapp/admin.py`). |
| **REST‑Ready Structure** | Clean separation of models, forms, views, and URLs for future API extensions. |
| **Migrations** | 16 migration files covering schema evolution from the initial model to the latest `papersubmission` table. |

---

## Tech Stack  

| Layer | Technology |
|-------|------------|
| **Language** | Python 3.9+ |
| **Web Framework** | Django 4.x |
| **Database** | SQLite (default) – can be swapped for PostgreSQL/MySQL |
| **Front‑end** | Django templates (Bootstrap optional) |
| **Blockchain** | Custom Python implementation (`myapp/blockchain.py`) |
| **Version Control** | Git (GitHub) |
| **Documentation** | Microsoft Word (`*.docx`) & Markdown (`README.md`) |

---

## Installation  

> **Prerequisite:** Python 3.9 or newer installed on your system.

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/automatic_question_final.git
   cd automatic_question_final
   ```

2. **Create and activate a virtual environment**  
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**  
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt   # (create this file if missing)
   ```

   *If a `requirements.txt` file is not present, the core packages are:*  

   ```text
   Django>=4.0
   ```

4. **Apply database migrations**  
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin)**  
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**  
   ```bash
   python manage.py runserver
   ```

7. **Access the app**  
   Open a browser and navigate to `http://127.0.0.1:8000