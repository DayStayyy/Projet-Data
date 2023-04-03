import pyautogui
import json
import requests
import chess
# import chess.engine
from optparse import OptionParser
import IaMinMax

parser = OptionParser()
parser.add_option("-c", "--color", dest="player_color", default="white", help="The color of the player (white or black)")
(options, args) = parser.parse_args()

x, y, width, height = 86, 135, 560, 560
# x, y, width, height = 146, 202, 488, 488

coordinates = { 
    "a": 121, "b": 191, "c": 261, "d": 331, "e": 401, "f": 471, "g": 541, "h": 611,
    "8": 170, "7": 240, "6": 310, "5": 380, "4": 450, "3": 520, "2": 590, "1": 660 
    }
# coordinates = {
#     "a": 176.5, "b": 237.5, "c": 298.5, "d": 359.5, "e": 420.5, "f": 481.5, "g": 542.5, "h": 603.5,
#     "8": 232.5, "7": 293.5, "6": 354.5, "5": 415.5, "4": 476.5, "3": 537.5, "2": 598.5, "1": 659.5 
# }

def get_board():
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save("chess_board.png")

    url = "https://web-vrnocjtpaa-an.a.run.app/board_to_fen"
    files = {'image': open('chess_board.png', 'rb')}
    response = requests.post(url, files=files)
    data = json.loads(response.text)

    if options.player_color == "white":
        return chess.Board(data['fen'])
    elif options.player_color == "black":
        return chess.Board(data['fen'] + " b - - 0 1")

# engine = chess.engine.SimpleEngine.popen_uci("stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2.exe")
old_fen_board = "8/8/8/8/8/8/8/8 w - - 0 1"
board = chess.Board()

chessAI = IaMinMax.ChessMinMax(2)

while True:
    if get_board().fen().split()[0] != old_fen_board.split()[0]:
        board = get_board()

        # result = engine.play(board, chess.engine.Limit(time=5.0))
        # best_move = result.move

        best_move = chessAI.selectmove(board)

        pyautogui.click(coordinates[best_move.uci()[0]], coordinates[best_move.uci()[1]], button='left')
        pyautogui.click(coordinates[best_move.uci()[2]], coordinates[best_move.uci()[3]], button='left')

        # TODO: Rempalcer par un dictionnaire
        if best_move.uci()[3] == '1' or best_move.uci()[3] == '8':
            if best_move.uci()[-2:] == '8q':
                pyautogui.click(coordinates[best_move.uci()[2]], coordinates['8'], button='left')
            elif best_move.uci()[-2:] == '8n':
                pyautogui.click(coordinates[best_move.uci()[2]], coordinates['7'], button='left')
            elif best_move.uci()[-2:] == '8r':
                pyautogui.click(coordinates[best_move.uci()[2]], coordinates['6'], button='left')
            elif best_move.uci()[-2:] == '8b':
                pyautogui.click(coordinates[best_move.uci()[2]], coordinates['5'], button='left')
            elif best_move.uci()[-2:] == '1q':
                pyautogui.click(coordinates[best_move.uci()[2]], coordinates['1'], button='left')
            elif best_move.uci()[-2:] == '1n':
                pyautogui.click(coordinates[best_move.uci()[2]], coordinates['2'], button='left')
            elif best_move.uci()[-2:] == '1r':
                pyautogui.click(coordinates[best_move.uci()[2]], coordinates['3'], button='left')
            elif best_move.uci()[-2:] == '1b':
                pyautogui.click(coordinates[best_move.uci()[2]], coordinates['4'], button='left')

        board.push(best_move)
        if board.is_checkmate():
            break

        if get_board().fen().split()[0] != old_fen_board.split()[0]:    
            old_fen_board = get_board().fen()

# engine.quit()