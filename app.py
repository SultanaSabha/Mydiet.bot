import streamlit as st
from qa_chain import get_qa_chain

# Load QA chain
qa_chain = get_qa_chain()

# ---- Streamlit UI ----
st.set_page_config(page_title="MyDiet.Bot", page_icon="🥗", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem !important;
        color: #2E8B57;
        text-align: center;
    }
    .quick-question-btn {
        width: 100%;
        margin: 5px 0;
    }
    .metric-card {
        background-color: #f0f8f0;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
    }
</style>
""", unsafe_allow_html=True)

# ---- Sidebar with User Profile ----
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>👤 Your Profile</h2>", unsafe_allow_html=True)
    
    with st.form("user_profile"):
        col1, col2 = st.columns(2)
        with col1:
            user_weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1)
        with col2:
            user_height = st.number_input("Height (cm)", min_value=100.0, max_value=220.0, value=170.0, step=1.0)
        
        user_age = st.number_input("Age", min_value=10, max_value=100, value=30)
        user_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        user_goal = st.selectbox("Primary Goal", ["Weight Loss", "Maintenance", "Muscle Gain", "General Health"])
        user_activity = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
        
        if st.form_submit_button("💾 Save Profile"):
            st.success("Profile saved!")
    
    # Calculate BMR and Daily Calories
    st.markdown("---")
    st.markdown("<h4>📊 Your Metrics</h4>", unsafe_allow_html=True)
    
    if user_gender == "Male":
        bmr = 10 * user_weight + 6.25 * user_height - 5 * user_age + 5
    else:
        bmr = 10 * user_weight + 6.25 * user_height - 5 * user_age - 161
    
    activity_multipliers = {"Sedentary": 1.2, "Lightly Active": 1.375, "Moderately Active": 1.55, "Very Active": 1.725}
    daily_calories = bmr * activity_multipliers[user_activity]
    
    st.markdown(f"""
    <div class='metric-card'>
        <b>BMR:</b> {bmr:.0f} kcal<br>
        <b>Daily Calories:</b> {daily_calories:.0f} kcal<br>
        <b>BMI:</b> {(user_weight/((user_height/100)**2)):.1f}
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("---")
    st.markdown("<h4>⚡ Quick Actions</h4>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# ---- Main Content Area ----
st.markdown("<h1 class='main-header'>🥗 MyDiet.Bot</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #555;'>Your friendly AI nutritionist!</h3>", unsafe_allow_html=True)

# ---- Quick Question Buttons ----
st.markdown("### 💡 Quick Questions")
quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)

quick_questions = {
    "🍳 Breakfast Ideas": "Give me 3 healthy breakfast ideas with calories",
    "⚖️ Weight Loss Tips": "What are the best foods for weight loss?",
    "💪 Protein Sources": "What are good protein sources for vegetarians?",
    "🥦 Healthy Snacks": "Suggest some low-calorie healthy snacks",
    "🍽️ Meal Planning": "Create a sample 1500-calorie meal plan",
    "💧 Hydration": "How much water should I drink daily?",
    "🏋️‍♂️ Pre-Workout": "What should I eat before workout?",
    "🛌 Late Night Craving": "Healthy options for late night cravings"
}

with quick_col1:
    if st.button(list(quick_questions.keys())[0], use_container_width=True):
        st.session_state.quick_question = list(quick_questions.values())[0]
with quick_col2:
    if st.button(list(quick_questions.keys())[1], use_container_width=True):
        st.session_state.quick_question = list(quick_questions.values())[1]
with quick_col3:
    if st.button(list(quick_questions.keys())[2], use_container_width=True):
        st.session_state.quick_question = list(quick_questions.values())[2]
with quick_col4:
    if st.button(list(quick_questions.keys())[3], use_container_width=True):
        st.session_state.quick_question = list(quick_questions.values())[3]

quick_col5, quick_col6, quick_col7, quick_col8 = st.columns(4)
with quick_col5:
    if st.button(list(quick_questions.keys())[4], use_container_width=True):
        st.session_state.quick_question = list(quick_questions.values())[4]
with quick_col6:
    if st.button(list(quick_questions.keys())[5], use_container_width=True):
        st.session_state.quick_question = list(quick_questions.values())[5]
