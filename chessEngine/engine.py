import chess
import oldevalfuction as oef
import search as s
from collections import defaultdict
import csv



class Engine:
    def __init__(self, depth):
        self.ns = s.NegaSearch(depth)

    def printeval(self, fen: str):
        board = chess.Board(fen)
        
        print(board)
        moves = self.ns.search(board)

        for m, e in moves:
            print(f'Move: {board.san(m)}, eval: {e}')
            board.push(m)
            print(f'board:\n{board}')

        print(moves)
    
    def findmoves(self, fens):
        out = []
        for i in range(len(fens)):
            out.append(self.bestmove(fens[i]))

            #print(f'fen evaluated: {i}/{len(fens)}')

        return out
    
    def bestmove(self, fen):
        board = chess.Board(fen)
        self.ns.search(board)
        return board.san(self.ns.bestMove)

if __name__ == '__main__':
    e = Engine(6)

    e.printeval('2r4r/1bn1qpk1/p3p2p/1p1pP2R/3N1QP1/8/PPP3BP/3R2K1 w - - 1 28')
