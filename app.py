import streamlit as st
from ultralytics import YOLO
from analysis import Analyzer

def main():
    st.title("Basket Ball Dribbling Analysis")
    st.write("This is a basket ball dribbling video analysis program.")

    model = YOLO('models/yolov8n.pt')
    model = YOLO('models/old_best.pt')
    analyzer = Analyzer(model)
    
    st.sidebar.title("Upload Video File")
    vid = st.sidebar.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])
    vid_bttn = st.sidebar.button("Analyze Video File")
    cam_bttn = st.sidebar.button("Use Webcam")
    example_bttn = st.sidebar.button("Watch Example Video")
    
    st.markdown(
        '''
        ### Analysis Variables
        - Bounces: The number of times the ball bounces on the ground
        - Speed: The speed of the dribble (Fast, Medium, Slow)
        - Bounce type: The type of bounce (High, Medium, Low) 
        - Direction: The direction of the dribble (Across, Up & Down)
        - The metrics will be overlaid on the frames of the video.  ''')
    
    if vid_bttn and vid is not None:
        with st.spinner("Analyzing the video file..."):
            analyzer.run_video_file(vid)
    elif cam_bttn:
        analyzer.run_webcam()
    elif example_bttn:
        with st.spinner("Analyzing the example video..."):
            vid = open("WHATSAAP ASSIGNMENT.mp4", "rb")
            analyzer.run_video_file(vid)

    else:
        st.error("Use the Example Video to see how the program works. (Assignment)")
        
if __name__ == "__main__":
    main()