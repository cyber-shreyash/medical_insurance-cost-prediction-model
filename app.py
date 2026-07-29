import streamlit as st
import pandas as pd
import pickle

# ---------------------------
# Load Model and Scaler
# ---------------------------
with open("medical_model.pkl", "rb") as file:
    model = pickle.load(file)

with open("scaler_medical.pkl", "rb") as file:
    scaler = pickle.load(file)

# ---------------------------
# Streamlit Page Config
# ---------------------------
st.set_page_config(
    page_title="Medical Insurance Cost Predictor",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 Medical Insurance Cost Prediction")
st.markdown("Enter your details below to estimate your insurance charges.")

st.divider()

# ---------------------------
# User Inputs
# ---------------------------

age = st.slider("Age", 18, 100, 25)

sex = st.selectbox(
    "Gender",
    ["male", "female"]
)

bmi = st.number_input(
    "BMI",
    min_value=10.0,
    max_value=60.0,
    value=25.0,
    step=0.1
)

children = st.slider(
    "Number of Children",
    0,
    10,
    0
)

smoker = st.selectbox(
    "Smoker",
    ["no", "yes"]
)

region = st.selectbox(
    "Region",
    [
        "southwest",
        "southeast",
        "northwest",
        "northeast"
    ]
)

# ---------------------------
# Encoding
# ---------------------------

sex = 0 if sex == "male" else 1

smoker = 1 if smoker == "yes" else 0

region_map = {
    "southwest": 0,
    "southeast": 1,
    "northwest": 2,
    "northeast": 3
}

region = region_map[region]

# ---------------------------
# DataFrame
# ---------------------------

input_df = pd.DataFrame({
    "age": [age],
    "sex": [sex],
    "bmi": [bmi],
    "children": [children],
    "smoker": [smoker],
    "region": [region]
})

# ---------------------------
# Scale Input
# ---------------------------

input_scaled = scaler.transform(input_df)

# ---------------------------
# Prediction
# ---------------------------

if st.button("Predict Insurance Charges"):

    prediction = model.predict(input_scaled)

    st.success(
        f"Estimated Insurance Cost: ${prediction[0]:,.2f}"
    )

    st.balloons()

st.divider()

st.caption(
    "Model Used: CatBoost Regressor | Developed using Streamlit"
)