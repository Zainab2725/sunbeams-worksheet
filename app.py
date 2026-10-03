import streamlit as st

from utils.session import init_session
from utils.image_utils import prepare_image
from services.image_analyzer import analyze_material
from services.worksheet_generator import generate_worksheet, regenerate_question
from services.quality_checker import quality_check
from services.flashcard_generator import generate_flashcards
from services.quiz_generator import generate_quiz
from services.revision_generator import generate_revision_notes
from pdf.worksheet_pdf import build_worksheet_pdf
from pdf.answer_key_pdf import build_answer_key_pdf


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Sunbeams Worksheet Studio",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# SESSION
# =========================================================

init_session()

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# =========================================================
# CUSTOM STYLE
# =========================================================

st.markdown(
    """
    <style>
    :root {
        --purple: #6C4CCF;
        --purple-dark: #5136A6;
        --cream: #FBF9F5;
        --ink: #252136;
        --muted: #756F82;
        --card: #FFFFFF;
        --soft: #F1ECFA;
    }

    .stApp {
        background: var(--cream);
        color: var(--ink);
    }

    [data-testid="stSidebar"] {
        background: #F1ECFA;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 1.6rem;
    }

    .hero {
        padding: 28px 32px;
        border-radius: 24px;
        background: linear-gradient(135deg,#F1ECFA,#FFFFFF);
        border: 1px solid #E2D9F5;
        margin-bottom: 22px;
    }

    .hero h1 {
        margin: 0;
        color: #252136;
        font-size: 2.3rem;
    }

    .hero p {
        color: #756F82;
        font-size: 1.02rem;
        margin-top: 8px;
    }

    .card {
        background: white;
        border: 1px solid #E7E1EF;
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 12px;
    }

    .small-muted {
        color: #756F82;
        font-size: 0.88rem;
    }

    div.stButton > button,
    div.stDownloadButton > button {
        border-radius: 10px;
        border: 1px solid #6C4CCF;
    }

    div.stButton > button[kind="primary"] {
        background: #6C4CCF;
        color: white;
    }

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #E7E1EF;
        padding: 12px;
        border-radius: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("## SUNBEAMS")
    st.caption("Spread the Light")
    st.markdown("---")

    pages = [
        "Dashboard",
        "Create Worksheet",
        "Flashcards",
        "Quiz",
        "Revision Notes",
    ]

    page = st.radio(
        "Workspace",
        pages,
        index=pages.index(st.session_state.page),
        label_visibility="collapsed",
    )

    st.session_state.page = page

    st.markdown("---")

    if st.session_state.material_analysis:
        st.markdown("**Current material**")
        st.write(
            st.session_state.material_analysis.get(
                "title",
                "Analyzed material"
            )
        )
        st.caption(
            st.session_state.material_analysis.get(
                "subject",
                ""
            )
        )

    st.caption("Session-only storage in this version.")


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">
        <h1>Sunbeams Worksheet Studio</h1>
        <p>
            Turn classroom material into polished,
            classroom-ready learning resources.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.subheader("Teacher Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    history = st.session_state.resource_history

    c1.metric(
        "Worksheets",
        sum(x["type"] == "Worksheet" for x in history)
    )

    c2.metric(
        "Flashcard sets",
        sum(x["type"] == "Flashcards" for x in history)
    )

    c3.metric(
        "Quizzes",
        sum(x["type"] == "Quiz" for x in history)
    )

    c4.metric(
        "Revision notes",
        sum(x["type"] == "Revision Notes" for x in history)
    )

    st.markdown("### Start creating")

    a, b, c, d = st.columns(4)

    if a.button(
        "Create Worksheet",
        use_container_width=True
    ):
        st.session_state.page = "Create Worksheet"
        st.rerun()

    if b.button(
        "Create Flashcards",
        use_container_width=True
    ):
        st.session_state.page = "Flashcards"
        st.rerun()

    if c.button(
        "Create Quiz",
        use_container_width=True
    ):
        st.session_state.page = "Quiz"
        st.rerun()

    if d.button(
        "Revision Notes",
        use_container_width=True
    ):
        st.session_state.page = "Revision Notes"
        st.rerun()

    if history:
        st.markdown("### Recent resources")

        for item in history[-8:][::-1]:
            st.markdown(
                f"**{item['name']}** — "
                f"{item['type']} · "
                f"{item.get('detail', '')}"
            )


# =========================================================
# CREATE WORKSHEET
# =========================================================

elif page == "Create Worksheet":

    st.subheader("1. Upload learning material")

    uploads = st.file_uploader(
        "Upload one or more lesson images",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True,
        help="Use clear photos with the full page visible.",
    )

    if uploads:

        st.session_state.uploaded_names = [
            x.name for x in uploads
        ]

        cols = st.columns(min(4, len(uploads)))

        image_bytes = []

        for i, file in enumerate(uploads):

            data, image = prepare_image(file)

            image_bytes.append(data)

            cols[i % len(cols)].image(
                image,
                caption=file.name,
                use_container_width=True,
            )

        st.markdown("### 2. Teacher settings")

        left, right = st.columns(2)

        with left:

            grade = st.selectbox(
                "Grade / Class",
                [
                    "Nursery",
                    "KG",
                    "Grade 1",
                    "Grade 2",
                    "Grade 3",
                    "Grade 4",
                    "Grade 5",
                    "Grade 6",
                    "Grade 7",
                    "Grade 8",
                    "Grade 9",
                    "Grade 10",
                    "Custom",
                ],
            )

            subject = st.selectbox(
                "Subject",
                [
                    "English",
                    "Mathematics",
                    "General Science",
                    "Biology",
                    "Chemistry",
                    "Physics",
                    "Computer Science",
                    "Pakistan Studies",
                    "Islamiat",
                    "Urdu",
                    "General Knowledge",
                    "Other",
                ],
            )

            difficulty = st.select_slider(
                "Difficulty",
                options=[
                    "Easy",
                    "Medium",
                    "Hard",
                    "Mixed",
                ],
                value="Medium",
            )

            language = st.selectbox(
                "Language",
                [
                    "English",
                    "Urdu",
                    "English + Urdu",
                ],
            )

        with right:

            cognitive = st.selectbox(
                "Thinking level",
                [
                    "Balanced",
                    "Remember",
                    "Understand",
                    "Apply",
                    "Analyze",
                ],
            )

            count = st.number_input(
                "Total questions",
                1,
                50,
                10,
            )

            time_limit = st.selectbox(
                "Estimated time",
                [
                    "No limit",
                    "10 minutes",
                    "15 minutes",
                    "20 minutes",
                    "30 minutes",
                    "45 minutes",
                    "60 minutes",
                ],
            )

            selected_topics = st.text_input(
                "Topics (optional)",
                placeholder="e.g. Photosynthesis, chlorophyll",
            )

        qtypes = st.multiselect(
            "Question types",
            [
                "MCQ",
                "Fill in the blanks",
                "True / False",
                "Short answer",
                "Matching",
                "Application",
            ],
            default=[
                "MCQ",
                "Short answer",
            ],
        )

        custom_instructions = st.text_area(
            "Additional teacher instructions (optional)",
            placeholder=(
                "Example: Keep vocabulary simple and "
                "include everyday examples."
            ),
        )

        # =====================================================
        # ANALYZE MATERIAL
        # =====================================================

        if st.button(
            "Analyze Material",
            type="primary",
            use_container_width=True,
        ):

            with st.spinner(
                "Reading and understanding the uploaded material..."
            ):

                try:

                    analysis = analyze_material(
                        image_bytes,
                        grade,
                        subject,
                    )

                    st.session_state.material_analysis = analysis

                    st.success("Material analyzed.")

                except Exception as e:

                    st.error(
                        f"Material analysis failed: {e}"
                    )

        # =====================================================
        # MATERIAL UNDERSTANDING
        # =====================================================

        if st.session_state.material_analysis:

            analysis = st.session_state.material_analysis

            st.markdown("### Material understanding")

            x, y = st.columns(2)

            with x:

                st.write(
                    "**Detected title:**",
                    analysis.get("title", "")
                )

                st.write(
                    "**Subject:**",
                    analysis.get("subject", "")
                )

                st.write(
                    "**Topics:**",
                    ", ".join(
                        analysis.get("topics", [])
                    )
                )

            with y:

                st.write(
                    "**Key concepts:**",
                    ", ".join(
                        analysis.get("key_concepts", [])
                    )
                )

                st.write(
                    "**Summary:**",
                    analysis.get("summary", "")
                )

            # =================================================
            # SETTINGS
            # =================================================

            settings = {
                "grade": grade,
                "subject": subject,
                "difficulty": difficulty,
                "language": language,
                "cognitive_level": cognitive,
                "count": int(count),
                "time_limit": time_limit,
                "topics": (
                    selected_topics
                    or ", ".join(
                        analysis.get("topics", [])
                    )
                ),
                "question_types": qtypes,
                "custom_instructions": custom_instructions,
            }

            # =================================================
            # GENERATE WORKSHEET
            # =================================================

            if st.button(
                "Generate Worksheet",
                type="primary",
                use_container_width=True,
            ):

                if not qtypes:

                    st.warning(
                        "Select at least one question type."
                    )

                else:

                    with st.spinner(
                        "Creating your worksheet..."
                    ):

                        try:

                            ws = generate_worksheet(
                                material_analysis=analysis,
                                grade=grade,
                                subject=subject,
                                difficulty=difficulty,
                                language=language,
                                cognitive_level=cognitive,
                                question_count=int(count),
                                question_types=qtypes,
                                topics=(
                                    selected_topics
                                    or ", ".join(
                                        analysis.get(
                                            "topics",
                                            []
                                        )
                                    )
                                ),
                                teacher_instructions=(
                                    custom_instructions
                                    or "Create a clear and age-appropriate worksheet."
                                ),
                            )

                            st.session_state.worksheet = ws

                            st.session_state.answer_key = ws

                            st.session_state.quality_check = (
                                quality_check(
                                    ws,
                                    analysis,
                                    settings,
                                )
                            )

                            st.session_state.resource_history.append(
                                {
                                    "type": "Worksheet",
                                    "name": ws.get(
                                        "title",
                                        "Worksheet"
                                    ),
                                    "detail": (
                                        f"{grade} · {subject} · "
                                        f"{language}"
                                    ),
                                }
                            )

                            st.success(
                                "Worksheet created. "
                                "Review it below."
                            )

                        except Exception as e:

                            st.error(
                                f"Worksheet generation failed: {e}"
                            )


    # =========================================================
    # TEACHER REVIEW
    # =========================================================

    if st.session_state.worksheet:

        ws = st.session_state.worksheet

        st.markdown("---")

        st.subheader("3. Teacher review")

        st.caption(
            "Edit, delete, or regenerate individual "
            "questions before downloading."
        )

        # Make sure these variables exist even after reruns.
        grade = locals().get("grade", "Selected grade")
        subject = locals().get("subject", "Selected subject")
        difficulty = locals().get(
            "difficulty",
            "Medium"
        )
        language = locals().get(
            "language",
            "English"
        )
        cognitive = locals().get(
            "cognitive",
            "Balanced"
        )
        count = locals().get(
            "count",
            len(ws.get("questions", []))
        )
        time_limit = locals().get(
            "time_limit",
            "No limit"
        )
        selected_topics = locals().get(
            "selected_topics",
            ""
        )
        qtypes = locals().get(
            "qtypes",
            ["MCQ"]
        )
        custom_instructions = locals().get(
            "custom_instructions",
            ""
        )

        for idx, q in enumerate(
            ws.get("questions", [])
        ):

            with st.expander(
                f"Question {idx + 1} · "
                f"{q.get('type', '').replace('_', ' ').title()}",
                expanded=False,
            ):

                new_q = st.text_area(
                    "Question",
                    q.get("question", ""),
                    key=f"qtext_{idx}",
                )

                q_type = str(
                    q.get("type", "")
                ).lower()

                if q_type in [
                    "mcq",
                    "multiple_choice",
                    "multiple choice",
                ]:

                    options = []

                    for j, opt in enumerate(
                        q.get("options", [])[:4]
                    ):

                        options.append(
                            st.text_input(
                                f"Option {chr(65 + j)}",
                                opt,
                                key=f"opt_{idx}_{j}",
                            )
                        )

                    q["options"] = options

                q["question"] = new_q

                q["answer"] = st.text_input(
                    "Answer",
                    q.get("answer", ""),
                    key=f"ans_{idx}",
                )

                q["marks"] = st.number_input(
                    "Marks",
                    1,
                    20,
                    int(q.get("marks", 1)),
                    key=f"marks_{idx}",
                )

                c1, c2 = st.columns(2)

                # =================================================
                # REGENERATE QUESTION
                # =================================================

                if c1.button(
                    "Regenerate this question",
                    key=f"regen_{idx}",
                ):

                    try:

                        with st.spinner(
                            "Regenerating..."
                        ):

                            replacement = regenerate_question(
                                material_analysis=(
                                    st.session_state.material_analysis
                                ),
                                original_question=q,
                                grade=grade,
                                subject=subject,
                                difficulty=difficulty,
                                language=language,
                                cognitive_level=cognitive,
                                question_type=q.get(
                                    "type",
                                    "MCQ"
                                ),
                                teacher_instructions=(
                                    custom_instructions
                                    or ""
                                ),
                            )

                            if replacement:

                                replacement["number"] = (
                                    idx + 1
                                )

                                ws["questions"][idx] = (
                                    replacement
                                )

                                st.rerun()

                    except Exception as e:

                        st.error(
                            f"Regeneration failed: {e}"
                        )

                # =================================================
                # DELETE QUESTION
                # =================================================

                if c2.button(
                    "Delete question",
                    key=f"delete_{idx}",
                ):

                    ws["questions"].pop(idx)

                    for n, item in enumerate(
                        ws["questions"],
                        1
                    ):

                        item["number"] = n
                        item["id"] = n

                    st.rerun()

        # =====================================================
        # ADD MANUAL QUESTION
        # =====================================================

        if st.button("Add manual question"):

            ws["questions"].append(
                {
                    "id": len(
                        ws["questions"]
                    ) + 1,
                    "number": len(
                        ws["questions"]
                    ) + 1,
                    "type": "short_answer",
                    "question": (
                        "Write your question here."
                    ),
                    "options": [],
                    "answer": "",
                    "explanation": "",
                    "marks": 1,
                }
            )

            st.rerun()

        # =====================================================
        # QUALITY CHECK
        # =====================================================

        qc = st.session_state.get(
            "quality_check"
        )

        if qc:

            st.markdown("### Quality check")

            checks = [
                (
                    "Source supported",
                    qc.get(
                        "source_supported",
                        False
                    ),
                ),
                (
                    "No duplicates",
                    qc.get(
                        "no_duplicates",
                        False
                    ),
                ),
                (
                    "Grade appropriate",
                    qc.get(
                        "grade_appropriate",
                        False
                    ),
                ),
                (
                    "Difficulty aligned",
                    qc.get(
                        "difficulty_aligned",
                        False
                    ),
                ),
                (
                    "Answers present",
                    qc.get(
                        "answers_present",
                        False
                    ),
                ),
            ]

            st.write(
                " · ".join(
                    (
                        "✓ " if ok else "⚠ "
                    ) + name
                    for name, ok in checks
                )
            )

            if qc.get("issues"):

                st.warning(
                    "Review: "
                    + " | ".join(
                        qc["issues"]
                    )
                )

        # =====================================================
        # DOWNLOAD
        # =====================================================

        st.markdown("### 4. Download")

        meta = {
            "grade": grade,
            "subject": subject,
            "difficulty": difficulty,
            "language": language,
            "time_limit": time_limit,
        }

        try:

            wp = build_worksheet_pdf(
                ws,
                meta
            )

            kp = build_answer_key_pdf(
                ws,
                meta
            )

            with open(wp, "rb") as f:

                worksheet_pdf = f.read()

            with open(kp, "rb") as f:

                answer_pdf = f.read()

            c1, c2 = st.columns(2)

            c1.download_button(
                "Download Worksheet PDF",
                worksheet_pdf,
                "sunbeams_worksheet.pdf",
                "application/pdf",
                type="primary",
                use_container_width=True,
            )

            c2.download_button(
                "Download Answer Key PDF",
                answer_pdf,
                "sunbeams_answer_key.pdf",
                "application/pdf",
                use_container_width=True,
            )

        except Exception as e:

            st.error(
                f"PDF generation failed: {e}"
            )


# =========================================================
# FLASHCARDS
# =========================================================

elif page == "Flashcards":

    st.subheader("Flashcards")

    if not st.session_state.material_analysis:

        st.info(
            "Analyze learning material first "
            "from Create Worksheet."
        )

    else:

        count = st.slider(
            "Number of cards",
            5,
            30,
            10,
        )

        grade = st.selectbox(
            "Grade",
            [
                "Grade 1",
                "Grade 2",
                "Grade 3",
                "Grade 4",
                "Grade 5",
                "Grade 6",
                "Grade 7",
                "Grade 8",
                "Grade 9",
                "Grade 10",
            ],
            key="fc_grade",
        )

        language = st.selectbox(
            "Language",
            [
                "English",
                "Urdu",
                "English + Urdu",
            ],
            key="fc_lang",
        )

        if st.button(
            "Create Flashcards",
            type="primary",
        ):

            with st.spinner(
                "Creating flashcards..."
            ):

                try:

                    cards = generate_flashcards(
                        {
                            "count": count,
                            "grade": grade,
                            "language": language,
                        },
                        st.session_state.material_analysis,
                    )

                    st.session_state.flashcards = cards

                    st.session_state.resource_history.append(
                        {
                            "type": "Flashcards",
                            "name": cards.get(
                                "title",
                                "Flashcards"
                            ),
                            "detail": f"{count} cards",
                        }
                    )

                except Exception as e:

                    st.error(
                        f"Flashcard generation failed: {e}"
                    )

        if st.session_state.flashcards:

            cards = st.session_state.flashcards.get(
                "cards",
                []
            )

            for i, card in enumerate(cards):

                with st.expander(
                    f"Card {i + 1}: "
                    f"{card.get('front', '')}"
                ):

                    st.write(
                        card.get("back", "")
                    )


# =========================================================
# QUIZ
# =========================================================

elif page == "Quiz":

    st.subheader("Interactive Quiz")

    if not st.session_state.material_analysis:

        st.info(
            "Analyze learning material first "
            "from Create Worksheet."
        )

    else:

        count = st.slider(
            "Number of questions",
            5,
            20,
            10,
            key="quiz_count",
        )

        if st.button(
            "Generate Quiz",
            type="primary",
        ):

            with st.spinner(
                "Creating quiz..."
            ):

                try:

                    st.session_state.quiz = generate_quiz(
                        {
                            "count": count,
                            "grade": "Selected grade",
                            "difficulty": "Medium",
                        },
                        st.session_state.material_analysis,
                    )

                    st.session_state.quiz_answers = {}

                except Exception as e:

                    st.error(
                        f"Quiz generation failed: {e}"
                    )

        if st.session_state.quiz:

            quiz = st.session_state.quiz

            st.write(
                f"**{quiz.get('title', 'Quiz')}**"
            )

            for i, q in enumerate(
                quiz.get("questions", [])
            ):

                answer = st.radio(
                    q.get("question", ""),
                    q.get("options", []),
                    key=f"quiz_{i}",
                    index=None,
                )

                st.session_state.quiz_answers[i] = answer

            if st.button(
                "Submit Quiz",
                type="primary",
            ):

                score = 0

                total = len(
                    quiz.get("questions", [])
                )

                for i, q in enumerate(
                    quiz.get("questions", [])
                ):

                    opts = q.get(
                        "options",
                        []
                    )

                    chosen = (
                        st.session_state.quiz_answers
                        .get(i)
                    )

                    if (
                        chosen
                        and opts
                        and chosen
                        == opts[
                            int(
                                q.get(
                                    "answer_index",
                                    0
                                )
                            )
                        ]
                    ):

                        score += 1

                st.success(
                    f"Score: {score} / {total}"
                )


# =========================================================
# REVISION NOTES
# =========================================================

elif page == "Revision Notes":

    st.subheader("Revision Notes")

    if not st.session_state.material_analysis:

        st.info(
            "Analyze learning material first "
            "from Create Worksheet."
        )

    else:

        if st.button(
            "Create Revision Notes",
            type="primary",
        ):

            with st.spinner(
                "Creating revision notes..."
            ):

                try:

                    st.session_state.revision_notes = (
                        generate_revision_notes(
                            {
                                "grade": "Selected grade",
                                "language": "English",
                            },
                            st.session_state.material_analysis,
                        )
                    )

                    st.session_state.resource_history.append(
                        {
                            "type": "Revision Notes",
                            "name": (
                                st.session_state
                                .revision_notes
                                .get(
                                    "title",
                                    "Revision Notes"
                                )
                            ),
                            "detail": "Study summary",
                        }
                    )

                except Exception as e:

                    st.error(
                        f"Revision note generation failed: {e}"
                    )

        notes = st.session_state.revision_notes

        if notes:

            st.markdown(
                f"## {notes.get('title', 'Revision Notes')}"
            )

            st.write(
                notes.get(
                    "summary",
                    ""
                )
            )

            st.markdown("### Key Concepts")

            for x in notes.get(
                "key_concepts",
                []
            ):

                st.write(
                    "• " + x
                )

            st.markdown("### Vocabulary")

            for item in notes.get(
                "vocabulary",
                []
            ):

                st.write(
                    f"**{item.get('term', '')}** — "
                    f"{item.get('meaning', '')}"
                )

            st.markdown("### Quick Review")

            for x in notes.get(
                "quick_questions",
                []
            ):

                st.write(
                    "• " + x
                )
