
import streamlit as st
import random
import re

st.set_page_config(
    page_title="Atomic Structure Chemistry Tutor",
    page_icon="⚛️",
    layout="wide"
)

st.title("⚛️ Atomic Structure Chemistry Tutor")
st.caption("A portfolio project demonstrating Chemistry knowledge, assessment design, scientific reasoning, and educational software development.")

# ---------- Data ----------
TOPICS = {
    "Subatomic particles": [
        ("What is the charge of a proton?", "positive"),
        ("What is the charge of a neutron?", "neutral"),
        ("What is the charge of an electron?", "negative"),
    ],
    "Atomic number & mass number": [
        ("What does atomic number represent?", "number of protons"),
        ("What does mass number represent?", "protons + neutrons"),
    ],
    "Isotopes": [
        ("What are isotopes?", "atoms of the same element with the same number of protons but different numbers of neutrons"),
    ],
    "Ions": [
        ("What happens when an atom loses electrons?", "it forms a positive ion"),
        ("What happens when an atom gains electrons?", "it forms a negative ion"),
    ],
}

QUIZ = [
    {
        "q": "An atom has 11 protons and 12 neutrons. What is its mass number?",
        "options": ["11", "12", "23", "24"],
        "answer": "23",
        "explanation": "Mass number = number of protons + number of neutrons = 11 + 12 = 23."
    },
    {
        "q": "An atom has 17 protons and 17 electrons. What is its net charge?",
        "options": ["+1", "0", "-1", "+17"],
        "answer": "0",
        "explanation": "Equal numbers of positive protons and negative electrons cancel, giving a neutral atom."
    },
    {
        "q": "Which particle determines the identity of an element?",
        "options": ["Electron", "Neutron", "Proton", "Nucleus"],
        "answer": "Proton",
        "explanation": "The atomic number is the number of protons, and atomic number identifies the element."
    },
    {
        "q": "Two atoms have the same number of protons but different numbers of neutrons. They are:",
        "options": ["Ions", "Isotopes", "Molecules", "Cations"],
        "answer": "Isotopes",
        "explanation": "Isotopes are atoms of the same element with the same proton number but different neutron numbers."
    },
    {
        "q": "An atom has 8 protons and 10 electrons. What is its charge?",
        "options": ["+2", "-2", "0", "+18"],
        "answer": "-2",
        "explanation": "Charge = protons - electrons = 8 - 10 = -2."
    },
    {
        "q": "If an atom loses two electrons, it becomes:",
        "options": ["A 2− ion", "A 2+ ion", "A neutral atom", "An isotope"],
        "answer": "A 2+ ion",
        "explanation": "Removing two negatively charged electrons leaves two more positive charges than negative charges."
    },
]

# ---------- Session state ----------
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = QUIZ.copy()
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False

# ---------- Sidebar ----------
st.sidebar.header("Project Modules")
module = st.sidebar.radio(
    "Choose a module",
    ["Learn", "Atom Builder", "Practice Quiz", "Answer Evaluator", "About Project"]
)

# ---------- Learn ----------
if module == "Learn":
    st.header("Learn Atomic Structure")
    st.write("Use the sections below as a compact revision guide.")

    with st.expander("1. Subatomic particles", expanded=True):
        st.markdown("""
        | Particle | Charge | Relative location |
        |---|---:|---|
        | Proton | +1 | Nucleus |
        | Neutron | 0 | Nucleus |
        | Electron | −1 | Outside the nucleus |
        """)
        st.info("The number of protons determines the identity of an element.")

    with st.expander("2. Atomic number and mass number"):
        st.markdown("""
        **Atomic number (Z)** = number of protons.

        **Mass number (A)** = number of protons + number of neutrons.

        Therefore:

        **Neutrons = mass number − atomic number**
        """)

    with st.expander("3. Isotopes"):
        st.write(
            "Isotopes are atoms of the same element with the same number of protons "
            "but different numbers of neutrons."
        )

    with st.expander("4. Ions"):
        st.write(
            "A positive ion (cation) forms when an atom loses electrons. "
            "A negative ion (anion) forms when an atom gains electrons."
        )

    st.success("Tip: When solving an atomic-structure problem, identify protons first, then neutrons, then electrons and charge.")

# ---------- Atom Builder ----------
elif module == "Atom Builder":
    st.header("Interactive Atom Builder")
    st.write("Change the particle counts and observe the resulting atomic properties.")

    c1, c2, c3 = st.columns(3)
    with c1:
        protons = st.number_input("Protons", min_value=0, max_value=118, value=6, step=1)
    with c2:
        neutrons = st.number_input("Neutrons", min_value=0, max_value=200, value=6, step=1)
    with c3:
        electrons = st.number_input("Electrons", min_value=0, max_value=118, value=6, step=1)

    mass_number = protons + neutrons
    charge = protons - electrons

    st.subheader("Result")
    r1, r2, r3 = st.columns(3)
    r1.metric("Atomic number", protons)
    r2.metric("Mass number", mass_number)
    r3.metric("Net charge", f"{charge:+d}")

    if protons == 0:
        st.warning("No element identity can be assigned when there are zero protons.")
    elif charge == 0:
        st.success("This particle combination represents a neutral atom.")
    elif charge > 0:
        st.info(f"This is a positive ion (cation) with charge +{charge}.")
    else:
        st.info(f"This is a negative ion (anion) with charge {charge}.")

    st.markdown("### Reasoning")
    st.write(f"Mass number = protons + neutrons = {protons} + {neutrons} = {mass_number}.")
    st.write(f"Net charge = protons − electrons = {protons} − {electrons} = {charge:+d}.")

