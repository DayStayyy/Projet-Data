import pyautogui
import json
import requests
import chess
# import chess.engine
from optparse import OptionParser
import IaMinMax as IaMinMax

parser = OptionParser()
parser.add_option("-c", "--color", dest="player_color", default="white", help="The color of the player (white or black)")
parser.add_option("-x", "--abscissa", dest="board_abscissa", default="146", help="The abscissa corresponding to the beginning of the board")
parser.add_option("-y", "--ordinate", dest="board_ordinate", default="202", help="The ordinate corresponding to the beginning of the board")
parser.add_option("-w", "--width", dest="board_width", default="634", help="The width of the board")
(options, args) = parser.parse_args()

x = int(options.board_abscissa)
y = int(options.board_ordinate)
width = int(options.board_width) - int(options.board_abscissa)

coordinates = { 
    "a": x + (width / 16), "b": x + (width / 16) + (width / 8), "c": x + (width / 16) + 2 *(width / 8), "d": x + (width / 16) + 3 *(width / 8), "e": x + (width / 16) + 4 *(width / 8), "f": x + (width / 16) + 5 *(width / 8), "g": x + (width / 16) + 6 *(width / 8), "h": x + (width / 16) + 7 *(width / 8),
    "8": y + (width / 16), "7": y + (width / 16) + (width / 8), "6": y + (width / 16) + 2 * (width / 8), "5": y + (width / 16) + 3 * (width / 8), "4": y + (width / 16) + 4 * (width / 8), "3": y + (width / 16) + 5 * (width / 8), "2": y + (width / 16) + 6 * (width / 8), "1": y + (width / 16) + 7 * (width / 8) 
    }

def get_board():
    screenshot = pyautogui.screenshot(region=(x, y, width, width))
    screenshot.save("chess_bot/chess_board.png")

    url = "https://web-vrnocjtpaa-an.a.run.app/board_to_fen"
    files = {'image': open('chess_bot/chess_board.png', 'rb')}
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