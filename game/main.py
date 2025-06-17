import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def change_color():
    os.system('color b')


row = [1, 2, 3, 4, 5, 6, 7, 8]
column = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


class Ship:

    def __init__(self, length, count):
        self.length = length
        self.count = count
        self.arr = []
        for i in range(self.count):
            self.arr.append(['W']*self.length)

    def prnt(self):
        print(self.arr)


class Player:
    str = ["a", "s", "sr", "ssr"]
    # str = ["ssr"]

    def __init__(self, name):
        self.name = name
        self.ssr = Ship(4, 1)
        self.sr = Ship(3, 2)
        self.s = Ship(2, 3)
        self.a = Ship(1, 4)
        self.total = [self.a.arr, self.s.arr, self.sr.arr, self.ssr.arr]
        # self.total = [self.ssr.arr]
        self.pos = []
        self.score = 20
        # self.score = 4
        self.board = [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
    ]


class Game:
    def __init__(self):
        self.player1 = None
        self.player2 = None
    # when self. is not used we make method static by @staticmethod
    @staticmethod
    def print_game(m1, m2):
        print("player1\t\t\t\tplayer2")
        print(" ", *row, "   ", *row)
        for i in range(len(column)):
            print(column[i], *m1[i], " ", column[i], *m2[i])
        print()

    @staticmethod
    def print_mat(player_x: Player):
        print(" ", *row)
        for i in range(len(column)):
            print(column[i], *player_x.board[i])

    @staticmethod
    def show_available_ships(player_x: Player):
        for i in range(len(player_x.total)):
            print(player_x.str[i], " ", *player_x.total[i], f" x{len(player_x.total[i])}")

    @staticmethod
    def get_coord():
        while True:
            try:
                placement = input("Enter row and column (e.g. c,7): ").strip()
                x, y = placement.split(',')
                x = ord(x.strip().lower()) - ord('a') + 1
                y = int(y.strip())
                if not (1 <= x <= 8 and 1 <= y <= 8):
                    print("Error! Coordinates out of board range (a-h, 1-8).")
                    continue
                return x, y
            except Exception:
                print("Error!! Invalid input! Please enter coordinate like 'c,7'.")

    def get_pos(self):
        pos = input("choose horizontal or vertical position h/v: ")
        if pos == "v" or pos == "h":
            return pos
        else:
            print("Error!! Invalid input! Please enter valid position! 'v' or 'h'!!!")
            return self.get_pos()

    def place_ship(self, player_x: Player, length):
        data = []
        x, y = self.get_coord()
        pos = self.get_pos()

        if pos == "h":
            if (8-y+1) < length:
                print("cant place, not enough space")
                return False

            for i in range(length + 2):
                max_y = y-2+i

                if max_y >= 8:
                    break
                if max_y < 0:
                    continue
                if player_x.board[x-1][max_y] == "W":
                    print("ships must be at least one cell away from each other, cant place")
                    return False
                elif x <= 7 and player_x.board[x][max_y] == "W":
                    print("ships must be at least one cell away from each other, cant place")
                    return False
                elif x-2 >= 0 and player_x.board[x-2][max_y] == "W":
                    print("ships must be at least one cell away from each other, cant place")
                    return False
            for i in range(length):
                player_x.board[x-1][y-1+i] = "W"
            del player_x.total[length-1][0]
            # del player_x.total[0][0]

        elif pos == "v":
            if (8-x+1) < length:
                print("cant place, not enough space")
                return False

            for i in range(length + 2):
                max_x = x-2+i

                if max_x >= 8:
                    break
                if max_x < 0:
                    continue
                if player_x.board[max_x][y-1] == "W":
                    print("ships must be at least one cell away from each other, cant place")
                    return False
                elif y <= 7 and player_x.board[max_x][y] == "W":
                    print("ships must be at least one cell away from each other, cant place")
                    return False
                elif y-2 >= 0 and player_x.board[max_x][y-2] == "W":
                    print("ships must be at least one cell away from each other, cant place")
                    return False

            for i in range(length):
                player_x.board[x-1+i][y-1] = "W"
            del player_x.total[length-1][0]
            # del player_x.total[0][0]

        data.append(x-1)
        data.append(y-1)
        data.append(length)
        data.append(pos)
        player_x.pos.append(data)
        # print(player_x.pos)
        return True

    def pl_init(self, player_x: Player):
        print(f"\n--- {player_x.name}'s turn to place ships! --- (Type 'exit' to quit at any prompt)")
        while any(inner for inner in player_x.total):
            print("Place your available ships (see below):")
            self.show_available_ships(player_x)
            self.print_mat(player_x)
            ship_choice = input("Choose ship to place (ssr, sr, s, a): ").lower().strip()
            match ship_choice:
                case "ssr":
                    # if player_x.total[0]:
                    if player_x.total[3]:
                        if self.place_ship(player_x, len(player_x.ssr.arr[0])):
                            clear_screen()
                    else:
                        clear_screen()
                        print("No more 'ssr' rank ships available")

                case "sr":
                    if player_x.total[2]:
                        if self.place_ship(player_x, len(player_x.sr.arr[0])):
                            clear_screen()
                    else:
                        clear_screen()
                        print("No more 'sr' rank ships available")

                case "s":
                    if player_x.total[1]:
                        if self.place_ship(player_x, len(player_x.s.arr[0])):
                            clear_screen()
                    else:
                        clear_screen()
                        print("No more 's' rank ships available")

                case "a":
                    if player_x.total[0]:
                        if self.place_ship(player_x, len(player_x.a.arr[0])):
                            clear_screen()
                    else:
                        clear_screen()
                        print("No more 'a' rank ships available")

                case "exit":
                    return False
                case _:
                    clear_screen()
                    print("Invalid ship!! Enter valid ship rank 'a', 's', 'sr' or 'ssr'")
                    continue

        self.print_mat(player_x)
        aaa = input("this is your final matrix, press enter to continue: ")
        return True


    @staticmethod
    def check_destruction(player_x, x, y, m, i):
        if player_x.pos[i][3] == "h":
            for j in range(player_x.pos[i][2]):
                print(f"j {j} x-1 {x - 1} y-1+j {player_x.pos[i][1] + j}")
                if m[x - 1][player_x.pos[i][1] + j] != "X":
                    return False
            return True
        elif player_x.pos[i][3] == "v":
            for j in range(player_x.pos[i][2]):
                if m[player_x.pos[i][0] + j][y - 1] != "X":
                    return False
            return True

    def check_ship(self, player_x: Player, x, y, m):
        for i in range(len(player_x.pos)):

            if player_x.pos[i][3] == "h" and x-1 == player_x.pos[i][0]:
                if player_x.pos[i][1] <= y-1 < player_x.pos[i][1] + player_x.pos[i][2]:
                    if self.check_destruction(player_x, x, y, m, i):
                        if player_x.pos[i][1] - 1 >= 0:
                            m[x - 1][player_x.pos[i][1] - 1] = "#"
                        if player_x.pos[i][1] + player_x.pos[i][2] <= 7:
                            m[x - 1][player_x.pos[i][1] + player_x.pos[i][2]] = "#"
                        for k in range(player_x.pos[i][2] + 2):
                            draw = player_x.pos[i][1] - 1 + k

                            if 0 <= draw <= 7:
                                if x - 2 >= 0:
                                    m[x - 2][draw] = "#"
                                if x <= 7:
                                    m[x][draw] = "#"

            elif player_x.pos[i][3] == "v" and y-1 == player_x.pos[i][1]:
                if player_x.pos[i][0] <= x-1 < player_x.pos[i][0] + player_x.pos[i][2]:
                    if self.check_destruction(player_x, x, y, m, i):
                        if player_x.pos[i][0] - 1 >= 0:
                            m[player_x.pos[i][0] - 1][y - 1] = "#"
                        if player_x.pos[i][0] + player_x.pos[i][2] <= 7:
                            m[player_x.pos[i][0] + player_x.pos[i][2]][y - 1] = "#"
                        for k in range(player_x.pos[i][2] + 2):
                            # print(k, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                            draw = player_x.pos[i][0] - 1 + k

                            # print(f"y-2 {y-2} y {y} draw {draw}")
                            if 0 <= draw <= 7:
                                if y - 2 >= 0:
                                    m[draw][y - 2] = "#"
                                if y <= 7:
                                    m[draw][y] = "#"

    def playing_order(self, player_x, player_y, m1, m2, p):
        if player_x.score == 0:
            print(f"\n***** {player_y.name} WON THE GAME! *****\n")
            return
        elif player_y.score == 0:
            print(f"\n***** {player_x.name} WON THE GAME! *****\n")
            return

        if p:
            self.print_game(m1, m2)
        else:
            self.print_game(m2, m1)

        print(f"{player_x.name} enter position to attack: ")
        x, y = self.get_coord()
        if player_y.board[x - 1][y - 1] == "O" and m2[x - 1][y - 1] == "O":
            clear_screen()
            m2[x - 1][y - 1] = "#"
            self.playing_order(player_y, player_x, m2, m1, not p)
        elif player_y.board[x - 1][y - 1] == "W" and m2[x - 1][y - 1] == "O":
            clear_screen()
            m2[x - 1][y - 1] = "X"
            self.check_ship(player_y, x, y, m2)
            player_y.score -= 1
            self.playing_order(player_x, player_y, m1, m2, p)
        else:
            clear_screen()
            print("Cell already attacked! choose another one")
            self.playing_order(player_x, player_y, m1, m2, p)

    def battle(self, player_x, player_y):
        m1 = [['O' for _ in range(8)] for _ in range(8)]
        m2 = [['O' for _ in range(8)] for _ in range(8)]

        return self.playing_order(player_x, player_y, m1, m2, True)

    def game_start(self, player1_name, player2_name):
        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)

        change_color()
        clear_screen()

        print(f"\n--- Game starting: {self.player1.name} vs. {self.player2.name}! ---")  # NEW: Welcome message
        print(f"\n--- {self.player1.name}: Place Your Ships ---")
        self.pl_init(self.player1)

        clear_screen()

        print(f"\n--- {self.player2.name}: Place Your Ships ---")
        self.pl_init(self.player2)
        clear_screen()

        print("\n--- All ships placed! Starting Battle! ---")
        cont_input = input("Press Enter to begin the battle, or type 'exit' to quit: ").strip()
        if cont_input.lower() == 'exit':
            return False
        clear_screen()

        self.battle(self.player1, self.player2)
        return True


if __name__ == "__main__":
    game = Game()
    game.game_start("StandalonePlayer1", "StandalonePlayer2")
