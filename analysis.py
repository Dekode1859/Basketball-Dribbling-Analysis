
import streamlit as st
import cv2, time, tempfile
from kalmanfilter import KalmanFilter

class Analyzer:
    def __init__(self, model):
        self.model = model
        self.queue = []
        self.bounces = 0
        self.bounce_flag = False
        self.bounce_time = None
        self.speed_type = None
        self.bounce_type = None
        self.dribble = None
        
    def add_to_queue(self, p1, p2):
        if len(self.queue) == 30:
            self.queue.pop(0)
        self.queue.append((p1, p2))
        return self.queue
    
    def predict_trajectory(self):
        kf = KalmanFilter()
        predicted = []
        for i in range(1, len(self.queue)):
            x, y = kf.predict(self.queue[i][0], self.queue[i][1])
            predicted.append((x, y))
        return predicted
    
    def classify_dribble_speed(self, time_diff):
        if time_diff < 0.5:
            return "Fast dribble"
        else:
            return "Slow dribble"
        
    def calculate_height_difference(self):
        if len(self.queue) < 2:
            return None
        first_point = self.queue[0]
        last_point = self.queue[-1]
        height_diff = abs(last_point[1] - first_point[1])
        return height_diff

    def classify_bounce_height(self, height_diff):
        if height_diff is None:
            return "No bounce"
        elif height_diff > 50:
            return "High bounce"
        elif height_diff > 20:
            return "Medium bounce"
        else:
            return "Low bounce"

    def calculate_x_difference(self):
        if len(self.queue) < 2:
            return None
        first_point = self.queue[0]
        last_point = self.queue[-1]
        x_diff = abs(last_point[0] - first_point[0])
        return x_diff

    def classify_dribble_direction(self, x_diff):
        if x_diff is None:
            return "No dribble"
        elif x_diff > 50:
            return "Across"
        else:
            return "Up & Down"

    def run_analysis(self, frame):
        result = self.model(frame, stream=True)
        bounce_types = set()
        speed_types = set()
        dribble_types = set()
        for r in result:
            try:
                box = r.boxes
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                c1, c2 = int((x1 + x2) / 2), int((y1 + y2) / 2)
                cv2.circle(frame, (c1, c2), 10, (255, 0, 0), -1)
                self.queue = self.add_to_queue(c1, c2)
                predicted = self.predict_trajectory()
                try:
                    x,y = predicted[-1]
                    cv2.circle(frame, (int(x), int(y)), 38, (0, 0, 255), 4)
                    if y < c2 and not self.bounce_flag:
                        if self.bounce_time is not None:
                            time_diff = time.time() - self.bounce_time
                            height_diff = self.calculate_height_difference()
                            x_diff = self.calculate_x_difference()
                            self.bounce_type = self.classify_bounce_height(height_diff)
                            bounce_types.add(self.bounce_type)
                            self.speed_type = self.classify_dribble_speed(time_diff)
                            speed_types.add(self.speed_type)
                            self.dribble = self.classify_dribble_direction(x_diff)
                            dribble_types.add(self.dribble)
                        self.bounce_time = time.time()
                        self.bounces += 1
                        self.bounce_flag = True
                    elif y > c2:
                        self.bounce_flag = False
                    cv2.putText(frame, f"Bounces: {self.bounces}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(frame, f"Speed: {self.speed_type}", (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(frame, f"Bounce type: {self.bounce_type}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(frame, f"Direction: {self.dribble}", (20, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    print("Metrics: ", bounce_types, speed_types, dribble_types)
                except:
                    print("No prediction")
                    pass
            except:
                pass
        return frame
        
    def run_video_file(self, vid):
        if vid is not None:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(vid.read())
            cap = cv2.VideoCapture(tfile.name)
            stframe = st.empty()
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 1)
                frame = self.run_analysis(frame)
                stframe.image(frame, channels="RGB")
            cap.release()

            
    def run_webcam(self):
        cap = cv2.VideoCapture(0)
        stframe = st.empty()
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)
            frame = self.run_analysis(frame)
            stframe.image(frame, channels="RGB")
        cap.release()
