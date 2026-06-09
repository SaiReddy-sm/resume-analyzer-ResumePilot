from PyPDF2 import PdfReader
import re

TECHNICAL_SKILLS_LIST = [
    # Languages
    "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#", "PHP", "Go", "Rust",
    # Frontend
    "HTML", "CSS", "React", "Next.js", "Angular", "Vue", "Bootstrap", "Tailwind",
    # Backend
    "Node.js", "Express", "Flask", "Django", "Spring Boot",
    # Databases
    "MongoDB", "MySQL", "PostgreSQL", "SQL", "SQLite",
    # Cloud
    "AWS", "Azure", "GCP",
    # DevOps
    "Docker", "Kubernetes", "Jenkins", "CI/CD", "Linux", "Git", "GitHub",
    # Data Science
    "Pandas", "NumPy", "Matplotlib", "Scikit-learn",
    # AI/ML
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "OpenCV",
    # APIs
    "REST API", "GraphQL",
    # Tools
    "Postman", "VS Code", "Figma", "Power BI", "Excel"
]

RESUME_SECTIONS = [
    "Skills",
    "Projects",
    "Education",
    "Certifications",
    "Experience"
]

ROLE_SKILLS = {
    "Frontend Developer": [
        "HTML", "CSS", "JavaScript", "React",
        "TypeScript", "Next.js", "Tailwind",
        "Bootstrap", "Git", "REST API"
    ],
    "Backend Developer": [
        "Python", "Java", "Node.js",
        "Express", "Django", "Flask",
        "SQL", "PostgreSQL", "MongoDB",
        "REST API"
    ],
    "Full Stack Developer": [
        "HTML", "CSS", "JavaScript",
        "React", "Node.js", "Express",
        "MongoDB", "SQL", "Git",
        "REST API"
    ],
    "Data Analyst": [
        "Python", "Pandas", "NumPy",
        "Excel", "Power BI", "SQL",
        "Matplotlib"
    ],
    "AI / ML Engineer": [
        "Python", "TensorFlow",
        "PyTorch", "Machine Learning",
        "Deep Learning", "NumPy",
        "Pandas"
    ]
}

ACTION_VERBS = [
    "developed", "built", "created", "implemented", "designed",
    "improved", "optimized", "managed", "led", "delivered",
    "engineered", "architected", "formulated", "coordinated", "accelerated"
]

