import cv2
import mediapipe as mp
import pyautogui
x1 = y1 = x2 = y2 = 0
# Initialize webcam
webcam = cv2.VideoCapture(0)
if not webcam.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Initialize MediaPipe Hands
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

while True:
    # Capture frame from webcam
    ret, image = webcam.read()
    if not ret:
        print("Error: Could not read frame from webcam.")
        break
    
    # Get frame dimensions
    image = cv2.flip(image,1)
    frame_height, frame_width, _ = image.shape
    
    # Convert BGR to RGB for MediaPipe processing
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks
    
    # If hands are detected
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:  # Tip of the index finger
                    cv2.circle(image, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                    x1=x
                    y1=y
                if id == 4:  # Base of the thumb
                    cv2.circle(image, center=(x, y), radius=8, color=(0, 0, 255), thickness=3)
                    x2=x
                    y2=y
        dist = ((x2-x1)**2 + (y2-y1)**2)**0.5//4
        cv2.line(image,(x1,y1),(x2,y2),(0,255,0),5)
        if dist > 50:
            pyautogui.press("volumeup")
        else:
            pyautogui.press("volumedown")
    # Display the video feed
    cv2.imshow("Hand Volume Control using Python", image)
    
    # Exit loop on pressing ESC key
    key = cv2.waitKey(10)
    if key == 27:  # ESC key
        break

# Release resources
webcam.release()
cv2.destroyAllWindows()
