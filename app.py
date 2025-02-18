import streamlit as st

# Title and Introduction
st.title("Growth Mindset Challenge")
st.subheader("Embrace Challenges, Learn from Mistakes, and Keep Growing!")

# Explanation of Growth Mindset
st.write(
    """
    A **growth mindset** is the belief that intelligence and abilities can be developed through effort and learning.
    Here are some key principles of a growth mindset:
    - 💡 **Embrace challenges** as opportunities to grow.
    - 🔄 **Learn from mistakes** and see failure as feedback.
    - 🔥 **Stay persistent** even when things get tough.
    - 🎉 **Celebrate effort** rather than just results.
    - 🌱 **Stay curious** and open to new ideas.
    """
)

# User Interaction
name = st.text_input("What's your name?")
if name:
    st.success(f"Hi {name}, are you ready to develop a Growth Mindset? 🚀")

# Progress Tracker
progress = st.slider("How much do you believe in the Growth Mindset?", 0, 100, 50)
st.write(f"Your Growth Mindset score: **{progress}%**")

# Challenge Section
st.subheader("📌 Your Growth Mindset Challenge")
if st.button("Get a Challenge"):
    challenges = [
        "Write down 3 things you learned from a recent failure.",
        "Try solving a problem you previously gave up on.",
        "Ask a friend for constructive feedback and act on it.",
        "Spend 30 minutes learning something outside your comfort zone.",
        "Teach someone else a concept you struggled with before."
    ]
    st.write("💪 Challenge: " + random.choice(challenges))

st.write("**Keep learning and growing! You’ve got this! 🚀**")