with quick_col7:
    if st.button(list(quick_questions.keys())[6], use_container_width=True):
        st.session_state.quick_question = list(quick_questions.values())[6]
with quick_col8:
    if st.button(list(quick_questions.keys())[7], use_container_width=True):
        st.session_state.quick_question = list(quick_questions.values())[7]

# ---- Meal Logging Section ----
st.markdown("---")
st.markdown("### 📝 Log Your Meals Today")

meal_col1, meal_col2, meal_col3, meal_col4 = st.columns(4)

if "meals" not in st.session_state:
    st.session_state.meals = []

with meal_col1:
    with st.form("breakfast_form"):
        st.subheader("🍳 Breakfast")
        breakfast_items = st.text_area("What did you eat?", height=80, key="breakfast")
        breakfast_cals = st.number_input("Calories", min_value=0, value=0, key="breakfast_cals")
        if st.form_submit_button("Log Breakfast"):
            if breakfast_items:
                st.session_state.meals.append({"meal": "Breakfast", "items": breakfast_items, "calories": breakfast_cals})
                st.success("Breakfast logged!")

with meal_col2:
    with st.form("lunch_form"):
        st.subheader("🍽️ Lunch")
        lunch_items = st.text_area("What did you eat?", height=80, key="lunch")
        lunch_cals = st.number_input("Calories", min_value=0, value=0, key="lunch_cals")
        if st.form_submit_button("Log Lunch"):
            if lunch_items:
                st.session_state.meals.append({"meal": "Lunch", "items": lunch_items, "calories": lunch_cals})
                st.success("Lunch logged!")

with meal_col3:
    with st.form("dinner_form"):
        st.subheader("🍛 Dinner")
        dinner_items = st.text_area("What did you eat?", height=80, key="dinner")
        dinner_cals = st.number_input("Calories", min_value=0, value=0, key="dinner_cals")
        if st.form_submit_button("Log Dinner"):
            if dinner_items:
                st.session_state.meals.append({"meal": "Dinner", "items": dinner_items, "calories": dinner_cals})
                st.success("Dinner logged!")

with meal_col4:
    with st.form("snacks_form"):
        st.subheader("🍎 Snacks")
        snacks_items = st.text_area("What did you eat?", height=80, key="snacks")
        snacks_cals = st.number_input("Calories", min_value=0, value=0, key="snacks_cals")
        if st.form_submit_button("Log Snacks"):
            if snacks_items:
                st.session_state.meals.append({"meal": "Snacks", "items": snacks_items, "calories": snacks_cals})
                st.success("Snacks logged!")

# Display logged meals and calculate total calories
if st.session_state.meals:
    st.markdown("### 📊 Today's Food Log")
    total_cals = 0
    for i, meal in enumerate(st.session_state.meals):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.write(f"**{meal['meal']}:** {meal['items']}")
        with col2:
            st.write(f"**Calories:** {meal['calories']} kcal")
        with col3:
            if st.button("❌", key=f"delete_{i}"):
                st.session_state.meals.pop(i)
                st.rerun()
        total_cals += meal['calories']
    
    st.markdown(f"**🔥 Total Calories Today: {total_cals} kcal**")
    
    # Progress bar for daily calorie goal
    if daily_calories > 0:
        progress = min(total_cals / daily_calories, 1.0)
        st.progress(progress)
        st.write(f"({total_cals:.0f} / {daily_calories:.0f} kcal)")

# ---- Chat Interface ----
st.markdown("---")
st.markdown("### 💬 Chat with MyDiet.Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history with better avatars
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant", avatar="🥗"):
            st.write(msg["content"])

# Handle quick questions or regular chat input
if hasattr(st.session_state, 'quick_question'):
    prompt = st.session_state.quick_question
    del st.session_state.quick_question
else:
    prompt = st.chat_input("Type your nutrition question here...")

if prompt:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    # Bot response
    with st.chat_message("assistant", avatar="🥗"):
        with st.spinner("🍎 Analyzing your question..."):
            try:
                result = qa_chain.invoke({"query": prompt})
                response = result["result"]
            except Exception as e:
                response = f"⚠️ Error: {str(e)}"
        
        st.write(response)
    
    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})