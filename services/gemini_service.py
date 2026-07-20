import google.generativeai as genai
import streamlit as st

from utils.quiz_parser import parse_quiz


def build_quiz_prompt(source_text: str, question_count: int) -> str:
    return f"""
Dựa vào nội dung sau:
---
{source_text}
---
Hãy tạo {question_count} câu hỏi trắc nghiệm bằng tiếng Việt.
Chỉ trả về JSON hợp lệ, không thêm chữ bên ngoài. JSON là một mảng; mỗi phần tử có dạng:
{{
  "question": "Nội dung câu hỏi",
  "options": {{"A": "Đáp án A", "B": "Đáp án B", "C": "Đáp án C", "D": "Đáp án D"}},
  "answer": "A",
  "explanation": "Giải thích ngắn"
}}
"""


def generate_quiz(source_text: str, question_count: int) -> list[dict]:
    """Generate and validate quiz questions with Gemini."""
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(build_quiz_prompt(source_text, question_count))
    return parse_quiz(response.text)
