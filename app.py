import streamlit as st

st.set_page_config(page_title="Astrocyte", page_icon="✨", layout="centered")

st.title("Welcome to Astrocyte 🚀")
st.markdown("### Your sleek, rapid prototype homepage.")
st.write("This is a live test to verify our setup and functionality.")

if st.button("Run System Test"):
    st.success("System operational! The pipeline is fully functional.")