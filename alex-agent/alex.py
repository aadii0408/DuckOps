# alex.py

import os
import re
import pandas as pd
from dotenv import load_dotenv
import openai
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class ResearchAssistantAgent:
    def __init__(self, prof_csv_path: str, lab_pdf_path: str):
        self.prof_data = pd.read_csv(prof_csv_path)
        self.knowledge_base = self._load_lab_pdf(lab_pdf_path)

    def _load_lab_pdf(self, filepath: str) -> dict:
        reader = PdfReader(filepath)
        raw_text = "\n".join([page.extract_text() or "" for page in reader.pages])
        pattern = r"(?=([A-Z][A-Za-z\s&()'\-]+(?:Laboratory|Center|Institute|Systems)))"
        parts = re.split(pattern, raw_text)

        labs = {}
        for i in range(1, len(parts), 2):
            title = parts[i].strip().lower()
            content = parts[i + 1].strip() if i + 1 < len(parts) else ""
            labs[title] = content
        return labs

    def _get_professor_context(self, question: str) -> str:
        for _, row in self.prof_data.iterrows():
            name = str(row.get("Name", "")).strip().lower()
            if name and name in question.lower():
                return "\n".join([f"{col}: {row[col]}" for col in self.prof_data.columns if pd.notna(row[col])])
        return ""

    def _get_lab_context(self, question: str) -> str:
        for lab_name in self.knowledge_base:
            if lab_name in question.lower():
                return self.knowledge_base[lab_name]
        return "\n".join(list(self.knowledge_base.values())[:2])

    def answer_question(self, question: str, system_instruction: str) -> str:
        try:
            prof_context = self._get_professor_context(question)
            if prof_context:
                context = f"Professor Info:\n{prof_context}"
            else:
                context = self._get_lab_context(question)

            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
                ],
                max_tokens=600,
                temperature=0
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"⚠️ Error generating response: {e}"
