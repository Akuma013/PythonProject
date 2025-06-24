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
        self.free_pos = []


class Game:
    def __init__(self):
        self.player1 = None
        self.player2 = None
    # when self. is not used we make method static by @staticmethod
    @staticmethod
    def print_game(player_x: Player, player_y: Player, m1, m2):
        print(f"{player_x.name}\t\t\t{player_y.name}")
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
        if not player_x.free_pos:
            self.delete_ship(player_x)
            self.find_free_space(player_x, length)
            clear_screen()
            print("Now try to place ship you wanted!")
            print(" If the space is free then you will, if not, you will have to delete one more ship")
            self.show_available_ships(player_x)
            self.print_mat(player_x)
            return self.place_ship(player_x, length)
        data = []
        x, y = self.get_coord()
        placement = self.get_pos()
        for free_pos in player_x.free_pos:
            print(x-1, y-1, length, placement)
            if x-1 == free_pos[0] and y-1 == free_pos[1] and length == free_pos[2] and placement == free_pos[3]:
                if placement == "v":
                    for i in range(length):
                        player_x.board[x - 1 + i][y - 1] = "W"
                    del player_x.total[length - 1][0]
                elif placement == "h":
                    for i in range(length):
                        player_x.board[x - 1][y - 1 + i] = "W"
                    del player_x.total[length - 1][0]
                data.append(x - 1)
                data.append(y - 1)
                data.append(length)
                data.append(placement)
                player_x.pos.append(data)
                return True

            print("Error! Cant place there! But you have other free positions to choose! ")
            print(f"e.g. position-> '{chr(ord('a') + player_x.free_pos[0][1])},{player_x.free_pos[0][0]+1}'"
                  f" length <= {player_x.free_pos[0][2]} placement= {player_x.free_pos[0][3]}")
                # del player_x.total[0][0]



        return False


    def pl_init(self, player_x: Player):
        #  --- (Type 'exit' to quit at any prompt)
        print(f"\n--- {player_x.name}'s turn to place ships!")
        while any(inner for inner in player_x.total):
            print("Place your available ships (see below):")
            self.show_available_ships(player_x)
            self.print_mat(player_x)
            ship_choice = input("Choose ship to place (ssr, sr, s, a): ").lower().strip()
            match ship_choice:
                case "ssr":
                    # if player_x.total[0]:
                    if player_x.total[3]:
                        self.find_free_space(player_x, len(player_x.ssr.arr[0]))
                        if self.place_ship(player_x, len(player_x.ssr.arr[0])):
                            clear_screen()
                        else:
                            clear_screen()
                            print("Error! Cant place ship there! Not enough space!")
                    else:
                        clear_screen()
                        print("No more 'ssr' rank ships available")

                case "sr":
                    if player_x.total[2]:
                        self.find_free_space(player_x, len(player_x.sr.arr[0]))
                        if self.place_ship(player_x, len(player_x.sr.arr[0])):
                            clear_screen()
                        else:
                            clear_screen()
                            print("Error! Cant place ship there! Not enough space!")
                    else:
                        clear_screen()
                        print("No more 'sr' rank ships available")

                case "s":
                    if player_x.total[1]:
                        self.find_free_space(player_x, len(player_x.s.arr[0]))
                        if self.place_ship(player_x, len(player_x.s.arr[0])):
                            clear_screen()
                        else:
                            clear_screen()
                            print("Error! Cant place ship there! Not enough space!")
                    else:
                        clear_screen()
                        print("No more 's' rank ships available")

                case "a":
                    if player_x.total[0]:
                        self.find_free_space(player_x, len(player_x.a.arr[0]))
                        if self.place_ship(player_x, len(player_x.a.arr[0])):
                            clear_screen()
                        else:
                            clear_screen()
                            print("Error! Cant place ship there! Not enough space!")
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
                # print(f"j {j} x-1 {x - 1} y-1+j {player_x.pos[i][1] + j}")
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

    @staticmethod
    def check_horizontal(player_x: Player, i, j, length):
        for row in range(3):
            for col in range(length + 2):
                if i - 1 + row < 0 or i - 1 + row > 7 or j - 1 + col < 0 or j - 1 + col > 7:
                    continue
                if player_x.board[i - 1 + row][j - 1 + col] != 'O':
                    return False
        return True

    @staticmethod
    def check_vertical(player_x: Player, i, j, length):
        for col in range(3):
            for row in range(length + 2):
                if i - 1 + row < 0 or i - 1 + row > 7 or j - 1 + col < 0 or j - 1 + col > 7:
                    continue
                if player_x.board[i - 1 + row][j - 1 + col] != 'O':
                    return False
        return True

    def find_free_space(self, player_x: Player, length):
        player_x.free_pos = []
        x_y_length_pos = []
        for i in range(len(player_x.board)):
            for j in range(len(player_x.board[0])):
                if j + length - 1 <= 7:
                    if self.check_horizontal(player_x, i, j, length):
                        x_y_length_pos.append(i)
                        x_y_length_pos.append(j)
                        x_y_length_pos.append(length)
                        x_y_length_pos.append("h")
                        player_x.free_pos.append(x_y_length_pos)
                x_y_length_pos = []
                if i + length - 1 <= 7:
                    if self.check_vertical(player_x, i, j, length):
                        x_y_length_pos.append(i)
                        x_y_length_pos.append(j)
                        x_y_length_pos.append(length)
                        x_y_length_pos.append("v")
                        player_x.free_pos.append(x_y_length_pos)
                x_y_length_pos = []

    def delete_ship(self, player_x: Player):
        print("There is no place on the board left to place your ship! choose another ship to delete!")
        x, y = self.get_coord()
        for i in range(len(player_x.pos)):
            placed_ship = player_x.pos[i]
            if placed_ship[3] == "h":
                if placed_ship[0] == x - 1 and placed_ship[1] <= y - 1 <= placed_ship[1] + placed_ship[2]-1:
                    # print(placed_ship)
                    for j in range(placed_ship[2]):
                        player_x.board[placed_ship[0]][placed_ship[1] + j] = "O"
                    player_x.total[placed_ship[2]-1].append(['W']*placed_ship[2])
                    del player_x.pos[i]
                    return True
            elif placed_ship[3] == "v":
                if placed_ship[0] <= x - 1 <= placed_ship[0] + placed_ship[2] - 1 and placed_ship[1] == y - 1:
                    # print(placed_ship)
                    for j in range(placed_ship[2]):
                        player_x.board[placed_ship[0] + j][placed_ship[1]] = "O"
                    player_x.total[placed_ship[2]-1].append(['W']*placed_ship[2])
                    del player_x.pos[i]
                    return True
        print("Invalid ship coordinates to delete, try again")
        return self.delete_ship(player_x)




    def playing_order(self, player_x, player_y, m1, m2, p):
        if player_x.score == 0:
            print(f"\n***** {player_y.name} WON THE GAME! *****\n")
            return
        elif player_y.score == 0:
            print(f"\n***** {player_x.name} WON THE GAME! *****\n")
            return

        if p:
            self.print_game(player_x, player_y, m1, m2)
        else:
            self.print_game(player_x, player_y, m2, m1)

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

    def game_start(self):
        player1_name = input("Enter Player 1's Name (e.g., Alice): ").strip()
        if not player1_name:  # Provide a default if nothing is entered
            player1_name = "Player 1"

        player2_name = input("Enter Player 2's Name (e.g., Bob): ").strip()
        if not player2_name:  # Provide a default if nothing is entered
            player2_name = "Player 2"

        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)

        change_color()
        clear_screen()

        print(f"\n--- Game starting: {self.player1.name} vs. {self.player2.name}! ---")  # NEW: Welcome message
        print(f"\n--- {self.player1.name}: Place Your Ships ---")
        # self.find_free_space(self.player1,4)
        # print(len(self.player1.free_pos))
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
    game.game_start()



