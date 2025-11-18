#테트리스

import pygame
import sys
import random


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30 #블록 하나당 30X30 픽셀

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255,0,0)
CYAN = (0,255,255)
YELLOW = (255,255,0)
PURPLE = (128,0,128)
GREEN = (0,255,0)
BLUE = (0,0,255)
ORANGE = (255,165,0)
#각 블록에 맞게 색상 정리

BLOCKS = [
    [ # 0: I 블록(4 X 4) - 긴 막대
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    [ # 1: 0 블록(2X2) - 네모
        [1, 1],
        [1, 1]
    ],
    [ # 2 : T 블록
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0]
    ],
    [ # 3: S 블록(3 X 3) - 번개 모양 1
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0]
    ],
    [ # 4 : Z 블록(3X3) - 번개 모양 2
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0]
    ],
    [ # 5 : J 블록(3 X 3) - ㄴ 반대 모양
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0]
    ],
    [ # 6 : L 블록 (3 X 3) - ㄴ 모양
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0]
    ]
]

BLOCKS_COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE]


#전역변수
#
#
#
#

class Block:
    def __init__(self, x, y, shape_index):
        self.x = x #게임판 기준 가로 위치 (칸 단위 0~9)
        self.y = y #게임판 기준 세로 위치 (칸 단위, 0 ~19)
        self.shape_index = shape_index
        self.shape = BLOCKS[shape_index] # 모양 > 2차원 리스트
        self.color = BLOCKS_COLORS[shape_index] #색
        self.rotation = 0 # 회전 상태(나중에 사용)


    def draw(self, surface):
        #블록의 모양을 순회하며 1인 부분만 그림.
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell == 1:
                    #블록의 실제 화면상 좌표 계산
                    #(블록의 기준 위치 + 현재 칸의 상대 위치) * 칸 크기
                    rect_x = (self.x + x) * BLOCK_SIZE
                    rect_y = (self.y + y) * BLOCK_SIZE

                    #사각형 그리기 (안쪽 채우기)
                    pygame.draw.rect(surface, self.color, (rect_x, rect_y, BLOCK_SIZE, BLOCK_SIZE))

                    #테두리 그리기 > 더 잘보일 수 있
                    pygame.draw.rect(surface, BLACK, (rect_x, rect_y, BLOCK_SIZE, BLOCK_SIZE), 2)

    def rotate(self): #블록을 시계 방향 90도 회전
                      #알고리즘 1. 행렬 전치 > 2. 행렬 좌우 반전

        # 1. 전치(행과 열을 뒤집음 r T)
        new_shape = [
            [self.shape[y][x] for y in range(len(self.shape))]
            for x in range(len(self.shape[0]))
        ]
        # 2. 좌우 반전
        self.shape = [row [::-1] for row in new_shape]




    

