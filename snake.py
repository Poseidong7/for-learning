import sys
import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BLOCK_SIZE = 40 #뱀 한칸의 크기
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)


# --- 격자 함수 ---
def draw_grid(surface): 
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE): #X 중앙
        for y in range(BLOCK_SIZE * 2, SCREEN_HEIGHT, BLOCK_SIZE): #Y 중앙
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE) #rect 변수에 사이즈 넣고
            pygame.draw.rect(surface, GRAY, rect, 1) # 그리기

def spawn_food(current_snake_body):
    while True:
        food_pos = (random.randint(0, 19), random.randint(2, 19)) # y를 2부터 시작해 점수판 피하기
        if food_pos not in current_snake_body:
            return food_pos #뱀 몸통에 없으면 확정


# --- 메인 함수 ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("스네이크 게임")
    clock = pygame.time.Clock()


    # --- 프로그램 구동 ---
    program_running = True
    while program_running:
        # --- 게임 한 판 초기화 ---
        snake_body = [(10, 10), (9, 10), (8, 10)]
        direction = (1, 0) #뱀의 초기 방향 (1 = 오른쪽, 0 = 안움직임)
        game_state = "intro"
        score = 0
        
        food_pos = spawn_food(snake_body)
            


        game_running = True
        while game_running:
            #1. 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    program_running = False #X 누르면 전체 종료


            # 1-1. 인트로 화면 전환
            if event.type == pygame.KEYDOWN: # 상태 전환 엔터
                if event.key == pygame.K_RETURN:
                    if game_state == "intro":
                        game_state = "playing"
                    elif game_state == "gameover":
                        game_running = False #재시작

                # 뱀 방향 전환
                if game_state == "playing":
                    if event.key == pygame.K_LEFT and direction != (1, 0):
                        direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                        direction = (1, 0)
                    elif event.key == pygame.K_UP and direction != (0, 1):
                        direction = (0, -1)
                    elif event.key == pygame.K_DOWN and direction != (0, -1):
                        direction = (0, 1)
            

            # game_state가 playing 일때만 뱀이 움직임
            if game_state == "playing":  

                #2. 로직 업데이트 (선입선출) > 그리기 전 위치 먼저 계산
                current_head = snake_body[0]
                new_head = (current_head[0] + direction[0], current_head[1] + direction[1])
                
                #범위에 부딪히면 게임 종료
                if new_head[0] < 0 or new_head[0] >= 20 or new_head[1] < 2 or new_head[1] > 19 or new_head in snake_body:
                    game_state = "gameover"
                
                else: #충돌 하지 않았을 때만 뱀이 움직임
                    snake_body.insert(0, new_head)
                    
                    # 먹기 로직
                    if new_head == food_pos:
                        score += 1
                        food_pos = spawn_food(snake_body)
                    else:
                        snake_body.pop() #꼬리를 리스트 뒤에서 제거
                    

            # 3. 화면 지우기
            screen.fill(WHITE)

            # 3-1. 화면 격자 그리기
            draw_grid(screen)

            if game_state == "intro":
                screen.fill(WHITE) #인트로 흰색
                font = pygame.font.Font(None, 60)
                text = font.render("SNAKE GAME", True, GREEN)
                screen.blit(text, (250, 300))
                font_2 = pygame.font.SysFont("malgungothic", 30)
                text_2 = font_2.render("엔터를 눌러 게임을 시작하세요", True, BLACK)
                screen.blit(text_2, (250, 400))

            elif game_state == "playing": # 게임 중일 때 뱀 그리기
                screen.fill(BLACK)
                draw_grid(screen)
                
                # A. 뱀 그리기 (그리드 -> 픽셀 변환)
                for segment in snake_body:
                    # segment[0] * BLOCK_SIZE = x 픽셀 좌표
                    # segment[1] * BLOCK_SIZE = y 픽셀 좌표
                    pygame.draw.rect(screen, GREEN, (segment[0] * BLOCK_SIZE, segment[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

                # B 먹이 그리기
                pygame.draw.rect(screen, RED, (food_pos[0] * BLOCK_SIZE, food_pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


                # C 점수 및 랭크 표시
                font = pygame.font.SysFont("malgungothic", 30)
                scroe_text = font.render(f"점수 : {score}", True, WHITE)
                screen.blit(scroe_text, (10, 10))

                rank = "뱀린이"
                if score >= 30:
                    rank = "용"
                elif score >= 20:
                    rank = "이무기"
                elif score >= 10:
                    rank = "도마뱀"
                rank_text = font.render(f"랭크 : {rank}", True, WHITE)
                screen.blit(rank_text, (200, 10))


            elif game_state == "gameover":
                screen.fill(BLACK)
                draw_grid(screen)
                font = pygame.font.Font(None, 60)
                text = font.render("GAME OVER", True, RED)
                screen.blit(text, (250, 300))
                font_2 = pygame.font.SysFont("malgungothic", 30)
                text_2 = font_2.render("엔터를 눌러 재시작하세요.", True, BLACK)
                screen.blit(text_2, (250, 400))
            
            # 4. 화면 업데이트
            pygame.display.flip()


            # 5. 속도 조절
            clock.tick(10) #초당 15 프레임

    pygame.quit()
    sys.exit()

main()