def extract_text(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print("PDF Error:", e)
    return text


def detect_skills(text):
    text_lower = text.lower()
    found = []
    for skill in TECHNICAL_SKILLS_LIST:
        if re.search(r"\b" + re.escape(skill.lower()) + r"\b", text_lower):
            found.append(skill)
    missing = [skill for skill in TECHNICAL_SKILLS_LIST if skill not in found]
    return found, missing


def detect_sections(text):
    text_lower = text.lower()
    found = []
    for section in RESUME_SECTIONS:
        if section.lower() in text_lower:
            found.append(section)
    missing = [section for section in RESUME_SECTIONS if section not in found]
    return found, missing


def get_career_matches(found_skills):
    matches = {}
    found_set = set(found_skills)
    for role, role_skills in ROLE_SKILLS.items():
        matched = len(found_set.intersection(role_skills))
        percentage = round((matched / len(role_skills)) * 100)
        matches[role] = percentage
    return dict(sorted(matches.items(), key=lambda x: x[1], reverse=True))


def get_relevant_missing_skills(found_skills):
    matches = get_career_matches(found_skills)
    best_role = list(matches.keys())[0] if matches else "Full Stack Developer"
    role_skills = ROLE_SKILLS.get(best_role, [])
    missing = []
    for skill in role_skills:
        if skill not in found_skills:
            missing.append(skill)
    return best_role, missing[:8]


def calculate_score(found_sections, found_skills, text=""):
    score = 0
    text_lower = text.lower()

    # 1. Section Presence (Max 25 points)
    section_weights = {
        "Experience": 8,
        "Skills": 6,
        "Projects": 5,
        "Education": 4,
        "Certifications": 2
    }
    section_score = sum(section_weights[sec] for sec in found_sections if sec in section_weights)
    score += section_score

    # 2. Skill Density & Overstuffing Analysis (Max 25 points)
    num_skills = len(found_skills)
    if 1 <= num_skills <= 5:
        score += 10
    elif 6 <= num_skills <= 15:
        score += 20
    elif 16 <= num_skills <= 30:
        score += 25
    elif num_skills > 30:
        score += 15

    # 3. Contact & Format Parsing Standards (Max 20 points)
    if re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text_lower):
        score += 5
    if re.search(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", text_lower):
        score += 5
    if "linkedin.com" in text_lower:
        score += 5
    if "github.com" in text_lower:
        score += 5

    # 4. Metrics & Quantified Achievements (Max 15 points)
    metric_matches = re.findall(
        r"\b(?:\d{1,3}(?:,\d{3})*(?:\.\d+)?\s*(?:%|years|employees|users|million|billion|k|m)\b|(?:\$\d+(?:\.\d+)?\s*(?:million|billion|k|m|b)?))",
        text_lower
    )
    num_metrics = len(metric_matches)
    if num_metrics == 0:
        score += 0
    elif 1 <= num_metrics <= 2:
        score += 5
    elif 3 <= num_metrics <= 5:
        score += 10
    else:
        score += 15

    # 5. Action Verb Diversity (Max 15 points)
    verbs_found = [verb for verb in ACTION_VERBS if verb in text_lower]
    score += min(len(verbs_found) * 2.5, 15)

    # 6. Quality Checks & Deductions
    cliches = ["team player", "synergy", "hard worker", "motivated self-starter", "results-driven"]
    cliche_count = sum(1 for word in cliches if word in text_lower)
    if cliche_count >= 3:
        score -= 5

    return max(0, min(round(score), 100))


def analyze_resume_strength(score):
    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Strong"
    elif score >= 60:
        return "Average"
    return "Needs Improvement"


def generate_suggestions(found_sections, found_skills, text=""):
    suggestions = []
    text_lower = text.lower()

    # 1. Section Checks (5 Checks)
    for section in RESUME_SECTIONS:
        if section in found_sections:
            suggestions.append({
                "name": f"{section} Section Presence",
                "category": "Structure",
                "status": "pass",
                "message": f"Successfully parsed the '{section}' structural module."
            })
        else:
            suggestions.append({
                "name": f"{section} Section Presence",
                "category": "Structure",
                "status": "fail",
                "message": f"Missing '{section}' structural section. Ensure this header is clean."
            })

    # 2. Contact Information Diagnostics (5 Checks)
    if re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text_lower):
        suggestions.append({
            "name": "Email Verification",
            "category": "Contact",
            "status": "pass",
            "message": "Valid email structural markers matched successfully."
        })
    else:
        suggestions.append({
            "name": "Email Verification",
            "category": "Contact",
            "status": "fail",
            "message": "Email address not recognized. Maintain simple contact details."
        })

    if re.search(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", text_lower):
        suggestions.append({
            "name": "Phone Connectivity Check",
            "category": "Contact",
            "status": "pass",
            "message": "Valid structural telephone mapping identified."
        })
    else:
        suggestions.append({
            "name": "Phone Connectivity Check",
            "category": "Contact",
            "status": "fail",
            "message": "Missing standard phone details on contact line."
        })

    if "linkedin.com" in text_lower:
        suggestions.append({
            "name": "LinkedIn Integration",
            "category": "Contact",
            "status": "pass",
            "message": "LinkedIn profile URL present on contact segment."
        })
    else:
        suggestions.append({
            "name": "LinkedIn Integration",
            "category": "Contact",
            "status": "warning",
            "message": "Adding a LinkedIn URL can boost technical profile viability."
        })

    if "github.com" in text_lower:
        suggestions.append({
            "name": "GitHub Repository link",
            "category": "Contact",
            "status": "pass",
            "message": "GitHub links correctly discovered in header metadata."
        })
    else:
        suggestions.append({
            "name": "GitHub Repository link",
            "category": "Contact",
            "status": "warning",
            "message": "Missing portfolio repository reference. Include standard GitHub URLs."
        })

    if "http://" in text_lower or "https://" in text_lower or ".com" in text_lower:
        suggestions.append({
            "name": "Personal Domain Presence",
            "category": "Contact",
            "status": "pass",
            "message": "Active portfolio index links successfully cataloged."
        })
    else:
        suggestions.append({
            "name": "Personal Domain Presence",
            "category": "Contact",
            "status": "warning",
            "message": "Consider adding an active portfolio index page link."
        })

    # 3. Keyword & Word Density Metrics (6 Checks)
    words = text_lower.split()
    word_count = len(words)
    if word_count == 0:
        suggestions.append({
            "name": "Parsing Feasibility Check",
            "category": "Content",
            "status": "fail",
            "message": "Resume text could not be processed. Make sure it is not an image-only PDF."
        })
    elif word_count < 300:
        suggestions.append({
            "name": "Information Volume Threshold",
            "category": "Content",
            "status": "warning",
            "message": f"Resume is quite brief ({word_count} words). Aim for a robust 400-800 word range."
        })
    elif word_count > 1200:
        suggestions.append({
            "name": "Information Volume Threshold",
            "category": "Content",
            "status": "warning",
            "message": f"Resume text is dense ({word_count} words). Streamline components to avoid content bloat."
        })
    else:
        suggestions.append({
            "name": "Information Volume Threshold",
            "category": "Content",
            "status": "pass",
            "message": f"Optimally scaled formatting structure verified ({word_count} words)."
        })

    if len(found_skills) > 30:
        suggestions.append({
            "name": "Keyword Optimization Density",
            "category": "Skills",
            "status": "warning",
            "message": "Keyword stuffing detected. Curate core skill list to pass enterprise parser penalties."
        })
    elif len(found_skills) >= 5:
        suggestions.append({
            "name": "Keyword Optimization Density",
            "category": "Skills",
            "status": "pass",
            "message": f"Healthy distribution of keywords mapped successfully ({len(found_skills)} items)."
        })
    else:
        suggestions.append({
            "name": "Keyword Optimization Density",
            "category": "Skills",
            "status": "fail",
            "message": "Minimal targeted keywords found. Add standard terms related to target jobs."
        })

    cliches = ["team player", "synergy", "hard worker", "motivated self-starter", "results-driven"]
    cliche_count = sum(1 for word in cliches if word in text_lower)
    if cliche_count >= 3:
        suggestions.append({
            "name": "Buzzword Usage Filter",
            "category": "Content",
            "status": "warning",
            "message": f"Avoid generic buzzwords ({cliche_count} found). Replace them with objective work accomplishments."
        })
    else:
        suggestions.append({
            "name": "Buzzword Usage Filter",
            "category": "Content",
            "status": "pass",
            "message": "Professional, jargon-minimized writing style verified."
        })

    # 4. Metrics & Work Impact Elements (6 Checks)
    metric_matches = re.findall(r"\b(?:\d+%)|(?:\$\d+)", text_lower)
    if len(metric_matches) > 0:
        suggestions.append({
            "name": "Quantifiable Achievements",
            "category": "Impact",
            "status": "pass",
            "message": "Excellent use of quantitative metrics on accomplishment descriptions."
        })
    else:
        suggestions.append({
            "name": "Quantifiable Achievements",
            "category": "Impact",
            "status": "fail",
            "message": "No numeric impact variables present. Quantify projects with milestones."
        })

    verbs_found = [verb for verb in ACTION_VERBS if verb in text_lower]
    if len(verbs_found) >= 5:
        suggestions.append({
            "name": "Action Verb Diversity",
            "category": "Impact",
            "status": "pass",
            "message": "Assertive achievement statements constructed using active verbs."
        })
    else:
        suggestions.append({
            "name": "Action Verb Diversity",
            "category": "Impact",
            "status": "warning",
            "message": "Achievement syntax is weak. Incorporate strong active phrases."
        })

    bullet_symbols = ["•", "-", "▪", "●", "*"]
    bullets_found = sum(text.count(sym) for sym in bullet_symbols)
    if bullets_found >= 10:
        suggestions.append({
            "name": "Layout Uniformity & Bullets",
            "category": "Structure",
            "status": "pass",
            "message": "Clean bullet-point scanning hierarchy mapped correctly."
        })
    else:
        suggestions.append({
            "name": "Layout Uniformity & Bullets",
            "category": "Structure",
            "status": "warning",
            "message": "Minimal bullet points detected. Structure long paragraphs into bullet lists."
        })

    return suggestions