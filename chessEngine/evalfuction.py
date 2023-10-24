from functools import reduce
import chess
import unittest

import typing as t

import pieceNeigboursDict as pnd


class PieceTables:
    def __init__(self) -> None:
        self.PIECE_SQUARE_TABLES = {
            chess.PAWN: [   # Pawn
                0,   0,   0,   0,   0,   0,  0,  0,
                5,  10,  10, -20, -20,  10, 10,  5,
                5,  -5, -10,   0,   0, -10, -5,  5,
                0,   0,   0,  20,  20,   0,  0,  0,
                5,   5,  10,  25,  25,  10,  5,  5,
                10,  10,  20,  30,  30,  20, 10, 10,
                50,  50,  50,  50,  50,  50, 50, 50,
                0,   0,   0,   0,   0,   0,  0,  0
            ],
            chess.KNIGHT: [   # Knight
                -50, -40, -30, -30, -30, -30, -40, -50,
                -40, -20,   0,   0,   0,   0, -20, -40,
                -30,   5,  10,  15,  15,  10,   5, -30,
                -30,   0,  15,  20,  20,  15,   0, -30,
                -30,   0,  10,  15,  15,  10,   0, -30,
                -30,   5,  15,  20,  20,  15,   5, -30,
                -40, -20,   0,   5,   5,   0, -20, -40,
                -50, -40, -30, -30, -30, -30, -40, -50
            ],
            chess.BISHOP: [   # Bishop
                -20, -10, -10, -10, -10, -10, -10, -20,
                -10,   5,   0,   0,   0,   0,   5, -10,
                -10,  10,  10,  10,  10,  10,  10, -10,
                -10,   0,  10,  10,  10,  10,   0, -10,
                -10,   5,   5,  10,  10,   5,   5, -10,
                -10,   0,   5,  10,  10,   5,   0, -10,
                -10,   0,   0,   0,   0,   0,   0, -10,
                -20, -10, -10, -10, -10, -10, -10, -20
            ],
            chess.ROOK: [   # Rook
                0,  0,  0,  5,  5,  0,  0,  0,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                5, 10, 10, 10, 10, 10, 10,  5,
                0,  0,  0,  0,  0,  0,  0,  0
            ],
            chess.QUEEN: [   # Queen
                -20, -10, -10, -5, -5, -10, -10, -20,
                -10,   0,   5,  0,  0,   0,   0, -10,
                -10,   5,   5,  5,  5,   5,   0, -10,
                0,   0,   5,  5,  5,   5,   0,  -5,
                -5,   0,   5,  5,  5,   5,   0,  -5,
                -10,   0,   5,  5,  5,   5,   0, -10,
                -10,   0,   0,  0,  0,   0,   0, -10,
                -20, -10, -10, -5, -5, -10, -10, -20
            ],
            chess.KING: [   # King mid-game
                20,  30,  10,   0,   0,  10,  30,  20,
                20,  20,   0,   0,   0,   0,  20,  20,
                -10, -20, -20, -20, -20, -20, -20, -10,
                -20, -30, -30, -40, -40, -30, -30, -20,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
            ]
        }

class Parameters:
    def __init__(self,

        ## ROOK PARAMETERS
        rValue: float = 500,
        rOpenFile: float = 27,
        rSemiOpenFile: float = 57,
        rClosedFile: float = -46,
        rSeventh: float = 41,
        rMob: float = 9,

        ## PAWN PARAMETERS
        pValue: float = 100,
        pCenter: float = -8,
        pIso: float = -3,
        pDouble: float = -7,
        pPass: float = 62,
        pRookBehindPawn: float = 30,
        pBackward: float = -14,
        pBlocked: float = -23,

        ## KNIGHT PARAMETERS
        kValue: float = 300,
        kPeriphery0: float = -51,
        kPeriphery1: float = -18,
        kPeriphery2: float = 45,
        kPeriphery3: float = -1,
        kSupported: float  = 40,
        kMob: float = 14,

        ## BISHOP PARAMETERS
        bValue: float = 300,
        bOnMainDiag: float = 74,
        bMob: float = 13,

        ## QUEEN PARAMETERS
        qValue: float = 900,
        qMob: float = 3
    ) -> None:

        ## ROOK PARAMETERS
        self.rValue: float        = rValue
        self.rOpenFile: float     = rOpenFile 
        self.rSemiOpenFile: float = rSemiOpenFile 
        self.rClosedFile: float   = rClosedFile 
        self.rSeventh: float      = rSeventh
        self.rMob: float          = rMob

        ## PAWN PARAMETERS 
        self.pValue: float          = pValue
        self.pCenter: float         = pCenter
        self.pIso: float            = pIso
        self.pDouble: float         = pDouble
        self.pPass: float           = pPass
        self.pRookBehindPawn: float = pRookBehindPawn
        self.pBackward: float       = pBackward
        self.pBlocked: float        = pBlocked

        ## KNIGHT PARAMETERS
        self.kValue: float      = kValue
        self.kPeriphery0: float = kPeriphery0
        self.kPeriphery1: float = kPeriphery1
        self.kPeriphery2: float = kPeriphery2
        self.kPeriphery3: float = kPeriphery3
        self.kSupported: float  = kSupported
        self.kMob: float        = kMob

        ## BISHOP PARAMETERS
        self.bValue: float      = bValue
        self.bOnMainDiag: float = bOnMainDiag
        self.bMob: float        = bMob

        ## QUEEN PARAMETERS
        self.qValue: float  = qValue
        self.qMob: float    = qMob

