__all__ = (
    'HOST', 'PORT', 'CLIENT_RESET', 'CLIENT_STEP',
    'CLIENT_STARTED', 'CLIENT_AWAIT', 'PLAYER_BUY_WORKER', 'PLAYER_BUY_WARRIOR', 'PLAYER_ACTION_ATTACK',
    'PLAYER_FINISH_STEP', 'IS_WARRIOR', 'IS_WORKER', 'PRICE_WARRIOR', 'PRICE_WORKER'
)

HOST = "localhost"
PORT = 5555

CLIENT_STARTED = '0'
CLIENT_RESET = '1'
CLIENT_STEP = '2'
CLIENT_AWAIT = '3'

PLAYER_BUY_WORKER = '4'
PLAYER_BUY_WARRIOR = '5'
PLAYER_ACTION_ATTACK = '6'
PLAYER_FINISH_STEP = '7'

IS_WORKER = 1
IS_WARRIOR = 2

PRICE_WORKER = 5
PRICE_WARRIOR = 10
