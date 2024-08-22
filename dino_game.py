# import libraries
import cv2
import mediapipe as mp
import pyautogui
import math

# initialization
capture_hands = mp.solutions.hands.Hands()
drawing_option = mp.solutions.drawing_utils
camera = cv2.VideoCapture(0)

# frame counter
frame_count = 0

# calculate euclidean distance
def calculate_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

while True:
    # read image
    _, image = camera.read()
    image_height, image_width, _ = image.shape

    # flips the image
    image = cv2.flip(image, 1)

    # convert to rgb
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # detect hand
    output_hands = capture_hands.process(rgb_image)
    all_hands = output_hands.multi_hand_landmarks

    # if hand detected
    if all_hands:
        for hand in all_hands:
            # maps landmarks
            drawing_option.draw_landmarks(image, hand, mp.solutions.hands.HAND_CONNECTIONS)
            one_hand_landmarks = hand.landmark

            # calculate position
            index_finger_tip = [int(one_hand_landmarks[8].x * image_width), int(one_hand_landmarks[8].y * image_height)]
            thumb_tip = [int(one_hand_landmarks[4].x * image_width), int(one_hand_landmarks[4].y * image_height)]

            # circle pointer, thumb fingers
            cv2.circle(image, (index_finger_tip[0], index_finger_tip[1]), 5, (0, 255, 0), cv2.FILLED)
            cv2.circle(image, (thumb_tip[0], thumb_tip[1]), 5, (255, 255, 255), cv2.FILLED)

            distance = calculate_distance(index_finger_tip, thumb_tip)

            # every other frame
            if frame_count % 2 == 0:
                # if farther
                if distance > 60:
                    pyautogui.press('space')

    # increase frame counter
    frame_count += 1

    cv2.imshow("Hand movement video capture", image)
    key = cv2.waitKey(1)

    # if esc break from loop
    if key == 27:
        break

# close camera
camera.release()
cv2.destroyAllWindows()
