from collections import Counter


class Player:
    def __init__(self) -> None:
        self.history = []

    def cooperate(self, opponent_history: list) -> bool:
        return True


class Cheater(Player):
    def cooperate(self, opponent_history: list) -> bool:
        return False


class Cooperator(Player):
    def cooperate(self, opponent_history: list) -> bool:
        return True


class Copycat(Player):
    def cooperate(self, opponent_history: list) -> bool:
        if len(opponent_history) == 0:
            return True
        return opponent_history[-1]


class Grudger(Player):
    def cooperate(self, opponent_history: list) -> bool:
        if False in opponent_history:
            return False
        return True


class Detective(Player):
    def cooperate(self, opponent_history: list) -> bool:
        if len(opponent_history) < 4:
            start = [True, False, True, True]
            return start[len(opponent_history)]
        if False in opponent_history:
            return opponent_history[-1]
        else:
            return False


class Aboba(Player):
    def cooperate(self, opponent_history: list) -> bool:
        if len(opponent_history) == 0:
            return True
        return False


class Game(object):

    def __init__(self, matches=10):
        self.matches = matches
        self.registry = Counter()

    def play(self, player1, player2):
        for _ in range(0, self.matches):
            p1 = player1.cooperate(player2.history)
            p2 = player2.cooperate(player1.history)
            if p1 and p2:
                # оба сотрудничают
                self.registry[player1.__class__.__name__] += 2
                self.registry[player2.__class__.__name__] += 2
            elif not (p1 or p2):
                # оба обманули
                pass
            elif p1:
                # второй обманул
                self.registry[player2.__class__.__name__] += 3
                self.registry[player1.__class__.__name__] -= 1
            elif p2:
                # первый обманул
                self.registry[player2.__class__.__name__] -= 1
                self.registry[player1.__class__.__name__] += 3

            player1.history.append(p1)
            player2.history.append(p2)

    def top3(self):
        top_three = self.registry.most_common(3)
        for player, score in top_three:
            print(f"{player.lower()} {score}")


if __name__ == "__main__":
    game = Game(5)
    game.play(Cooperator(), Cheater())
    game.play(Cooperator(), Grudger())
    game.play(Cheater(), Grudger())
    game.top3()
