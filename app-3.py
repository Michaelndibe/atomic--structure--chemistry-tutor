import streamlit as st
import random
import re

st.set_page_config(
    page_title="Atomic Structure Chemistry Tutor",
    page_icon="⚛️",
    layout="wide"
)

# =========================
# DATA
# =========================

ELEMENTS = {
    1: ("Hydrogen", "H"), 2: ("Helium", "He"), 3: ("Lithium", "Li"),
    4: ("Beryllium", "Be"), 5: ("Boron", "B"), 6: ("Carbon", "C"),
    7: ("Nitrogen", "N"), 8: ("Oxygen", "O"), 9: ("Fluorine", "F"),
    10: ("Neon", "Ne"), 11: ("Sodium", "Na"), 12: ("Magnesium", "Mg"),
    13: ("Aluminium", "Al"), 14: ("Silicon", "Si"), 15: ("Phosphorus", "P"),
    16: ("Sulfur", "S"), 17: ("Chlorine", "Cl"), 18: ("Argon", "Ar"),
    19: ("Potassium", "K"), 20: ("Calcium", "Ca")
}

QUIZ = [
    {"q":"What is the charge of a proton?","options":["+1","0","-1","+2"],"answer":"+1","explanation":"A proton carries one positive charge."},
    {"q":"What is the charge of a neutron?","options":["+1","0","-1","+2"],"answer":"0","explanation":"A neutron has no electrical charge."},
    {"q":"What is the charge of an electron?","options":["+1","0","-1","+2"],"answer":"-1","explanation":"An electron carries one negative charge."},
    {"q":"Where are protons found in an atom?","options":["Nucleus","Electron shell","Outside the atom","Orbit only"],"answer":"Nucleus","explanation":"Protons are located in the nucleus."},
    {"q":"Where are neutrons found?","options":["Nucleus","Electron shell","Outside the atom","Valence shell only"],"answer":"Nucleus","explanation":"Neutrons are located in the nucleus together with protons."},
    {"q":"Where are electrons mainly found?","options":["Nucleus","Outside the nucleus","Inside neutrons","Inside protons"],"answer":"Outside the nucleus","explanation":"Electrons occupy regions outside the nucleus called electron shells or energy levels."},
    {"q":"Which subatomic particle determines the identity of an element?","options":["Electron","Neutron","Proton","Nucleus"],"answer":"Proton","explanation":"The number of protons is the atomic number and identifies the element."},
    {"q":"What is atomic number?","options":["Number of neutrons","Number of protons","Protons + neutrons","Number of electrons + neutrons"],"answer":"Number of protons","explanation":"Atomic number is defined as the number of protons in the nucleus."},
    {"q":"What is mass number?","options":["Protons + neutrons","Protons + electrons","Neutrons + electrons","Electrons only"],"answer":"Protons + neutrons","explanation":"Mass number is the total number of protons and neutrons in the nucleus."},
    {"q":"An atom has 11 protons and 12 neutrons. What is its mass number?","options":["11","12","23","24"],"answer":"23","explanation":"Mass number = protons + neutrons = 11 + 12 = 23."},
    {"q":"An atom has atomic number 8. How many protons does it have?","options":["6","8","10","16"],"answer":"8","explanation":"Atomic number equals the number of protons."},
    {"q":"An atom has 17 protons and 18 neutrons. What is its mass number?","options":["17","18","35","36"],"answer":"35","explanation":"Mass number = 17 + 18 = 35."},
    {"q":"How many neutrons are in an atom with mass number 23 and atomic number 11?","options":["11","12","23","34"],"answer":"12","explanation":"Neutrons = mass number − atomic number = 23 − 11 = 12."},
    {"q":"Two atoms have the same number of protons but different numbers of neutrons. They are:","options":["Ions","Isotopes","Molecules","Cations"],"answer":"Isotopes","explanation":"Isotopes are atoms of the same element with the same proton number but different neutron numbers."},
    {"q":"Which particles are responsible for most of the mass of an atom?","options":["Protons and neutrons","Electrons only","Protons and electrons","Neutrons and electrons"],"answer":"Protons and neutrons","explanation":"Protons and neutrons are much more massive than electrons and make up nearly all atomic mass."},
    {"q":"Which statement about a neutral atom is correct?","options":["More protons than electrons","More electrons than protons","Equal protons and electrons","No neutrons"],"answer":"Equal protons and electrons","explanation":"A neutral atom has equal positive proton charge and negative electron charge."},
    {"q":"An atom has 8 protons and 10 electrons. What is its charge?","options":["+2","-2","0","+18"],"answer":"-2","explanation":"Net charge = protons − electrons = 8 − 10 = −2."},
    {"q":"If an atom loses two electrons, it becomes:","options":["A 2− ion","A 2+ ion","A neutral atom","An isotope"],"answer":"A 2+ ion","explanation":"Losing two negatively charged electrons leaves a net charge of +2."},
    {"q":"If an atom gains one electron, its charge becomes:","options":["+1","0","-1","+2"],"answer":"-1","explanation":"Gaining one negative electron gives the atom a net charge of −1 if it was initially neutral."},
    {"q":"A positive ion is called a:","options":["Anion","Cation","Isotope","Neutron"],"answer":"Cation","explanation":"A cation is a positively charged ion, usually formed by loss of electrons."},
    {"q":"A negative ion is called an:","options":["Cation","Proton","Anion","Isotope"],"answer":"Anion","explanation":"An anion is a negatively charged ion, usually formed by gaining electrons."},
    {"q":"An atom contains 13 protons and 14 neutrons. Which element is it?","options":["Carbon","Aluminium","Silicon","Magnesium"],"answer":"Aluminium","explanation":"Atomic number 13 corresponds to aluminium."},
    {"q":"What happens to atomic number when an atom gains an electron?","options":["Increases by 1","Decreases by 1","Remains unchanged","Becomes the mass number"],"answer":"Remains unchanged","explanation":"Atomic number depends on protons, not electrons. Gaining an electron changes charge only."},
    {"q":"What happens to mass number when an atom gains an electron?","options":["Increases by 1","Decreases by 1","Remains essentially unchanged","Becomes zero"],"answer":"Remains essentially unchanged","explanation":"Mass number counts protons and neutrons. Electrons are not included in the mass number."},
    {"q":"Which formula gives the number of neutrons?","options":["Atomic number + mass number","Mass number − atomic number","Protons + electrons","Electrons − protons"],"answer":"Mass number − atomic number","explanation":"Since mass number = protons + neutrons and atomic number = protons, neutrons = mass number − atomic number."}
]

