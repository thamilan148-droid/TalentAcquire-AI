import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier

# 1. Full Screen Configuration
st.set_page_config(page_title="TalentAcquire AI", page_icon="🎯", layout="wide")

st.title("🎯 TalentAcquire AI: Recruitment Analytics Dashboard")
st.markdown("---")

# 2. Sidebar Setup
with st.sidebar:
    st.header("Candidate Profiling")
    name = st.text_input("Candidate Name", "John Doe")
    input_sem = st.slider("Semester Score (%)", 0, 100, 85)
    input_att = st.slider("Attendance (%)", 0, 100, 90)
    input_intern = st.number_input("Internships Done", 0, 10, 2)
    input_skill = st.slider("Skill Score (1-10)", 1, 10, 8)
    predict_btn = st.button("Evaluate Candidate 🚀")

# 3. Model & Data
file_path = r'C:\Users\Tamilan\OneDrive\Documents\Student_Project\Student__data.csv'
df = pd.read_csv(file_path)
X = df[['Sem_Percentage', 'Attendance', 'Internships', 'Skill_Level']]
y = df['Performance_Labal']
model = RandomForestClassifier(n_estimators=100).fit(X, y)

if predict_btn:
    prediction = model.predict([[input_sem, input_att, input_intern, input_skill]])[0]
    
    # Metrics Display
    m1, m2, m3 = st.columns(3)
    m1.metric("AI Prediction", prediction)
    m2.metric("HR Action", "Shortlist ✅" if prediction == "Best" else "Review ⏳")
    m3.metric("Final Rank", "Qualified")

    # --- CLEAN REPORT (RED MARKS REMOVED) ---
    # Simple words use pannuna notepad-la red line varathu
    report_text = f"""
OFFICIAL CANDIDATE DATA
***********************
Name: {name.upper()}
Academic Score: {input_sem}%
Internships: {input_intern}
AI Prediction: {prediction}
***********************
    """
    st.download_button(f"📥 Download {name} Report", report_text, f"{name}_Report.txt")

# 4. Wide Table for HR
st.markdown("---")
st.subheader("🏆 Executive Selection Dashboard (Top Performers)")

best_df = df[df['Performance_Labal'] == 'Best'].copy()

if not best_df.empty:
    # Adding clean SNo
    best_df.insert(0, 'No', range(1, len(best_df) + 1))
    
    # Blue Box Table
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>No</b>", "<b>Candidate Name</b>", "<b>Score %</b>", "<b>Internships</b>"],
            fill_color='#1f77b4', align='center', font=dict(color='white', size=15), height=40
        ),
        cells=dict(
            values=[best_df['No'], best_df['Name'], best_df['Sem_Percentage'], best_df['Internships']],
            fill_color='#f8f9fa', align='center', font=dict(color='black', size=13), height=30
        ))
    ])
    fig.update_layout(autosize=True, margin=dict(l=0, r=0, t=0, b=0), height=400)
    st.plotly_chart(fig, use_container_width=True)

    # --- HR LIST WITHOUT RED MARKS ---
    # Header names-ai notepad-ukku puriyura maari simple-ah mathiruken
    hr_list_data = best_df[['No', 'Name', 'Sem_Percentage', 'Internships']]
    hr_list_data.columns = ['No', 'Name', 'Percentage', 'Internships']
    
    hr_list_final = "SELECTED LIST\n" + "*"*20 + "\n"
    hr_list_final += hr_list_data.to_string(index=False)
    
    st.download_button("📥 Download Official HR List", hr_list_final, "HR_Shortlist.txt")