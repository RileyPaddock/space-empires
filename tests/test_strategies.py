import sys
sys.path.append('src')
from game import Game
from strategies.dumb_strategy1 import DumbStrategyLevel1
from strategies.random_strategy1 import RandomStrategyLevel1
from strategies.beserker_strategy1 import BerserkerStrategyLevel1
from strategies.riley_strategy import RileyStrategy

strategy_1 = DumbStrategyLevel1
strategy_2 = RandomStrategyLevel1
strategy_3 = BerserkerStrategyLevel1
strategy_4 = RileyStrategy

print("Dumb v. Berserker")
new_game = Game(logging = False, die_rolls = 'descending', restricted = 'True')
new_game.add_player(strategy_1(0), [2,0])
new_game.add_player(strategy_3(1), [2,4])
new_game.initialize_game()
new_game.run_to_completion()
print(new_game.winner)


print("Berserker v. Berserker")
new_game = Game(logging = False, die_rolls = 'descending', restricted = 'True')
new_game.add_player(strategy_3(0), [2,0])
new_game.add_player(strategy_3(1), [2,4])
new_game.initialize_game()
new_game.run_to_completion()
print(new_game.winner)


print("Random v. Berserker")
new_game = Game(logging = False, die_rolls = 'descending', restricted = 'True')
new_game.add_player(strategy_2(0), [2,0])
new_game.add_player(strategy_3(1), [2,4])
new_game.initialize_game()
new_game.run_to_completion()
print(new_game.winner)



print("Riley v. Dumb")
new_game = Game(logging = False, die_rolls = 'descending', restricted = 'True')
new_game.add_player(strategy_4(0), [2,0])
new_game.add_player(strategy_1(1), [2,4])
new_game.initialize_game()
new_game.run_to_completion()
print(new_game.winner)



print("Riley v. Random")
new_game = Game(logging = False, die_rolls = 'descending', restricted = 'True')
new_game.add_player(strategy_4(0), [2,0])
new_game.add_player(strategy_2(1), [2,4])
new_game.initialize_game()
new_game.run_to_completion()
print(new_game.winner)



print("Riley v. Berserker")
new_game = Game(logging = False, die_rolls = 'descending', restricted = 'True')
new_game.add_player(strategy_4(0), [2,0])
new_game.add_player(strategy_3(1), [2,4])
new_game.initialize_game()
new_game.run_to_completion()
print(new_game.winner)
