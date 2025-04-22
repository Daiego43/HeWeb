import requests
import streamlit as st
import yaml

SET_EMOTION_ENDPOINT = "http://127.0.0.1:5000/set_emotion_goal"
EMOTION_DATA_PATH = "data/emotions"

class EmotionControl:
    def __init__(self):
        self.main()

    def main(self):
        st.title("HeWo Face Control")
        st.text(
            "Move each of the expression points I designed to control hewo's face. Discover and save the emotion for later study.")
        left_eye, mouth, right_eye = st.columns([1, 2, 1])
        with left_eye:
            self.left_eye()
        with mouth:
            self.mouth()
        with right_eye:
            self.right_eye()
        self.save_emotion()
        self.slider_values()

    def slider_values(self):
        st.sidebar.write("### Current Slider Values")
        data = self.get_slider_values()
        st.sidebar.json(data)
        self.send_request(data)

    def send_request(self, data):
        try:
            requests.post(SET_EMOTION_ENDPOINT, json=data)
        except requests.exceptions.ConnectionError:
            st.error("Error: Unable to connect to HeWo.")
            return

    def save_emotion(self):
        st.sidebar.title("Save emotion values")
        emotion_name = st.sidebar.text_input("Emotion name", key="emotion_name")
        if st.sidebar.button("Save emotion"):
            data = self.get_slider_values()
            with open(f"{EMOTION_DATA_PATH}/{emotion_name}.yaml", "a") as file:
                yaml.dump(data, file)
            st.sidebar.success("Emotion saved successfully")

    def left_eye(self):
        st.write("## Left eye")

        # Crear columnas para cada grupo de sliders
        st.write("#### Pupil")
        st.slider("Leftt pupil size", 0, 100, 100, key="lps")

        col1, col2, col3 = st.columns([2, 0.1, 2])

        with col1:
            st.write("#### Upper eyebrow")
            st.slider("letl_a", 0, 100, 0, key="letl_a")
            st.slider("letl_b", 0, 100, 0, key="letl_b")
            st.slider("letl_c", 0, 100, 0, key="letl_c")

        with col3:
            st.write("#### Lower eyebrow")
            st.slider("lebl_a", 0, 100, 0, key="lebl_a")
            st.slider("lebl_b", 0, 100, 0, key="lebl_b")
            st.slider("lebl_c", 0, 100, 0, key="lebl_c")

    def right_eye(self):
        st.write("## Right eye")

        # Crear columnas para cada grupo de sliders
        st.write("#### Pupil")
        st.slider("Right pupil size", 0, 100, 100, key="rps")

        col1, col2, col3 = st.columns([2, 0.1, 2])
        with col1:
            st.write("#### Upper eyebrow")
            st.slider("retl_a", 0, 100, 0, key="retl_a")
            st.slider("retl_b", 0, 100, 0, key="retl_b")
            st.slider("retl_c", 0, 100, 0, key="retl_c")

        with col3:
            st.write("#### Lower eyebrow")
            st.slider("rebl_a", 0, 100, 0, key="rebl_a")
            st.slider("rebl_b", 0, 100, 0, key="rebl_b")
            st.slider("rebl_c", 0, 100, 0, key="rebl_c")

    def mouth(self):
        st.write("## Mouth")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write("#### Upper lip")
            lip_keys = ['tl_a', 'tl_b', 'tl_c', 'tl_d', 'tl_e', ]
            for key in lip_keys:
                st.slider(key, 0, 100, 0, key=key)

        with col2:
            st.write("#### Lower lip")
            lip_keys = ['bl_a', 'bl_b', 'bl_c', 'bl_d', 'bl_e', ]
            for key in lip_keys:
                st.slider(key, 0, 100, 0, key=key)

    def get_slider_values(self):
        # Filtra los valores de los sliders de `st.session_state`
        slider_keys = [
            "lps", "letl_a", "letl_b", "letl_c", "lebl_a", "lebl_b", "lebl_c",
            "rps", "retl_a", "retl_b", "retl_c", "rebl_a", "rebl_b", "rebl_c",
            "tl_a", "tl_b", "tl_c", "tl_d", "tl_e",
            "bl_a", "bl_b", "bl_c", "bl_d", "bl_e"
        ]
        return {key: st.session_state[key] for key in slider_keys}


EmotionControl()
