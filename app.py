import streamlit as st
import random
from datetime import datetime
from firebase_config import auth, db

# Page Configuration
st.set_page_config(page_title="Growth Mindset Challenge 🌱", page_icon="🚀", layout="centered")

# --- TITLE ---
st.title("🌱 Growth Mindset Challenge")
st.subheader("Embrace Challenges, Learn from Mistakes, and Keep Growing!")

# --- SESSION STATE ---
if "user" not in st.session_state:
    st.session_state.user = None
if "user_data" not in st.session_state:
    st.session_state.user_data = None

# --- SIDEBAR MENU ---
menu = st.sidebar.radio("Menu", ["Login", "Sign Up"])

# --- AUTH FUNCTIONS ---
def fetch_user_data(user_uid, token):
    """Fetch user data from Firebase."""
    try:
        return db.child("users").child(user_uid).get(token).val()
    except Exception as e:
        st.warning(f"⚠️ Could not load user data: {str(e)}")
        return None

def update_user_data(user_uid, token, data):
    """Update user data in Firebase."""
    try:
        db.child("users").child(user_uid).update(data, token=token)
        return True
    except Exception as e:
        st.error(f"❌ Error updating data: {str(e)}")
        return False

def get_badge(challenges_completed):
    """Determine badge level based on completed challenges."""
    if challenges_completed <= 5:
        return "🟢 Beginner"
    elif 6 <= challenges_completed <= 15:
        return "🔵 Explorer"
    elif 16 <= challenges_completed <= 25:
        return "🔴 Master"
    elif 26 <= challenges_completed <= 50:
        return "🟣 Grandmaster"
    else:
        return "🟠 Legend"

# --- SIGN-UP SECTION ---
if menu == "Sign Up":
    st.sidebar.subheader("🔑 Create an Account")
    email = st.sidebar.text_input("📧 Email")
    password = st.sidebar.text_input("🔒 Password", type="password")

    if st.sidebar.button("📝 Sign Up"):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            uid, token = user["localId"], user["idToken"]

            # Initialize User Data
            new_user_data = {
                "email": email,
                "progress": 50,
                "badges": [],
                "streak": 0,
                "challenges_completed": 0,
                "last_active": str(datetime.today().date())
            }
            update_user_data(uid, token, new_user_data)

            st.session_state.user = user
            st.success("✅ Sign-up successful! Please log in.")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# --- LOGIN SECTION ---
if menu == "Login":
    st.sidebar.subheader("🔓 Log In")
    email = st.sidebar.text_input("📧 Email")
    password = st.sidebar.text_input("🔒 Password", type="password")

    if st.sidebar.button("🔑 Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.user = user
            st.success(f"🎉 Welcome back, {email}!")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# --- MAIN CONTENT (AFTER LOGIN) ---
if st.session_state.user:
    user_email = st.session_state.user["email"]
    user_uid = st.session_state.user["localId"]
    token = st.session_state.user["idToken"]

    st.sidebar.subheader(f"🔑 Logged in as: **{user_email}**")

    # --- Logout ---
    if st.sidebar.button("🚪 Logout"):
        st.session_state.user = None
        st.session_state.user_data = None
        st.experimental_rerun()

    # --- Fetch User Data Efficiently ---
    if st.session_state.user_data is None:
        user_data = fetch_user_data(user_uid, token)
        st.session_state.user_data = user_data
    else:
        user_data = st.session_state.user_data

    progress = user_data.get("progress", 50)
    badges = user_data.get("badges", [])
    streak = user_data.get("streak", 0)
    last_active = user_data.get("last_active", str(datetime.today().date()))

    # --- Streak System ---
    today = str(datetime.today().date())
    if last_active != today:
        streak += 1
        update_user_data(user_uid, token, {"streak": streak, "last_active": today})
        st.session_state.user_data["streak"] = streak
        st.success(f"🔥 Streak Updated! You're on a **{streak}-day** learning streak!")

    # --- Progress Tracking ---
    st.subheader("📊 Track Your Growth Mindset Progress")
    new_progress = st.slider("💡 How much do you believe in the Growth Mindset?", 0, 100, progress)
    st.progress(new_progress / 100)  # Show progress visually

    if st.button("💾 Save Progress"):
        if update_user_data(user_uid, token, {"progress": new_progress}):
            st.session_state.user_data["progress"] = new_progress
            st.success("✅ Progress saved successfully!")

    # --- Display Badges ---
    st.subheader("🏅 Your Achievements")
    badge = user_data.get("badge", "No Badge Earned Yet")
    st.write(f"🏆 **Current Badge:** {badge}")

    if badges:
        for badge in badges:
            st.write(f"✔️ {badge}")
    else:
        st.write("🔹 No badges earned yet. Keep growing!")

    # --- Challenge Section ---
    st.subheader("📌 Your Growth Mindset Challenge")
    if st.button("🎯 Get a Challenge"):
        challenges_completed = user_data.get("challenges_completed", 0) + 1
        update_user_data(user_uid, token, {"challenges_completed": challenges_completed})

        badge = get_badge(challenges_completed)
        update_user_data(user_uid, token, {"badge": badge})
        st.session_state.user_data["badge"] = badge

        challenges = [
            "📖 Write down 3 things you learned from a recent failure.",
            "🧩 Try solving a problem you previously gave up on.",
            "💬 Ask a friend for constructive feedback and act on it.",
            "⏳ Spend 30 minutes learning something outside your comfort zone.",
            "🎓 Teach someone else a concept you struggled with before."
        ]
        st.success("💪 Challenge: " + random.choice(challenges))

    # --- Leaderboard (Top 5 Users) ---
    st.subheader("🏆 Growth Leaderboard")
    try:
        users = db.child("users").get(token).val()
        if users:
            sorted_users = sorted(users.items(), key=lambda x: x[1].get("progress", 0), reverse=True)[:5]
            for idx, (uid, data) in enumerate(sorted_users, start=1):
                st.write(f"**{idx}. {data.get('email', 'Unknown User')}** - {data.get('progress', 0)}% Growth")
        else:
            st.write("🚀 No users found.")
    except Exception as e:
        st.error(f"⚠️ Error loading leaderboard: {str(e)}")
