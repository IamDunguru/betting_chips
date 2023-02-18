import os

class Player :
    def setdata(self, name, chips) :
        self.name = name
        self.chips = chips
        self.state = 'alive'
        self.betting = 0
    
    def chip_printing(self) :
        print("{}| ".format(self.name), end='')
        for i in range(self.chips) :
            print("🪙", end='')
        print('  | {}개'.format(self.chips))

def max_chip(players, player_num) :
    MaxChip = 0
    for i in range(player_num) :
        if MaxChip < players[i+1].chips :
            MaxChip = players[i+1].chips
    return MaxChip

def show_me_the_chips(players, player_num) :
    size = max_chip(players, player_num)+15
    for i in range(size) :
        print("-", end='')
    print()
    for i in range(player_num+1) :
        players[i].chip_printing()
        print()
    for i in range(size) :
        print("-", end='')
    print()

def purchasing(players, customer) :
    print("Do you wanna purchase other's chip?")
    print()
    for i in range(player_num) :
        print(" {}: {} ||".format(players[i+1].name,i+1), end='')
    print()
    print()
    celler = int(input("From who? >>> "))
    print()
    moving_chips = int(input("How much? >>> "))
    customer.chips += moving_chips
    players[celler].chips -= moving_chips
    print()
    print(" Thank you for visiting :D ")
    print()
    input("Press any key to quit >>")

def processing (players, player_num):
    # 기본 베팅
    for i in range(player_num) :
        players[i+1].chips -= 1
    players[0].chips += player_num
    show_me_the_chips(players, player_num)
    total_betting = 0

    while(True) :
        menu = int(input("( 베팅: 1  ||  정산: 2 ) >> "))
        if menu == 2 : # 정산
            print()
            for i in range(player_num) :
                print(" {}: {} ||".format(players[i+1].name,i+1), end='')
            print()
            print()
            winner = int(input("who is winner? >> "))
            # 승자가 모인 칩 다 먹기
            players[winner].chips += players[0].chips
            players[0].chips = 0
            # 세팅 초기화 (state, betting)
            for human in players :
                human.state = 'alive'
                human.betting = 0
            total_betting = 0
            # 결과 출력
            os.system('clear')
            show_me_the_chips(players, player_num)

            for i in range(player_num) :
                if players[i+1].chips == 0 :
                    purchasing(players, players[i+1])
            break

        else : # 베팅
            print()
            for i in range(player_num) :
                print(" {}: {} ||".format(players[i+1].name,i+1), end='')
            print()
            print()
            while True : 
                starter = int(input("who gonna first? >> "))
                if starter <= player_num :
                    if players[starter].state == 'alive' :
                        break
            turn = starter
            match = True
            pre_choice = 'check'

            while(match) :
                now_P = players[turn]
                print()
                print(" [ {}'s turn ] ".format(now_P.name))
                # 해당 턴의 선택 입력
                if pre_choice == 'raise' :
                    choice = input("( raise: 1  ||  call: 3  ||  die: 4 ) >> ")
                else : 
                    choice = input("( raise: 1  ||  check: 2  ||  die: 4 ) >> ")
                
                if choice == '1' : # raise 선택한 경우
                    pre_choice = 'raise'
                    print()
                    while True :
                        betting = int(input("How many? >> "))
                        if betting <= now_P.chips-total_betting :
                            break
                    total_betting += betting
                    now_P.chips -= total_betting-now_P.betting
                    players[0].chips += total_betting-now_P.betting
                    now_P.betting = total_betting
                elif choice == '2' : # check 선택한 경우
                    pre_choice = 'check'
                elif choice == '3' : # call 선택한 경우
                    if total_betting-now_P.betting > now_P.chips :
                        now_P.chips = 0
                    else :
                        now_P.chips -= total_betting-now_P.betting
                    pre_choice = 'raise'
                    players[0].chips += total_betting-now_P.betting
                    now_P.betting = total_betting
                elif choice == '4' : # die 선택한 경우
                    now_P.state = 'die'
                
                # 결과 출력
                os.system('clear')
                show_me_the_chips(players, player_num)
                # 다음 턴으로 turn 변경
                while True :
                    turn += 1
                    if turn > player_num :
                        turn = 1
                    if players[turn].state == 'alive' :
                        break
                # 모두 베팅한 금액이 같은 경우, 게임 진행
                if pre_choice != 'check' and players[turn].betting == total_betting and total_betting != 0:
                    match = False
                # 모두 check한 경우, 게임 진행
                if turn == starter and pre_choice == 'check' :
                    match = False
                    


if __name__ == "__main__" :
    player_num = int(input("플레이어 수를 입력하세요: "))
    chip_setting = int(input("초기 칩 개수를 입력하세요: "))
    players = ['딜러']
    players[0] = Player()
    players[0].setdata('베팅', 0)
    for i in range(player_num) :
        name = input("플레이어 {}의 이름을 입력하세요: ".format(i+1))
        players.append(i+1)
        players[i+1] = Player()
        players[i+1].setdata(name, chip_setting)

    while(True) :
        os.system('clear')
        print('''
        
              ||| Welcome to the new game |||
        
        ''')
        
        processing(players, player_num)

