import os
# import os는 Python에 내장된 운영체제 관련 기능을 가져온다.
# 화면을 지우는 기능 os.system을 쓰기 위해 필요.
import random
# import random은 random으로 숫자를 설정해줌.

def clear_screen():
    """화면을 깨끗하게 지우는 함수."""
    os.system('cls' if os.name == 'nt' else 'clear')
    #윈도우는 cls, 맥이나 리눅스는 clear로 화면을 지운다.

def battle(enemy_name, player_lives): #매개변수를 줘야될 거 같음.
    """게임 배틀룰 가위바위보 미니게임 함수
        1. while True 루프로 비기기 구현.
        2. return 값으로 현재 목숨 player_lives 반환."""
    clear_screen()
    print("--- [전투 발생!] ---")
    print(f"{enemy_name}이(가) 당신에게 배틀을 신청한다!")
    print(f"현재 목숨 : {player_lives}")
    print("------------------\n")

    outcome = "loss" #기본값 패배.
    
    while True:
        print("1. 가위")
        print("2. 바위")
        print("3. 보")

        user_choice = input("\n무엇을 내시겠습니까? > ")

        options = ["가위", "바위", "보"]
        computer_choice = random.choice(options)

        if user_choice == '1':
            user_move = "가위"
        elif user_choice == '2':
            user_move = "바위"
        elif user_choice == '3':
            user_move = "보"
        else:
            print("잘못된 선택입니다! 딴 생각을 하다가 한 대 맞았습니다...")
            player_lives -= 1
            print(f"현재 목숨 : {player_lives}")
            print("--------------------")
            continue

        print(f"\n당신은 [{user_move}] 를 냈습니다.")
        print(f"{enemy_name} 은(는) [{computer_choice}] 를 냈습니다.\n")

        if user_move == computer_choice:
            print("...비겼습니다! 다시 한 판!")
            print("--------------------")
            continue #continue가 루프 처음으로 다시 돌아가는거임.
        
        elif (user_move == "가위" and computer_choice == "보") or (user_move == "바위" and computer_choice == "가위") or (user_move == "보" and computer_choice == "바위"):
            print(f"...이겼습니다! {enemy_name} (이)가 패배를 인정합니다.")
            outcome = "win"
            break
        else:
            print("...졌습니다.")
            player_lives -= 1
            print(f"현재 목숨 : {player_lives}")
            outcome = "loss"
            break

    #---[2. 'Game Over 처리 및 목숨 값 리턴.'] ---
    if player_lives <= 0:
        print("\n=======================")
        print("모든 목숨을 잃었습니다... Game Over")
        print("\n=======================")
        input("...아무 키나 눌러 메인 메뉴로 돌아갑니다.")
    else:
        input("전투 종료. (아무 키나 눌러 돌아가세요.)")

    clear_screen()

    return player_lives, outcome #최종 목숨 값과 승패 반환.




