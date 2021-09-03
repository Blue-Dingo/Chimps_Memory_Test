#################################################################
# ### import
import pygame
from random import *

#################################################################
# ### pygame 초기화
pygame.init()

screen_w, screen_h = 1080, 480
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Chimp's Memory Test")

#################################################################
# constance & variables
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

cell_size = 120
button_size = 100  # 마진 줘서 button끼리 구분되게
screen_x_margin = 50  # 화면 여백
screen_y_margin = 50
num_rows = (screen_h-screen_y_margin*2) // cell_size
num_cols = (screen_w-screen_x_margin*2) // cell_size
offset_x = (screen_w-screen_x_margin*2) % cell_size + \
    screen_x_margin  # 여백과 짜투리빼고 실제 cell 시작 x좌표
offset_y = (screen_h-screen_y_margin*2) % cell_size + screen_y_margin

game_font = pygame.font.Font(None, 60)

buttons = []  # 문제버튼리스트 (rect)
game_start = False
hidden = False  # 힌트감추기
start_ticks = None  # 힌트감추기를 위한 타이머
display_time = None  # hidden 되기까지의 시간
level = 1

#################################################################
# funcs


def Display_Start_Screen():
    pygame.draw.circle(screen, WHITE, start_button.center, 60, 5)


def Display_Game_Screen():
    global hidden
    global start_ticks
    global display_time

    # 타이머 후 자동 감추기
    if not hidden:
        elapsed = pygame.time.get_ticks()-start_ticks
        if elapsed > display_time*1000:
            hidden = True

    for n, button in enumerate(buttons, start=1):
        if hidden:
            # 박스만 보이기
            pygame.draw.rect(screen, WHITE, button)
        else:
            # 테두리와 숫자 보이기
            pygame.draw.rect(screen, WHITE, button, 5)
            text = game_font.render(str(n), True, WHITE)
            screen.blit(text, text.get_rect(center=button.center))


def Display_GameOver_Screen(level):
    screen.fill(BLACK)
    text1 = game_font.render("Game Over", True, YELLOW)
    text2 = game_font.render(f"Lv. {level}", True, YELLOW)
    rect1 = text1.get_rect(center=(screen_w/2, screen_h/2))
    rect1.top -= 50
    rect2 = text2.get_rect(center=(screen_w/2, screen_h/2))
    rect2.top += 50
    screen.blit(text1, rect1)
    screen.blit(text2, rect2)


def Check_NumberButton(pos):
    global game_start
    global running
    global level
    global hidden

    for button in buttons:
        if button.collidepoint(pos):
            # 1번 클릭시 hidden
            if button == buttons[0]:
                buttons.remove(button)
                hidden = True
            # 틀리면 종료
            else:
                running = False
            break
    # 다 맞추면 레벨업
    if len(buttons) == 0:
        level += 1
        game_start = False


def Check_Button(pos):
    global game_start
    # 문제버튼 클릭 확인
    if game_start:
        Check_NumberButton(pos)
    # 시작버튼 클릭 확인
    elif start_button.collidepoint(pos):
        game_start = True
        Setup(level)


def Setup(level):
    global hidden
    global start_ticks
    global display_time

    hidden = False
    start_ticks = pygame.time.get_ticks()  # hidden 타이머 시작
    display_time = 5 - (level//3)   # display_time 후 hidden
    display_time = max(display_time, 1)  # 최소 1초

    # 랜덤 grid 맵 작성 후, 그에 해당하는 버튼리스트 생성 (rect)
    grid = [[0 for col in range(num_cols)] for row in range(num_rows)]

    num_buttons = level//3 + 5
    num_buttons = min(num_buttons, 20)  # 최대 20개

    n = 1
    while (n <= num_buttons):
        row = randrange(0, num_rows)
        col = randrange(0, num_cols)
        if grid[row][col] == 0:
            grid[row][col] = n
            n += 1

            center_x = offset_x + col*cell_size+cell_size/2
            center_y = offset_y + row*cell_size+cell_size/2
            button = pygame.Rect(0, 0, button_size, button_size)
            button.center = (center_x, center_y)
            buttons.append(button)


#################################################################
# 시작 버튼

start_button = pygame.Rect(0, 0, 120, 120)
start_button.center = (120, screen_h-120)  # center좌표 지정으로 rect값 재조정


#################################################################
# ### 구동 loop
running = True
while running:
    click_pos = None

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.MOUSEBUTTONUP:
            click_pos = pygame.mouse.get_pos()  # or evnet.pos

    screen.fill(BLACK)

    if game_start:
        Display_Game_Screen()
    else:
        Display_Start_Screen()

    if click_pos:
        Check_Button(click_pos)

    pygame.display.update()

Display_GameOver_Screen(level)
pygame.display.update()

pygame.time.delay(2000)
pygame.quit()
