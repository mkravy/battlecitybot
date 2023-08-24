from ORM.GamesORM import Game
from ORM.PlayersORM import Player
from ORM.ResultsORM import Result
from _log import log

game = Game()
result = Result()
player = Player()

# План
# 1. Занести результат партии в games
# 2. Пересчитать лучший результат по тегу в results
# 3. Пересчитать результат по игроку в players

# 1. Внесение результата партии в games
game.insert_game()

# 1.1 Ищем новых игроков для добавления в players
players = player.select_players()
_players = game.select_new_players()
names = [] #Список для имен действующих игроков

for p in players:
    names.append(p.name)

for p in _players:
    name = p[0]
    tag = name[:5]
    if name not in names:
        player.insert(name, tag)

# 2. Пересчет результатов по тегу в results
result.update_results(game, result)

# 3. Пересчет результатов игрока в players
player.update_players(player, result)

# 4. Вывод результатов
players = player.select_all()

for player in players:
    name = player.name
    level = player.level
    points = player.points
    print(f"{name} | {level} | {points}")