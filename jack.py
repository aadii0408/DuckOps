import os
import re
import streamlit as st
from dotenv import load_dotenv
import PyPDF2
import docx
from openai import OpenAI
import json
import pandas as pd
from typing import Optional, Dict, List, Any

# Load environment variables
load_dotenv()


class SkillAssessmentAgent:
    def __init__(self):
        """Initialize the Skill Assessment Agent"""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def _extract_text_from_pdf(self, file) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            st.error(f"PDF parsing error: {e}")
            return ""

    def _extract_text_from_docx(self, file) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            st.error(f"DOCX parsing error: {e}")
            return ""

    def _clean_text(self, text: str) -> str:
        """Remove non-ASCII characters and clean text"""
        if not text:
            return ""

        # Remove non-ASCII characters
        text = "".join(char for char in text if ord(char) < 128)

        # Remove extra whitespaces
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def parse_resume(self, file) -> str:
        """Parse resume based on file type"""
        filename = file.name.lower()

        try:
            # Extract text based on file type
            if filename.endswith(".pdf"):
                text = self._extract_text_from_pdf(file)
            elif filename.endswith((".docx", ".doc")):
                text = self._extract_text_from_docx(file)
            else:
                raise ValueError("Unsupported file type. Please upload PDF or DOCX.")

            # Clean and return text
            return self._clean_text(text)

        except Exception as e:
            st.error(f"Resume parsing error: {e}")
            return ""

    def analyze_resume(
        self, resume_text: str, job_description: str
    ) -> Dict[str, List[str]]:
        """Analyze resume skills and generate assessment"""
        try:
            # First approach: Direct text extraction with clear formatting instructions
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional career advisor analyzing resumes. Provide your analysis in clear, distinct sections.",
                    },
                    {
                        "role": "user",
                        "content": f"""
                        Analyze this resume against the job description:
                        
                        RESUME:
                        {resume_text}
                        
                        JOB DESCRIPTION:
                        {job_description}
                        
                        Format your analysis in these EXACT five sections with lists:
                        
                        TECHNICAL SKILLS:
                        - [skill 1]
                        - [skill 2]
                        
                        SOFT SKILLS:
                        - [skill 1]
                        - [skill 2]
                        
                        STRENGTHS:
                        - [strength 1]
                        - [strength 2]
                        
                        IMPROVEMENT AREAS:
                        - [area 1]
                        - [area 2]
                        
                        CAREER RECOMMENDATIONS:
                        - [recommendation 1]
                        - [recommendation 2]
                        """,
                    },
                ],
                max_tokens=1000,
            )

            result_text = response.choices[0].message.content

            # Define result structure
            assessment = {
                "technical_skills": [],
                "soft_skills": [],
                "strengths": [],
                "improvement_areas": [],
                "career_recommendations": [],
            }

            # Parse sections
            current_section = None

            for line in result_text.strip().split("\n"):
                line = line.strip()
                if not line:
                    continue

                # Check for section headers (case insensitive)
                line_lower = line.lower()

                if "technical skills" in line_lower and ":" in line:
                    current_section = "technical_skills"
                    continue
                elif "soft skills" in line_lower and ":" in line:
                    current_section = "soft_skills"
                    continue
                elif line_lower.startswith("strengths") and ":" in line:
                    current_section = "strengths"
                    continue
                elif (
                    "improvement areas" in line_lower
                    or "areas for improvement" in line_lower
                ) and ":" in line:
                    current_section = "improvement_areas"
                    continue
                elif "career recommendations" in line_lower and ":" in line:
                    current_section = "career_recommendations"
                    continue

                # Process line if we're in a section and it starts with - or *
                if current_section and (line.startswith("-") or line.startswith("*")):
                    # Remove - or * and trim
                    clean_line = line[1:].strip()
                    assessment[current_section].append(clean_line)

            # Add default items if sections are empty
            for section, items in assessment.items():
                if not items:
                    # Try to find lines without bullet points in that section
                    for line in result_text.strip().split("\n"):
                        if (
                            section.replace("_", " ") in line.lower()
                            and not line.startswith("-")
                            and not line.startswith("*")
                        ):
                            assessment[section] = [
                                "Found in analysis but not in bullet format"
                            ]
                            break
                    else:
                        assessment[section] = ["Not specifically mentioned"]

            return assessment

        except Exception as e:
            # In case of any error, provide default response
            st.error(f"Error analyzing resume: {str(e)}")
            return {
                "technical_skills": ["Error processing skills - please try again"],
                "soft_skills": ["Error processing skills - please try again"],
                "strengths": ["Error processing strengths - please try again"],
                "improvement_areas": [
                    "Error processing improvement areas - please try again"
                ],
                "career_recommendations": [
                    "Error processing recommendations - please try again"
                ],
            }

    def generate_learning_plan(
        self,
        resume_text: str,
        job_description: str,
        skill_assessment: Dict[str, List[str]],
    ) -> List[Dict[str, Any]]:
        """Generate a 14-day skill development plan"""
        try:
            # Format the assessment as bullet points to include in the prompt
            assessment_text = ""
            for category, items in skill_assessment.items():
                formatted_category = category.replace("_", " ").title()
                assessment_text += f"{formatted_category}:\n"
                for item in items:
                    assessment_text += f"- {item}\n"
                assessment_text += "\n"

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional career coach creating detailed interview preparation plans.",
                    },
                    {
                        "role": "user",
                        "content": f"""
                        Create a detailed 14-day interview preparation plan for a candidate with the following profile:
                        
                        RESUME SUMMARY:
                        {resume_text[:500]}...
                        
                        JOB DESCRIPTION:
                        {job_description[:500]}...
                        
                        SKILL ASSESSMENT:
                        {assessment_text}
                        
                        For each day (Days 1-14), provide this EXACT format with clear headers:
                        
                        DAY 1:
                        LEARNING GOALS: [specific goals]
                        SKILL FOCUS: [primary skill]
                        RESOURCES: [resource 1, resource 2]
                        PRACTICE EXERCISES: [specific exercises]
                        PROGRESS TRACKING: [tracking method]
                        
                        DAY 2:
                        ...
                        
                        (Continue for all 14 days)
                        """,
                    },
                ],
                max_tokens=2000,
            )

            result_text = response.choices[0].message.content

            # Parse the 14-day plan
            learning_plan = []
            current_day = None
            day_data = {}

            # Split by DAY X: pattern
            day_blocks = re.split(r"DAY\s+(\d+):", result_text, flags=re.IGNORECASE)

            # Process day blocks (skip first element as it's text before Day 1)
            for i in range(1, len(day_blocks), 2):
                if i + 1 < len(day_blocks):
                    day_num = int(day_blocks[i])
                    day_content = day_blocks[i + 1]

                    day_data = {
                        "day": day_num,
                        "learning_goals": "Not specified",
                        "skill_focus": "Not specified",
                        "resources": ["Not specified"],
                        "practice_exercises": "Not specified",
                        "progress_tracking": "Not specified",
                    }

                    # Extract sections using regex
                    learning_goals = re.search(
                        r"LEARNING GOALS:(.*?)(?:SKILL FOCUS:|$)",
                        day_content,
                        re.DOTALL | re.IGNORECASE,
                    )
                    if learning_goals:
                        day_data["learning_goals"] = learning_goals.group(1).strip()

                    skill_focus = re.search(
                        r"SKILL FOCUS:(.*?)(?:RESOURCES:|$)",
                        day_content,
                        re.DOTALL | re.IGNORECASE,
                    )
                    if skill_focus:
                        day_data["skill_focus"] = skill_focus.group(1).strip()

                    resources = re.search(
                        r"RESOURCES:(.*?)(?:PRACTICE EXERCISES:|$)",
                        day_content,
                        re.DOTALL | re.IGNORECASE,
                    )
                    if resources:
                        resource_text = resources.group(1).strip()
                        # Split by commas or bullet points
                        resource_list = re.split(r",|\n-|\n\*", resource_text)
                        day_data["resources"] = [
                            r.strip() for r in resource_list if r.strip()
                        ]

                    exercises = re.search(
                        r"PRACTICE EXERCISES:(.*?)(?:PROGRESS TRACKING:|$)",
                        day_content,
                        re.DOTALL | re.IGNORECASE,
                    )
                    if exercises:
                        day_data["practice_exercises"] = exercises.group(1).strip()

                    tracking = re.search(
                        r"PROGRESS TRACKING:(.*?)(?:\n\n|$)",
                        day_content,
                        re.DOTALL | re.IGNORECASE,
                    )
                    if tracking:
                        day_data["progress_tracking"] = tracking.group(1).strip()

                    learning_plan.append(day_data)

            # Fill in missing days if needed
            while len(learning_plan) < 14:
                next_day = len(learning_plan) + 1
                learning_plan.append(
                    {
                        "day": next_day,
                        "learning_goals": f"Continue building skills from previous days",
                        "skill_focus": "Mixed skills review",
                        "resources": ["Online courses", "Practice interviews"],
                        "practice_exercises": "Review and apply previous lessons",
                        "progress_tracking": "Self-assessment",
                    }
                )

            return learning_plan[:14]  # Ensure exactly 14 days

        except Exception as e:
            # In case of any error, provide a default 14-day plan
            st.error(f"Error generating learning plan: {str(e)}")
            default_plan = []
            for day in range(1, 15):
                default_plan.append(
                    {
                        "day": day,
                        "learning_goals": f"Skill development for Day {day}",
                        "skill_focus": "Career development",
                        "resources": ["Online resources"],
                        "practice_exercises": "Practice interviews",
                        "progress_tracking": "Self-assessment",
                    }
                )
            return default_plan


