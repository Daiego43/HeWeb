import streamlit as st
st.set_page_config(layout="wide")

class HeWeb:
    def __init__(self):
        self.main()

    def main(self):
        col1, col2 = st.columns([1, 1])
        with col1:
            self.introduction()
        with col2:
            self.features()

    def introduction(self):
        st.title("HeWo Web App")
        st.image("images/hewo_face.png")
        st.write("This is a developer app to test and manage the oncoming features in the HeWo project.")

    def features(self):
        st.title("Features")
        st.write("The following features are available in the HeWo project:")
        st.checkbox("Face emotion control", disabled=True, value=True)
        st.checkbox("Face emotion study", disabled=True)


HeWeb()