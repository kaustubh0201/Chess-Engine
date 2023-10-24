import chess
import evalfuction as ef
import oldevalfuction as oef

import utility as u

import random as r
import typing as t
from dataclasses import dataclass 
import enum
import copy

class ZobristHash:

    def __init__(self) -> None:
        self.pieceSquareHash = {}
        self.blackTurnHash = None
        self.castlingRightsHash = {} 
        self.passantFileHash = {}

        self.randomNumbersUsed = []

        self._genRandomArray()

    def _genRandomArray(self) -> None:
        
        # (square, color, piece)
        for s in chess.SQUARES:
            for c in [chess.WHITE, chess.BLACK]:
                for p in chess.PIECE_TYPES:
                    self.pieceSquareHash[(s, c, p)] = self._getRandom()

        self.blackTurnHash = self._getRandom()

        # (white kingside, white queenside, black kingside, black queenside)
        for i in range(0, 16):
            self.castlingRightsHash[i] = self._getRandom()

        for f in range(0, 8):
            self.passantFileHash[f] = self._getRandom()

    def getInitalZobristKey(self) -> int:
        key = 0
        
        # white pawns
        key ^= self.pieceSquareHash[(chess.A2, chess.WHITE, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.B2, chess.WHITE, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.C2, chess.WHITE, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.D2, chess.WHITE, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.E2, chess.WHITE, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.F2, chess.WHITE, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.G2, chess.WHITE, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.H2, chess.WHITE, chess.PAWN)]

        # white pieces
        key ^= self.pieceSquareHash[(chess.A1, chess.WHITE, chess.ROOK)]
        key ^= self.pieceSquareHash[(chess.B1, chess.WHITE, chess.KNIGHT)]
        key ^= self.pieceSquareHash[(chess.C1, chess.WHITE, chess.BISHOP)]
        key ^= self.pieceSquareHash[(chess.D1, chess.WHITE, chess.QUEEN)]
        key ^= self.pieceSquareHash[(chess.E1, chess.WHITE, chess.KING)]
        key ^= self.pieceSquareHash[(chess.F1, chess.WHITE, chess.BISHOP)]
        key ^= self.pieceSquareHash[(chess.G1, chess.WHITE, chess.KNIGHT)]
        key ^= self.pieceSquareHash[(chess.H1, chess.WHITE, chess.ROOK)]


        # black pawns
        key ^= self.pieceSquareHash[(chess.A7, chess.BLACK, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.B7, chess.BLACK, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.C7, chess.BLACK, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.D7, chess.BLACK, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.E7, chess.BLACK, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.F7, chess.BLACK, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.G7, chess.BLACK, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.H7, chess.BLACK, chess.PAWN)]

        # black pieces
        key ^= self.pieceSquareHash[(chess.A8, chess.BLACK, chess.ROOK)]
        key ^= self.pieceSquareHash[(chess.B8, chess.BLACK, chess.KNIGHT)]
        key ^= self.pieceSquareHash[(chess.C8, chess.BLACK, chess.BISHOP)]
        key ^= self.pieceSquareHash[(chess.D8, chess.BLACK, chess.QUEEN)]
        key ^= self.pieceSquareHash[(chess.E8, chess.BLACK, chess.KING)]
        key ^= self.pieceSquareHash[(chess.F8, chess.BLACK, chess.BISHOP)]
        key ^= self.pieceSquareHash[(chess.G8, chess.BLACK, chess.KNIGHT)]
        key ^= self.pieceSquareHash[(chess.H8, chess.BLACK, chess.ROOK)]

        # all sides castling possible
        key ^= self.castlingRightsHash[15]

        return key

    def _getCastlingRightsAfterMoveHash(self, 
        board: chess.Board, 
        move: chess.Move
        ) -> int:

        beforeMoveCastleID: int = self._getCastleID(board)
        board.push(move)
        afterMoveCastleID: int = self._getCastleID(board)
        board.pop()

        return self.castlingRightsHash[beforeMoveCastleID] ^ \
        self.castlingRightsHash[afterMoveCastleID]

    def _getPieceMoveHash(self, board: chess.Board, move: chess.Move) -> int:
        fromSquare: chess.Square = move.from_square
        toSquare: chess.Square = move.to_square

        movedPiece = board.piece_at(fromSquare)

        # None if no piece is captured
        capturedPiece = board.piece_at(toSquare) 

        if(capturedPiece == None):
            return \
               self.pieceSquareHash[(fromSquare, movedPiece.color, movedPiece.piece_type)]\
            ^  self.pieceSquareHash[(toSquare, movedPiece.color, movedPiece.piece_type)] 

        return \
           self.pieceSquareHash[(fromSquare, movedPiece.color, movedPiece.piece_type)]\
        ^  self.pieceSquareHash[(toSquare, movedPiece.color, movedPiece.piece_type)]\
        ^  self.pieceSquareHash[(toSquare, capturedPiece.color, capturedPiece.piece_type)]
 
    def _getEnPassantFileHash(self, board: chess.Board, move: chess.Move) -> int:
        beforeEnPassantFiles = self._getEnPassantFiles(board)
        board.push(move)
        afterEnPassantFiles = self._getEnPassantFiles(board)
        board.pop()

        finalHash = 0
        for f in (beforeEnPassantFiles + afterEnPassantFiles):
            finalHash ^= self.passantFileHash[f]

        return finalHash 

    def makeMove(self, board: chess.Board, move: chess.Move, key: int) -> int:
        p = board.piece_at(move.to_square)

        if(p == chess.KING or p == chess.ROOK):
            key ^= self._getCastlingRightsAfterMoveHash(board, move) 
            
        ## piece move
        if(move != chess.Move.null()):
            key ^= self._getPieceMoveHash(board, move) 
        
        ## turn
        key ^= self.blackTurnHash 

        ## en passant
        if(p == chess.PAWN):
            key ^= self._getEnPassantFileHash(board, move)

        return key

    def hashOfPosition(self, board: chess.Board) -> int:
        # castling
        castlingHash: int = self.castlingRightsHash[self._getCastleID(board)] 

        # piece position
        pieceMap: t.Dict[chess.Square, chess.Piece] =  board.piece_map()
        piecePositionHash: int = 0
        for s, p in pieceMap.items():

            piecePositionHash ^= self.pieceSquareHash[(
                s, p.color, p.piece_type 
            )]
        
        # turn
        blackTurnHash = self.blackTurnHash if board.turn == chess.BLACK else 0

        # en passant files
        enPassantHash = 0
        for f in self._getEnPassantFiles(board):
            enPassantHash ^= self.passantFileHash[f]               

        return castlingHash ^ piecePositionHash ^ enPassantHash ^ blackTurnHash 
    
    def _getEnPassantFiles(self, board: chess.Board) -> t.List[int]:
        legalMoves = board.legal_moves

        return [
            chess.square_file(move.to_square) 
            for move in legalMoves 
                if (board.is_en_passant(move))
            ]

    def _getCastleID(self, board: chess.Board) -> int:
        wk = int(board.has_kingside_castling_rights(chess.WHITE))
        wq = int(board.has_queenside_castling_rights(chess.WHITE))
        bk = int(board.has_kingside_castling_rights(chess.BLACK))
        bq = int(board.has_queenside_castling_rights(chess.BLACK))

        return u.listToBinary([wk, wq, bk, bq]) 

    def _getRandom(self) -> int: 
        num = r.getrandbits(64)
        while(num in self.randomNumbersUsed):
            num = r.getrandbits(64)

        self.randomNumbersUsed.append(num)
        return num 