def save_assessment_to_json(
    assessment: Dict[str, List[str]], learning_plan: List[Dict[str, Any]], filename: str
):
    """Save skill assessment and learning plan to a JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as writeJSON:
            json.dump(
                {"assessment": assessment, "learning_plan": learning_plan},
                writeJSON,
                ensure_ascii=False,
                indent=2,
            )
        return True
    except Exception as e:
        st.error(f"Error saving assessment: {e}")
        return False


def main():
    # Page configuration
    st.set_page_config(
        page_title="Jack - Career Advisor", page_icon="📊", layout="wide"
    )

    # API Key Validation
    if not os.getenv("OPENAI_API_KEY"):
        st.error(
            "⚠️ OpenAI API Key not found. Please set your API key in the .env file."
        )
        return

    # Header
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("https://img.icons8.com/color/96/000000/robot.png", width=80)
    with col2:
        st.title("Jack - Career Advisor and  Assessment Agent")
        st.markdown(
            "*Upload your latest resume and a job description to get a personalized skills assessment and 14-day interview preparation plan*"
        )

    # Create two columns for inputs
    col1, col2 = st.columns(2)

    with col1:
        # Resume Upload
        uploaded_file = st.file_uploader(
            "📄 Upload Resume (PDF/DOCX) *",
            type=["pdf", "docx"],
            help="Upload your professional resume (Required)",
        )

    with col2:
        # Required Job Description
        job_description = st.text_area(
            "💼 Job Description *",
            height=150,
            help="Paste the job description for precise skill matching (Required)",
        )

    # Analysis Trigger
    analyze_button = st.button(
        "🔍 Analyze Profile", type="primary", use_container_width=True
    )

    if analyze_button:
        # Validate inputs
        if not uploaded_file:
            st.error("⚠️ Please upload a resume")
            return

        if not job_description:
            st.error("⚠️ Please provide a job description")
            return

        try:
            # Initialize Agent
            agent = SkillAssessmentAgent()

            # Parse Resume
            with st.spinner("📄 Parsing resume..."):
                resume_text = agent.parse_resume(uploaded_file)

            if not resume_text:
                st.error("Failed to extract text from resume")
                return

            # Skills Assessment
            with st.spinner("🧠 Analyzing profile against job requirements..."):
                skill_assessment = agent.analyze_resume(resume_text, job_description)

            # Display assessment using tabs and tables
            st.subheader("🎯 Skills Assessment")

            # Convert assessment to DataFrames for tabular display
            tabs = st.tabs(
                [
                    "Technical Skills",
                    "Soft Skills",
                    "Strengths",
                    "Improvement Areas",
                    "Career Recommendations",
                ]
            )

            with tabs[0]:
                st.table(
                    pd.DataFrame(
                        {
                            "Technical Skills": skill_assessment.get(
                                "technical_skills", []
                            )
                        }
                    )
                )

            with tabs[1]:
                st.table(
                    pd.DataFrame(
                        {"Soft Skills": skill_assessment.get("soft_skills", [])}
                    )
                )

            with tabs[2]:
                st.table(
                    pd.DataFrame({"Strengths": skill_assessment.get("strengths", [])})
                )

            with tabs[3]:
                st.table(
                    pd.DataFrame(
                        {
                            "Improvement Areas": skill_assessment.get(
                                "improvement_areas", []
                            )
                        }
                    )
                )

            with tabs[4]:
                st.table(
                    pd.DataFrame(
                        {
                            "Career Recommendations": skill_assessment.get(
                                "career_recommendations", []
                            )
                        }
                    )
                )

            # Learning Plan
            with st.spinner(
                "📚 Creating personalized 14-day interview preparation plan..."
            ):
                learning_plan = agent.generate_learning_plan(
                    resume_text, job_description, skill_assessment
                )

            # Display plan as a table
            st.subheader("📝 14-Day Interview Preparation Plan")

            # Create a DataFrame from the learning plan for tabular display
            plan_data = []
            for day in learning_plan:
                plan_data.append(
                    {
                        "Day": f"Day {day.get('day', 'N/A')}",
                        "Skill Focus": day.get("skill_focus", "N/A"),
                        "Learning Goals": day.get("learning_goals", "N/A"),
                        "Resources": ", ".join(day.get("resources", ["N/A"])),
                        "Practice Exercises": day.get("practice_exercises", "N/A"),
                        "Progress Tracking": day.get("progress_tracking", "N/A"),
                    }
                )

            # Display as a table with alternating colors
            plan_df = pd.DataFrame(plan_data)
            st.dataframe(
                plan_df,
                column_config={
                    "Day": st.column_config.TextColumn("Day", width="small"),
                    "Skill Focus": st.column_config.TextColumn(
                        "Skill Focus", width="medium"
                    ),
                    "Learning Goals": st.column_config.TextColumn(
                        "Learning Goals", width="large"
                    ),
                    "Resources": st.column_config.TextColumn(
                        "Resources", width="large"
                    ),
                    "Practice Exercises": st.column_config.TextColumn(
                        "Practice Exercises", width="large"
                    ),
                    "Progress Tracking": st.column_config.TextColumn(
                        "Progress Tracking", width="medium"
                    ),
                },
                use_container_width=True,
                hide_index=True,
            )

            # Download options
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Assessment & Plan", type="primary"):
                    if save_assessment_to_json(
                        skill_assessment, learning_plan, "career_assessment.json"
                    ):
                        st.success("✅ Assessment and plan saved successfully!")

            with col2:
                # Create CSV download button for the plan
                csv = plan_df.to_csv(index=False)
                st.download_button(
                    label="📊 Download Plan as CSV",
                    data=csv,
                    file_name="interview_preparation_plan.csv",
                    mime="text/csv",
                    type="primary",
                )

        except Exception as e:
            st.error(f"Analysis error: {e}")
            st.exception(e)  # Show full traceback for debugging


if __name__ == "__main__":
    main()
