
# ui.py
import cv2

class StopButtonUI:
    def __init__(self):
        self.stop_clicked = False
        self.btn = (10, 60, 120, 40)

    def draw_button(self, frame):
        x,y,w,h = self.btn
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), -1)
        cv2.putText(frame, "STOP", (x+20,y+28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    def mouse_callback(self, event, mx, my, flags, param):
        x,y,w,h = self.btn
        if event == cv2.EVENT_LBUTTONDOWN:
            if x <= mx <= x+w and y <= my <= y+h:
                self.stop_clicked = True
