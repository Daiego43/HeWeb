import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import requests

SERVER = os.environ.get("SERVER")
EMOTION_DATA_PATH = "data/emotions/emotions.csv"
SET_EMOTION_ENDPOINT = f"http://{SERVER}:8000/hewo/set_emotion_goal"


class EmotionDataView:
    def __init__(self):
        st.title("Emotion Dataset Viewer")
        st.caption("Browse, inspect and send stored emotions to HeWo")
        if "selected_emotions" not in st.session_state:
            st.session_state["selected_emotions"] = []

        # Cargar CSV
        if not os.path.exists(EMOTION_DATA_PATH):
            st.warning("No emotion data found yet.")
            st.stop()

        self.emotion_data_df = pd.read_csv(EMOTION_DATA_PATH)

    def views(self):
        cols = st.columns(2)
        with cols[0]:
            self.view_dataset()
            st.divider()
            self.view_emotion_button_grid()
        with cols[1]:
            self.view_emotion_radar_plot()

    def view_dataset(self):
        cols = ["emotion_name"] + [c for c in self.emotion_data_df.columns if c != "emotion_name"]
        df = self.emotion_data_df[cols]
        st.dataframe(df, use_container_width=True)

    def view_emotion_button_grid(self):
        st.subheader("Send any emotion to HeWo")

        latest_emotions = self.emotion_data_df.groupby("emotion_name").tail(1).reset_index(drop=True)

        def send_button(row):
            if st.button(row['emotion_name'], key=f"send_{row['emotion_name']}", use_container_width=True):
                payload = row.drop("emotion_name").to_dict()
                try:
                    requests.post(SET_EMOTION_ENDPOINT, json=payload)
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to HeWo.")

                if row["emotion_name"] not in st.session_state["selected_emotions"]:
                    st.session_state["selected_emotions"].append(row["emotion_name"])

        cols = st.columns(3)
        for idx, row in latest_emotions.iterrows():
            col = cols[idx % 3]
            with col:
                st.markdown(f"**{row['emotion_name']}**", help="Click to send this emotion")
                send_button(row)

    def view_emotion_radar_plot(self):
        st.subheader("Emotion Graphs")
        st.caption("Visualize selected emotions as expressive radar shapes")

        emotion_names = self.emotion_data_df["emotion_name"].dropna().unique()
        selected = st.multiselect("Select emotions to plot", emotion_names, default=st.session_state["selected_emotions"])
        selected += st.session_state["selected_emotions"]

        if selected:
            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

            emotion_keys = [col for col in self.emotion_data_df.columns if col != "emotion_name"]
            num_vars = len(emotion_keys)
            angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
            angles += angles[:1]

            for name in selected:
                latest = self.emotion_data_df[self.emotion_data_df["emotion_name"] == name].iloc[-1]
                values = [latest[k] for k in emotion_keys]
                values += values[:1]
                ax.plot(angles, values, label=name)
                ax.fill(angles, values, alpha=0.1)

            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(emotion_keys, fontsize=8)
            ax.set_yticklabels([])
            ax.set_title("Radar Plot of Emotion Values")
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
            st.pyplot(fig)
        else:
            st.info("Select one or more emotions to display.")


EmotionControl = EmotionDataView()
EmotionControl.views()