RUBRICS = {
    "Explain atomic number.": {
        "criteria": [
            ("States that atomic number is the number of protons.", ["atomic number", "number of protons", "number of proton"], 2),
            ("Identifies the protons as being in the nucleus.", ["nucleus", "nuclear"], 1),
            ("Explains that proton number identifies the element.", ["identifies the element", "identify the element", "identity of the element", "element identity"], 1),
        ],
        "model": "Atomic number is the number of protons in the nucleus of an atom. It identifies the element."
    },
    "Explain mass number.": {
        "criteria": [
            ("Mentions protons.", ["proton", "protons"], 1),
            ("Mentions neutrons.", ["neutron", "neutrons"], 1),
            ("States that mass number is the total of protons and neutrons.", ["protons and neutrons", "proton and neutron", "protons plus neutrons", "proton plus neutron"], 2),
        ],
        "model": "Mass number is the total number of protons and neutrons in the nucleus."
    },
    "Explain isotopes.": {
        "criteria": [
            ("States that isotopes are atoms of the same element.", ["same element"], 1),
            ("States that they have the same number of protons.", ["same number of protons", "same number of proton", "same proton"], 1),
            ("States that they have different numbers of neutrons.", ["different number of neutrons", "different numbers of neutrons", "different neutron"], 2),
        ],
        "model": "Isotopes are atoms of the same element with the same number of protons but different numbers of neutrons."
    },
    "Explain what happens when an atom loses electrons.": {
        "criteria": [
            ("States that electrons are lost or removed.", ["lose electrons", "loses electrons", "lost electrons", "remove electrons", "removes electrons", "removed electrons"], 1),
            ("States that the particle becomes positively charged.", ["positive", "positively charged", "positive charge", "plus charge"], 2),
            ("Uses the term cation.", ["cation"], 1),
        ],
        "model": "When an atom loses electrons, it forms a positive ion called a cation."
    },
    "Explain what happens when an atom gains electrons.": {
        "criteria": [
            ("States that electrons are gained or added.", ["gain electrons", "gains electrons", "gained electrons", "add electrons", "adds electrons", "added electrons"], 1),
            ("States that the particle becomes negatively charged.", ["negative", "negatively charged", "negative charge", "minus charge"], 2),
            ("Uses the term anion.", ["anion"], 1),
        ],
        "model": "When an atom gains electrons, it forms a negative ion called an anion."
    }
}

# =========================
# SESSION STATE
# =========================

