import cv2
import mediapipe as mp
import numpy as np

import threading
import pygame


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Initialize pygame mixer
pygame.mixer.init()
# Load sound
pygame.mixer.music.load("go_lower.mp3")

def must_go_lower():
    print("Must go lower!")
    pygame.mixer.music.play()
    
    

np_drawing = mp.solutions.drawing_utils
np_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)
### Setup mediapipe instance
with np_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.6) as pose:

    # Initialize variables
    display_must_go_lower_counter = 0
    not_low_enough = False
    has_gone_down = False
    pushup_stage_frames = 0
    number_of_pushups = 0
    stage = None # stage of the pushup

    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor Image to rgb
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make Detections
        results = pose.process(image)

        # Recolor Image to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


        #Extract Landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            #print(landmarks)
        except:
            pass




        # Render detections
        np_drawing.draw_landmarks(image, results.pose_landmarks, np_pose.POSE_CONNECTIONS,
                                  np_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  np_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                  )


        # Render left_angle 
        left_angle = None
        try:
            left_shoulder = [landmarks[np_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[np_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[np_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[np_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[np_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[np_pose.PoseLandmark.LEFT_WRIST.value].y]
            left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            #print(f'left_angle : ', left_angle)

            cv2.putText(image, f"{left_angle:.1f}", tuple(np.multiply(left_elbow, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX,
                        .5, (255, 0, 0), 1, cv2.LINE_AA)
        except:
            pass


        # Render right_angle
        right_angle = None
        try:
            right_shoulder = [landmarks[np_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[np_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [landmarks[np_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[np_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist = [landmarks[np_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[np_pose.PoseLandmark.RIGHT_WRIST.value].y]
            right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            #print(f'right_angle : ', right_angle)

            cv2.putText(image, f"{right_angle:.1f}", tuple(np.multiply(right_elbow, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX,
                        .5, (255, 0, 0), 1, cv2.LINE_AA)
        except:
            pass


        body_angle = None
        # Render body angle
        try:

            right_hip = [landmarks[np_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[np_pose.PoseLandmark.RIGHT_HIP.value].y]
            right_shoulder = [landmarks[np_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[np_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

            # calculate angle relative to the horizontal line
            point_above_hip = [right_hip[0], right_hip[1] - 0.1]  # A point slightly above the hip
            body_angle = calculate_angle(point_above_hip, right_hip, right_shoulder) - 90 # Adjusting for the horizontal line
            #print(f'body angle : ', angle)

            cv2.putText(image, f"{body_angle:.1f}", tuple(np.multiply(right_hip, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX,
                        .5, (255, 0, 0), 1, cv2.LINE_AA)
            
            # render point above hip
            point_above_hip = [right_hip[0], right_hip[1] - 0.1]  # A point slightly above the hip
            cv2.circle(image, tuple(np.multiply(point_above_hip, [640, 480]).astype(int)), 5, (0, 255, 0), -1)

        except:
            pass
        


        
        # Pushup counter logic state machine
        
        chosen_angle = None
        if left_angle:
            chosen_angle = left_angle

        elif right_angle:
            chosen_angle = right_angle
        
        if chosen_angle: # check if angle is not None     
            if chosen_angle > 160: 
                stage = "up"
                if pushup_stage_frames != 0:
                    pushup_stage_frames += -1
                else:
                    if has_gone_down:
                        number_of_pushups += 1
                        has_gone_down = False
                        not_low_enough = False
                        pushup_stage_frames = 0
                    if not_low_enough:
                        number_of_pushups += 1
                        has_gone_down = False
                        not_low_enough = False
                        pushup_stage_frames = 0
                        
                        must_go_lower()
                        display_must_go_lower_counter = 30 * 5# in frames at 30 fps

            if pushup_stage_frames < 3:
                if chosen_angle < 90:
                    stage = "down"
                    pushup_stage_frames += 1
                elif chosen_angle < 130: # not low enough
                    not_low_enough = True
                    
            else:
                has_gone_down = True
                
                
                

                
                
        
        # show must go lower
        if display_must_go_lower_counter > 0:
            cv2.putText(image, "Go lower!", (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            display_must_go_lower_counter -= 1
            display_must_go_lower_counter += -1
        
                
        
            

        # render number of pushups 
        cv2.putText(image, f"Pushups: {number_of_pushups}", (400, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        # render stage
        cv2.putText(image, f"{stage}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        # render fps
        fps = cap.get(cv2.CAP_PROP_FPS)
        cv2.putText(image, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        

        cv2.imshow('Mediapipe Feed', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()