@enum.unique
class NodeType(enum.Enum):
    UPPERBOUND = enum.auto()
    LOWERBOUND = enum.auto()
    EXACT = enum.auto()

@dataclass
class TTEntry:
    value: float 
    depth: int
    nodeType: NodeType
    bestMove: chess.Move


class TranspositionTable:
    def __init__(self) -> None:
        self.table: t.Dict[int, TTEntry] = {}

    def isInTable(self, hash:int) -> bool:
        return hash in self.table

    def add(self, hash: int, value: float, depth: int, nodeType: NodeType):
        self.table[hash] = TTEntry(value = value, depth = depth, nodeType = nodeType)

    def add(self, hash: int, entry: TTEntry):
        self.table[hash] = entry 

    def get(self, hash: int) -> t.Union[TTEntry, None]:
        return self.table.get(hash, None) 

class MoveOrdering:
    
    def __init__(self) -> None:
        self.CAPTURED_PIECE_MULTIPLIER: int = 10
        self.KILLERMOVE_BONUS: int          = 100
        self.BESTOVE_BONUS: int             = 200
        self.KILLERMOVES_COUNT: int         = 3

        self.bestMove : chess.Move = None
        self.killerMoves : t.Dict[int, t.List[chess.Move]] = {}

    def _capturedPieceBonus(self, 
        board: chess.Board, 
        move: chess.Move
        ) -> t.Tuple[int, bool]:

        pieceValues: t.Dict[int, int] = {
            chess.PAWN: 1,
            chess.KNIGHT: 3, 
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 1
        }


        fromSquare: chess.Square = move.from_square
        toSquare: chess.Square = move.to_square

        movedPiece = board.piece_at(fromSquare)
        capturedPiece = board.piece_at(toSquare)

        if(capturedPiece == None):
            return 0, False

        return self.CAPTURED_PIECE_MULTIPLIER \
        * pieceValues[capturedPiece.piece_type] \
        - pieceValues[movedPiece.piece_type], True

    def _killerMoveBonus(self, depth: int, move: chess.Move):
        if (depth in self.killerMoves and move in self.killerMoves[depth]):
            return self.KILLERMOVE_BONUS

        return 0 

    def orderMoves(self, board: chess.Board, depth: int) -> t.List[chess.Move]:
        moves = []

        for move in board.legal_moves:
            priority: int = 0

            # capture priority increase
            bonus, isCapture = self._capturedPieceBonus(board, move) 
            priority += bonus 

            if(not isCapture):
                priority += self._killerMoveBonus(depth, move)

            # if(move == self.bestMove):
            #     priority += self.BESTOVE_BONUS

            moves.append((priority, move))

        moves = sorted(moves, key = lambda k: k[0], reverse = True)
        return [m[1] for m in moves] 

    def setBestMove(self, move: chess.Move) -> None:
        self.bestMove = move

    def addKillerMove(self, move: chess.Move, depth: int) -> None:
        if(depth in self.killerMoves):
            self.killerMoves[depth].insert(0, move)

            if(len(self.killerMoves[depth]) > self.KILLERMOVES_COUNT):
                self.killerMoves[depth].pop()

        else:
            self.killerMoves[depth] = [move]
        
