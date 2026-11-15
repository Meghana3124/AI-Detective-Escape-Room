
import streamlit as st
from google import genai
from google.colab import userdata
import json

st.set_page_config(page_title="AI Detective", page_icon="🕵️", layout="wide")

@st.cache_resource
def get_client():
    return genai.Client(api_key=userdata.get("GEMINI_API_KEY"))

client = get_client()

st.title("🕵️ AI DETECTIVE: THE MYSTERY SOLVER")
st.subheader("Version 2 — Gemini AI Powered Escape Room")
st.write("Investigate clues, identify the criminal and unlock the exit.")

if "case" not in st.session_state:
    st.session_state.case = None
if "solved" not in st.session_state:
    st.session_state.solved = False
if "score" not in st.session_state:
    st.session_state.score = 100
if "hints" not in st.session_state:
    st.session_state.hints = 0

difficulty = st.selectbox("Choose difficulty", ["Easy", "Medium", "Hard"])

def generate_case():
    prompt = f"""
    Create a logical {difficulty} detective escape room.
    Return ONLY valid JSON with:
    title, story, suspects, clues, culprit, explanation.
    suspects: exactly 3 objects with name and description.
    clues: exactly 3 clues.
    culprit: exact name of one suspect.
    Make the evidence logically consistent and sufficient
    to identify exactly one culprit.
    Do not reveal the culprit in the story or clues.
    """
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )
    result = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(result)

if st.button("🕵️ Generate New AI Mystery", type="primary"):
    try:
        with st.spinner("Gemini is creating your mystery..."):
            st.session_state.case = generate_case()
            st.session_state.solved = False
            st.session_state.score = 100
            st.session_state.hints = 0
    except Exception as e:
        st.error(f"AI generation error: {e}")

if st.session_state.case:
    case = st.session_state.case

    st.header(case["title"])
    st.write(case["story"])

    st.subheader("🔍 Evidence Board")
    for i, clue in enumerate(case["clues"], 1):
        st.info(f"Clue {i}: {clue}")

    st.subheader("👥 Suspects")
    for suspect in case["suspects"]:
        st.markdown(f"**{suspect['name']}** — {suspect['description']}")

    if not st.session_state.solved:
        names = [s["name"] for s in case["suspects"]]
        choice = st.selectbox("Who is the culprit?", names)

        if st.button("Submit accusation"):
            if choice.strip().lower() == case["culprit"].strip().lower():
                st.session_state.solved = True
                st.balloons()
                st.success("Correct! The escape door is unlocked!")
            else:
                st.error("Incorrect! Re-examine the evidence.")
                st.session_state.score = max(0, st.session_state.score - 10)

        if st.button("💡 Ask Gemini for a hint"):
            try:
                hint = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=f"Give one helpful but non-revealing hint for this mystery: {case['story']} Clues: {case['clues']} Suspects: {case['suspects']}. Never reveal the culprit."
                )
                st.session_state.hints += 1
                st.session_state.score = max(0, st.session_state.score - 15)
                st.info(hint.text)
            except Exception as e:
                st.error(f"Hint error: {e}")

    else:
        st.success("🎉 CASE SOLVED — YOU ESCAPED!")
        st.write("Culprit:", case["culprit"])
        st.write("Explanation:", case["explanation"])
        st.metric("Final score", st.session_state.score)