if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = QUIZ.copy()

if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

if "quiz_answered" not in st.session_state:
    st.session_state.quiz_answered = False

if "quiz_last_answer" not in st.session_state:
    st.session_state.quiz_last_answer = None

if "assessment_result" not in st.session_state:
    st.session_state.assessment_result = None

if "assessment_history" not in st.session_state:
    st.session_state.assessment_history = []

# =========================
# FUNCTIONS
# =========================

def restart_quiz():
    questions = QUIZ.copy()
    random.shuffle(questions)
    st.session_state.quiz_questions = questions
    st.session_state.quiz_index = 0
    st.session_state.quiz_score = 0
    st.session_state.quiz_answered = False
    st.session_state.quiz_last_answer = None


def evaluate_response(prompt, response):
    rubric = RUBRICS[prompt]
    text = re.sub(r"\s+", " ", response.lower()).strip()

    earned = 0
    results = []

    for criterion, keywords, points in rubric["criteria"]:
        matched = any(keyword in text for keyword in keywords)
        if matched:
            earned += points
        results.append({
            "criterion": criterion,
            "matched": matched,
            "points": points
        })

    max_score = sum(item[2] for item in rubric["criteria"])
    percentage = round((earned / max_score) * 100)

    if percentage >= 80:
        level = "Strong"
        feedback = "The response covers most or all of the key scientific ideas in the rubric."
    elif percentage >= 50:
        level = "Developing"
        feedback = "The response contains some correct scientific ideas but needs additional detail or precision."
    else:
        level = "Needs Improvement"
        feedback = "The response is missing important scientific ideas identified by the rubric."

    return {
        "earned": earned,
        "max_score": max_score,
        "percentage": percentage,
        "level": level,
        "feedback": feedback,
        "criteria": results,
        "model": rubric["model"]
    }

# =========================
# HEADER
# =========================

st.title("⚛️ Atomic Structure Chemistry Tutor")
st.write(
    "An interactive Chemistry learning and assessment system demonstrating "
    "subject knowledge, educational technology, quiz design, scoring, feedback, "
    "and rubric-based assessment."
)

# =========================
# NAVIGATION
# =========================

module = st.sidebar.radio(
    "Project Modules",
    [
        "Home",
        "Learn",
        "Atom Builder",
        "Quiz & Scoring",
        "Short-Answer Assessment",
        "Assessment Rubric",
        "Portfolio Evidence"
    ]
)

# =========================
# HOME
# =========================

if module == "Home":
    st.header("Welcome")

    st.info(
        "This application demonstrates a complete Chemistry learning-and-assessment workflow: "
        "learn a concept, practise it, receive a score and feedback, and evaluate written responses "
        "against an explicit rubric."
    )

    st.subheader("What can you demonstrate?")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Quiz Questions", "25")
        st.caption("Multiple-choice assessment with scoring and explanations.")

    with c2:
        st.metric("Assessment Rubrics", "5")
        st.caption("Short-answer questions with criterion-level scoring.")

    with c3:
        st.metric("Interactive Modules", "7")
        st.caption("Learning, modelling, testing and portfolio evidence.")

    st.subheader("Assessment workflow")
    st.markdown("""
    **1. Learn → 2. Build an atom → 3. Take the quiz → 4. Review score and feedback →  
    5. Complete a short-answer assessment → 6. Inspect the rubric and evidence.**
    """)

    st.success("Use the sidebar to open the Quiz & Scoring or Short-Answer Assessment modules.")

# =========================
# LEARN
# =========================

elif module == "Learn":
    st.header("📚 Learn Atomic Structure")

    with st.expander("1. Subatomic particles", expanded=True):
        st.markdown("""
        | Particle | Charge | Location |
        |---|---:|---|
        | Proton | +1 | Nucleus |
        | Neutron | 0 | Nucleus |
        | Electron | −1 | Outside the nucleus |
        """)
        st.info("The number of protons determines the identity of an element.")

    with st.expander("2. Atomic number and mass number"):
        st.write("Atomic number = number of protons.")
        st.write("Mass number = number of protons + number of neutrons.")
        st.write("Number of neutrons = mass number − atomic number.")

    with st.expander("3. Isotopes"):
        st.write(
            "Isotopes are atoms of the same element with the same number of protons "
            "but different numbers of neutrons."
        )

    with st.expander("4. Ions"):
        st.write(
            "A cation is a positive ion formed when an atom loses electrons. "
            "An anion is a negative ion formed when an atom gains electrons."
        )

# =========================
# ATOM BUILDER
# =========================

