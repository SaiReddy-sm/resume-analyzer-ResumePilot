# 🚀 ResumePilot – AI-Powered ATS Resume Analyzer

An intelligent **AI-based Resume Analyzer** that evaluates resumes against ATS (Applicant Tracking System) standards, predicts career roles, and provides personalized improvement suggestions to help candidates increase interview chances.

🌐 **Live Demo:** [https://resumepilot-upz4.onrender.com](https://resumepilot-upz4.onrender.com)

---

## 📌 Features

* 📄 Upload Resume (PDF/DOCX support)
* 🧠 AI-powered resume text extraction
* 📊 ATS Score calculation (0–100)
* 🧩 Skill detection & gap analysis
* 🎯 Career role prediction (multiple roles)
* 📈 Resume strength evaluation (Technical, Projects, Structure, Keywords)
* 🧠 Smart improvement suggestions
* 📋 22-point resume quality checklist
* 🎨 Modern UI with glassmorphism design
* 🌙 Dark / Light mode support
* ⚡ Animated score meter & progress bars

---

## 🏗️ Project Architecture

```
resume-analyzer-ResumePilot/
│
├── app.py                # Flask backend
├── analyzer.py           # Core ATS + NLP logic
├── requirements.txt      # Dependencies
│
├── templates/
│   ├── index.html        # Upload page
│   └── result.html       # Results dashboard
│
└── uploads/              # Temporary file storage
```

---

## ⚙️ Tech Stack

**Frontend:**

* HTML5
* Tailwind CSS
* JavaScript
* Jinja2 Templates

**Backend:**

* Python
* Flask
* Gunicorn

**AI/Logic:**

* Rule-based NLP scoring
* Keyword matching algorithm
* Skill extraction engine

---

## 📊 How ATS Scoring Works

The system evaluates resumes based on:

* Skills Match Percentage
* Resume Structure Quality
* Project Relevance
* Keyword Optimization
* Experience & Action Verbs

Final Score Formula (simplified):

```
ATS Score = Weighted sum of:
- Technical Skills (40%)
- Keywords Match (25%)
- Structure (20%)
- Projects (15%)
```

---

## 🧠 Career Prediction Engine

The system predicts multiple career paths such as:

* Frontend Developer
* Backend Developer
* Full Stack Developer
* Data Analyst
* AI/ML Engineer

Each role is ranked based on skill similarity and keyword alignment.

---

## 📦 Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/SaiReddy-sm/resume-analyzer-ResumePilot.git
cd resume-analyzer-ResumePilot
```

### 2️⃣ Create Virtual Environment (optional)

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Application

```bash
python app.py
```

App runs at:

```
http://127.0.0.1:5000
```

---

## 🌐 Deployment

This project is deployed using **Render**

👉 Live URL:
[https://resumepilot-upz4.onrender.com](https://resumepilot-upz4.onrender.com)

---

## 📸 UI Preview

* ATS Score Dashboard 🎯
* Resume Strength Meter 📊
* Career Match Engine 💼
* Skill Gap Insights 🧩

---

## 🚀 Future Improvements

* 🤖 AI GPT-based resume feedback
* 📊 Real ML-based scoring model
* 💾 User login & resume history
* 📄 Downloadable ATS report PDF
* 📈 Career growth roadmap visualization

---

## 👨‍💻 Author

**Ch.Sai Reddy**
Full Stack Developer | AI Enthusiast

---

## ⭐ If you like this project

Give a ⭐ on the repo and share it with others!