# --- 함수 정의 ---
def draw_grid(surface, grid): #인자로 grid 받
    #게임판 배경 임시함수
    #가로 10칸, 세로 20칸 격자

    for x in range(0, 300, BLOCK_SIZE):
        for y in range(0,600, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, GRAY, rect, 1)#1은 두께

    for y, row in enumerate(grid):
        for x, cell_value in enumerate(row):
            if cell_value != 0: #0이 아니다 > 블록이 있으면
                color = BLOCKS_COLORS[cell_value - 1] #1~7 값을 0~6 인덱스 변환
                rect_x = x * BLOCK_SIZE
                rect_y = y * BLOCK_SIZE

                pygame.draw.rect(surface, color, (rect_x, rect_y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(surface, BLACK, (rect_x, rect_y, BLOCK_SIZE, BLOCK_SIZE), 2)
            


# --- 충돌 감지 함수 ---
def check_collision(block, grid):
    #1. 블록의 모양을 순회
    for y, row in enumerate(block.shape):
        for x, cell in enumerate(row):
            if cell == 1:
                #2. 이 칸의 실제 게임판 위 x, y 좌표.
                grid_x = block.x + x
                grid_y = block.y + y

                #3. 충돌 검사.
                #(1) 좌우 벽에 충돌했는가? 0~9 순환.
                if not(0 <= grid_x < 10):
                    return True

                #(2) 바닥에 충돌했는가?
                if grid_y >= 20:
                    return True
                
                #(3) 다른 블록과 겹쳤는가?
                if grid[grid_y][grid_x] != 0:
                    return True

    return False #충돌 없음(안전한 위치다.)


def lock_block(block, grid): #멈춘 블록을 그리드에 고정

    for y, row in enumerate(block.shape):
        for x, cell in enumerate(row):
            if cell == 1: #블록의 그리드 좌표(grid_x, grid_y)
                grid_x = block.x + x
                grid_y = block.y + y

                #그리드에 블록 색인 기록.
                #block 클래스가 자신의 shape_index 알아야 함.

                #색깔 인덱스 저장(임시)
                grid[grid_y][grid_x] = block.shape_index + 1


def clear_lines(grid): #그리드에서 꽉 찬 줄을 찾아 삭제, 빈 줄 추가
    lines_cleared = 0

    #1. 20줄 모두 검사.(위에서부터)
    y = 0
    while y < len(grid): #y가 0부터 20까지 쭉 검사
        row = grid[y]

        #2. 만약 한 줄(10칸)이 모두 0이 아니면(꽉 차면)
        if all(cell_value != 0 for cell_value in row):
            del grid[y] # 그 줄 삭제

            grid.insert(0, [0 for _ in range(10)]) #4. 맨 위 다시 빈 줄 추가

            lines_cleared += 1

            #5. y를 증가시키지 않는다. 윗줄이 내려와 새로운 y줄 생성
            # 그 줄도 다시 검사

        else:
            y += 1 # 다 안 찼으면 다음 줄

    return lines_cleared


                

#--- 메인 함수 ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("테트리스 (Tetris)")
    clock = pygame.time.Clock() #프레임


    last_fall_time = pygame.time.get_ticks()


    """핵심! 2차원 배열 만들기
        세로 20줄(row), 가로 10칸(col) 모두 0으로 채우기
    
    grid = [[0 for col in range(10)] for row in range(20)]
    #파이썬의 리스트 컴프리헨션(List Comprehension) 기능 => 2중 포문 1줄로 간략하게
    # 가로 10칸 만들고 새로 20줄 채워가는거
    """

    program_running = True

    while program_running:
        # 1. 게임 한 판 초기화 구역.
        # 나중에 reset_game() 같은 초기화 코드 넣기
        
        grid = [[0 for col in range(10)] for row in range(20)]

        score = 0 #점수 변수 0점 시작
        
        game_state = "intro" #시작은 인트로
        current_block = Block(3, 0, random.randint(0, 6)) #현재 블록
        next_block = Block(12, 2, random.randint(0, 6)) #다음 블

        
        game_running = True
        while game_running:
            # --- 이벤트 처리 ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    program_running = False #프로그램 전체 종료.

                # --- 인트로 화면 전환 ---
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if game_state == "intro":
                            game_state = "playing"
                            last_fall_time = pygame.time.get_ticks()
                            
                        elif game_state == "playing":
                            game_state = "gameover"

                            
                        elif game_state == "gameover":
                            game_running = False #현재 판 종료 -> 재시작


                    if game_state == "playing":
                        if event.key == pygame.K_LEFT:
                            current_block.x -= 1 #1. 이동
                            if check_collision(current_block, grid): #2. 검사
                                current_block.x += 1 #3. 충돌 시 원위치.
                                
                        elif event.key == pygame.K_RIGHT:
                            current_block.x += 1
                            if check_collision(current_block, grid):
                                current_block.x -= 1

                        elif event.key == pygame.K_UP:
                            old_shape = current_block.shape #1. 원래 모양 기억
                            current_block.rotate() #2. 회전
                            
                            if check_collision(current_block, grid):
                                #충돌 시 원위치(원래 모양)
                                current_block.shape = old_shape

                        elif event.key == pygame.K_SPACE: #스페이스 하드 드롭

                            #1. 충돌(false)까지 계속 내림
                            while not check_collision(current_block, grid):
                                current_block.y += 1

                            current_block.y -= 1 #충돌 시 한칸 원위치

                            lock_block(current_block, grid) # 그 자리 고정

                            lines = clear_lines(grid)
                            if lines > 0:
                                #점수 계산
                                if lines == 1:
                                    score += 100
                                elif lines == 2:
                                    score += 200
                                elif lines == 3:
                                    score += 300
                                elif lines == 4:
                                    score += 400

                            lines = clear_lines(grid) # 줄 삭제 검사


                            current_block = next_block #다음 블록을 현재로
                            current_block.x = 3     #위치 리셋
                            current_block.y = 0

                            next_block = Block(12, 2, random.randint(0, 6))

                            

                            if check_collision(current_block, grid):
                                game_state = "gameover" #게임 오버로 변경

                            last_fall_time = current_time # 타이머 리셋
                            
                        

            if game_state == "playing":
                keys = pygame.key.get_pressed()
                if keys[pygame.K_DOWN]:
                    current_fall_speed = 100
                else:
                    current_fall_speed = 1000

                current_time = pygame.time.get_ticks()
                if current_time - last_fall_time > current_fall_speed:
                    current_block.y += 1

                    if check_collision(current_block, grid): # 충돌 검사
                        current_block.y -= 1 #한 칸 원위치(겹침 방지)

                        lock_block(current_block, grid) #블록을 그리드에 고정


                        lines = clear_lines(grid)
                        if lines > 0:
                            #점수 계산
                            if lines == 1:
                                score += 100
                            elif lines == 2:
                                score += 200
                            elif lines == 3:
                                score += 300
                            elif lines == 4:
                                score += 400
                        

                        #블록 고정 후 즉시 줄 검사
                        lines = clear_lines(grid)

    
                        random_index = random.randint(0, 6) #새 블록 생성
                        current_block = Block(3, 0, random_index)

                        if check_collision(current_block, grid):
                            game_state = "gameover" #게임 오버로 변경

                        last_fall_time = current_time # 타이머 리셋

                    else:    
                        last_fall_time = current_time
                    


            # --- 화면 그리기 ---
            screen.fill(WHITE)

            if game_state == "intro":
                #인트로 화면

                font = pygame.font.Font(None, 60)
                text = font.render("TETRIS", True, BLACK)
                screen.blit(text, (150,250))
                font_2 = pygame.font.SysFont("malgungothic", 30)
                text_2 = font_2.render("엔터를 눌러 시작하세요.", True, BLACK)
                screen.blit(text_2, (150, 300))


            elif game_state == "playing":
                #게임 화면
                draw_grid(screen, grid) #격자 그리기
                current_block.draw(screen)


                font = pygame.font.SysFont("malgungothic", 30)
                score_text = font.render(f"점수 : {score}", True, BLACK)
                screen.blit(score_text, (550, 20)) #오른쪽 상단


                # --- 다음 블록 표시 ---
                font = pygame.font.SysFont("malgungothic", 30)
                next_label = font.render("다음 블록", True, BLACK)
                screen.blit(next_label, (350, 20))

                next_block.draw(screen) #다음 블록 그리기

            elif game_state == "gameover":
                #(임시) 게임 오버 화면
                font = pygame.font.Font(None, 60)
                text = font.render("GAME OVER", True, RED)
                screen.blit(text, (50, 250))
                font_2 = pygame.font.SysFont("malgungothic", 30)
                text_2 = font_2.render("엔터를 눌러 다시 하세요.", True, RED)
                screen.blit(text_2, (50, 350))


            pygame.display.flip()
            clock.tick(60)


    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


 