elif module == "Atom Builder":
    st.header("⚛️ Interactive Atom Builder")
    st.write("Change the number of protons, neutrons and electrons.")

    col1, col2, col3 = st.columns(3)

    with col1:
        protons = st.number_input("Protons", min_value=0, max_value=118, value=6, step=1)

    with col2:
        neutrons = st.number_input("Neutrons", min_value=0, max_value=200, value=6, step=1)

    with col3:
        electrons = st.number_input("Electrons", min_value=0, max_value=118, value=6, step=1)

    atomic_number = protons
    mass_number = protons + neutrons
    charge = protons - electrons

    st.subheader("Calculated Properties")

    a, b, c, d = st.columns(4)
    a.metric("Atomic Number", atomic_number)
    b.metric("Mass Number", mass_number)
    c.metric("Net Charge", f"{charge:+d}")

    if protons in ELEMENTS:
        name, symbol = ELEMENTS[protons]
        d.metric("Element", f"{name} ({symbol})")
    else:
        d.metric("Element", "Outside demo range")

    st.divider()

    st.write("**Calculation:** Net charge = protons − electrons.")

    if charge == 0:
        st.success("The particle is neutral.")
    elif charge > 0:
        st.info(f"The particle is a positive ion (cation), charge +{charge}.")
    else:
        st.info(f"The particle is a negative ion (anion), charge {charge}.")

# =========================
# QUIZ
# =========================

elif module == "Quiz & Scoring":
    st.header("📝 Chemistry Quiz & Scoring")
    st.write(
        "Complete the 10-question atomic-structure quiz. Each question is scored "
        "automatically and includes scientific feedback."
    )

    if st.button("🔄 Restart Quiz"):
        restart_quiz()
        st.rerun()

    total = len(st.session_state.quiz_questions)
    index = st.session_state.quiz_index

    if index < total:
        st.progress(index / total)
        st.caption(
            f"Question {index + 1} of {total}  |  "
            f"Current score: {st.session_state.quiz_score}/{index}"
        )

        question = st.session_state.quiz_questions[index]

        selected = st.radio(
            question["q"],
            question["options"],
            key=f"quiz_answer_{index}"
        )

        if not st.session_state.quiz_answered:
            if st.button("Check Answer", type="primary"):
                st.session_state.quiz_last_answer = selected
                st.session_state.quiz_answered = True

                if selected == question["answer"]:
                    st.session_state.quiz_score += 1

                st.rerun()

        else:
            if st.session_state.quiz_last_answer == question["answer"]:
                st.success("Correct answer.")
            else:
                st.error(
                    f"Your answer: {st.session_state.quiz_last_answer}  |  "
                    f"Correct answer: {question['answer']}"
                )

            st.info(question["explanation"])

            if st.button("Next Question", type="primary"):
                st.session_state.quiz_index += 1
                st.session_state.quiz_answered = False
                st.session_state.quiz_last_answer = None
                st.rerun()

    else:
        score = st.session_state.quiz_score
        percentage = round((score / total) * 100)

        st.balloons()
        st.header("🎯 Quiz Complete")

        x, y, z = st.columns(3)
        x.metric("Score", f"{score}/{total}")
        y.metric("Percentage", f"{percentage}%")

        if percentage >= 80:
            level = "Strong performance"
            st.success("Strong performance. Review missed questions and continue practising.")
        elif percentage >= 50:
            level = "Developing performance"
            st.warning("Developing performance. Review the learning section and retry the quiz.")
        else:
            level = "Needs more practice"
            st.error("More practice is recommended. Review the learning section before retrying.")

        z.metric("Result", level)

        st.subheader("Assessment Feedback")
        st.write(
            f"You answered {score} out of {total} questions correctly. "
            f"Your final score is {percentage}%."
        )

        if st.button("Take Quiz Again", type="primary"):
            restart_quiz()
            st.rerun()

# =========================
# SHORT ANSWER ASSESSMENT
# =========================