class EvalFunc:
    
    def __init__(self, params: Parameters = None) -> None:

        self.pieceValues = { 
                'kingpawnshield': 35,
                'kingcastled': 60,
                'rankpasspawn': 5,
                'blockedpasspawn': -10, 
                'rookconnected': 12,
                'knightonweaksquare': -39,
                }

        self.VALIDRANGE = range(8)
        self.pieceTables = PieceTables()

        if(params == None):
            self.parameters = Parameters()
        else:
            self.parameters = params

    
    def testEval(self, board: chess.Board) -> float:
        # self._setpieces(board)

        eval_score = self.piecesValueEvaluation(board) 
        return eval_score

    def testEval2(self, board:chess.Board) -> float:
        
        EVAL_FUNCS = {
            chess.ROOK: self.rookEvaluation,
            chess.PAWN: self.pawnEvaluation,
            chess.BISHOP: self.bishopEvaluation,
            chess.KNIGHT: self.knightEvaluation
        }

        color = board.turn
        contrib: t.Dict[bool, int] = {
            color: 1,
            (not color): -1
        } 

        evalScore = self.piecesValueEvaluation(board) + self.mobEvaluation(board)

        piecemap = board.piece_map()
        for s, p in piecemap.items():
            if(p.piece_type == chess.QUEEN or p.piece_type == chess.KING):
                continue 

            evalScore += contrib[p.color] * EVAL_FUNCS[p.piece_type](s, board, p.color)

        return evalScore 

    def _adjacentPieces(self, square: int, board: chess.Board, color: bool, mask: int) -> t.Dict[int, chess.Piece]:
        outDict: t.Dict[int, chess.Piece] = {}

        for s, i, j in pnd.PIECE_NEIGHBOURS_DICT[(square, color)]:
            p = board.occupied_co[color] & mask & chess.BB_SQUARES[s] 
            outDict[(i, j)] = True if p != 0 else False

        return outDict


    def rookEvaluation(self, square: int, board: chess.Board, color: bool) -> float:
        file: int = chess.square_file(square) 
        rank: int = chess.square_rank(square)

        bonus = 0

        ##
        ## FILE TYPE BONUS
        ##

        # 0 -> open file
        # 1 -> semi open file
        # 3 -> closed file
        rookFileType: int = 0 

        # checking every rank 
        piecesOnRooksFile = board.piece_map(
            mask = chess.BB_FILES[file] 
        )

        for s, p in piecesOnRooksFile.items():
            if(p.piece_type == chess.PAWN):

                if(p.color == color):
                    rookFileType |= 0x1

                if(p.color == (not color)):
                    rookFileType |= 0x2

        if(rookFileType == 0):
            bonus += self.parameters.rOpenFile
        elif (rookFileType == 1):
            bonus += self.parameters.rSemiOpenFile
        elif(rookFileType == 3):
            bonus += self.parameters.rClosedFile
    
        ##
        ## RANK BONUS
        ##
        BONUS_RANKS = {chess.WHITE: 6, chess.BLACK: 1}
        if(rank == BONUS_RANKS[color]):
            bonus += self.parameters.rSeventh 

        return bonus
    
    def pawnEvaluation(self, square: int, board: chess.Board, color: bool) -> float:
        file: int = chess.square_file(square) 
        rank: int = chess.square_rank(square)

        bonus: float = 0

        ##
        ## CENTER PAWN BONUS
        ##
        CENTER_SQUARES = [chess.E4, chess.E5, chess.D4, chess.D5]
        isCentral = False
        if(square in CENTER_SQUARES):
            isCentral = True
            bonus += self.parameters.pCenter

        ##
        ## ISOLATED PAWNS
        ##
        adjacentPieces: t.Dict[int, chess.Piece] = self._adjacentPieces(square, board, color, board.pawns)

        isIso = any(adjacentPieces.values()) == False

        if(isIso):
            bonus += self.parameters.pIso
        
        ##
        ## DOUBLED PAWNS
        ## 
        piecesAboveMask, piecesBelowMask = pnd.RANK_MASKS[rank]

        if(color == chess.BLACK):
            piecesAboveMask, piecesBelowMask = piecesBelowMask, piecesAboveMask 

        piecesBehindMask = piecesBelowMask & chess.BB_FILES[file]
        pawnsBehind =  piecesBehindMask & board.pawns & board.occupied_co[color]
        isDouble = pawnsBehind != 0

        if(isDouble):
            bonus += self.parameters.pDouble

        ##
        ## PASS PAWNS
        ##
        adjacentFilesMask = pnd.ADJACENT_FILES_MASK[file]

        piecesAheadOnNeighbouringFilesMask = piecesAboveMask & adjacentFilesMask
        enemyPawnsAheadOnNeighbouringFiles =  piecesAheadOnNeighbouringFilesMask & board.pawns & board.occupied_co[not color] 

        isPassPawn = enemyPawnsAheadOnNeighbouringFiles == 0
       
        if(isPassPawn):
            bonus += self.parameters.pPass

        ##
        ## ROOK BEHIND PASS PAWN 
        ##
        if(isPassPawn and (not isDouble)):
            rooksBehind = piecesBehindMask & board.rooks & board.occupied_co[color]

            if(rooksBehind != 0):
                bonus += self.parameters.pRookBehindPawn

        ##
        ## BACKWARD PAWNS 
        ##
        if(not isIso):
            b1 = adjacentPieces.get((1, -1), False)
            b2 = adjacentPieces.get((0, -1), False)
            b3 = adjacentPieces.get((-1, -1), False)

            if(b1 == b2 == b3 == False):
                a1 = adjacentPieces.get((1, 1), False)
                a3 = adjacentPieces.get((-1, 1), False)

                isBackward = a1 or a3 

                if(isBackward):
                    bonus += self.parameters.pBackward

        ##
        ## BLOCKED PAWN
        ##
        if(isCentral):
            piecesAhead = piecesAboveMask & chess.BB_FILES[file] & board.occupied_co[color] 

            isBlocked = piecesAhead != 0 

            if(isBlocked):
                bonus += self.parameters.pBlocked

        return bonus


    def knightEvaluation(self, square: int, board: chess.Board, color: bool) -> float:
        file: int = chess.square_file(square) 
        rank: int = chess.square_rank(square)

        bonus: float = 0

        ##
        ## KNIGHT PERIPHERY
        ## 
        k0: float = self.parameters.kPeriphery0
        k1: float = self.parameters.kPeriphery1
        k2: float = self.parameters.kPeriphery2
        k3: float = self.parameters.kPeriphery3

        KNIGHT_PERIPHERY = [   # Knight
            k0, k0, k0, k0, k0, k0, k0, k0,
            k0, k1, k1, k1, k1, k1, k1, k0,
            k0, k1, k2, k2, k2, k2, k1, k0,
            k0, k1, k2, k3, k3, k2, k1, k0,
            k0, k1, k2, k3, k3, k2, k1, k0,
            k0, k1, k2, k2, k2, k2, k1, k0,
            k0, k1, k1, k1, k1, k1, k1, k0,
            k0, k0, k0, k0, k0, k0, k0, k0
        ]

        bonus += KNIGHT_PERIPHERY[square]

        ##
        ## KNIGHT SUPPORTED 
        ##

        adjacentPieces: t.Dict[int, chess.Piece] = self._adjacentPieces(square, board, color, board.pawns)
        b1 = adjacentPieces.get((-1, -1), False)
        b3 = adjacentPieces.get((1, -1), False)

        isSupported = b1 or b3 
        if(isSupported):
            bonus += self.parameters.kSupported

        return bonus

    def bishopEvaluation(self, square: int, board: chess.Board, color: bool) -> float:
        file: int = chess.square_file(square) 
        rank: int = chess.square_rank(square)

        bonus: float = 0

        ##
        ## BISHOP ON LARGE
        ## 
        WHITEDIAGSQUARES: t.List[chess.Move] = [
                chess.H1, chess.G2, chess.F3, chess.E4,
                chess.D5, chess.C6, chess.B7, chess.A8]
        
        BLACKDIAGSQUARES: t.List[chess.Move] = [
                chess.A1, chess.B2, chess.C3, chess.D4,
                chess.E5, chess.F6, chess.G7, chess.H8
                ]

        if(square in WHITEDIAGSQUARES or square in BLACKDIAGSQUARES):
            bonus += self.parameters.bOnMainDiag

        return bonus

    def mobEvaluation(self, board: chess.Board) -> float:
        color: bool = board.turn 

        pieceBonus: t.Dict[int, float] = {
            chess.ROOK: self.parameters.rMob,
            chess.KNIGHT: self.parameters.kMob,
            chess.BISHOP: self.parameters.bMob,
            chess.QUEEN: self.parameters.qMob
        }

        bonus: float = 0

        contrib: t.Dict[bool, int] = {
            color: 1,
            (not color): -1
        } 

        for move in board.legal_moves:
            p = board.piece_at(move.from_square)

            if(p.piece_type == chess.KING or p.piece_type == chess.PAWN):
                continue
            
            bonus += contrib[p.color] * pieceBonus[p.piece_type] 

        return bonus

    def piecesValueEvaluation(self, board: chess.Board) -> float:
        color: bool = board.turn 

        pieceBonus: t.Dict[int, float] = {
            chess.ROOK: self.parameters.rValue,
            chess.KNIGHT: self.parameters.kValue,
            chess.BISHOP: self.parameters.bValue,
            chess.QUEEN: self.parameters.qValue,
            chess.PAWN: self.parameters.pValue
        }

        bonus: float = 0

        contrib: t.Dict[bool, int] = {
            color: 1,
            (not color): -1
        } 

        piecemap = board.piece_map()
 
        for s, p in piecemap.items():
            if(p.piece_type == chess.KING):
                continue

            bonus += contrib[p.color] * pieceBonus[p.piece_type] 

        return bonus

    def _kingPawnShield(self, board: chess.Board, color: chess.Color) -> int:
        kposition : chess.Square = board.king(color)

        file : int = chess.square_file(kposition)
        rank : int = chess.square_rank(kposition)
            
        count : int = 0

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]: 
                if((file + i) in self.VALIDRANGE and (rank + j) in self.VALIDRANGE):
                    pos = chess.square(file + i, rank + j)
                    piece = board.piece_at(pos)   
                    
                    if(piece != None and piece.piece_type == chess.PAWN):
                        count += 1

                
        return count


    def _kingAttacked(self, board: chess.Board, color: chess.Color) -> t.Dict[int, int]: 
        kposition : chess.Square = board.king(color)
        file : int = chess.square_file(kposition)
        rank : int = chess.square_rank(kposition)
 
        eneColor : chess.Color = not chess.Color

        outdict = {
                chess.PAWN: 0,
                chess.BISHOP: 0,
                chess.KNIGHT: 0,
                chess.QUEEN: 0,
                chess.ROOK: 0
                }



        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]: 
                if((file + i) in self.VALIDRANGE and (rank + j) in self.VALIDRANGE):
                    pos = chess.square(file + i, rank + j)
                    piece = board.piece_at(pos)   
                    
                    if(piece != None and piece.color == eneColor and piece.piece_type != chess.KING):
                        outdict[piece.piece_type] += 1

        return outdict 


    def _kingDefended(self, board: chess.Board, color: chess.Color) -> t.Dict[int, int]: 
        kposition : chess.Square = board.king(color)
        file : int = chess.square_file(kposition)
        rank : int = chess.square_rank(kposition)
 
        outdict = {
                chess.PAWN: 0,
                chess.BISHOP: 0,
                chess.KNIGHT: 0,
                chess.QUEEN: 0,
                chess.ROOK: 0
                }

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]: 
                if((file + i) in self.VALIDRANGE and (rank + j) in self.VALIDRANGE):
                    pos = chess.square(file + i, rank + j)
                    piece = board.piece_at(pos)   
                    
                    if(piece != None and piece.color == color and piece.piece_type != chess.KING):
                        outdict[piece.piece_type] += 1

        return outdict 
    
    def _kingCastled(self, board: chess.Board, color: chess.Color) -> bool:
        pass
    


    def _bishopPair(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        
        count = 0
        for s, p in pieceDict.items():
            if(p.piece_type == chess.BISHOP and p.color == color):
                count += 1
        
        return 1 if len(self.pieceSquares[(color, chess.BISHOP)]) == 2 else 0
    
    def _rankPassedPawn(self, board: chess.Board, color: chess.Color) -> int:
        pass
    
    def _blockedPassedPawn(self, board: chess.Board, color: chess.Color) -> int:
        pass


    def _rookCon(self, board: chess.Board, color: chess.Color) -> int:
        pass

        
class EvalFuncTest(unittest.TestCase):

    def setUp(self):
        self.ef = EvalFunc()



    def testPiecesValue(self):
        b = chess.Board('3k4/2q5/8/8/8/8/8/3K4 w - - 0 1')
        v = self.ef.piecesValueEvaluation(b)

        self.assertEqual(v, -900)
        b = chess.Board('3k4/2q5/8/8/8/8/2Q1N3/3K4 w - - 0 1')
        v = self.ef.piecesValueEvaluation(b)
        self.assertEqual(v, 300)
        
        b = chess.Board('3k4/2q5/8/8/8/8/8/3K4 b - - 0 1')
        v = self.ef.piecesValueEvaluation(b)

        self.assertEqual(v, 900)
        b = chess.Board('3k4/2q5/8/8/8/8/2Q1N3/3K4 b - - 0 1')
        v = self.ef.piecesValueEvaluation(b)
        self.assertEqual(v, -300)

    def testMobility(self):
        b = chess.Board('8/8/3p4/8/8/3R4/3P4/8 w - - 0 1')
        v = self.ef.mobEvaluation(b)

        self.assertEqual(v, 10 * 9)
        b = chess.Board('8/8/3p4/8/5p2/4B3/3P4/8 w - - 0 1')
        v = self.ef.mobEvaluation(b)
        self.assertEqual(v, 13 * 7)
        
        b = chess.Board('8/8/3p4/8/5p2/4Q3/3P4/8 w - - 0 1')
        v = self.ef.mobEvaluation(b)

        self.assertEqual(v, 3 * 21)
        b = chess.Board('8/8/8/5p2/2p5/4N3/2P5/8 w - - 0 1')
        v = self.ef.mobEvaluation(b)
        self.assertEqual(v, 7 * 14)

    def testAdjacentPieces(self):
        b = chess.Board('8/8/8/8/3p4/3PN3/5p2/8 w - - 0 1')
        v = self.ef._adjacentPieces(chess.E3, b, chess.WHITE, b.pawns)

        self.assertDictEqual(v, {
            (1, -1): False,
            (-1, 0): True,
            (-1, 1): False,
            (-1, -1): False,
            (1, 1): False,
            (1, 0): False,
            (0, 1): False,
            (0, -1): False,
        })

        b = chess.Board('8/8/8/8/3p4/3Pn3/5p2/8 w - - 0 1')
        v = self.ef._adjacentPieces(chess.E3, b, chess.BLACK, b.pawns)

        self.assertDictEqual(v, {
            (1, -1): False,
            (-1, 0): False,
            (-1, 1): False,
            (-1, -1): True,
            (1, 1): True,
            (1, 0): False,
            (0, 1): False,
            (0, -1): False,
        })

        b = chess.Board('8/8/8/8/3p2P1/7N/6p1/8 w - - 0 1')
        v = self.ef._adjacentPieces(chess.H3, b, chess.WHITE, b.pawns)

        self.assertDictEqual(v, {
            (-1, 0): False,
            (-1, 1): True,
            (-1, -1): False,
            (0, 1): False,
            (0, -1): False,
        })


    
        b = chess.Board('8/8/8/8/3p2P1/7n/6p1/8 w - - 0 1')
        v = self.ef._adjacentPieces(chess.H3, b, chess.BLACK, b.pawns)

        self.assertDictEqual(v, {
            (-1, 0): False,
            (-1, 1): True,
            (-1, -1): False,
            (0, 1): False,
            (0, -1): False,
        })

        b = chess.Board('8/8/8/8/3p4/8/3P4/4Np2 w - - 0 1')
        v = self.ef._adjacentPieces(chess.E1, b, chess.WHITE, b.pawns)

        self.assertDictEqual(v, {
            (-1, 0): False,
            (-1, 1): True,
            (1, 1): False,
            (1, 0): False,
            (0, 1): False,
        })
   
        b = chess.Board('8/8/8/8/3p4/8/3P4/4np2 w - - 0 1')
        v = self.ef._adjacentPieces(chess.E1, b, chess.BLACK, b.pawns)

        self.assertDictEqual(v, {
            (1, -1): False,
            (-1, 0): False,
            (-1, -1): False,
            (1, 0): True,
            (0, -1): False,
            (0, -1): False 
        })
    
    def testRookEvaluation(self):
        b = chess.Board('8/3P1R2/1p1P4/8/8/1R1R2R1/1P3r2/8 w - - 0 1')
        v = self.ef.rookEvaluation(chess.G3, b, chess.WHITE)
        self.assertEqual(v, 27)

        v = self.ef.rookEvaluation(chess.D3, b, chess.WHITE)
        self.assertEqual(v, 57)

        v = self.ef.rookEvaluation(chess.B3, b, chess.WHITE)
        self.assertEqual(v, -46)

        v = self.ef.rookEvaluation(chess.F2, b, chess.BLACK)
        self.assertEqual(v, 41 + 27)

        v = self.ef.rookEvaluation(chess.F7, b, chess.WHITE)
        self.assertEqual(v, 41 + 27)

    def testKnightEvaluation(self):
        b = chess.Board('8/3n2N1/7P/n4n2/3n4/2p3p1/5n2/8 w - - 0 1')
        v = self.ef.knightEvaluation(chess.A5, b, chess.BLACK)
        self.assertEqual(v, -51)

        v = self.ef.knightEvaluation(chess.D7, b, chess.BLACK)
        self.assertEqual(v, -18)

        v = self.ef.knightEvaluation(chess.F5, b, chess.BLACK)
        self.assertEqual(v, 45)

        v = self.ef.knightEvaluation(chess.D4, b, chess.BLACK)
        self.assertEqual(v, -1)

        v = self.ef.knightEvaluation(chess.F2, b, chess.BLACK)
        self.assertEqual(v, 40 + -18)

        v = self.ef.knightEvaluation(chess.G7, b, chess.WHITE)
        self.assertEqual(v, 40 + -18)

    def testBishopEvaluation(self):
        b = chess.Board('8/3b4/2b2b2/8/8/2B2B2/8/3B4 w - - 0 1')
        v = self.ef.bishopEvaluation(chess.C3, b, chess.WHITE)
        self.assertEqual(v, 74)

        v = self.ef.bishopEvaluation(chess.F3, b, chess.WHITE)
        self.assertEqual(v, 74)

        v = self.ef.bishopEvaluation(chess.C6, b, chess.BLACK)
        self.assertEqual(v, 74)

        v = self.ef.bishopEvaluation(chess.F6, b, chess.BLACK)
        self.assertEqual(v, 74)

        v = self.ef.bishopEvaluation(chess.D7, b, chess.BLACK)
        self.assertEqual(v, 0)

        v = self.ef.bishopEvaluation(chess.D1, b, chess.WHITE)
        self.assertEqual(v, 0)

    def testPawnEvaluation(self):
        b = chess.Board('8/8/8/4N3/3PP3/8/8/8 w - - 0 1')
        v = self.ef.pawnEvaluation(chess.D4, b, chess.WHITE)

        self.assertEqual(v, -8 + 62)

        v = self.ef.pawnEvaluation(chess.E4, b, chess.WHITE)
        self.assertEqual(v, -8 + 62 + -23) 

        b = chess.Board('8/8/8/8/3P4/8/8/8 w - - 0 1')
        v = self.ef.pawnEvaluation(chess.D4, b, chess.WHITE)
        self.assertEqual(v, -8 + -3 + 62)

        b = chess.Board('8/8/8/8/3P4/3P4/8/8 w - - 0 1')
        v = self.ef.pawnEvaluation(chess.D4, b, chess.WHITE)
        self.assertEqual(v, -8 + 62 + -7)

        b = chess.Board('8/8/8/8/3P4/8/8/3R4 w - - 0 1')
        v = self.ef.pawnEvaluation(chess.D4, b, chess.WHITE)
        self.assertEqual(v, -8 + 62 + 30 + -3)

        b = chess.Board('8/8/8/8/3P4/3P4/8/3R4 w - - 0 1')
        v = self.ef.pawnEvaluation(chess.D4, b, chess.WHITE)
        self.assertEqual(v, -8 + 62 + -7)

        b = chess.Board('8/8/8/4P3/3P4/8/8/8 w - - 0 1')
        v = self.ef.pawnEvaluation(chess.D4, b, chess.WHITE)
        self.assertEqual(v, -8 + 62 + -14)


if __name__ == '__main__':
    unittest.main()

