import pygame
import logging

from game import Game
from network import Network
import data_json

pygame.font.init()

pygame.init()
size_main_window = (1200, 800)
Name_Game = "Card_game"
sc = pygame.display.set_mode(size_main_window)
pygame.display.set_caption(Name_Game)

bg_surf = pygame.image.load("Picture/menu1.JPG").convert()
sc.blit(bg_surf, (0, 0))

clock = pygame.time.Clock()
FPS = 30
pygame.display.update()


class Statistics:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 100
        self.height = 50

    def draw(self, sc):
        font = pygame.font.SysFont("comicsans", 45)
        text = font.render(self.text, 1, (0, 255, 255))
        sc.blit(text, (self.x, self.y))


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, sc):
        pygame.draw.rect(sc, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        sc.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                       self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redraw_window(sc, game, p):
    sc.blit(pygame.image.load("Picture/BackGround.jpg").convert(), (0, 0))
    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Подождите напарника для игры", 1, (255, 0, 0), True)
        sc.blit(text,
                (size_main_window[0] / 2 - text.get_width() / 2, size_main_window[1] / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Вы", 1, (0, 255, 255))
        sc.blit(text, (467, 450))
        redraw_stat(sc, game, p)
        text = font.render("Соперник", 1, (0, 255, 255))
        sc.blit(text, (467, 20))
        text_round = font.render("Раунд - " + str(Game.match), 1, (0, 255, 255))
        sc.blit(text_round, (467, size_main_window[1] / 3))

        if game.p1Went and game.get_player_move(0)[0] == "З" or game.p1Went and game.get_player_move(0)[0] == "А":
            text1 = font.render("Сделал ход", 1, (255, 127, 80))
        else:
            text1 = font.render("Ожидание...", 1, (255, 127, 80))

        if game.p2Went and game.get_player_move(1)[0] == "З" or game.p2Went and game.get_player_move(1)[0] == "А":
            text2 = font.render("Сделал ход", 1, (255, 127, 80))
        else:
            text2 = font.render("Ожидание...", 1, (255, 127, 80))

        if p == 1:
            sc.blit(text2, (467, 500))
            sc.blit(text1, (467, 67))

        else:
            sc.blit(text1, (467, 500))
            sc.blit(text2, (467, 67))
        for btn in btns:
            btn.draw(sc)
    pygame.display.update()


btns = [
    Button("Рабочий", 467, 600, (255, 0, 0)),
    Button("Воин", 667, 600, (0, 255, 0)),
    Button("Атака", 867, 600, (0, 0, 250)),
    Button("Закончить ход", 967, 300, (0, 0, 250))]


def redraw_stat(sc, game, p):
    if p == 0:
        stats = [Statistics("Монеток: " + game.get_coins1(), 0, 0, (0, 0, 0)),
                 Statistics("Войнов: " + game.get_warrior1(), 0, 50, (0, 0, 0)),
                 Statistics("Рабочих: " + game.get_worker1(), 0, 100, (0, 0, 0))]
        for stat in stats:
            stat.draw(sc)
    else:
        stats = [Statistics("Монеток: " + game.get_coins2(), 0, 0, (0, 0, 0)),
                 Statistics("Войнов: " + game.get_warrior2(), 0, 50, (0, 0, 0)),
                 Statistics("Рабочих: " + game.get_worker2(), 0, 100, (0, 0, 0))]
        for stat in stats:
            stat.draw(sc)


def main():
    n = Network()
    player_position = int(n.get_pos())

    # TODO: Добавить обработку ошибки, когда нет соединения с сервером на
    #  стороне клиента. Однотипный код вынести в отдлельный функции.
    print("You are player", player_position)
    font = pygame.font.SysFont("comicsans", 60)

    while True:
        clock.tick(FPS)
        try:
            game = n.send("get")
        except Exception as e:
            logging.error(e)
            print("Couldn't get game")
            # Завершаем работу, если есть какая-то ошибка при инициализации и дальше код не будет отрабатывать.
            return None

        is_next_round1, is_next_round2, is_fight1, is_fight2 = False, False, False, False

        if game.p1Went:
            if game.get_player_move(0)[0] == "Р" or game.get_player_move(0)[0] == "В":
                game.choose_card1()
                redraw_stat(sc, game, player_position)
            if game.get_player_move(0)[0] == "З":
                is_next_round1 = True
            elif game.get_player_move(0)[0] == "А":
                is_fight1 = True
            else:
                try:
                    game = n.send("reset1")
                except Exception as e:
                    logging.error(e)
                    print("Couldn't get game")
                    return None
                is_next_round1 = False

        if game.p2Went:
            if game.get_player_move(1)[0] == "Р" or game.get_player_move(1)[0] == "В":
                game.choose_card2()
            if game.get_player_move(1)[0] == "З":
                is_next_round2 = True
            elif game.get_player_move(1)[0] == "А":
                is_fight2 = True
            else:
                try:
                    game = n.send("reset2")
                except Exception as e:
                    logging.error(e)
                    print("Couldn't get game")
                    return None
                is_next_round2 = False

        if is_next_round1 and is_next_round2:
            game.builder_mines()
            Game.match += 1
            pygame.time.delay(500)

        if is_fight1 or is_fight2:
            if game.p1Went and game.p2Went:
                if (game.is_winner() == 1 and player_position == 1) or (game.is_winner() == 0 and player_position == 0):
                    text = font.render("Вы выйграли!", 1, (255, 0, 0))
                    Game.match = 1
                    Game.coins[0] = 5
                    Game.worker[0] = 5
                    Game.warrior[0] = 1

                    Game.coins[1] = 5
                    Game.worker[1] = 5
                    Game.warrior[1] = 1
                else:
                    text = font.render("Вы проиграли", 1, (255, 0, 0))
                    Game.match = 1
                    Game.coins[0] = 5
                    Game.worker[0] = 5
                    Game.warrior[0] = 1

                    Game.coins[1] = 5
                    Game.worker[1] = 5
                    Game.warrior[1] = 1

                sc.blit(
                    text,
                    (
                        size_main_window[0] / 2 - text.get_width() / 2,
                        size_main_window[1] / 2 - text.get_height() / 2
                    )
                )

                pygame.display.update()
                pygame.time.delay(3000)
        redraw_window(sc, game, player_position)

        if game.both_went():
            redraw_window(sc, game, player_position)
            try:
                game = n.send("reset")
            except Exception as e:
                logging.error(e)
                print("Couldn't get game")
                return None
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player_position == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redraw_window(sc, game, player_position)


while True:
    isGaming = True
    while isGaming:
        clock.tick(FPS)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                isGaming = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 300 < pygame.mouse.get_pos()[0] < 900 and 200 < pygame.mouse.get_pos()[1] < 400:
                        isGaming = False
    main()