def boss_battle(enemy_name, player_lives):
    boss_lives = 3
    clear_screen()
    print("--- [전투 발생!] ---")
    print(f"{enemy_name}이(가) 당신에게 배틀을 신청한다!")
    print(f"현재 목숨 : {player_lives}")
    print(f"남은 보스 목숨 : {boss_lives}")
    print("------------------\n")

    while True:
        print("1. 가위")
        print("2. 바위")
        print("3. 보")

        user_choice = input("\n무엇을 내시겠습니까? > ")

        options = ["가위", "바위", "보"]
        computer_choice = random.choice(options)

        if user_choice == '1':
            user_move = "가위"
        elif user_choice == '2':
            user_move = "바위"
        elif user_choice == '3':
            user_move = "보"
        else:
            print("잘못된 선택입니다! 딴 생각을 하다가 한 대 맞았습니다...")
            player_lives -= 1
            print(f"현재 목숨 : {player_lives}")
            print(f"남은 보스 목숨 : {boss_lives}")
            print("--------------------")
            continue

        print(f"\n당신은 [{user_move}] 를 냈습니다.")
        print(f"{enemy_name} 은(는) [{computer_choice}] 를 냈습니다.\n")

        if user_move == computer_choice:
            print("...비겼습니다! 다시 한 판!")
            print("--------------------")
            continue #continue가 루프 처음으로 다시 돌아가는거임.
        
        elif (user_move == "가위" and computer_choice == "보") or (user_move == "바위" and computer_choice == "가위") or (user_move == "보" and computer_choice == "바위"):
            boss_lives -= 1
            if boss_lives <= 0:
                print(f"...이겼습니다! {enemy_name} (이)가 패배를 인정합니다.")
                break
            else:
                print(f"{enemy_name}이(가) 고통에 몸부림 칩니다.")
                print(f"남은 보스 목숨 : {boss_lives}")
                continue
        
            
        else:
            player_lives -= 1
            print(f"현재 목숨 : {player_lives}")
            if player_lives <= 0:
                print("전투에서 패배했습니다.. Game Over")
                break
            else:
                continue

    if player_lives <= 0:
        input("\n...아무 키나 눌러 돌아갑니다.")
    else:
        input("\n...전투 승리..!!(아무 키나 눌러 돌아가세요.)")


    clear_screen()

    return player_lives




def display_main_menu():
    """
    def로 메뉴를 그리는 기능을 묶어두면 나중에
    메뉴를 보여주고 싶을 때마다 dis~menu()라고 호출하면 바로 사용 가능.
    """

    print("=" * 70) #'=' 문자를 70번 반복해서 출력.(구분선)
    print("") # 여백 만들기

    print("가위바위보 용사".center(70))
    #"문자열".center(숫자)는 해당 문자열을 숫자 만큼의 공간 중앙에 배치.
    print("")
    print("")
    print("1. 게임 시작".center(70))
    print("2. 게임 나가기".center(70))
    print("")
    print("="*70)


def start_game():
    """게임을 시작하고, 캐릭터 이름 설정을 진행."""
    clear_screen()
    player_name = input("당신의 이름을 설정해주세요: ")
    print(f"\n{player_name}이군요. 멋진 이름입니다! 모험을 시작합니다!\n")
    clear_screen()

    
    
    print("이 세계는 가위바위보로 모든 것을 정하는 세계.. 바위조아 제국의 황제 시저스에게는 사랑스러운 딸이 있었다.")
    print("그녀의 이름은 페이피.. 그녀의 미모는 왕국 그 누구보다 아름다워 평소 그를 흠모하던 마물 드래고니아는")
    print(f"그녀를 납치하고 만다.. 이 사실을 안 황제 시저스는 용사 {player_name}에게 도움을 청한다.")

    player_lives = 3 #목숨 3개 받고 시작.
    
    while True:

        print("")
        print("1. 방을 살펴본다.\n")
        print("2. 방을 나가 마을을 둘러본다.\n")
        print("3. 서둘러 성으로 향한다.(게임 진행)\n")
        print("4. 메인 메뉴로 돌아가기(게임 종료)")

        print(f"\n ---[현재 위치 : 집 / 남은 목숨 : {player_lives} ---")
        command = input(f"[{player_name}]님, 무엇을 하시겠습니까? > ")

        
        if command == '1':
            player_lives = look_around_room(player_lives, player_name)
            #이렇게 하면 look~room 함수에서도 목숨이랑 이름 변수를 사용 가능.
        elif command == '2':
            player_lives = go_to_village(player_lives, player_name)
        elif command == '3':
            player_lives = go_to_castle(player_lives, player_name)
        elif command == '4':
            print("게임을 종료하고 메인 메뉴로 돌아갑니다.")
            break
        else:
            print(f"{command}은(는) 알 수 없는 명령어입니다. 1, 2, 3, 4 중 하나를 입력해주세요.")
            clear_screen()

        if player_lives <= 0:
            break



