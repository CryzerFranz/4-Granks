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
cell_size = 70
player1_img = pygame.transform.scale(player1_img, (cell_size - 10, cell_size - 10))
player2_img = pygame.transform.scale(player2_img, (cell_size - 10, cell_size - 10))

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
board = [[0 for _ in range(7)] for _ in range(6)]  # 6x7 board
index_tip_pos = None
game_over = False
current_player = 1

button_color = (200, 0, 0)
button_hover_color = (255, 155, 0)
button_rect = pygame.Rect(screen_width - 150, 20, 120, 50)  # Close button
restart_button_rect = pygame.Rect(screen_width // 2 - 60, screen_height // 2 + 50, 120, 50)

# Funktionen
def draw_title(screen, screen_width, title_font):
    title_text = title_font.render("4 Granks", True, (255, 255, 255))
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 10))
    
def draw_board(screen_width, screen_height, screen, player1_img, player2_img, cell_size, board):
    from main import screen_width, screen_height  
    board_color = (30, 144, 255)  # Dodger Blue
    board_x = int(screen_width // 2 - 3.5 * cell_size)  # Center the board (convert to int)
    board_y = int(screen_height // 2 - 3 * cell_size)  # Convert to int

    for row in range(6):
        for col in range(7):
            cell_x = board_x + col * cell_size
            cell_y = board_y + row * cell_size
            pygame.draw.rect(screen, board_color, (cell_x, cell_y, cell_size, cell_size))
            pygame.draw.rect(screen, (0, 0, 0), (cell_x, cell_y, cell_size, cell_size), 2)
            pygame.draw.circle(screen, (0, 0, 0), (cell_x + cell_size // 2, cell_y + cell_size // 2), cell_size // 3)
            if board[row][col] == 1:
                screen.blit(player1_img, (cell_x + 5, cell_y + 5))
            elif board[row][col] == 2:
                screen.blit(player2_img, (cell_x + 5, cell_y + 5))
                
def check_winner(board, player):
    # Check rows, columns, and diagonals for a win
    for row in range(6):
        for col in range(7 - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    for row in range(6 - 3):
        for col in range(7):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    for row in range(6 - 3):
        for col in range(7 - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    for row in range(3, 6):
        for col in range(7 - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def draw_close_button(screen, button_color, button_hover_color, button_rect, font):
    mouse_pos = pygame.mouse.get_pos()
    color = button_hover_color if button_rect.collidepoint(mouse_pos) else button_color
    pygame.draw.rect(screen, color, button_rect)
    close_text = font.render("X", True, (255, 255, 255))
    screen.blit(close_text, (button_rect.x + 10, button_rect.y + 10))
    

def draw_restart_button(screen, button_color, button_hover_color, button_rect, font):
    mouse_pos = pygame.mouse.get_pos()
    color = button_hover_color if button_rect.collidepoint(mouse_pos) else button_color
    pygame.draw.rect(screen, color, button_rect)
    restart_text = font.render("Neu", True, (255, 255, 255))
    screen.blit(restart_text, (button_rect.x + 10, button_rect.y + 10))

#Spiel
running = True
while running:
    # OS Event schließen abfangen und selber handlen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
           if button_rect.collidepoint(event.pos):  # Close button
               running = False
           if game_over and restart_button_rect.collidepoint(event.pos):  # Restart button
               # Reset the game
               board = [[0 for _ in range(7)] for _ in range(6)]
               game_over = False
               current_player = 1
    
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
    draw_board(screen_width, screen_height, screen, player1_img, player2_img, cell_size, board)
    
    # Spieler anzeige
    if index_tip_pos:
        screen.blit(player1_img if current_player == 1 else player2_img, index_tip_pos)
    
    if game_over:
        draw_restart_button(screen, button_color, button_hover_color, restart_button_rect, winner_font)
    
    draw_close_button(screen, button_color, button_hover_color, button_rect, winner_font)
    
    pygame.display.flip()
# freigabe der resourcen beim schließen
cap.release()
hands.close()
pygame.quit() 
    