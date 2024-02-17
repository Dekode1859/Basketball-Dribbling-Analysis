# this is a basket ball dribbling video analysis program in which we will have a streamlit app that 
# will have two options one is for webcam and other is for video file. for the webcam part we will use openCV 
# and for the video file we will use openCV and streamlit. we only detect the basket ball using a custom trained yolo model that works on a video file and webcam.

# import the necessary packages
import numpy as np
import cv2
import time
import streamlit as st
import os
import tempfile
from PIL import Image

def run_webcam():
    cap = cv2.VideoCapture(0)
    stframe = st.empty()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB")
        if st.button("Exit"):
            cap.release()
            break
        
def run_video_file():
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4"])
    if uploaded_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        cap = cv2.VideoCapture(tfile.name)
        stframe = st.empty()
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            stframe.image(frame, channels="RGB")
            if st.button("Exit"):
                cap.release()
                break
        os.unlink(tfile.name)

def main():
    # Title
    st.title("Basket Ball Dribbling Analysis")
    st.write("This is a basket ball dribbling video analysis program in which we will have a streamlit app that will have two options one is for webcam and other is for video file. for the webcam part we will use openCV and for the video file we will use openCV and streamlit. we only detect the basket ball using a custom trained yolo model that works on a video file and webcam.")

    # Sidebar
    st.sidebar.title("Choose the option")
    option = st.sidebar.radio("", ("Webcam", "Video File"))

    # Webcam
    if option == "Webcam":
        st.subheader("Webcam")
        run_webcam()
    # Video File
    elif option == "Video File":
        st.subheader("Video File")
        run_video_file()