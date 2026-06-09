from flask import Flask, render_template, request
import os

from analyzer import (
    extract_text,
    detect_skills,
    detect_sections,
    calculate_score,
    generate_suggestions,
    get_career_matches,
    get_relevant_missing_skills,
    analyze_resume_strength
)

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files["resume"]
        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )
        file.save(filepath)

        # 1. Extract and analyze resume text content
        text = extract_text(filepath)
        skills, missing_skills = detect_skills(text)
        sections, missing_sections = detect_sections(text)

        # 2. Run detailed parser calculations
        score = calculate_score(
            sections,
            skills,
            text
        )

        suggestions = generate_suggestions(
            sections,
            skills,
            text=text
        )

        career_matches = get_career_matches(skills)
        recommended_role, relevant_missing_skills = get_relevant_missing_skills(skills)
        strength = analyze_resume_strength(score)

        # calculate dynamic metric percentages
        total_keywords = len(skills) + len(relevant_missing_skills)
        keyword_match_val = round((len(skills) / total_keywords) * 100) if total_keywords > 0 else 0

        # 3. Dynamic recruiter feedback comments depending on final scores
        if score >= 90:
            recruiter_comment = {
                "type": "success",
                "title": "Immediate Interview Pick!",
                "message": "Absolute unicorn. Pristine structure, dense core stack markers, and quantifiable metrics on accomplishments. Pushing to the hiring team immediately!"
            }
        elif score >= 75:
            recruiter_comment = {
                "type": "info",
                "title": "Strong Technical Candidate",
                "message": "Resume checks out. Clean sections and respectable stack coverage. If they resolve the small formatting suggestions, I would move them to interview loops."
            }
        elif score >= 60:
            recruiter_comment = {
                "type": "warning",
                "title": "Average Profile Quality",
                "message": "Readable but relies heavily on generic text blocks. Needs to swap corporate buzzwords with metrics and projects, but has potential."
            }
        else:
            recruiter_comment = {
                "type": "error",
                "title": "Needs Structural Revision",
                "message": "This candidate is testing my patience. No action metrics, missing contact metadata, and key section blocks are empty. Is this a draft?"
            }

        # 4. Construct response dictionary matching exact result.html template keys
        results = {
            "score": score,
            "strength": strength,
            "recommended_role": recommended_role,
            "career_matches": career_matches,

            "keyword_match": keyword_match_val,

            "summary": (
                f"Your resume demonstrates core capabilities in "
                f"{', '.join(skills[:4]) if skills else 'general technical fundamentals'}. "
                f"Based on detected key patterns, your background aligns closest with a "
                f"{recommended_role} development pathway. "
                f"Integrating quantifiable metrics, project contributions, "
                f"and active verbs will optimize index parsers further."
            ),

            "skills_detected": skills,
            "skills_missing": relevant_missing_skills,

            "strength_technical": min(len(skills) * 6, 100),
            "strength_projects": 95 if "Projects" in sections else 45,
            "strength_structure": min(len(sections) * 20, 100),
            "strength_keywords": keyword_match_val,

            "recruiter_popup": recruiter_comment,
            "suggestions": suggestions,

            "roadmap": [
                {
                    "phase": "Phase 1",
                    "timeframe": "Immediate",
                    "task": "Structure Contact Details",
                    "desc": (
                        f"Include personal portfolio and links. Validate and check structure "
                        f"for: {', '.join(missing_sections) if missing_sections else 'no missing headers.'}"
                    )
                },
                {
                    "phase": "Phase 2",
                    "timeframe": "This Week",
                    "task": "Target Tech Stack Gaps",
                    "desc": (
                        f"Integrate key missing skills: "
                        f"{', '.join(relevant_missing_skills[:3]) if relevant_missing_skills else 'Review framework keywords.'}"
                    )
                },
                {
                    "phase": "Phase 3",
                    "timeframe": "Next 2 Weeks",
                    "task": "Incorporate Core Metrics",
                    "desc": "Swap plain descriptors for impact percentages or metric parameters inside your experience line blocks."
                }
            ]
        }

        # Delete analyzed file from uploads directory to preserve storage
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                print("Failed to delete file:", e)

        return render_template("result.html", results=results)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)