import pygame #pygame 라이브러리 가져오기.
import sys # sys는 파이썬 시스템을 제어. (게임 종료 가능.)
import random #돌을 랜덤으로 뿌리기 위해 필요.

SCREEN_WIDTH = 480 # 창 너비 설정
SCREEN_HEIGHT = 640 # 창 높이 설정
ADD_SPEED = 0 #추가 난이도 상승을 위한 변수

WHITE = (255, 255, 255) # 색상 설정.
BLACK = (0, 0, 0)

class Player(pygame.sprite.Sprite):
    #플레이어를 만들기 위한 설계도(Class)
    #pygame.sprite.Sprite은 pygame이 제공하는 게임 물체의 기본 설계도를 상속 받는다는 뜻.

    def __init__(self):
        #__init__ (초기화 함수/생성자)
        #Player 설계도로 실제 플레이어(객체)를 찍어낼 때
        #단 한 번 자동으로 호출되는 함수.
        #self는 객체 자신을 뜻함. (Player1.x = 100 == self.x = 100)
        

        super().__init__() #1. pygame의 Sprite 부모 클래스를 먼저 초기화.(필수)

        self.image = pygame.Surface([40, 50])
        # 2. 가로 40, 세로 50의 사각형 플레이어.
        self.image.fill(BLACK)
        #배경이 흰색이니까 플레이어는 검정으로 잘 보이게.


        #3. 플레이어의 위치 정보를 만들기.
        #self.rect는 pygame이 물체의 위치/크기를 관리하는 사각형 정보.
        self.rect = self.image.get_rect()

        #4. 플레이어의 초기 위치 설정.
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 30 #바닥에서 30픽셀 위

        self.speed = 5

    def update(self): #플레이어의 움직임 처리 함수.

        keys = pygame.key.get_pressed()
        #1. 현재 눌려있는 모든 키의 목록을 가져온다.

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            #왼쪽 키가 눌리면 현재 위치에서 속도만큼 뺀다.(왼쪽 이동.)

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            #왼쪽과 같은 원리로 오른쪽 이동

        if self.rect.left < 0: #왼쪽 벽을 넘어간다면
            self.rect.left = 0 #더이상 못가게 벽에 붙게.

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH #오른쪽은 어디가 끝인지 모르니까 창 크기 변수를 넣어주는거임.




class Stone(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #1. 돌의 모습 구현.(10, 10 크기에 회색.)
        self.image = pygame.Surface([10, 10])
        self.image.fill((128, 128, 128))


        #2. 돌의 위치 정보
        self.rect = self.image.get_rect()

        #3. 초기 위치 설정(랜덤)
        self.rect.x = random.randrange(0, SCREEN_WIDTH - 30) #화면 위 쪽에서 시작해서 안 보이게

        self.rect.y = random.randrange(-100, -40)
        
        self.speedy = random.randrange(3, 8)


    def update(self):
        self.rect.y += self.speedy

        if self.rect.top > SCREEN_HEIGHT: #다시 올라가서 재활용.
            self.rect.x = random.randrange(0, SCREEN_WIDTH - 30)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 8) + ADD_SPEED
            

        

        

        

def main(): # 메인 함수 > start_game과 같은 맥락.
    global ADD_SPEED #전역 변수 수정 권한 얻기

    
    pygame.init() #pygame 초기화. > 필수 과정

    #창 크기 설정 및 생성.
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    #창 제목 설정
    pygame.display.set_caption("돌 피하기(V0.1)")


    #실시간 루프를 위한 시계 생성.
    #input()은 멈추는 데 시계는 루프 속도를 제어하며 계속 흐르게 감.
    clock = pygame.time.Clock()


    all_sprites = pygame.sprite.Group() #모든 물체를 담는 큰 그릇
    stones = pygame.sprite.Group() #돌만 따로 담는 그릇(충돌 검사용)

    player = Player()
    all_sprites.add(player)

    for i in range(8):
        stone = Stone()
        all_sprites.add(stone)
        stones.add(stone)

    title_font = pygame.font.SysFont("malgungothic", 60, bold = True)
    #폰트 맑은 고딕 60 굵게

    menu_font = pygame.font.SysFont("malgungothic", 40)

    title_text = title_font.render("돌 피하기(V0.1)", True, BLACK)
    start_text = menu_font.render("게임 시작", True, BLACK)
    quit_text = menu_font.render("게임 나가기", True, BLACK)

    title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, 150))
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH/2, 350))
    quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH/2, 450))
    


    game_state = "intro"
    start_ticks = pygame.time.get_ticks() #게임 시작 시점의 시간 기록.


    
    running = True #while True와 같은 효과.

    while running:

        for event in pygame.event.get():
            #루프가 돌 때마다 이벤트 확인.

            if event.type == pygame.QUIT: #종료 이벤트 발생시
                pygame.quit()
                sys.exit()

            if game_state == "intro":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #마우스가 클릭됐는지 확인.
                    if start_rect.collidepoint(event.pos): #게임 시작 클릭

                        game_state = "playing" #게임 중으로 변경.
                        start_ticks = pygame.time.get_ticks()
                        #게임 시간 리셋

                    elif quit_rect.collidepoint(event.pos): #게임 나가기 클릭
                        pygame.quit()
                        sys.exit()



                    

        if game_state == "intro":
            screen.fill(WHITE)
            screen.blit(title_text, title_rect)
            screen.blit(start_text, start_rect)
            screen.blit(quit_text, quit_rect)



        elif game_state == "playing":
            all_sprites.update()
            #모든 물체의 update() 함수를 일괄 실행.

            hits = pygame.sprite.spritecollide(player, stones, False)
            #충돌 검사 : 플레이어와 돌 그룹이 부딪혔는지를 확인,
            #Ture면 돌이 사라지고 False면 부딪혀도 돌이 남아있음.

            if hits:
                running = False #게임 종료
                

        

            #화면 그리기
            #화면을 흰색으로 덮어씌워 지우기.
            screen.fill(WHITE)


            # 1. 경과 시간 계산 (현재 시간 - 시작 시간) / 1000 = 초 단위 시간
            r_time = (pygame.time.get_ticks() - start_ticks) / 1000
    
            # 2. 시간 표시할 폰트 설정
            timer_font = pygame.font.Font(None, 36)

            # 3. 글자 그리기(소수점 첫째 자리까지 표시)
            timer_text = timer_font.render(f"Time: {r_time:.1f}s", True, (0,0,0))
    
        
            # 4. 화면 왼쪽 위 표시
            screen.blit(timer_text, (10,10))
    
            ADD_SPEED = int(r_time / 5)
        
        
            all_sprites.draw(screen) #화면에 그리는거임.


        pygame.display.flip() #그린 걸 실제화면에 업데이트 함.
        clock.tick(60) #루프 속도 제어. 1초에 60번 반복 60 FPS


        #1. 게임 루프가 끝났다는 거는 2가지 뜻이 있음.
        #플레이어가 스스로 게임을 종료 or 게임 오버. < 이 상황에 메세지 띄우기

    font = pygame.font.Font(None, 74) #None 기본 폰트 / 74는 크기
    text = font.render("GAME OVER", True, (255,0,0)) #빨간 게임 오버
    text_rect = text.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(text, text_rect) #화면 글자 그리기
    pygame.display.flip() # 화면 업데이트

    pygame.time.wait(2000) # 2초정도의 시간 유지



        #루프가 끝나고 게임 종료.
    pygame.quit()
    sys.exit()



            
            


                
if __name__ == "__main__":
    main()

        