# def place_ship(self, player_x: Player, length):
    #     data = []
    #     x, y = self.get_coord()
    #     pos = self.get_pos()
    #
    #     if pos == "h":
    #         if (8-y+1) < length:
    #             print("cant place, not enough space")
    #             return False
    #
    #         for i in range(length + 2):
    #             max_y = y-2+i
    #
    #             if max_y >= 8:
    #                 break
    #             if max_y < 0:
    #                 continue
    #             if player_x.board[x-1][max_y] == "W":
    #                 print("ships must be at least one cell away from each other, cant place")
    #                 return False
    #             elif x <= 7 and player_x.board[x][max_y] == "W":
    #                 print("ships must be at least one cell away from each other, cant place")
    #                 return False
    #             elif x-2 >= 0 and player_x.board[x-2][max_y] == "W":
    #                 print("ships must be at least one cell away from each other, cant place")
    #                 return False
    #         for i in range(length):
    #             player_x.board[x-1][y-1+i] = "W"
    #         del player_x.total[length-1][0]
    #         # del player_x.total[0][0]
    #
    #     elif pos == "v":
    #         if (8-x+1) < length:
    #             print("cant place, not enough space")
    #             return False
    #
    #         for i in range(length + 2):
    #             max_x = x-2+i
    #
    #             if max_x >= 8:
    #                 break
    #             if max_x < 0:
    #                 continue
    #             if player_x.board[max_x][y-1] == "W":
    #                 clear_screen()
    #                 print("ships must be at least one cell away from each other, cant place")
    #                 return False
    #             elif y <= 7 and player_x.board[max_x][y] == "W":
    #                 clear_screen()
    #                 print("ships must be at least one cell away from each other, cant place")
    #                 return False
    #             elif y-2 >= 0 and player_x.board[max_x][y-2] == "W":
    #                 clear_screen()
    #                 print("ships must be at least one cell away from each other, cant place")
    #                 return False
    #
    #         for i in range(length):
    #             player_x.board[x-1+i][y-1] = "W"
    #         del player_x.total[length-1][0]
    #         # del player_x.total[0][0]
    #
    #     data.append(x-1)
    #     data.append(y-1)
    #     data.append(length)
    #     data.append(pos)
    #     player_x.pos.append(data)
    #     # print(player_x.pos)
    #     return True


    # def pl_init(self, player_x: Player):
    #     #  --- (Type 'exit' to quit at any prompt)
    #     print(f"\n--- {player_x.name}'s turn to place ships!")
    #     while any(inner for inner in player_x.total):
    #         print("Place your available ships (see below):")
    #         self.show_available_ships(player_x)
    #         self.print_mat(player_x)
    #         ship_choice = input("Choose ship to place (ssr, sr, s, a): ").lower().strip()
    #         match ship_choice:
    #             case "ssr":
    #                 # if player_x.total[0]:
    #                 if player_x.total[3]:
    #                     if self.place_ship(player_x, len(player_x.ssr.arr[0])):
    #                         clear_screen()
    #                 else:
    #                     clear_screen()
    #                     print("No more 'ssr' rank ships available")
    #
    #             case "sr":
    #                 if player_x.total[2]:
    #                     if self.place_ship(player_x, len(player_x.sr.arr[0])):
    #                         clear_screen()
    #                 else:
    #                     clear_screen()
    #                     print("No more 'sr' rank ships available")
    #
    #             case "s":
    #                 if player_x.total[1]:
    #                     if self.place_ship(player_x, len(player_x.s.arr[0])):
    #                         clear_screen()
    #                 else:
    #                     clear_screen()
    #                     print("No more 's' rank ships available")
    #
    #             case "a":
    #                 if player_x.total[0]:
    #                     if self.place_ship(player_x, len(player_x.a.arr[0])):
    #                         clear_screen()
    #                 else:
    #                     clear_screen()
    #                     print("No more 'a' rank ships available")
    #
    #             case "exit":
    #                 return False
    #             case _:
    #                 clear_screen()
    #                 print("Invalid ship!! Enter valid ship rank 'a', 's', 'sr' or 'ssr'")
    #                 continue
    #
    #     self.print_mat(player_x)
    #     aaa = input("this is your final matrix, press enter to continue: ")
    #     return True
