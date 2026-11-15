import streamlit as st

st.set_page_config(page_title="AI Detective Escape Room - V1", page_icon="🕵️", layout="centered")
st.title("🕵️ The Locked Library")
st.subheader("Version 1 — Classic Detective Escape Room")
st.write("A valuable diamond has disappeared. Solve three puzzles to identify the thief and unlock the exit.")

PUZZLES = [
    {"title":"Puzzle 1: The muddy footprint", "story":"A muddy footprint was found beside the display case. Which suspect had been gardening in the rain?", "options":["Maya the gardener","Leo the chef","Nora the pianist"], "answer":"Maya the gardener", "hint":"Look for the suspect whose job involves soil and plants."},
    {"title":"Puzzle 2: The broken clock", "story":"The library clock stopped at 8:15. The guard says the lights went out at 8:10. Which time is the likely time of the theft?", "options":["7:30","8:15","9:00"], "answer":"8:15", "hint":"The stopped clock records the moment it was damaged."},
    {"title":"Puzzle 3: The final key", "story":"A note says: 'I work with plants, and my shoes were muddy.' Who took the diamond?", "options":["Maya","Leo","Nora"], "answer":"Maya", "hint":"Combine the footprint clue with the note."}
]

if "v1_step" not in st.session_state:
    st.session_state.v1_step = 0
if "v1_score" not in st.session_state:
    st.session_state.v1_score = 0
if "v1_done" not in st.session_state:
    st.session_state.v1_done = set()

if st.button("🔄 Restart Version 1"):
    st.session_state.v1_step = 0
    st.session_state.v1_score = 0
    st.session_state.v1_done = set()
    st.rerun()

step = st.session_state.v1_step
if step < len(PUZZLES):
    p = PUZZLES[step]
    st.progress(step / len(PUZZLES))
    st.markdown(f"### {p['title']}")
    st.write(p["story"])
    choice = st.radio("Choose your answer:", p["options"], key=f"v1_choice_{step}")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Submit answer", type="primary"):
            if choice == p["answer"]:
                st.success("Correct! The evidence is added to your case file.")
                if step not in st.session_state.v1_done:
                    st.session_state.v1_score += 1
                    st.session_state.v1_done.add(step)
                st.session_state.v1_step += 1
                st.rerun()
            else:
                st.error("Not quite. Review the evidence and try again.")
    with c2:
        if st.button("Show hint"):
            st.info(p["hint"])
else:
    st.balloons()
    st.success("CASE SOLVED — EXIT UNLOCKED!")
    st.write("Maya took the diamond. You solved the mystery and escaped the library.")
    st.metric("Score", f"{st.session_state.v1_score}/3")
