import sys
import subprocess

try:
    import streamlit as st
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
    import streamlit as st

st.set_page_config(
    page_title="vel.py",
    page_icon="🚀",
    layout="wide"
)

st.title("Streamlit Application")

st.sidebar.header("Navigation & Settings")
app_mode = st.sidebar.selectbox("Choose a page", ["Home", "Text Analyzer", "Settings"])

if app_mode == "Home":
    st.subheader("Welcome to the Streamlit App")
    st.write("Use the sidebar to navigate through the application.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("⚡ **Fast & Interactive**\n\nBuild rich UI components instantly.")
    with col2:
        st.success("📊 **Data Visualization**\n\nAnalyze text and visualize word frequencies.")
    with col3:
        st.warning("⚙️ **Customizable**\n\nConfigure settings to fit your needs.")

elif app_mode == "Text Analyzer":
    st.subheader("Text Vector & Analysis Tool")
    
    text_input = st.text_area("Enter text to analyze", "Streamlit makes it easy to build custom web apps for machine learning and data science.", height=150)
    
    if st.button("Process Text", type="primary"):
        words = text_input.split()
        
        vector = {}
        for word in words:
            clean_word = word.lower().strip(".,!?:;\"'")
            if clean_word:
                vector[clean_word] = vector.get(clean_word, 0) + 1
                
        col1, col2, col3 = st.columns(3)
        col1.metric("Word Count", len(words))
        col2.metric("Character Count", len(text_input))
        col3.metric("Unique Words", len(vector))
        
        st.subheader("Word Frequency Vector")
        tab1, tab2 = st.tabs(["Chart", "JSON Data"])
        with tab1:
            if vector:
                st.bar_chart(vector)
            else:
                st.info("No words to display in chart.")
        with tab2:
            st.json(vector)

elif app_mode == "Settings":
    st.subheader("Settings")
    theme = st.selectbox("Select Theme", ["Light", "Dark", "System"])
    notifications = st.toggle("Enable Notifications", value=True)
    font_size = st.slider("Font Size", 12, 24, 16)
    st.success(f"Selected theme: {theme}")

if __name__ == "__main__":
    is_streamlit = False
    try:
        from streamlit.runtime import exists
        is_streamlit = exists()
    except ImportError:
        pass

    if not is_streamlit:
        try:
            from streamlit.web import cli as stcli
        except ImportError:
            from streamlit import cli as stcli
        sys.argv = ["streamlit", "run", __file__]
        sys.exit(stcli.main())
