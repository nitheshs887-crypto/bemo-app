import sys
import subprocess

try:
    import streamlit as st
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
    import streamlit as st

st.set_page_config(
    page_title="Streamlit App",
    page_icon="🚀",
    layout="wide"
)

st.title("Streamlit Application")

st.sidebar.header("Navigation & Settings")
app_mode = st.sidebar.selectbox("Choose a page", ["Home", "Text Analyzer", "Settings"])

if app_mode == "Home":
    st.subheader("Welcome to the Streamlit App")
    st.write("Use the sidebar to navigate through the application.")
    st.info("This application is built with Streamlit.")

elif app_mode == "Text Analyzer":
    st.subheader("Text Vector & Analysis Tool")
    
    text_input = st.text_area("Enter text to analyze", "Streamlit makes it easy to build custom web apps for machine learning and data science.", height=150)
    
    if st.button("Process Text"):
        words = text_input.split()
        st.write(f"**Word Count:** {len(words)}")
        st.write(f"**Character Count:** {len(text_input)}")
        
        vector = {}
        for word in words:
            clean_word = word.lower().strip(".,!?:;\"'")
            if clean_word:
                vector[clean_word] = vector.get(clean_word, 0) + 1
                
        st.subheader("Word Frequency Vector")
        st.json(vector)

elif app_mode == "Settings":
    st.subheader("Settings")
    theme = st.selectbox("Select Theme", ["Light", "Dark", "System"])
    st.success(f"Selected theme: {theme}")
