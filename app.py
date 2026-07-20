import streamlit as st

from services.gemini_service import generate_quiz
from utils.pdf_reader import extract_text_from_pdf


def reset_score() -> None:
    """Hide the score whenever an answer changes."""
    st.session_state.quiz_submitted = False


def render_quiz() -> None:
    questions = st.session_state.get("quiz_questions", [])
    if not questions:
        if "quiz_questions" in st.session_state:
            st.warning("Chưa tách được quiz tự động. Hãy bấm Tạo câu hỏi lại.")
        return

    submitted = st.session_state.get("quiz_submitted", False)

    for index, item in enumerate(questions, start=1):
        st.subheader(f"Câu {index}: {item['question']}")
        choices = [f"{key}. {value}" for key, value in item["options"].items()]
        selected = st.radio(
            "Chọn đáp án",
            choices,
            index=None,
            key=f"question_{index}",
            on_change=reset_score,
        )

        if submitted and selected:
            selected_key = selected.split(".", 1)[0]
            if selected_key == item["answer"]:
                st.success(f"Đúng rồi! Đáp án đúng là {item['answer']}.")
            else:
                correct_text = item["options"][item["answer"]]
                st.error(f"Chưa đúng. Đáp án đúng là {item['answer']}. {correct_text}")

            if item["explanation"]:
                st.info(item["explanation"])
        st.divider()

    if st.button("Chấm điểm"):
        st.session_state.quiz_submitted = True
        st.rerun()

    if submitted:
        selected_answers = [
            st.session_state.get(f"question_{index}")
            for index in range(1, len(questions) + 1)
        ]
        correct_count = sum(
            answer is not None and answer.split(".", 1)[0] == question["answer"]
            for answer, question in zip(selected_answers, questions)
        )
        unanswered_count = selected_answers.count(None)
        total_questions = len(questions)
        wrong_count = total_questions - correct_count - unanswered_count
        score = correct_count / total_questions * 10

        st.subheader("Kết quả")
        st.metric("Điểm", f"{score:.1f}/10")
        st.write(
            f"Đúng: {correct_count}/{total_questions} | "
            f"Sai: {wrong_count} | Không trả lời: {unanswered_count}"
        )


def main() -> None:
    st.set_page_config(page_title="QuizAI", page_icon="📝")
    st.title("Tạo đề trắc nghiệm - QuizAI")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    question_count = st.number_input(
        "Chọn số câu hỏi", min_value=1, max_value=50, value=10, step=1
    )

    if not uploaded_file:
        return

    try:
        pdf_text = extract_text_from_pdf(uploaded_file)
    except Exception as error:
        st.error(f"Không thể đọc PDF: {error}")
        return

    if not pdf_text:
        st.warning("Không tìm thấy nội dung văn bản trong PDF này.")
        return

    st.success("Đã đọc PDF!")
    if st.button("Tạo câu hỏi"):
        try:
            with st.spinner("Đang tạo câu hỏi..."):
                st.session_state.quiz_questions = generate_quiz(pdf_text, int(question_count))
            st.session_state.quiz_submitted = False
        except Exception as error:
            st.error(f"Không thể tạo câu hỏi: {error}")

    render_quiz()


if __name__ == "__main__":
    main()
