import pygame
import random
import time
import requests
from io import BytesIO
from PIL import Image

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
CARD_SIZE = 175
GRID_SIZE = 4
WHITE = (255, 255, 255)
FLIP_DELAY = 0.3
BUTTON_WIDTH = 150
BLACK = (0, 0, 0)
BUTTON_HEIGHT = 50
TIMER_LIMIT = 90


image_urls = [
    "https://i.pinimg.com/564x/4a/96/07/4a96076997d63ac600ce1b79dfa99ac7.jpg",
    "https://i.pinimg.com/564x/a0/ee/bf/a0eebfd11d47eece75fa8593895b8e22.jpg",
    "https://i.pinimg.com/564x/46/00/45/460045bb38a915f849506facf1a7c510.jpg",
    "https://i.pinimg.com/564x/2e/86/b6/2e86b6af557d73772cfda869819010fb.jpg",
    "https://i.pinimg.com/564x/00/71/a6/0071a6a0fa67c9543c16703d2f48c2a3.jpg",
    "https://i.pinimg.com/564x/0f/14/49/0f1449780ee68a1b49509414a37e7ea7.jpg",
    "https://i.pinimg.com/564x/07/d6/37/07d63788be282dc4e49a21be34fdafc7.jpg",
    "https://i.pinimg.com/564x/6f/9b/05/6f9b05dafa86d1920f70d0ca8559cb52.jpg"
]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memory Puzzle Game")


response = requests.get(
    "https://i.pinimg.com/564x/da/3d/bc/da3dbcecce7355b17b8c6f9649af73a3.jpg")
image = Image.open(BytesIO(response.content))
image = image.convert("RGB")
with BytesIO() as img_bytes:
    image.save(img_bytes, "PNG")
    img_bytes.seek(0)
    card_back = pygame.image.load(img_bytes)

card_images = []
for url in image_urls:
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image = image.convert("RGB")
    with BytesIO() as img_bytes:
        image.save(img_bytes, "PNG")
        img_bytes.seek(0)
        card_images.append(pygame.image.load(img_bytes))


card_images *= 2
random.shuffle(card_images)
card_state = [False] * (GRID_SIZE ** 2)

flipped_cards = []
matched_pairs = 0
moves = 0
timer_start_time = time.time()

font = pygame.font.Font(None, 40)


def point_in_rect(point, rect):
    x, y = point
    rx, ry, rw, rh = rect
    return rx < x < rx + rw and ry < y < ry + rh
def draw_timer():
    elapsed_time = max(0, int(time.time() - timer_start_time))
    remaining_time = max(0, TIMER_LIMIT - elapsed_time)
    timer_text = font.render(f"Time: {remaining_time}s", True, BLACK)
    screen.blit(timer_text, (SCREEN_WIDTH - 180, 10))
def display_message(message):
    message_text = font.render(message, True, BLACK)
    text_rect = message_text.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(message_text, text_rect)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            restart_button_rect = (
                SCREEN_WIDTH - BUTTON_WIDTH - 20, 20, BUTTON_WIDTH, BUTTON_HEIGHT)
            if point_in_rect((mouse_x, mouse_y), restart_button_rect):
                random.shuffle(card_images)
                card_state = [False] * (GRID_SIZE ** 2)
                flipped_cards = []
                matched_pairs = 0
                moves = 0
                timer_start_time = time.time()
            else:
                col = mouse_x // CARD_SIZE
                row = mouse_y // CARD_SIZE
                index = row * GRID_SIZE + col
                if not card_state[index] and len(flipped_cards) < 2:
                    card_state[index] = True
                    flipped_cards.append(index)
                    moves +=1
    screen.fill(WHITE)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            index = i * GRID_SIZE + j
            pygame.draw.rect(screen, WHITE, (j * CARD_SIZE,
                                             i * CARD_SIZE, CARD_SIZE, CARD_SIZE))
            if card_state[index] or index in flipped_cards:
                card = card_images[index]
            else:
                card = card_back
            card = pygame.transform.scale(card, (CARD_SIZE - 8, CARD_SIZE - 8))
            screen.blit(card, (j * CARD_SIZE + 4, i * CARD_SIZE + 4))


    moves_text = font.render(f"Moves: {moves}", True, WHITE)
    screen.blit(moves_text, (10, 10))



    draw_timer()

    if len(flipped_cards) == 2:
        time.sleep(FLIP_DELAY)
        if card_images[flipped_cards[0]] == card_images[flipped_cards[1]]:
            matched_pairs += 1
            flipped_cards = []
        else:
            card_state[flipped_cards[0]] = False
            card_state[flipped_cards[1]] = False
            flipped_cards = []

    if matched_pairs == GRID_SIZE ** 2 // 2:
        display_message("Congratulations! You found all the pairs:)")
        pygame.display.flip()
        time.sleep(2)
        running = False

    elapsed_time = time.time() - timer_start_time
    if elapsed_time >= TIMER_LIMIT:
        display_message("Time's up! You lost the game:(")
        pygame.display.flip()
        time.sleep(2)
        running = False

    pygame.display.flip()

pygame.quit()
