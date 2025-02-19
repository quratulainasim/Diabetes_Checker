import streamlit as st
from fpdf import FPDF
import base64

st.title("Diabetes Risk Assessment App")

st.header("Assess Your Risk of Type 2 Diabetes")

st.write("""
This app calculates your risk of developing Type 2 diabetes based on common risk factors.
Answer the following questions to get your risk score and precautionary measures.
""")

st.subheader("1. Age")
age = st.number_input("Enter your age", min_value=0, max_value=100, value=00)

st.subheader("2. Weight Status")
bmi = st.number_input("Enter your BMI (Body Mass Index)", min_value=10.0, max_value=30.0,value=10.0)

st.subheader("3. Glucose Level")
glucose = st.number_input("Enter your fasting glucose level (mg/dL)", min_value=50, max_value=300, value=90)

st.subheader("4. Physical Activity")
activity = st.radio(
    "How often do you engage in physical activity?",
    options=["Rarely", "1-2 times a week", "3-5 times a week", "Daily"]
)

st.subheader("5. Family History")
family_history = st.radio(
    "Do you have a family history of diabetes?",
    options=["No", "Yes"]
)

st.subheader("6. Blood Pressure")
blood_pressure = st.radio(
    "Do you have high blood pressure?",
    options=["No", "Yes"]
)

risk_score = 0

if age >= 30:
    risk_score += 1

if bmi >= 20:
    risk_score += 1

if activity in ["Rarely", "1-2 times a week"]:
    risk_score += 1

if family_history == "Yes":
    risk_score += 1

if blood_pressure == "Yes":
    risk_score += 1

if glucose >= 100:
    risk_score += 1

st.subheader("Your Diabetes Risk Score")
st.write(f"Your risk score is: **{risk_score}** out of 6.")

st.subheader("Risk Chances")
if risk_score == 0:
    st.success("Low Risk: You have a low risk of being affected by Type 2 diabetes.")
    precautions = [
        "Maintain a healthy diet rich in fruits, vegetables, and whole grains.",
        "Do regular physical activity (e.g., 30 minutes of exercise most days of the week).",
        "Maintain your weight and BMI.",
        "Get regular health check-ups to monitor your blood sugar levels."
    ]
elif risk_score <= 3:
    st.warning("Moderate Risk:  You have a moderate risk of being affected by Type 2 diabetes. Consider consulting a healthcare provider.")
    precautions = [
        "Adopt a balanced diet with reduced sugar and refined carbohydrates.",
        "Increase physical activity to at least 150 minutes per week.",
        "Lose weight if you are overweight or obese.",
        "Monitor your blood pressure and cholesterol levels regularly.",
        "Consult a healthcare provider for personalized advice."
    ]
else:
    st.error("High Risk: You have a high risk of beind affected by Type 2 diabetes. Please consult a healthcare provider for further treatment.")
    precautions = [
        "Follow a strict diet plan recommended by a healthcare provider.",
        "Engage in regular physical activity (e.g., 30 minutes daily).",
        "Lose weight if you are overweight or obese.",
        "Monitor your blood sugar, blood pressure, and cholesterol levels regularly.",
        "Consult a healthcare provider immediately for further evaluation and treatment."
    ]

st.subheader("Precautionary Measures")
for i, precaution in enumerate(precautions, 1):
    st.write(f"{i}. {precaution}")

def create_pdf(age, bmi, activity, family_history, blood_pressure, glucose, risk_score, precautions):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Diabetes Risk Assessment Report", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="User Inputs:", ln=True)
    pdf.cell(200, 10, txt=f"Age: {age}", ln=True)
    pdf.cell(200, 10, txt=f"BMI: {bmi}", ln=True)
    pdf.cell(200, 10, txt=f"Physical Activity: {activity}", ln=True)
    pdf.cell(200, 10, txt=f"Family History of Diabetes: {family_history}", ln=True)
    pdf.cell(200, 10, txt=f"High Blood Pressure: {blood_pressure}", ln=True)
    pdf.cell(200, 10, txt=f"Fasting Glucose Level: {glucose} mg/dL", ln=True)
    pdf.cell(200, 10, txt=f"Risk Score: {risk_score} out of 6", ln=True)
    pdf.cell(200, 10, txt="Precautionary Measures:", ln=True)
    for precaution in precautions:
        pdf.cell(200, 10, txt=f"- {precaution}", ln=True)
    pdf_output = pdf.output(dest="S").encode("latin1")
    return pdf_output

if st.button("Generate Report"):
    pdf_output = create_pdf(age, bmi, activity, family_history, blood_pressure, glucose, risk_score, precautions)
    b64 = base64.b64encode(pdf_output).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="diabetes_risk_report.pdf">Download Report</a>'
    st.markdown(href, unsafe_allow_html=True)