import pygame
import cv2
import sys
import numpy as np
import mediapipe as mp

# Engine init
pygame.init()

# Fenster einstellungen
screen_width, screen_height = 1280, 720                         # double buffering für flüssigeres erlebnis
screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)  
pygame.display.set_caption("4 Granks (4 Gewinnt) mit gestenerkennung")

# Assets
player1_img = pygame.image.load("assets/Frankkopf.png")  
player2_img = pygame.image.load("assets/gramann.png")
background_img = pygame.image.load("assets/background.jpg")

# Assets scalling
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Fonts
title_font = pygame.font.Font(None, 72)  
winner_font = pygame.font.Font(None, 48)

# Init webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    sys.exit()
    
#  Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Variablen
index_tip_pos = None
game_over = False
current_player = 1

# Funktionen
def draw_title(screen, screen_width, title_font):
    title_text = title_font.render("4 Granks", True, (255, 255, 255))
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 10))

#Spiel
running = True
while running:
    # OS Event schließen abfangen und selber handlen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    ret, frame = cap.read()
    if not ret:
        print("Fehler: Frame konnte von der Webcam nicht gelesen werden")
        break
    # OpenCV anpassung für pygame
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results = hands.process(frame_rgb)
    hand_open = False
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame_rgb, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            def landmark_to_point(landmark):
                return np.array([landmark.x, landmark.y])

            index_tip = landmark_to_point(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP])
            index_dip = landmark_to_point(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP])
            index_pip = landmark_to_point(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP])
            index_mcp = landmark_to_point(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP])

            middle_tip = landmark_to_point(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP])
            middle_mcp = landmark_to_point(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP])

            thumb_tip = landmark_to_point(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP])

            # Check hand offen
            hand_open = all(
                hand_landmarks.landmark[i].y < hand_landmarks.landmark[i - 2].y
                for i in [
                    mp_hands.HandLandmark.THUMB_TIP,
                    mp_hands.HandLandmark.INDEX_FINGER_TIP,
                    mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                    mp_hands.HandLandmark.RING_FINGER_TIP,
                    mp_hands.HandLandmark.PINKY_TIP,
                ]
            )
            
            # Check zeige finger ist oben
            is_index_straight = (index_tip[1] < index_dip[1] < index_pip[1] < index_mcp[1])
            are_others_folded = (
                middle_tip[1] > middle_mcp[1] and
                hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y and
                hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y
            )
            is_thumb_far = (np.linalg.norm(index_tip - thumb_tip) > 0.15)
            
            if is_index_straight and are_others_folded and is_thumb_far:
                    # Update zeige finger postion der spitze
                    index_tip_pos = (int((1 - index_tip[0]) * screen_width), int(index_tip[1] * screen_height))

    if hand_open and not game_over:
        current_player = 3 - current_player
        
    # Darstellungen
    screen.blit(background_img, (0, 0))
    draw_title(screen, screen_width, title_font)
    # Spieler anzeige
    if index_tip_pos:
        screen.blit(player1_img if current_player == 1 else player2_img, index_tip_pos)
        
    pygame.display.flip()
# freigabe der resourcen beim schließen
cap.release()
hands.close()
pygame.quit() 
    