import chess
import unittest

import typing as t


class EvalFunc:
    
    def __init__(self,
        value = {
                chess.PAWN: 100,
                chess.KNIGHT: 300,
                chess.BISHOP: 300,
                chess.ROOK: 500,
                chess.QUEEN: 900
                } ) -> None:

        self.pieceValues = {
                'pawnvalue': 100,
                'knightvalue': 342,
                'bishopvalue': 374,
                'rookvalue': 530,
                'queenvalue': 911,
                'centerpawns': -8,
                'kingpawnshield': 35,
                'kingcastled': 60,
                'bishoponlarge': 74,
                'bishoppair': 5,
                'bishopmob': 13,
                'knightmob': 14,
                'knightsupport': 40,
                'knightperiphery0': -51,
                'knightperiphery1': -18,
                'knightperiphery2': 45,
                'knightperiphery3': -1,
                'isopawn': -3,
                'doublepawn': -7,
                'passpawn': 62,
                'rookbehindpawn': 30,
                'backwardpawn': -14,
                'rankpasspawn': 5,
                'blockedpawn': -23,
                'blockedpasspawn': -10,
                'rookonopenfile': 27,
                'rookonsemiopen': 57,
                'rookonclosed': -46,
                'rookonseventh': 41,
                'rookmob': 9,
                'rookconnected': 12,
                'knightonweaksquare': -39,
                'queenmobility': 3 
                }

        self.VALIDRANGE = range(8)
        self.value = value

    
    def _setpieces(self, board: chess.Board) -> None:
        self.pieceSquares = {
                (chess.BLACK, chess.PAWN) : [],
                (chess.BLACK, chess.ROOK) : [],
                (chess.BLACK, chess.QUEEN) : [],
                (chess.BLACK, chess.BISHOP) : [],
                (chess.BLACK, chess.KNIGHT) : [],
                (chess.BLACK, chess.KING) : [],

                (chess.WHITE, chess.PAWN) : [],
                (chess.WHITE, chess.ROOK) : [],
                (chess.WHITE, chess.QUEEN) : [],
                (chess.WHITE, chess.BISHOP) : [],
                (chess.WHITE, chess.KNIGHT) : [],
                (chess.WHITE, chess.KING) : [],
                }


        piecemap = board.piece_map()
        
        for s, p in piecemap.items():
            self.pieceSquares[(p.color, p.piece_type)].append(s)
    
    def testEval(self, board: chess.Board) -> float:
        self._setpieces(board)

        eval_score = 0.0
                
        # pieces -> Dict[chess.Square, chess.Piece] 
        color = board.turn
        
        for p in range(1, 6):
            eval_score += len(self.pieceSquares[(color, p)]) * self.value[p] 

        for p in range(1, 6):
            eval_score -= len(self.pieceSquares[(not color, p)]) * self.value[p] 

        
        return eval_score

    def eval(self, board : chess.Board) -> float:
        self._setpieces(board)

        eval_score = 0.0
        
        
        # pieces -> Dict[chess.Square, chess.Piece] 
        color = board.turn

        pDict = self._allPieces(board, color)
        
        val = 0
        for k, v in pDict.items():
            if(k == chess.PAWN):
                val += v * self.pieceValues['pawnvalue']
            elif(k == chess.BISHOP):
                val += v * self.pieceValues['bishopvalue']
            elif(k == chess.ROOK):
                val += v * self.pieceValues['rookvalue']
            elif(k == chess.KNIGHT):
                val += v * self.pieceValues['knightvalue']
            elif(k == chess.QUEEN):
                val += v * self.pieceValues['queenvalue']


        pDict = self._kingAttacked(board, color)
        for k, v in pDict.items():
            if(k == chess.PAWN):
                val -= v * self.pieceValues['pawnvalue']
            elif(k == chess.BISHOP):
                val -= v * self.pieceValues['bishopvalue']
            elif(k == chess.ROOK):
                val -= v * self.pieceValues['rookvalue']
            elif(k == chess.KNIGHT):
                val -= v * self.pieceValues['knightvalue']
            elif(k == chess.QUEEN):
                val -= v * self.pieceValues['queenvalue']

        pDict = self._kingDefended(board, color)
        for k, v in pDict.items():
            if(k == chess.PAWN):
                val += v * self.pieceValues['pawnvalue']
            elif(k == chess.BISHOP):
                val += v * self.pieceValues['bishopvalue']
            elif(k == chess.ROOK):
                val += v * self.pieceValues['rookvalue']
            elif(k == chess.KNIGHT):
                val += v * self.pieceValues['knightvalue']
            elif(k == chess.QUEEN):
                val += v * self.pieceValues['queenvalue']



        eval_score = \
                self._centerpawnCount(board, color) * self.pieceValues['centerpawns'] \
            +   self._kingPawnShield(board, color) * self.pieceValues['kingpawnshield'] \
            +   self._bishopMob(board, color) * self.pieceValues['bishopmob'] \
            +   self._bishopMob(board, color) * self.pieceValues['bishoponlarge'] \
            +   self._bishopPair(board, color) * self.pieceValues['bishoppair'] \
            +   self._knightMob(board, color) * self.pieceValues['knightmob'] \
            +   self._knightSupport(board, color) * self.pieceValues['knightsupport'] \
            +   self._knightPeriphery0(board, color) * self.pieceValues['knightperiphery0'] \
            +   self._knightPeriphery1(board, color) * self.pieceValues['knightperiphery1'] \
            +   self._knightPeriphery2(board, color) * self.pieceValues['knightperiphery2'] \
            +   self._knightPeriphery3(board, color) * self.pieceValues['knightperiphery3'] \
            +   self._isoPawn(board, color) * self.pieceValues['isopawn'] \
            +   self._doubledPawn(board, color) * self.pieceValues['doublepawn'] \
            +   self._passPawn(board, color) * self.pieceValues['passpawn'] \
            +   self._rookBehindPassPawn(board, color) * self.pieceValues['rookbehindpawn'] \
            +   self._backwardPawn(board, color) * self.pieceValues['backwardpawn'] \
            +   self._blockPawn(board, color) * self.pieceValues['blockedpawn'] \
            +   self._rookopenfile(board, color) * self.pieceValues['rookonopenfile'] \
            +   self._rooksemiopenfile(board, color) * self.pieceValues['rookonsemiopen'] \
            +   self._rookclosedfile(board, color) * self.pieceValues['rookonclosed'] \
            +   self._rookOnSeventh(board, color) * self.pieceValues['rookonseventh'] \
            +   self._rookMob(board, color) * self.pieceValues['rookmob'] \
            +   self._queenMob(board, color) * self.pieceValues['queenmobility'] \
            +   val

               
        return eval_score

    def _centerpawnCount(self, board: chess.Board, color: chess.Color) -> int:
        e4: chess.Piece = board.piece_at(chess.E4)
        e5: chess.Piece = board.piece_at(chess.E5)
        d4: chess.Piece = board.piece_at(chess.D4)
        d5: chess.Piece = board.piece_at(chess.D5)

        
        count: int = 0
        if e4 != None:
            count += e4.color == color

        if d4 != None:
            count += d4.color == color

        if e5 != None:
            count += e5.color == color

        if d5 != None:
            count += d5.color == color
        
        return count

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

    def _bishopMob(self, board: chess.Board, color: chess.Color) -> int:
        # finding the bishop squares
        bSquares: t.Dict[chess.Square, int] = {} 
        for s in self.pieceSquares[(color, chess.BISHOP)]:
                bSquares[s] = 0
        

        for m in board.legal_moves:
            if(m.from_square in bSquares):
                bSquares[m.from_square] += 1 

        return sum(bSquares.values())
    
    def _bishopOnLarge(self, board: chess.Board, color: chess.Color) -> int:
        whiteDiagSquares: t.List[chess.Move] = [
                chess.H1, chess.G2, chess.F3, chess.E4,
                chess.D5, chess.C6, chess.B7, chess.A8]
        
        blackDiagSquares: t.List[chess.Move] = [
                chess.A1, chess.B2, chess.C3, chess.D4,
                chess.E5, chess.F6, chess.G7, chess.H8
                ]

        
        whiteDiag = False
        blackDiag = False

        for s in whiteDiagSquares:
            piece: chess.Piece = board.piece_at(s)

            if(piece != None and piece.piece_type == chess.BISHOP and piece.color == color):
                whiteDiag = True

                break

        for s in blackDiagSquares:
            piece: chess.Piece = board.piece_at(s)

            if(piece != None and piece.piece_type == chess.BISHOP and piece.color == color):
                blackDiag = True

                break

        return int(whiteDiag) + int(blackDiag) 

    def _bishopPair(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        
        count = 0
        for s, p in pieceDict.items():
            if(p.piece_type == chess.BISHOP and p.color == color):
                count += 1
        
        return 1 if len(self.pieceSquares[(color, chess.BISHOP)]) == 2 else 0

    def _knightMob(self, board: chess.Board, color: chess.Color) -> int:

        # finding the bishop squares
        kSquares: t.Dict[chess.Square, int] = {} 
        for s in self.pieceSquares[(color, chess.KNIGHT)]:
            kSquares[s] = 0
        

        for m in board.legal_moves:
            if(m.from_square in kSquares):
                kSquares[m.from_square] += 1 

        return sum(kSquares.values())
    
    # number of supported knights
    def _knightSupport(self, board: chess.Board, color: chess.Color) -> int:
        kSquares: t.List[chess.Square] = self.pieceSquares[(color, chess.KNIGHT)] 
        
        count = 0
        for s in kSquares:
            file : int = chess.square_file(s)
            rank : int = chess.square_rank(s)
            
            rank += -1 if color else +1

            for f in [file-1, file+1]:
                if(rank in self.VALIDRANGE and f in self.VALIDRANGE):
                    piece : chess.Piece = board.piece_at(chess.square(f, rank))

                    if(piece != None and piece.piece_type == chess.PAWN and piece.color == color):
                        count += 1
                        break

        return count 

    def _knightPeriphery0(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        kSquares: t.List[chess.Square] = [] 
        for s, p in pieceDict.items():
            if(p.piece_type == chess.KNIGHT and p.color == color):
                kSquares.append(s)
        
        count = 0
        for s in kSquares:
            file : int = chess.square_file(s)
            rank : int = chess.square_rank(s)
            
            #print(file, rank)
            if(file in [0, 7] or rank in [0, 7]):
                count += 1
        
        return count 


    def _knightPeriphery1(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        kSquares: t.List[chess.Square] = [] 
        for s, p in pieceDict.items():
            if(p.piece_type == chess.KNIGHT and p.color == color):
                kSquares.append(s)
        
        count = 0
        for s in kSquares:
            file : int = chess.square_file(s)
            rank : int = chess.square_rank(s)
            
            #print(file, rank)
            positions = list(zip([1] * 6, range(1, 7)))\
            + list(zip([6] * 6, range(1, 7)))\
            + list(zip(range(1, 7), [1] * 6))\
            + list(zip(range(1, 7), [6] * 6))


            if((file, rank) in positions):
                count += 1
        
        return count 

    def _knightPeriphery2(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        kSquares: t.List[chess.Square] = [] 
        for s, p in pieceDict.items():
            if(p.piece_type == chess.KNIGHT and p.color == color):
                kSquares.append(s)
        
        count = 0
        for s in kSquares:
            file : int = chess.square_file(s)
            rank : int = chess.square_rank(s)
            
            positions = list(zip([2] * 6, range(2, 6)))\
            + list(zip([5] * 6, range(2, 6)))\
            + list(zip(range(2, 6), [2] * 6))\
            + list(zip(range(2, 6), [5] * 6))


            if((file, rank) in positions):
                count += 1
        
        return count 

    def _knightPeriphery3(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        kSquares: t.List[chess.Square] = [] 
        for s, p in pieceDict.items():
            if(p.piece_type == chess.KNIGHT and p.color == color):
                kSquares.append(s)
        
        count = 0
        for s in kSquares:
            file : int = chess.square_file(s)
            rank : int = chess.square_rank(s)
            
            if((file, rank) in [(3, 4), (4, 3), (3, 3), (4, 4)]):
                count += 1

        return count 

    def _isoPawn(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        pSquares: t.List[chess.Square] = [] 
        for s, p in pieceDict.items():
            if(p.piece_type == chess.PAWN and p.color == color):
                pSquares.append(s)
        
        count = 0
        for s in pSquares:
            file : int = chess.square_file(s)
            rank : int = chess.square_rank(s)

            flag = True
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]: 
                    if(i == j == 0): 
                        continue

                    if((file + i) in self.VALIDRANGE and (rank + j) in self.VALIDRANGE):
                        p = board.piece_at(chess.square(file + i, rank + j))

                        if(p != None and p.piece_type == chess.PAWN and p.color == color):
                            flag = False
                
                if(not flag):
                    break

            if(flag):
                count += 1

        return count
    
    # number of doubled pawns
    def _doubledPawn(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        pSquares: t.Dict[int, int] = {
                0: 0,
                1: 0,
                2: 0,
                3: 0,
                4: 0,
                5: 0,
                6: 0,
                7: 0
                } 

        for s, p in pieceDict.items():
            if(p.piece_type == chess.PAWN and p.color == color):
                file = chess.square_file(s)
                pSquares[file] += 1
        
        count = 0
        for k, v in pSquares.items():
            if(v > 1):
                count += v

        return count

    def _passPawn(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        pSquares: t.List[chess.Square] = []

        for s, p in pieceDict.items():
            if(p.piece_type == chess.PAWN and p.color == color):
                pSquares.append(s)

        dir = +1 if color else -1
        lim = 7 if color else 0
        
        count = 0
        for s in pSquares:
            file = chess.square_file(s)
            rank = chess.square_rank(s) + dir
            
            flag = False
            while (rank != lim):
                
                for j in [-1, 0, +1]:
                    f = file + j 
                    
                    if(rank in self.VALIDRANGE and f in self.VALIDRANGE):
                        
                        if(f in self.VALIDRANGE):
                            sq = chess.square(f, rank)

                            piece = board.piece_at(sq)
                            if(piece != None and piece.piece_type == chess.PAWN and piece.color != color):
                                flag = True
                                break

                if(flag):
                    break

                rank += dir

            if(not flag):
                count += 1
        
        return count 

    def _rookBehindPassPawn(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        pSquares: t.List[chess.Square] = []

        for s, p in pieceDict.items():
            if(p.piece_type == chess.PAWN and p.color == color):
                pSquares.append(s)

        dir = +1 if color else -1
        lim = 7 if color else 0
        
        passedpawns = []
        for s in pSquares:
            file = chess.square_file(s)
            rank = chess.square_rank(s) + dir
            
            flag = False
            while (rank != lim):
                
                for j in [-1, 0, +1]:
                    f = file + j 
                    
                    if(rank in self.VALIDRANGE and f in self.VALIDRANGE):
                        
                        if(f in self.VALIDRANGE):
                            sq = chess.square(f, rank)

                            piece = board.piece_at(sq)
                            if(piece != None and piece.piece_type == chess.PAWN and piece.color != color):
                                flag = True
                                break

                if(flag):
                    break

                rank += dir

            if(not flag):
                passedpawns.append(s)
        
        dir = -1 if color else +1
        lim = 0 if color else 7
        
        count = 0
        for pp in passedpawns:
            file = chess.square_file(s)
            rank = chess.square_rank(s) + dir
            
            while (rank != lim):
                sq = chess.square(file, rank)
                piece = board.piece_at(sq)

                if(piece != None and piece.piece_type == chess.ROOK and piece.color == color):
                    count += 1
                    break

                rank += dir
             

        return count

    def _backwardPawn(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        pSquares: t.List[chess.Square] = []

        for s, p in pieceDict.items():
            if(p.piece_type == chess.PAWN and p.color == color):
                pSquares.append(s)
        

        beh = -1 if color else +1
        
        count = 0
        for p in pSquares:
            file = chess.square_file(p)
            rank = chess.square_rank(p)

            behRank = rank + beh
            forRank = rank - beh
            
            isPawn1 = False
            for i in [-1, 0, +1]:
                if(behRank in self.VALIDRANGE and (file + i) in self.VALIDRANGE):
                    sq = chess.square(file + i, behRank)
                    piece = board.piece_at(sq)

                    if(piece != None and piece.piece_type == chess.PAWN and piece.color == color):
                        isPawn1 = True
                        break

            isPawn2 = False
            for i in [-1, 0, +1]:
                if(forRank in self.VALIDRANGE and (file + i) in self.VALIDRANGE):
                    sq = chess.square(file + i, forRank)
                    piece = board.piece_at(sq)

                    if(piece != None and piece.piece_type == chess.PAWN and piece.color == color):
                        isPawn2 = True
                        break

            if(isPawn2 and not isPawn1):
                count += 1

        return count

    def _rankPassedPawn(self, board: chess.Board, color: chess.Color) -> int:
        pass
    
    def _blockPawn(self, board: chess.Board, color: chess.Color) -> int:
        e2 = board.piece_at(chess.E2)
        d2 = board.piece_at(chess.D2)
        
        count = 0
        if(e2 != None and e2.piece_type == chess.PAWN and e2.color == color):
            e3 = board.piece_at(chess.E3)
            e4 = board.piece_at(chess.E4)

            if(e3 != None and e3.color == color):
                count += 1

            elif (e4 != None and e4.color == color):
                count += 1

        if(d2 != None and d2.piece_type == chess.PAWN and d2.color == color):
            d3 = board.piece_at(chess.D3)
            d4 = board.piece_at(chess.D4)

            if(d3 != None and d3.color == color):
                count += 1

            elif (d4 != None and d4.color == color):
                count += 1

        return count

    def _blockedPassedPawn(self, board: chess.Board, color: chess.Color) -> int:
        pass

    def _rookopenfile(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        rSquares: t.List[chess.Square] = []

        for s, p in pieceDict.items():
            if(p.piece_type == chess.ROOK and p.color == color):
                rSquares.append(s)
        
        count = 0
        for s in rSquares:
            file = chess.square_file(s)
            rank = chess.square_rank(s)
            
            flag = False
            for i in range(0, 8):
                if(i == rank):
                    continue
                
                sq = chess.square(file, i)
                piece = board.piece_at(sq)

                if(piece != None and piece.piece_type == chess.PAWN):
                    flag = True
                    break

            if (not flag):
                count += 1

        return count


    def _rooksemiopenfile(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        rSquares: t.List[chess.Square] = []

        for s, p in pieceDict.items():
            if(p.piece_type == chess.ROOK and p.color == color):
                rSquares.append(s)
        
        count = 0
        for s in rSquares:
            file = chess.square_file(s)
            rank = chess.square_rank(s)
            
            flag = False
            for i in range(0, 8):
                if(i == rank):
                    continue
                
                sq = chess.square(file, i)
                piece = board.piece_at(sq)

                if(piece != None and piece.piece_type == chess.PAWN and piece.color == color):
                    flag = True
                    break

            if (not flag):
                count += 1

        return count

    def _rookclosedfile(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        rSquares: t.List[chess.Square] = []

        for s, p in pieceDict.items():
            if(p.piece_type == chess.ROOK and p.color == color):
                rSquares.append(s)
        
        count = 0
        for s in rSquares:
            file = chess.square_file(s)
            rank = chess.square_rank(s)
            
            flag1 = False
            flag2 = False
            for i in range(0, 8):
                if(i == rank):
                    continue
                
                sq = chess.square(file, i)
                piece = board.piece_at(sq)

                if(piece != None and piece.piece_type == chess.PAWN and piece.color == color):
                    flag1 = True
                if(piece != None and piece.piece_type == chess.PAWN and piece.color != color):
                    flag2 = True



            if (flag1 and flag2):
                count += 1

        return count

    def _rookOnSeventh(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        
        count = 0
        if(color):
            for s, p in pieceDict.items():
                if(p.piece_type == chess.ROOK and p.color == color):
                    rank = chess.square_rank(s)
                    
                    if(rank == 6):
                        count += 1
     
        else:
            for s, p in pieceDict.items():
                if(p.piece_type == chess.ROOK and p.color == color):
                    rank = chess.square_rank(s)

                    if(rank == 1):
                        count += 1

        return count


    def _rookMob(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()

        # finding the bishop squares
        rSquares: t.Dict[chess.Square, int] = {} 
        for s, p in pieceDict.items():
            if(p.piece_type == chess.ROOK and p.color == color):
                rSquares[s] = 0
        

        for m in board.legal_moves:
            if(m.from_square in rSquares):
                rSquares[m.from_square] += 1 

        return sum(rSquares.values())

    def _rookCon(self, board: chess.Board, color: chess.Color) -> int:
        pass

    def _queenMob(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()

        # finding the bishop squares
        qSquares: t.Dict[chess.Square, int] = {} 
        for s, p in pieceDict.items():
            if(p.piece_type == chess.QUEEN and p.color == color):
                qSquares[s] = 0
        

        for m in board.legal_moves:
            if(m.from_square in qSquares):
                qSquares[m.from_square] += 1 

        return sum(qSquares.values())



    def _allPieces(self, board: chess.Board, color: chess.Color) -> t.Dict[int, int]:
        outdict = {
                chess.PAWN: 0,
                chess.BISHOP: 0,
                chess.KNIGHT: 0,
                chess.QUEEN: 0,
                chess.ROOK: 0
                }

        pieceDict = board.piece_map()

        for s, p in pieceDict.items():
            if(p.piece_type != chess.KING and p.color == color):
                outdict[p.piece_type] += 1


        return outdict
        
class EvalFuncTest(unittest.TestCase):

    def setUp(self):
        self.ef = EvalFunc()

    def testCenterPawnCount(self):
        b = chess.Board('4k3/8/8/3P4/4P3/8/8/4K3 w - - 0 1')

        bCount = self.ef._centerpawnCount(b, chess.BLACK)
        wCount = self.ef._centerpawnCount(b, chess.WHITE)

        self.assertEqual(bCount, 0)
        self.assertEqual(wCount, 2)

        b = chess.Board('4k3/8/8/3pP3/4P3/8/8/4K3 w - - 0 1')

        bCount = self.ef._centerpawnCount(b, chess.BLACK)
        wCount = self.ef._centerpawnCount(b, chess.WHITE)

        self.assertEqual(bCount, 1)
        self.assertEqual(wCount, 2)
    
    def testKingPawnShield(self):
        b = chess.Board("8/8/8/8/8/8/1P6/K7 w - - 0 1")
        wCount = self.ef._kingPawnShield(b, chess.WHITE)

        self.assertEqual(wCount, 1)

        b = chess.Board("8/8/8/4P3/2PK4/4P3/8/8 w - - 0 1")
        wCount = self.ef._kingPawnShield(b, chess.WHITE)

        self.assertEqual(wCount, 3)

        b = chess.Board("3K4/3P4/8/8/2P5/4P3/8/8 w - - 0 1")
        wCount = self.ef._kingPawnShield(b, chess.WHITE)

        self.assertEqual(wCount, 1)

        b = chess.Board("8/8/6P1/7K/2P4P/8/8/8 w - - 0 1")
        wCount = self.ef._kingPawnShield(b, chess.WHITE)

        self.assertEqual(wCount, 2)

    def testKingDefended(self):
        b = chess.Board('8/8/8/3bP3/2PK4/3RP3/8/8 w - - 0 1')

        pieces = self.ef._kingDefended(b, chess.WHITE)
        self.assertEqual([chess.PAWN, chess.ROOK, chess.PAWN, chess.PAWN], pieces)

    def testKingAttacked(self):
        b = chess.Board('8/8/8/3bP3/2PK4/3RP3/8/8 w - - 0 1')

        pieces = self.ef._kingAttacked(b, chess.WHITE)
        self.assertEqual([chess.BISHOP], pieces)

    def testBishopMob(self):
        b = chess.Board('3k4/8/8/4PB2/2PK4/3RP3/1B6/8 w - - 0 1')
        self.ef._setpieces(b)
        mob = self.ef._bishopMob(b, chess.WHITE)
        self.assertEqual(mob, 12)

    def testBishopOnLarge(self):
        b = chess.Board('3k4/8/8/4P3/2PKB3/1B1RP3/8/8 w - - 0 1')
        res = self.ef._bishopOnLarge(b, chess.WHITE)
        self.assertEqual(res, 1)

        b = chess.Board('3k4/8/3B4/4P3/2PK4/3RP3/1B6/8 w - - 0 1')
        res = self.ef._bishopOnLarge(b, chess.WHITE)
        self.assertEqual(res, 1)

    
    def testBishopPair(self):
        b = chess.Board('3k4/8/8/4P3/2PKB3/1B1RP3/8/8 w - - 0 1')
        res = self.ef._bishopPair(b, chess.WHITE)
        self.assertEqual(res, 1)

        b = chess.Board('3k4/8/8/4P3/2PKB3/1R1RP3/8/8 w - - 0 1')
        res = self.ef._bishopPair(b, chess.WHITE)
        self.assertEqual(res, 0)

    def testKnightMob(self):
        b = chess.Board('3k4/8/8/4PN2/2PK4/3RP3/1N6/8 w - - 0 1')


        mob = self.ef._knightMob(b, chess.WHITE)
        self.assertEqual(mob, 8)

    def testKnightSupport(self):
        b = chess.Board('3k4/8/8/5N2/8/8/1N6/3K4 w - - 0 1')
        mob = self.ef._knightSupport(b, chess.WHITE)
        self.assertEqual(mob, 0)

        b = chess.Board('3k4/8/8/5N2/6P1/8/1N6/3K4 w - - 0 1')
        mob = self.ef._knightSupport(b, chess.WHITE)
        self.assertEqual(mob, 1)

        b = chess.Board('3k4/8/8/5N2/6P1/8/1N6/P2K4 w - - 0 1')
        mob = self.ef._knightSupport(b, chess.WHITE)
        self.assertEqual(mob, 2)

        b = chess.Board('3k4/8/6P1/5N2/8/P7/1N6/3K4 w - - 0 1')
        mob = self.ef._knightSupport(b, chess.WHITE)
        self.assertEqual(mob, 0)


        b = chess.Board('3k4/4n3/6P1/2n2N2/8/P7/1N6/3K4 w - - 0 1')
        mob = self.ef._knightSupport(b, chess.BLACK)
        self.assertEqual(mob, 0)

        b = chess.Board('3k4/8/6P1/2n2N1p/6n1/P7/1N6/3K4 w - - 0 1')
        mob = self.ef._knightSupport(b, chess.BLACK)
        self.assertEqual(mob, 1)

        b = chess.Board('3k4/8/1p4P1/2n2N1p/6n1/P7/1N6/3K4 w - - 0 1')
        mob = self.ef._knightSupport(b, chess.BLACK)
        self.assertEqual(mob, 2)

        b = chess.Board('3k4/4n3/4p1P1/2n2N2/2p5/P7/1N6/3K4 w - - 0 1')
        mob = self.ef._knightSupport(b, chess.BLACK)
        self.assertEqual(mob, 0)

    def testKnightPeriphery0(self):
        b = chess.Board('3k4/8/8/8/N6N/8/8/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery0(b, chess.WHITE)
        # print(mob)
        self.assertEqual(mob, 2)

        b = chess.Board('3k4/8/8/5N2/6P1/8/1N6/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery0(b, chess.WHITE)
        self.assertEqual(mob, 0)

        b = chess.Board('3k1N2/8/8/8/6P1/8/8/1N1K4 w - - 0 1')
        mob = self.ef._knightPeriphery0(b, chess.WHITE)
        self.assertEqual(mob, 2)

        b = chess.Board('2nk4/8/8/8/2N2N2/7n/8/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery0(b, chess.WHITE)
        self.assertEqual(mob, 0)

    def testKnightPeriphery1(self):
        b = chess.Board('3k4/8/8/8/6N1/8/1N6/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery1(b, chess.WHITE)
        # print(mob)
        self.assertEqual(mob, 2)

        b = chess.Board('3k4/8/8/5N2/6P1/2N5/8/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery1(b, chess.WHITE)
        self.assertEqual(mob, 0)

        b = chess.Board('3k4/4N3/8/8/6P1/8/2N5/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery1(b, chess.WHITE)
        self.assertEqual(mob, 2)

        b = chess.Board('3k4/2n5/8/8/2N2N2/8/6n1/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery1(b, chess.WHITE)
        self.assertEqual(mob, 0)


    def testKnightPeriphery2(self):
        b = chess.Board('3k4/8/8/8/2N2N2/8/8/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery2(b, chess.WHITE)
        # print(mob)
        self.assertEqual(mob, 2)

        b = chess.Board('3k4/8/8/3N4/4N1P1/8/8/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery2(b, chess.WHITE)
        self.assertEqual(mob, 0)

        b = chess.Board('3k4/8/4N3/8/6P1/3N4/8/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery2(b, chess.WHITE)
        self.assertEqual(mob, 2)

        b = chess.Board('3k4/8/2n5/8/3NN3/5n2/8/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery2(b, chess.WHITE)
        self.assertEqual(mob, 0)

    def testKnightPeriphery3(self):
        b = chess.Board('3k4/8/8/3N4/4N3/8/8/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery3(b, chess.WHITE)
        # print(mob)
        self.assertEqual(mob, 2)

        b = chess.Board('3k4/2N5/8/8/6P1/8/5N2/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery3(b, chess.WHITE)
        self.assertEqual(mob, 0)

        b = chess.Board('3k4/8/8/4N3/3N2P1/8/8/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery3(b, chess.WHITE)
        self.assertEqual(mob, 2)

        b = chess.Board('3k4/8/8/3n4/4n3/1N6/8/3KN3 w - - 0 1')
        mob = self.ef._knightPeriphery3(b, chess.WHITE)
        self.assertEqual(mob, 0)

    def testIsoPawn(self):
        b = chess.Board('3k4/8/8/8/3P2P1/1P2P3/8/3K4 w - - 0 1')
        mob = self.ef._isoPawn(b, chess.WHITE)
        # print(mob)
        self.assertEqual(mob, 2)


    def testDoubledPawn(self):
        b = chess.Board('3k4/8/8/8/4P1P1/1P2P3/8/3K4 w - - 0 1')
        dpc = self.ef._doubledPawn(b, chess.WHITE)
        self.assertEqual(dpc, 2)

    def testPassPawn(self):
        b = chess.Board('3k4/8/3p2p1/8/6P1/1P2P3/8/Q2K4 w - - 0 1')
        dpc = self.ef._passPawn(b, chess.WHITE)
        self.assertEqual(dpc, 1)

        b = chess.Board('3k4/8/2pp2p1/8/6P1/1P2P3/8/Q2K4 w - - 0 1')
        dpc = self.ef._passPawn(b, chess.WHITE)
        self.assertEqual(dpc, 0)

        b = chess.Board('3k4/8/2pp2p1/8/6P1/1P2P3/8/Q2K4 w - - 0 1')
        dpc = self.ef._passPawn(b, chess.BLACK)
        self.assertEqual(dpc, 0)

        b = chess.Board('3k4/8/2pp2p1/8/6P1/4P3/8/Q2K4 w - - 0 1')
        dpc = self.ef._passPawn(b, chess.BLACK)
        self.assertEqual(dpc, 1)


    def testRookBehindPassPawn(self):
        b = chess.Board('3k4/8/3p2p1/8/6P1/1P2P3/1R6/Q2K4 w - - 0 1')
        dpc = self.ef._rookBehindPassPawn(b, chess.WHITE)
        self.assertEqual(dpc, 1)

        b = chess.Board('3k4/8/2pp2p1/8/6P1/1P2P3/4R3/Q2K4 w - - 0 1')
        dpc = self.ef._rookBehindPassPawn(b, chess.WHITE)
        self.assertEqual(dpc, 0)

        b = chess.Board('2rk4/8/2pp2p1/8/6P1/1P2P3/8/Q2K4 w - - 0 1')
        dpc = self.ef._rookBehindPassPawn(b, chess.BLACK)
        self.assertEqual(dpc, 0)

        b = chess.Board('3k4/2r5/2pp2p1/8/6P1/4P3/8/Q2K4 w - - 0 1')
        dpc = self.ef._rookBehindPassPawn(b, chess.BLACK)
        self.assertEqual(dpc, 1)

    def testBackwardPawn(self):
        b = chess.Board('3k4/2r5/2pp2p1/8/3P2P1/4P3/8/Q2K4 w - - 0 1')
        dpc = self.ef._backwardPawn(b, chess.WHITE)
        self.assertEqual(dpc, 1)

        b = chess.Board('3k4/2r5/2pp2p1/8/6P1/4P3/8/Q2K4 w - - 0 1')
        dpc = self.ef._backwardPawn(b, chess.WHITE)
        self.assertEqual(dpc, 0)

        b = chess.Board('3k4/2r5/2p3p1/3p4/6P1/4P3/8/Q2K4 w - - 0 1')
        dpc = self.ef._backwardPawn(b, chess.BLACK)
        self.assertEqual(dpc, 1)

        b = chess.Board('2rk4/8/2pp2p1/8/6P1/1P2P3/8/Q2K4 w - - 0 1')
        dpc = self.ef._backwardPawn(b, chess.BLACK)
        self.assertEqual(dpc, 0)

    def testBlockPawn(self):
        b = chess.Board('3k4/2r5/2p3p1/3p4/6P1/3N4/3P4/Q2K4 w - - 0 1')
        dpc = self.ef._blockPawn(b, chess.WHITE)
        self.assertEqual(dpc, 1)

    def testRookOpenFile(self):
        b = chess.Board('3k4/2r5/1p4p1/3p4/6P1/3N4/3P4/Q2K4 w - - 0 1')
        dpc = self.ef._rookopenfile(b, chess.BLACK)
        self.assertEqual(dpc, 1)


    def testRookSemiOpenFile(self):
        b = chess.Board('3k4/2r5/1p4p1/3p4/6P1/2PN4/3P4/Q2K4 w - - 0 1')
        dpc = self.ef._rooksemiopenfile(b, chess.BLACK)
        self.assertEqual(dpc, 1)


    def testRookClosedFile(self):
        b = chess.Board('3k4/2r5/2p3p1/3p4/6P1/2PN4/3P4/Q2K4 w - - 0 1')
        dpc = self.ef._rookclosedfile(b, chess.BLACK)
        self.assertEqual(dpc, 1)

    def testRookOnSeventh(self):
        b = chess.Board('3k4/1Rr2R2/2p3p1/3p4/6P1/2PN4/3P4/Q2K4 w - - 0 1')
        dpc = self.ef._rookOnSeventh(b, chess.WHITE)
        self.assertEqual(dpc, 2)
    
    def testRookMob(self):
        b = chess.Board('3k4/1Rr2R2/2p3p1/3p4/6P1/2PN4/3P4/Q2K4 w - - 0 1')
        dpc = self.ef._rookMob(b, chess.WHITE)
        self.assertEqual(dpc, 21)
 
    def testQueenMob(self):
        b = chess.Board('3k4/1Rr2R2/2p3p1/3p4/6P1/2PN4/3P4/Q2K4 w - - 0 1')
        dpc = self.ef._queenMob(b, chess.WHITE)
        self.assertEqual(dpc, 10)
        

    def testAllPieces(self):
        b = chess.Board('1q1k4/4n1p1/8/2B2N2/4P1P1/1P2P1N1/8/Q2K1R2 w - - 0 1')
        dict = self.ef._allPieces(b, chess.WHITE)

        self.assertEqual(dict, {
            chess.ROOK: 1,
            chess.QUEEN: 1,
            chess.BISHOP: 1,
            chess.KNIGHT: 2,
            chess.PAWN: 4
            })

    def testTestEvaluation(self):
        b = chess.Board('3k4/2q5/8/8/8/8/8/3K4 w - - 0 1')
        v = self.ef.testEval(b)

        self.assertEqual(v, -900)
        b = chess.Board('3k4/2q5/8/8/8/8/2Q1N3/3K4 w - - 0 1')
        v = self.ef.testEval(b)
        self.assertEqual(v, 300)
        
        b = chess.Board('3k4/2q5/8/8/8/8/8/3K4 b - - 0 1')
        v = self.ef.testEval(b)

        self.assertEqual(v, 900)
        b = chess.Board('3k4/2q5/8/8/8/8/2Q1N3/3K4 b - - 0 1')
        v = self.ef.testEval(b)
        self.assertEqual(v, -300)

if __name__ == '__main__':
    unittest.main()

