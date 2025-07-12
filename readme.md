# StackIt – A Minimal Q&A Forum Platform

StackIt is a minimalist question-and-answer platform that encourages collaborative learning and structured knowledge sharing. Designed with simplicity and usability in mind, StackIt focuses on core features like asking, answering, and managing questions within a community environment.

---

## 🚀 Features

### 🧠 For Users:
- **Ask Questions**  
  Users can easily submit a new question by filling in:
  - **Title** – Concise and descriptive
  - **Description** – Supports rich-text formatting for clear, structured input

- **Answer Questions**  
  View and respond to existing questions, participate in meaningful knowledge exchange.

---

### 🔐 Admin Role:
- Reject inappropriate or spammy questions
- Ban users who violate community guidelines
- Monitor and manage:
  - Pending, accepted, or canceled interactions
- Broadcast announcements (e.g., feature updates, downtime alerts)
- Download activity reports, feedback logs, and question statistics

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **Backend:** Django (Python)
- **Database:** SQLite
- **Template Engine:** Django Templates
- **Admin Panel:** Django Admin
- **Deployment-ready:** Yes

<pre lang="markdown"> ``` stack_it/ ├── accounts/ # User authentication and profiles │ ├── migrations/ │ ├── admin.py │ ├── models.py │ ├── views.py │ └── ... │ ├── questions/ # Question and answer logic │ ├── migrations/ │ ├── management/ │ ├── templatetags/ │ ├── models.py │ └── ... │ ├── static/ # Static assets │ ├── css/ │ ├── images/ │ └── js/ │ ├── templates/ # HTML templates │ ├── ask_question.html │ ├── question_detail.html │ ├── login.html │ └── ... │ ├── db.sqlite3 # Default SQLite database ├── manage.py # Django management script └── settings.py # Project configurations ``` </pre>

## 🧪 How to Run Locally

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Faraaz05/ODOO-StackIT-Defenders.git
   cd stackit
