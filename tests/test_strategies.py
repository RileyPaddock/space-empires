import sys
sys.path.append('src')
from game import Game
from strategies.dumb_strategy1 import DumbStrategyLevel1
from strategies.random_strategy1 import RandomStrategyLevel1
from strategies.beserker_strategy1 import BerserkerStrategyLevel1
from strategies.flank_strategy import FlankerStrategyLevel1
from strategies.riley_strategy import RileyStrategy

strategy_1 = DumbStrategyLevel1
strategy_2 = RandomStrategyLevel1
strategy_3 = BerserkerStrategyLevel1
strategy_4 = FlankerStrategyLevel1
strategy_5 = RileyStrategy

def run_game(strategy1, strategy2):
    strats = {'Dumb':DumbStrategyLevel1, 'Random':RandomStrategyLevel1, 'Berserker':BerserkerStrategyLevel1, 'Flanker':FlankerStrategyLevel1, 'Riley':RileyStrategy}
    new_game = Game(logging = False, die_rolls = 'random', restricted = 'True')
    new_game.add_player(strats[strategy1](0), [2,0])
    new_game.add_player(strats[strategy2](1), [2,4])
    new_game.initialize_game()
    new_game.run_to_completion()
    return strategy1 if new_game.winner == 0 else strategy2


print('Random vs Dumb: ')
results = []
for _ in range(50):
    results.append(run_game('Random','Dumb'))

for _ in range(50):
    results.append(run_game('Dumb','Random'))

print('- Random wins ' + str(results.count('Random')/len(results)) + '% of the time')
print('- Dumb wins ' + str(results.count('Dumb')/len(results)) + '% of the time')


print('Berserker vs Dumb: ')
results = []
for _ in range(50):
    results.append(run_game('Berserker','Dumb'))

for _ in range(50):
    results.append(run_game('Dumb','Berserker'))

print('- Berserker wins ' + str(results.count('Berserker')/len(results)) + '% of the time')
print('- Dumb wins ' + str(results.count('Dumb')/len(results)) + '% of the time')


print('Berserker vs Random: ')
results = []
for _ in range(50):
    results.append(run_game('Berserker','Random'))

for _ in range(50):
    results.append(run_game('Random','Berserker'))

print('- Berserker wins ' + str(results.count('Berserker')/len(results)) + '% of the time')
print('- Random wins ' + str(results.count('Random')/len(results)) + '% of the time')


print('Flanker vs Random: ')
results = []
for _ in range(50):
    results.append(run_game('Flanker','Random'))

for _ in range(50):
    results.append(run_game('Random','Flanker'))

print('- Flanker wins ' + str(results.count('Flanker')/len(results)) + '% of the time')
print('- Random wins ' + str(results.count('Random')/len(results)) + '% of the time')


print('Flanker vs Berserker: ')
results = []
for _ in range(50):
    results.append(run_game('Flanker','Berserker'))

for _ in range(50):
    results.append(run_game('Berserker','Flanker'))

print('- Flanker wins ' + str(results.count('Flanker')/len(results)) + '% of the time')
print('- Berserker wins ' + str(results.count('Berserker')/len(results)) + '% of the time')