def look_around_room(player_lives, player_name):
    clear_screen()
    print("방을 둘러보니 맛있는 빵을 찾았다.")
    player_lives += 1
    print(f"음 맛있다! / 현재 목숨 : {player_lives}")
    print("이제 서둘러 성으로 가자..!")

    while True:
        print("")
        print("1. 서둘러 성으로 향한다.(게임 진행)")

        print(f"\n ---[현재 위치 : 집 / 남은 목숨 : {player_lives} ---")
        command = input(f"[{player_name}] : 서둘러 성으로 가야해..! > ")

        if command == '1':
            player_lives = go_to_castle(player_lives, player_name)
        else:
            print(f"{command}은(는) 알 수 없는 명령어입니다. 1을 입력해주세요.")
            input("...아무 키나 눌러 계속하세요.")

        if player_lives <= 0:
            break

    return player_lives
            

def go_to_village(player_lives, player_name):
    """1. 목숨과 이름을 매개변수로 받는다.
       2. battle 함수에 목숨과 이름을 전달, 최종 목숨을 return.
       3. start_game에 최종 목숨 return으로 보고.
    """
    
    clear_screen()
    print("마을을 둘러보다가 한 꼬마가 시비를 건다?!!")
    input("...아무 키나 눌러 전투를 준비하세요..!")

    player_lives, outcome = battle("꼬마", player_lives)

    while True:
        clear_screen()

        if outcome == "win":
            print(f" ---[마을 광장/ 현재 목숨 : {player_lives}] --- ")
            print("꼬마가 인생의 쓴 맛을 알고 돌아갑니다.")
            print("------------------\n")
        else:
            print("꼬마가 비웃으며 돌아갑니다.")

        print("늦었다. 서둘러 성으로 향하자.")
        print("1. 성으로 간다.(게임 진행)")

        choice = input("서둘러 성으로 가자..! > ")
    
        if choice == '1':
            player_lives = go_to_castle(player_lives, player_name)
        else:
             print(f"{choice}는 알 수 없는 명령어 입니다. 1을 입력하세요.")
             input("...아무 키나 눌러 계속하세요.")
    
        return player_lives
    


def go_to_castle(player_lives, player_name):

    print("")
    print("황제 시저스 : 오..! 용사여 와줬구나! 드래고니아는 지금 북쪽 묵찌빠 설산에 있네.. 부디.. 나의 딸을 구해주게..!")

    while True:
        clear_screen()
        print(f"--- [묵찌빠 설산으로 가는 길 / 현재 목숨 : {player_lives}] --- ")
        print("묵찌빠 설산으로 향하는 길입니다. 어느 길로 가시겠습니까?")
        print("---------------------------------------\n")
        print("1. 은밀한 지하동굴로 숨어간다.")
        print("2. 황폐한 대지로 돌아간다..")
        print("3. 다 필요없다. 바로 드래고니아와 싸우러 묵찌빠 설산으로 간다.")

        choice = input(f"{player_name}님, 무엇을 하시겠습니까? > ")

        if choice == '1':
            player_lives = go_to_cave(player_lives, player_name)
        elif choice == '2':
            player_lives = go_to_desert(player_lives, player_name)
        elif choice == '3':
            player_lives = go_to_boss(player_lives, player_name)
        else:
            print(f"{choice}는 알 수 없는 명령어 입니다. 1, 2, 3 중 하나를 입력하세요.")
            input("...아무 키나 눌러 계속하세요.")

        if player_lives <= 0:
            break


    clear_screen()

    return player_lives