# ---------- Quiz ----------
elif module == "Practice Quiz":
    st.header("Atomic Structure Practice Quiz")
    st.write("Answer each question and receive immediate feedback.")

    q = st.session_state.quiz_questions[st.session_state.quiz_index]
    st.subheader(f"Question {st.session_state.quiz_index + 1} of {len(st.session_state.quiz_questions)}")
    choice = st.radio(q["q"], q["options"], key=f"choice_{st.session_state.quiz_index}")

    if not st.session_state.answered:
        if st.button("Check Answer", type="primary"):
            st.session_state.answered = True
            if choice == q["answer"]:
                st.session_state.score += 1
                st.success("Correct!")
            else:
                st.error(f"Not quite. Correct answer: {q['answer']}")
            st.info(q["explanation"])
            st.rerun()
    else:
        # Show feedback after rerun
        if choice == q["answer"]:
            st.success(f"Correct! {q['explanation']}")
        else:
            st.error(f"Correct answer: {q['answer']}. {q['explanation']}")

        if st.session_state.quiz_index < len(st.session_state.quiz_questions) - 1:
            if st.button("Next Question"):
                st.session_state.quiz_index += 1
                st.session_state.answered = False
                st.rerun()
        else:
            percentage = round(st.session_state.score / len(st.session_state.quiz_questions) * 100)
            st.success(f"Quiz complete. Score: {st.session_state.score}/{len(st.session_state.quiz_questions)} ({percentage}%).")
            if st.button("Restart Quiz"):
                st.session_state.quiz_index = 0
                st.session_state.score = 0
                st.session_state.answered = False
                random.shuffle(st.session_state.quiz_questions)
                st.rerun()

# ---------- Answer Evaluator ----------
elif module == "Answer Evaluator":
    st.header("Scientific Answer Evaluator")
    st.write("Paste a student's short answer. The evaluator checks for key scientific ideas and gives structured feedback.")

    prompts = [
        "What is atomic number?",
        "What is mass number?",
        "What are isotopes?",
        "What happens when an atom loses electrons?"
    ]
    prompt = st.selectbox("Question", prompts)
    answer = st.text_area("Student answer", height=140, placeholder="Type the student's answer here...")

    rubrics = {
        "What is atomic number?": {
            "keywords": ["proton"],
            "good": "The answer should identify atomic number as the number of protons in the nucleus.",
            "missing": "Mention that atomic number is the number of protons."
        },
        "What is mass number?": {
            "keywords": ["proton", "neutron"],
            "good": "The answer should connect mass number with protons and neutrons.",
            "missing": "Mention both protons and neutrons."
        },
        "What are isotopes?": {
            "keywords": ["same element", "same number of proton", "different", "neutron"],
            "good": "A complete answer should state that isotopes are atoms of the same element with different numbers of neutrons.",
            "missing": "Mention the same element/proton number and different neutron number."
        },
        "What happens when an atom loses electrons?": {
            "keywords": ["positive", "cation"],
            "good": "The answer should state that losing electrons produces a positive ion/cation.",
            "missing": "State that loss of electrons produces a positive ion or cation."
        },
    }

    if st.button("Evaluate Answer", type="primary"):
        if not answer.strip():
            st.warning("Please enter an answer first.")
        else:
            text = answer.lower()
            rubric = rubrics[prompt]
            matches = sum(1 for k in rubric["keywords"] if k in text)

            if matches == len(rubric["keywords"]):
                st.success("Strong answer")
                st.write(rubric["good"])
            elif matches >= max(1, len(rubric["keywords"]) // 2):
                st.warning("Partially correct / incomplete")
                st.write(rubric["missing"])
            else:
                st.error("Needs improvement")
                st.write(rubric["missing"])

            st.write(f"Evidence terms detected: {matches}/{len(rubric['keywords'])}")

# ---------- About ----------
else:
    st.header("About This Portfolio Project")
    st.markdown("""
    **Project:** Atomic Structure Chemistry Tutor & Assessment System

    **Purpose:** Demonstrate practical Chemistry subject-matter knowledge together with
    educational technology, assessment design, scientific reasoning, and basic software development.

    **Built with:** Python and Streamlit.

    **Core features:**
    - Atomic structure learning guide
    - Interactive proton/neutron/electron builder
    - Automated multiple-choice assessment
    - Immediate explanations and scoring
    - Structured short-answer evaluation using a transparent rubric

    **Portfolio evidence:** The repository includes the source code, requirements file,
    documentation, and sample assessment content.
    """)

    st.subheader("Suggested portfolio description")
    st.code(
        "I built a Python/Streamlit Atomic Structure Chemistry Tutor and Assessment System "
        "that combines interactive atom modeling, automated quizzes, scientific explanations, "
        "and rubric-based evaluation of student responses. The project demonstrates my ability "
        "to translate Chemistry concepts into structured digital learning and assessment tools.",
        language="text"
    )

st.divider()
st.caption("Portfolio project by Michael Ndibe Chekwube • Chemistry Education / Scientific Content")
