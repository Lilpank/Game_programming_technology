class Game:
    match = 1
    coins = [5, 5]
    warrior = [1, 1]
    worker = [5, 5]
    price = [5, 10]

    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id

        self.moves = ["", ""]

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):
        if move is not None:
            self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def both_went(self):
        return self.p1Went and self.p2Went

    def is_winner(self):
        w1 = Game.warrior[0]
        w2 = Game.warrior[1]

        if w1 >= w2:
            winner = 0
        else:
            winner = 1
        return winner

    def round_next(self):
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]
        print(p1)
        if p1 == "З" and p2 == "З":
            return True
        else:
            return False

    def next_1(self):
        p1 = self.moves[0].upper()[0]
        if p1 == "З":
            return True
        else:
            return False

    def next_2(self):
        p2 = self.moves[1].upper()[0]
        if p2 == "З":
            return True
        else:
            return False

    def reset_went(self):
        self.p1Went = False
        self.p2Went = False

    def reset_went1(self):
        self.p1Went = False

    def reset_went2(self):
        self.p2Went = False

    def choose_card1(self):
        p1 = self.moves[0].upper()[0]
        if p1 == "Р" and Game.coins[0] >= Game.price[0]:
            Game.coins[0] -= Game.price[0]
            Game.worker[0] += 1
        elif p1 == "В" and Game.coins[0] >= Game.price[1]:
            Game.coins[0] -= Game.price[1]
            Game.warrior[0] += 1

    def choose_card2(self):
        p2 = self.moves[1].upper()[0]

        if p2 == "Р" and Game.coins[1] >= Game.price[0]:
            Game.coins[1] -= Game.price[0]
            Game.worker[1] += 1
        elif p2 == "В" and Game.coins[1] >= Game.price[1]:
            Game.coins[1] -= Game.price[1]
            Game.warrior[1] += 1
        print("choose_card", Game.warrior)
        print("choose_card", Game.worker)

    def to_fight(self):
        p1 = self.get_player_move(0)[0]
        p2 = self.get_player_move(1)[0]
        if p1 == "А" or p2 == "А":
            return True
        else:
            return False

    def to_fight1(self):
        p1 = self.get_player_move(0)[0]
        if p1 == "А":
            return True

    def to_fight2(self):
        p2 = self.get_player_move(1)[0]
        if p2 == "А":
            return True

    def builder_mines(self):
        Game.coins[0] += Game.worker[0]
        Game.coins[1] += Game.worker[1]
        print(Game.coins)
        return Game.coins

    def get_coins1(self):
        return str(Game.coins[0])

    def get_coins2(self):
        return str(Game.coins[1])

    def get_warrior1(self):
        return str(Game.warrior[0])

    def get_warrior2(self):
        return str(Game.warrior[1])

    def get_worker1(self):
        return str(Game.worker[0])

    def get_worker2(self):
        return str(Game.worker[1])
