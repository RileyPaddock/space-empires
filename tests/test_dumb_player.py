import sys
sys.path.append('src')
from game import Game
from players.player import Player
from strategies.dumb_strategy import DumbStrategy
from board import Board
from units.scout import Scout
del sys.path[-1]
sys.path.append('imported_strategies')
from colby_dumb_strategy import DumbStrategy as CDS
from elijah_dumb_strategy import DumbStrategy as EDS
from george_dumb_strategy import DumbStrategy as GDS
from david_dumb_strategy import DumbStrategy as DDS

for strategy in [DumbStrategy, EDS, DDS]:
    print("Strategy #: "+str([DumbStrategy, EDS, DDS].index(strategy)))
    b = Board([5,5],[(2,0),(2,4)])
    p1 = Player(strategy(0),(2,0),b)
    p2 = Player(strategy(1),(2,4),b)
    game = Game(players = [p1,p2],board = b,logging = False)



    def assert_player_scouts(player, pos, amt):
        state = game.generate_state()
        units = [u for u in state['players'][player-1]['units']
                if u['coords'] == pos and u['type'] == 'Scout']
        print(len(units), amt)
        #assert len(units) == amt, 'Incorrect num scouts, Got: '+ str(len(units))+' Wanted: '+ str(amt)


    def assert_player_economic(player, cps):
        state = game.generate_state()
        print(state['players'][player-1]['cp'], cps)
        #assert state['players'][player-1]['cp'] == cps, 'Incorrect CP, Got: ' + str(state['players'][player-1]['cp']) + ' Wanted: '+str(cps)


    # 1 Movement Phase
    print("Turn 1 Movement Phase")
    game.complete_movement_phase()
    assert_player_scouts(1, (4, 0), 3)
    assert_player_scouts(2, (4, 4), 3)

    # 1 Combat Phase (nothing happens)
    print("Turn 1 Combat Phase")
    game.complete_combat_phase()


    # 1 Economic Phase
    print("Turn 1 Economic Phase")
    game.complete_economic_phase()
    assert_player_economic(1, 5)
    assert_player_economic(2, 5)

    assert_player_scouts(1, (4, 0), 3)
    assert_player_scouts(2, (4, 4), 3)
    assert_player_scouts(1, (2, 0), 2)
    assert_player_scouts(2, (2, 4), 2)

    # 2 Movement Phase
    print("Turn 2 Movement Phase")
    print([unit.unit_type for unit in game.players[0].units])
    game.complete_movement_phase()
    assert_player_scouts(1, (4, 0), 5)
    assert_player_scouts(2, (4, 4), 5)

    # 2 Combat Phase (nothing happens)
    print("Turn 2 Combat Phase")
    game.complete_combat_phase()

    # 2 Economic Phase
    print("Turn 2 Economic Phase")
    game.complete_economic_phase()
    assert_player_economic(1, 2)
    assert_player_economic(2, 2)

    assert_player_scouts(1, (4, 0), 5)
    assert_player_scouts(2, (4, 4), 5)
    assert_player_scouts(1, (2, 0), 3)
    assert_player_scouts(2, (2, 4), 3)

    # 3 Movement Phase
    print("Turn 3 Movement Phase")
    game.complete_movement_phase()
    assert_player_scouts(1, (4, 0), 8)
    assert_player_scouts(2, (4, 4), 8)

    # 3 Combat Phase (nothing happens)
    print("Turn 3 Combat Phase")
    game.complete_combat_phase()

    # 3 Economic Phase
    print("Turn 3 Economic Phase")
    game.complete_economic_phase()
    assert_player_scouts(1, (4, 0), 8)
    assert_player_scouts(2, (4, 4), 8)
    assert_player_scouts(1, (2, 0), 2)
    assert_player_scouts(2, (2, 4), 2)

    assert_player_economic(1, 2)
    assert_player_economic(2, 2)

    # 4 Movement Phase
    print("Turn 4 Movement Phase")
    game.complete_movement_phase()
    assert_player_scouts(1, (4, 0), 10)
    assert_player_scouts(2, (4, 4), 10)

    # 4 Combat Phase (nothing happens)
    print("Turn 4 Combat Phase")
    game.complete_combat_phase()

    # 4 Economic Phase
    print("Turn 4 Economic Phase")
    game.complete_economic_phase()
    assert_player_scouts(1, (4, 0), 10)
    assert_player_scouts(2, (4, 4), 10)

    assert_player_economic(1, 0)
    assert_player_economic(2, 0)