elif module == "Short-Answer Assessment":
    st.header("✍️ Short-Answer Assessment")
    st.write(
        "Write a student's response below. The system evaluates the response "
        "against an explicit Chemistry rubric and gives criterion-level feedback."
    )

    prompt = st.selectbox(
        "Choose an assessment question",
        list(RUBRICS.keys())
    )

    response = st.text_area(
        "Student response",
        height=180,
        placeholder="Type the student's Chemistry answer here..."
    )

    if st.button("Evaluate Response", type="primary"):
        if not response.strip():
            st.warning("Please enter a response first.")
        else:
            result = evaluate_response(prompt, response)
            st.session_state.assessment_result = result
            st.session_state.assessment_history.append({
                "question": prompt,
                "score": result["earned"],
                "max_score": result["max_score"],
                "percentage": result["percentage"],
                "level": result["level"]
            })
            st.rerun()

    if st.session_state.assessment_result:
        result = st.session_state.assessment_result

        st.divider()
        st.subheader("Assessment Result")

        c1, c2, c3 = st.columns(3)
        c1.metric(
            "Rubric Score",
            f"{result['earned']}/{result['max_score']}"
        )
        c2.metric(
            "Percentage",
            f"{result['percentage']}%"
        )
        c3.metric(
            "Performance",
            result["level"]
        )

        if result["percentage"] >= 80:
            st.success(result["feedback"])
        elif result["percentage"] >= 50:
            st.warning(result["feedback"])
        else:
            st.error(result["feedback"])

        st.subheader("Criterion-Level Feedback")

        for item in result["criteria"]:
            if item["matched"]:
                st.success(
                    f"✓ {item['criterion']} — {item['points']} point(s) awarded."
                )
            else:
                st.error(
                    f"✗ {item['criterion']} — 0/{item['points']} point(s)."
                )

        with st.expander("Reference / Model Answer"):
            st.write(result["model"])

        st.caption(
            "Scoring method: transparent rule-based rubric using observable text evidence. "
            "It is presented as an educational assessment demonstration, not as a claim that "
            "automated keyword matching replaces professional teacher judgement."
        )

    if st.session_state.assessment_history:
        st.divider()
        st.subheader("Assessment History")

        for number, item in enumerate(
            reversed(st.session_state.assessment_history), start=1
        ):
            st.write(
                f"**Attempt {number}:** {item['score']}/{item['max_score']} "
                f"({item['percentage']}%) — {item['level']}"
            )

# =========================
# RUBRIC
# =========================

elif module == "Assessment Rubric":
    st.header("📊 Assessment Rubric")
    st.write(
        "This section provides visible evidence of assessment design, scoring criteria "
        "and feedback logic."
    )

    for question, rubric in RUBRICS.items():
        st.subheader(question)

        for criterion, keywords, points in rubric["criteria"]:
            st.markdown(
                f"- **{points} point(s):** {criterion}"
            )

        st.caption("Reference answer: " + rubric["model"])
        st.divider()

    st.subheader("Rubric Design Principles")
    st.markdown("""
    - Clear and observable criteria
    - Explicit point allocation
    - Criterion-level feedback
    - Reference/model answer
    - Percentage conversion
    - Performance-level interpretation
    - Transparent scoring logic
    """)

# =========================
# PORTFOLIO EVIDENCE
# =========================

else:
    st.header("📁 Portfolio Evidence")

    st.subheader("Project")
    st.write("Atomic Structure Chemistry Tutor & Assessment System")

    st.subheader("Purpose")
    st.write(
        "A Python/Streamlit educational application designed to demonstrate Chemistry "
        "subject-matter knowledge, interactive learning, assessment design, scientific "
        "reasoning and software development."
    )

    st.subheader("Full Program Features")
    st.markdown("""
    **Learning**
    - Atomic structure revision content
    - Subatomic particles
    - Atomic number and mass number
    - Isotopes
    - Ions

    **Interactive modelling**
    - Proton, neutron and electron inputs
    - Atomic number calculation
    - Mass number calculation
    - Net charge calculation
    - Element identification

    **Assessment**
    - 10-question multiple-choice quiz
    - Automatic scoring
    - Immediate scientific explanations
    - Final percentage score
    - Performance feedback

    **Constructed-response assessment**
    - 5 Chemistry short-answer prompts
    - Explicit scoring rubrics
    - Criterion-level feedback
    - Reference/model answers
    - Assessment history
    """)

    st.subheader("Portfolio Summary")
    st.code(
        "I built a Python/Streamlit Atomic Structure Chemistry Tutor and Assessment System "
        "that combines interactive atom modelling, multiple-choice assessment, automated scoring, "
        "scientific explanations, and rubric-based evaluation of student responses. The project "
        "demonstrates my ability to translate Chemistry concepts into structured digital learning "
        "and assessment tools.",
        language="text"
    )

    st.success(
        "This application provides visible evidence of both instructional design "
        "and assessment/rubric design."
    )

# =========================
# FOOTER
# =========================

st.divider()
st.caption(
    "Atomic Structure Chemistry Tutor & Assessment System • "
    "Chemistry Education Portfolio"
)