class NegaSearch:
    def __init__(self, maxDepth: int) -> None:
        self.maxDepth: int = maxDepth
        self.evaluation: ef.EvalFunc = ef.EvalFunc() 

        self.tt: TranspositionTable = TranspositionTable()
        self.hashFunc = ZobristHash()
        self.ordering = MoveOrdering()
        self.NULLMOVE_DEPTH = 2

    def search(self, board: chess.Board) -> None:
        initalHash = self.hashFunc.hashOfPosition(board)

        self.auxSearch(board, self.maxDepth, initalHash)

        return self.getPVLine(board, initalHash)
    
    def getPVLine(self, 
        board: chess.Board, 
        hash: int
        ) -> t.List[t.Tuple[chess.Move, float]]:

        line: t.List[t.Tuple[chess.Move, float]] = []

        ttEntry = self.tt.get(hash)
        tempBoard = copy.deepcopy(board)
        lineLen = 0
        while(
            ttEntry != None and 
            ttEntry.bestMove != None and 
            lineLen <= self.maxDepth
        ):
            line.append((ttEntry.bestMove, ttEntry.value))
            hash = self.hashFunc.makeMove(tempBoard, ttEntry.bestMove, hash) 
            tempBoard.push(ttEntry.bestMove)

            ttEntry = self.tt.get(hash)
            lineLen += 1


        return line


    @staticmethod
    def _canReduce(board: chess.Board) -> bool:
        return not board.is_check()

    @staticmethod 
    def _possibleZugzawng(board: chess.Board) -> bool:
        pieces = board.piece_map().values()

        for p in pieces:
            if(p != chess.KING and p != chess.PAWN):
                return False 

        return True 

    def auxSearch(self, 
        board: chess.Board, 
        depth: int, 
        hash: int,  
        alpha: float = float('-inf'), 
        beta: float = float('inf')) -> float:

        alphaOrg: float = alpha
        # Checking the transposition table
        entry: t.Union[TTEntry, None] = self.tt.get(hash) 
        if(entry != None and (entry.depth >= depth)):

            value: float = entry.value

            if(entry.nodeType == NodeType.EXACT):
                return value
            elif (entry.nodeType == NodeType.LOWERBOUND):
                alpha = max(alpha, value)
            elif (entry.nodeType == NodeType.UPPERBOUND):
                beta = min(beta, value)

            if(alpha >= beta):
                return value

        # Reached the leaf node
        if(depth <= 0):
            return self.evaluation.testEval2(board)

        # checkmate or stalemate
        if(board.legal_moves.count() == 0):
            if(board.is_checkmate()):
                return u.FLOAT_MAX if board.outcome().winner == board.turn else -u.FLOAT_MAX
 
            return 0.0

        if(NegaSearch._canReduce(board) and not NegaSearch._possibleZugzawng(board)):

            board.push(chess.Move.null())
            newHash = self.hashFunc.makeMove(board, chess.Move.null(), hash)
            value = - self.auxSearch(board, depth - 1 - self.NULLMOVE_DEPTH, newHash, -beta, -alpha) 
            board.pop()

            if(value >= beta):
                return value


        # search 
        newEntry: TTEntry = TTEntry(float('-inf'), depth, NodeType.EXACT, None)

        orderedMoves: t.List[chess.Move] = self.ordering.orderMoves(board, depth)
        bestEval = float('-inf')
        for i, move in enumerate(orderedMoves):

            # if(depth == self.maxDepth):
            #     print(move)

            newHash = self.hashFunc.makeMove(board, move, hash)

            value = 0
            if(i == 0):
                board.push(move)
                value = -self.auxSearch(board, depth - 1, newHash, -beta, -alpha) 
                board.pop()
            else:
                board.push(move)
                value = -self.auxSearch(board, depth - 1, newHash, -alpha - 1, -alpha)
                board.pop()

                if(alpha < value < beta):
                    board.push(move)
                    value = -self.auxSearch(board, depth - 1, newHash, -beta, -value)
                    board.pop()


            #board.push(move)
            #value = -self.auxSearch(board, depth - 1, newHash, -beta, -alpha) 
            #board.pop()

            if(value > bestEval):
                bestEval = value
                newEntry.bestMove = move

            alpha = max(value, alpha)

            if(alpha >= beta):
                if(not board.is_capture(move)):
                    self.ordering.addKillerMove(move, depth)
                break

            if(depth == self.maxDepth):
                print(move, " ", value, " ", (move, bestEval))

        newEntry.value = bestEval 

        if(bestEval <= alphaOrg):
            newEntry.nodeType = NodeType.UPPERBOUND
        elif (bestEval >= beta):
            newEntry.nodeType = NodeType.LOWERBOUND
        else:
            newEntry.nodeType = NodeType.EXACT


        self.tt.add(hash, newEntry)

        return bestEval 