import random
import math
import sys
sys.path.append('src')
from game import Game
from strategies.Level2.attack_berserker2 import AttackBerserkerLevel2
from strategies.Level2.defense_berserker2 import DefenseBerserkerLevel2
from strategies.Level2.movement_berserker2 import MovementBerserkerLevel2
from strategies.Level2.numbers_berserker2 import NumbersBerserkerLevel2
from strategies.Level2.flank_strategy2 import FlankerStrategyLevel2


strategy_1 = AttackBerserkerLevel2
strategy_2 = DefenseBerserkerLevel2
strategy_3 = MovementBerserkerLevel2
strategy_4 = NumbersBerserkerLevel2
strategy_5 = FlankerStrategyLevel2

def run_game(strategy1, strategy2, game_num):
    strats = {'Attack':strategy_1, 'Defense':strategy_2, 'Movement':strategy_3, 'Numbers':strategy_4, 'Flank':strategy_5}
    new_game = Game(logging = False, die_rolls = 'random', level = 2)
    new_game.add_player(strats[strategy1](0), [2,0])
    new_game.add_player(strats[strategy2](1), [2,4])
    new_game.initialize_game()
    new_game.combat_engine.seed = random.seed(game_num)
    new_game.run_to_completion()
    return strategy1 if new_game.winner == 0 else strategy2

print('Numbers vs Movement: ')
results = []
for _ in range(500):
    winner = run_game('Numbers','Movement',_)
    results.append(winner)

for _ in range(500):
    winner = run_game('Movement','Numbers',_+500)
    results.append(winner)

print('- Numbers wins ' + str(results.count('Numbers')/len(results)) + '% of the time')
print('- Movement wins ' + str(results.count('Movement')/len(results)) + '% of the time')

print('Numbers vs Attack: ')
results = []
for _ in range(500):
    winner = run_game('Numbers','Attack',_)
    results.append(winner)

for _ in range(500):
    winner = run_game('Attack','Numbers',_+500)
    results.append(winner)

print('- Numbers wins ' + str(results.count('Numbers')/len(results)) + '% of the time')
print('- Attack wins ' + str(results.count('Attack')/len(results)) + '% of the time')

print('Numbers vs Defense: ')
results = []
for _ in range(500):
    winner = run_game('Numbers','Defense',_)
    results.append(winner)

for _ in range(500):
    winner = run_game('Defense','Numbers',_+500)
    results.append(winner)

print('- Numbers wins ' + str(results.count('Numbers')/len(results)) + '% of the time')
print('- Defense wins ' + str(results.count('Defense')/len(results)) + '% of the time')

print('Numbers vs Flank: ')
results = []
for _ in range(500):
    winner = run_game('Numbers','Flank',_)
    results.append(winner)

for _ in range(500):
    winner = run_game('Flank','Numbers',_+500)
    results.append(winner)

print('- Numbers wins ' + str(results.count('Numbers')/len(results)) + '% of the time')
print('- Flank wins ' + str(results.count('Flank')/len(results)) + '% of the time')

print('Movement vs Attack: ')
results = []
for _ in range(500):
    winner = run_game('Movement','Attack',_)
    results.append(winner)

for _ in range(500):
    winner = run_game('Attack','Movement',_+500)
    results.append(winner)

print('- Movement wins ' + str(results.count('Movement')/len(results)) + '% of the time')
print('- Attack wins ' + str(results.count('Attack')/len(results)) + '% of the time')

print('Movement vs Defense: ')
results = []
for _ in range(500):
    winner = run_game('Movement','Defense',_)
    results.append(winner)

for _ in range(500):
    winner = run_game('Defense','Movement',_+500)
    results.append(winner)

print('- Movement wins ' + str(results.count('Movement')/len(results)) + '% of the time')
print('- Defense wins ' + str(results.count('Defense')/len(results)) + '% of the time')

print('Movement vs Flank: ')
results = []
for _ in range(500):
    winner = run_game('Movement','Flank',_)
    results.append(winner)

for _ in range(500):
    winner = run_game('Flank','Movement',_+500)
    results.append(winner)

print('- Movement wins ' + str(results.count('Movement')/len(results)) + '% of the time')
print('- Flank wins ' + str(results.count('Flank')/len(results)) + '% of the time')

print('Attack vs Defense: ')
results = []
for _ in range(500):
    winner = run_game('Attack','Defense',_)
    results.append(winner)

for _ in range(500):
    winner = run_game('Defense','Attack',_+500)
    results.append(winner)

print('- Attack wins ' + str(results.count('Attack')/len(results)) + '% of the time')
print('- Defense wins ' + str(results.count('Defense')/len(results)) + '% of the time')

print('Attack vs Flank: ')
results = []
for _ in range(500):
    winner = run_game('Attack','Flank',_)
    results.append(winner)

for _ in range(500):
    winner = run_game('Flank','Attack',_+500)
    results.append(winner)

print('- Attack wins ' + str(results.count('Attack')/len(results)) + '% of the time')
print('- Flank wins ' + str(results.count('Flank')/len(results)) + '% of the time')

print('Defense vs Flank: ')
results = []
for _ in range(500):
    winner = run_game('Defense','Flank',_)
    results.append(winner)

for _ in range(500):
    winner = run_game('Defense','Flank',_+50000)
    results.append(winner)

print('- Defense wins ' + str(results.count('Defense')/len(results)) + '% of the time')
print('- Flank wins ' + str(results.count('Flank')/len(results)) + '% of the time')