###배틀 승패만 받으면 됨.
def go_to_cave(player_lives, player_name):
    print("")
    print("어두운 동굴 속에서 수상한 소리가 들립니다?!!")
    print("이런..! 야생의 고블린이 나타났다..!")
    input("...아무 키나 눌러 전투를 준비하세요!")

    player_lives, outcome = battle("고블린", player_lives)

    print(f" ---[은밀한 지하동굴 / 현재 목숨 : {player_lives}] --- ")
    if outcome == "win":
        print("고블린이 눈물을 흘리며 도망갑니다.")
        print("땅에 떨어진 포션을 찾았다.")
        player_lives += 1
        print(f"음 맛있다! / 현재 목숨 : {player_lives}")
        print("------------------\n")
    else:
        print("고블린이 비웃으며 유유히 갈 길 갑니다.")


    while player_lives > 0:
        clear_screen()

        print("준비는 끝났다. 설산으로 가자..!")
        print("1. 설산으로 간다.(게임 진행)")

        choice = input("이제 설산으로 가자..! > ")

        if choice == '1':
            player_lives = go_to_boss(player_lives, player_name)
        else:
            print(f"{choice}는 알 수 없는 명령어 입니다. 1을 입력하세요.")
            input("...아무 키나 눌러 계속하세요.")

    return player_lives
    


def go_to_desert(player_lives, player_name):
    print("")
    print("황폐한 대지에서 거대한 오크가 달려옵니다..!!!")
    print("이런..! 야생의 오크가 나타났다!")
    input("...아무 키나 눌러 전투를 준비하세요!")

    player_lives, outcome = battle("오크", player_lives)

    
    print(f" ---[황폐한 대지 / 현재 목숨 : {player_lives}] --- ")
    if outcome == "win":
        print("오크가 당황하며 도망칩니다.")
        print("땅에 떨어진 포션을 찾았다.")
        player_lives += 1
        print(f"음 맛있다! / 현재 목숨 : {player_lives}")
        print("------------------\n")

    while player_lives > 0:
        clear_screen()

        print("준비는 끝났다. 설산으로 가자..!")
        print("1. 설산으로 간다.(게임 진행)")

        choice = input("이제 설산으로 가자..! > ")

        if choice == '1':
            player_lives = go_to_boss(player_lives, player_name)
        else:
            print(f"{choice}는 알 수 없는 명령어 입니다. 1을 입력하세요.")
            input("...아무 키나 눌러 계속하세요.")

    return player_lives



def go_to_boss(player_lives, player_name):
    print("")
    print("설산에 도착하니 거대한 기운이 용사를 두려움에 떨게 한다..")
    print("드래고니아 : 왔구나 어리석은 용사여.. 자 덤벼라..!!")
    input("...아무 키나 눌러 전투를 준비하세요..!")

    player_lives = boss_battle("드래고니아", player_lives)

    if player_lives <= 0:
        pass #그냥 통과 이미 Game Over 출력했기 때문에

    else:
        print("\n드래고니아를 물리쳤습니다..!!")
        print("공주 페이피 : 감사합니다 용사님..! 어서 성으로 돌아가시죠..!!")

        ending(player_lives, player_name)

        player_lives = 0

        input("\n [ The End ]\n아무 키나 눌러 메인 메뉴로 돌아갑니다.")
        

    return player_lives



def ending(player_lives, player_name):
    print(f"{player_name}은(는) 페이피 공주와 함께 성으로 환대를 받으며 돌아왔다. 이에 황제 시저스는 용사에게 페이피 공주와의 혼인을 권유했고 {player_name}와(과) 공주 페이피는 결혼해 오래오래 행복하게 살았다.. 끝!")
    
    



while True: #while True는 무한루프, 탈출하기 위해선 break 필요.
    clear_screen() # 1. 화면 지우기
    display_main_menu() # 2. 메뉴를 표시

    choice = input("원하는 작업의 번호를 입력하세요: ")
    if choice == '1':
        start_game() #1이라면 게임 시작


    elif choice == '2':
        print("게임을 종료합니다. 이용해주셔서 감사합니다.")

        break #가장 가까운 while 반복문 강제로 종료.


    else: #1,2모두 아니라면
        print("잘못된 입력입니다. 1, 2 중 하나만 입력해주세요.")
        input("...아무 키나 눌러 계속하세요.")

