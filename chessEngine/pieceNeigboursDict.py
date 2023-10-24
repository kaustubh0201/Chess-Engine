from functools import reduce
import chess

# outDict = {}

# for c in [chess.BLACK, chess.WHITE]:
#     for s in chess.SQUARES:
#         file: int = chess.square_file(s)
#         rank: int = chess.square_rank(s)

#         VALIDRANGE = range(0, 8)

#         yMult = -1 if c == chess.BLACK else 1
#         for i in [-1, 0, 1]:
#             for j in [-1, 0, 1]: 
#                 if(i == j == 0): 
#                     continue

#                 if((file + i) in VALIDRANGE and (rank + j) in VALIDRANGE):
#                     p = chess.square(file + i, rank + j)

#                     if(p != None):
#                         key = (s, c)
#                         if(key in outDict):
#                             outDict[key].append((p, i, j * yMult)) 
#                         else:
#                             outDict[key] = [(p, i, j * yMult)]

# print(outDict)


PIECE_NEIGHBOURS_DICT = {(0, False): [(8, 0, -1), (1, 1, 0), (9, 1, -1)], (1, False): [(0, -1, 0), (8, -1, -1), (9, 0, -1), (2, 1, 0), (10, 1, -1)], (2, False): [(1, -1, 0), (9, -1, -1), (10, 0, -1), (3, 1, 0), (11, 1, -1)], (3, False): [(2, -1, 0), (10, -1, -1), (11, 0, -1), (4, 1, 0), (12, 1, -1)], (4, False): [(3, -1, 0), (11, -1, -1), (12, 0, -1), (5, 1, 0), (13, 1, -1)], (5, False): [(4, -1, 0), (12, -1, -1), (13, 0, -1), (6, 1, 0), (14, 1, -1)], (6, False): [(5, -1, 0), (13, -1, -1), (14, 0, -1), (7, 1, 0), (15, 1, -1)], (7, False): [(6, -1, 0), (14, -1, -1), (15, 0, -1)], (8, False): [(0, 0, 1), (16, 0, -1), (1, 1, 1), (9, 1, 0), (17, 1, -1)], (9, False): [(0, -1, 1), (8, -1, 0), (16, -1, -1), (1, 0, 1), (17, 0, -1), (2, 1, 1), (10, 1, 0), (18, 1, -1)], (10, False): [(1, -1, 1), (9, -1, 0), (17, -1, -1), (2, 0, 1), (18, 0, -1), (3, 1, 1), (11, 1, 0), (19, 1, -1)], (11, False): [(2, -1, 1), (10, -1, 0), (18, -1, -1), (3, 0, 1), (19, 0, -1), (4, 1, 1), (12, 1, 0), (20, 1, -1)], (12, False): [(3, -1, 1), (11, -1, 0), (19, -1, -1), (4, 0, 1), (20, 0, -1), (5, 1, 1), (13, 1, 0), (21, 1, -1)], (13, False): [(4, -1, 1), (12, -1, 0), (20, -1, -1), (5, 0, 1), (21, 0, -1), (6, 1, 1), (14, 1, 0), (22, 1, -1)], (14, False): [(5, -1, 1), (13, -1, 0), (21, -1, -1), (6, 0, 1), (22, 0, -1), (7, 1, 1), (15, 1, 0), (23, 1, -1)], (15, False): [(6, -1, 1), (14, -1, 0), (22, -1, -1), (7, 0, 1), (23, 0, -1)], (16, False): [(8, 0, 1), (24, 0, -1), (9, 1, 1), (17, 1, 0), (25, 1, -1)], (17, False): [(8, -1, 1), (16, -1, 0), (24, -1, -1), (9, 0, 1), (25, 0, -1), (10, 1, 1), (18, 1, 0), (26, 1, -1)], (18, False): [(9, -1, 1), (17, -1, 0), (25, -1, -1), (10, 0, 1), (26, 0, -1), (11, 1, 1), (19, 1, 0), (27, 1, -1)], (19, False): [(10, -1, 1), (18, -1, 0), (26, -1, -1), (11, 0, 1), (27, 0, -1), (12, 1, 1), (20, 1, 0), (28, 1, -1)], (20, False): [(11, -1, 1), (19, -1, 0), (27, -1, -1), (12, 0, 1), (28, 0, -1), (13, 1, 1), (21, 1, 0), (29, 1, -1)], (21, False): [(12, -1, 1), (20, -1, 0), (28, -1, -1), (13, 0, 1), (29, 0, -1), (14, 1, 1), (22, 1, 0), (30, 1, -1)], (22, False): [(13, -1, 1), (21, -1, 0), (29, -1, -1), (14, 0, 1), (30, 0, -1), (15, 1, 1), (23, 1, 0), (31, 1, -1)], (23, False): [(14, -1, 1), (22, -1, 0), (30, -1, -1), (15, 0, 1), (31, 0, -1)], (24, False): [(16, 0, 1), (32, 0, -1), (17, 1, 1), (25, 1, 0), (33, 1, -1)], (25, False): [(16, -1, 1), (24, -1, 0), (32, -1, -1), (17, 0, 1), (33, 0, -1), (18, 1, 1), (26, 1, 0), (34, 1, -1)], (26, False): [(17, -1, 1), (25, -1, 0), (33, -1, -1), (18, 0, 1), (34, 0, -1), (19, 1, 1), (27, 1, 0), (35, 1, -1)], (27, False): [(18, -1, 1), (26, -1, 0), (34, -1, -1), (19, 0, 1), (35, 0, -1), (20, 1, 1), (28, 1, 0), (36, 1, -1)], (28, False): [(19, -1, 1), (27, -1, 0), (35, -1, -1), (20, 0, 1), (36, 0, -1), (21, 1, 1), (29, 1, 0), (37, 1, -1)], (29, False): [(20, -1, 1), (28, -1, 0), (36, -1, -1), (21, 0, 1), (37, 0, -1), (22, 1, 1), (30, 1, 0), (38, 1, -1)], (30, False): [(21, -1, 1), (29, -1, 0), (37, -1, -1), (22, 0, 1), (38, 0, -1), (23, 1, 1), (31, 1, 0), (39, 1, -1)], (31, False): [(22, -1, 1), (30, -1, 0), (38, -1, -1), (23, 0, 1), (39, 0, -1)], (32, False): [(24, 0, 1), (40, 0, -1), (25, 1, 1), (33, 1, 0), (41, 1, -1)], (33, False): [(24, -1, 1), (32, -1, 0), (40, -1, -1), (25, 0, 1), (41, 0, -1), (26, 1, 1), (34, 1, 0), (42, 1, -1)], (34, False): [(25, -1, 1), (33, -1, 0), (41, -1, -1), (26, 0, 1), (42, 0, -1), (27, 1, 1), (35, 1, 0), (43, 1, -1)], (35, False): [(26, -1, 1), (34, -1, 0), (42, -1, -1), (27, 0, 1), (43, 0, -1), (28, 1, 1), (36, 1, 0), (44, 1, -1)], (36, False): [(27, -1, 1), (35, -1, 0), (43, -1, -1), (28, 0, 1), (44, 0, -1), (29, 1, 1), (37, 1, 0), (45, 1, -1)], (37, False): [(28, -1, 1), (36, -1, 0), (44, -1, -1), (29, 0, 1), (45, 0, -1), (30, 1, 1), (38, 1, 0), (46, 1, -1)], (38, False): [(29, -1, 1), (37, -1, 0), (45, -1, -1), (30, 0, 1), (46, 0, -1), (31, 1, 1), (39, 1, 0), (47, 1, -1)], (39, False): [(30, -1, 1), (38, -1, 0), (46, -1, -1), (31, 0, 1), (47, 0, -1)], (40, False): [(32, 0, 1), (48, 0, -1), (33, 1, 1), (41, 1, 0), (49, 1, -1)], (41, False): [(32, -1, 1), (40, -1, 0), (48, -1, -1), (33, 0, 1), (49, 0, -1), (34, 1, 1), (42, 1, 0), (50, 1, -1)], (42, False): [(33, -1, 1), (41, -1, 0), (49, -1, -1), (34, 0, 1), (50, 0, -1), (35, 1, 1), (43, 1, 0), (51, 1, -1)], (43, False): [(34, -1, 1), (42, -1, 0), (50, -1, -1), (35, 0, 1), (51, 0, -1), (36, 1, 1), (44, 1, 0), (52, 1, -1)], (44, False): [(35, -1, 1), (43, -1, 0), (51, -1, -1), (36, 0, 1), (52, 0, -1), (37, 1, 1), (45, 1, 0), (53, 1, -1)], (45, False): [(36, -1, 1), (44, -1, 0), (52, -1, -1), (37, 0, 1), (53, 0, -1), (38, 1, 1), (46, 1, 0), (54, 1, -1)], (46, False): [(37, -1, 1), (45, -1, 0), (53, -1, -1), (38, 0, 1), (54, 0, -1), (39, 1, 1), (47, 1, 0), (55, 1, -1)], (47, False): [(38, -1, 1), (46, -1, 0), (54, -1, -1), (39, 0, 1), (55, 0, -1)], (48, False): [(40, 0, 1), (56, 0, -1), (41, 1, 1), (49, 1, 0), (57, 1, -1)], (49, False): [(40, -1, 1), (48, -1, 0), (56, -1, -1), (41, 0, 1), (57, 0, -1), (42, 1, 1), (50, 1, 0), (58, 1, -1)], (50, False): [(41, -1, 1), (49, -1, 0), (57, -1, -1), (42, 0, 1), (58, 0, -1), (43, 1, 1), (51, 1, 0), (59, 1, -1)], (51, False): [(42, -1, 1), (50, -1, 0), (58, -1, -1), (43, 0, 1), (59, 0, -1), (44, 1, 1), (52, 1, 0), (60, 1, -1)], (52, False): [(43, -1, 1), (51, -1, 0), (59, -1, -1), (44, 0, 1), (60, 0, -1), (45, 1, 1), (53, 1, 0), (61, 1, -1)], (53, False): [(44, -1, 1), (52, -1, 0), (60, -1, -1), (45, 0, 1), (61, 0, -1), (46, 1, 1), (54, 1, 0), (62, 1, -1)], (54, False): [(45, -1, 1), (53, -1, 0), (61, -1, -1), (46, 0, 1), (62, 0, -1), (47, 1, 1), (55, 1, 0), (63, 1, -1)], (55, False): [(46, -1, 1), (54, -1, 0), (62, -1, -1), (47, 0, 1), (63, 0, -1)], (56, False): [(48, 0, 1), (49, 1, 1), (57, 1, 0)], (57, False): [(48, -1, 1), (56, -1, 0), (49, 0, 1), (50, 1, 1), (58, 1, 0)], (58, False): [(49, -1, 1), (57, -1, 0), (50, 0, 1), (51, 1, 1), (59, 1, 0)], (59, False): [(50, -1, 1), (58, -1, 0), (51, 0, 1), (52, 1, 1), (60, 1, 0)], (60, False): [(51, -1, 1), (59, -1, 0), (52, 0, 1), (53, 1, 1), (61, 1, 0)], (61, False): [(52, -1, 1), (60, -1, 0), (53, 0, 1), (54, 1, 1), (62, 1, 0)], (62, False): [(53, -1, 1), (61, -1, 0), (54, 0, 1), (55, 1, 1), (63, 1, 0)], (63, False): [(54, -1, 1), (62, -1, 0), (55, 0, 1)], (0, True): [(8, 0, 1), (1, 1, 0), (9, 1, 1)], (1, True): [(0, -1, 0), (8, -1, 1), (9, 0, 1), (2, 1, 0), (10, 1, 1)], (2, True): [(1, -1, 0), (9, -1, 1), (10, 0, 1), (3, 1, 0), (11, 1, 1)], (3, True): [(2, -1, 0), (10, -1, 1), (11, 0, 1), (4, 1, 0), (12, 1, 1)], (4, True): [(3, -1, 0), (11, -1, 1), (12, 0, 1), (5, 1, 0), (13, 1, 1)], (5, True): [(4, -1, 0), (12, -1, 1), (13, 0, 1), (6, 1, 0), (14, 1, 1)], (6, True): [(5, -1, 0), (13, -1, 1), (14, 0, 1), (7, 1, 0), (15, 1, 1)], (7, True): [(6, -1, 0), (14, -1, 1), (15, 0, 1)], (8, True): [(0, 0, -1), (16, 0, 1), (1, 1, -1), (9, 1, 0), (17, 1, 1)], (9, True): [(0, -1, -1), (8, -1, 0), (16, -1, 1), (1, 0, -1), (17, 0, 1), (2, 1, -1), (10, 1, 0), (18, 1, 1)], (10, True): [(1, -1, -1), (9, -1, 0), (17, -1, 1), (2, 0, -1), (18, 0, 1), (3, 1, -1), (11, 1, 0), (19, 1, 1)], (11, True): [(2, -1, -1), (10, -1, 0), (18, -1, 1), (3, 0, -1), (19, 0, 1), (4, 1, -1), (12, 1, 0), (20, 1, 1)], (12, True): [(3, -1, -1), (11, -1, 0), (19, -1, 1), (4, 0, -1), (20, 0, 1), (5, 1, -1), (13, 1, 0), (21, 1, 1)], (13, True): [(4, -1, -1), (12, -1, 0), (20, -1, 1), (5, 0, -1), (21, 0, 1), (6, 1, -1), (14, 1, 0), (22, 1, 1)], (14, True): [(5, -1, -1), (13, -1, 0), (21, -1, 1), (6, 0, -1), (22, 0, 1), (7, 1, -1), (15, 1, 0), (23, 1, 1)], (15, True): [(6, -1, -1), (14, -1, 0), (22, -1, 1), (7, 0, -1), (23, 0, 1)], (16, True): [(8, 0, -1), (24, 0, 1), (9, 1, -1), (17, 1, 0), (25, 1, 1)], (17, True): [(8, -1, -1), (16, -1, 0), (24, -1, 1), (9, 0, -1), (25, 0, 1), (10, 1, -1), (18, 1, 0), (26, 1, 1)], (18, True): [(9, -1, -1), (17, -1, 0), (25, -1, 1), (10, 0, -1), (26, 0, 1), (11, 1, -1), (19, 1, 0), (27, 1, 1)], (19, True): [(10, -1, -1), (18, -1, 0), (26, -1, 1), (11, 0, -1), (27, 0, 1), (12, 1, -1), (20, 1, 0), (28, 1, 1)], (20, True): [(11, -1, -1), (19, -1, 0), (27, -1, 1), (12, 0, -1), (28, 0, 1), (13, 1, -1), (21, 1, 0), (29, 1, 1)], (21, True): [(12, -1, -1), (20, -1, 0), (28, -1, 1), (13, 0, -1), (29, 0, 1), (14, 1, -1), (22, 1, 0), (30, 1, 1)], (22, True): [(13, -1, -1), (21, -1, 0), (29, -1, 1), (14, 0, -1), (30, 0, 1), (15, 1, -1), (23, 1, 0), (31, 1, 1)], (23, True): [(14, -1, -1), (22, -1, 0), (30, -1, 1), (15, 0, -1), (31, 0, 1)], (24, True): [(16, 0, -1), (32, 0, 1), (17, 1, -1), (25, 1, 0), (33, 1, 1)], (25, True): [(16, -1, -1), (24, -1, 0), (32, -1, 1), (17, 0, -1), (33, 0, 1), (18, 1, -1), (26, 1, 0), (34, 1, 1)], (26, True): [(17, -1, -1), (25, -1, 0), (33, -1, 1), (18, 0, -1), (34, 0, 1), (19, 1, -1), (27, 1, 0), (35, 1, 1)], (27, True): [(18, -1, -1), (26, -1, 0), (34, -1, 1), (19, 0, -1), (35, 0, 1), (20, 1, -1), (28, 1, 0), (36, 1, 1)], (28, True): [(19, -1, -1), (27, -1, 0), (35, -1, 1), (20, 0, -1), (36, 0, 1), (21, 1, -1), (29, 1, 0), (37, 1, 1)], (29, True): [(20, -1, -1), (28, -1, 0), (36, -1, 1), (21, 0, -1), (37, 0, 1), (22, 1, -1), (30, 1, 0), (38, 1, 1)], (30, True): [(21, -1, -1), (29, -1, 0), (37, -1, 1), (22, 0, -1), (38, 0, 1), (23, 1, -1), (31, 1, 0), (39, 1, 1)], (31, True): [(22, -1, -1), (30, -1, 0), (38, -1, 1), (23, 0, -1), (39, 0, 1)], (32, True): [(24, 0, -1), (40, 0, 1), (25, 1, -1), (33, 1, 0), (41, 1, 1)], (33, True): [(24, -1, -1), (32, -1, 0), (40, -1, 1), (25, 0, -1), (41, 0, 1), (26, 1, -1), (34, 1, 0), (42, 1, 1)], (34, True): [(25, -1, -1), (33, -1, 0), (41, -1, 1), (26, 0, -1), (42, 0, 1), (27, 1, -1), (35, 1, 0), (43, 1, 1)], (35, True): [(26, -1, -1), (34, -1, 0), (42, -1, 1), (27, 0, -1), (43, 0, 1), (28, 1, -1), (36, 1, 0), (44, 1, 1)], (36, True): [(27, -1, -1), (35, -1, 0), (43, -1, 1), (28, 0, -1), (44, 0, 1), (29, 1, -1), (37, 1, 0), (45, 1, 1)], (37, True): [(28, -1, -1), (36, -1, 0), (44, -1, 1), (29, 0, -1), (45, 0, 1), (30, 1, -1), (38, 1, 0), (46, 1, 1)], (38, True): [(29, -1, -1), (37, -1, 0), (45, -1, 1), (30, 0, -1), (46, 0, 1), (31, 1, -1), (39, 1, 0), (47, 1, 1)], (39, True): [(30, -1, -1), (38, -1, 0), (46, -1, 1), (31, 0, -1), (47, 0, 1)], (40, True): [(32, 0, -1), (48, 0, 1), (33, 1, -1), (41, 1, 0), (49, 1, 1)], (41, True): [(32, -1, -1), (40, -1, 0), (48, -1, 1), (33, 0, -1), (49, 0, 1), (34, 1, -1), (42, 1, 0), (50, 1, 1)], (42, True): [(33, -1, -1), (41, -1, 0), (49, -1, 1), (34, 0, -1), (50, 0, 1), (35, 1, -1), (43, 1, 0), (51, 1, 1)], (43, True): [(34, -1, -1), (42, -1, 0), (50, -1, 1), (35, 0, -1), (51, 0, 1), (36, 1, -1), (44, 1, 0), (52, 1, 1)], (44, True): [(35, -1, -1), (43, -1, 0), (51, -1, 1), (36, 0, -1), (52, 0, 1), (37, 1, -1), (45, 1, 0), (53, 1, 1)], (45, True): [(36, -1, -1), (44, -1, 0), (52, -1, 1), (37, 0, -1), (53, 0, 1), (38, 1, -1), (46, 1, 0), (54, 1, 1)], (46, True): [(37, -1, -1), (45, -1, 0), (53, -1, 1), (38, 0, -1), (54, 0, 1), (39, 1, -1), (47, 1, 0), (55, 1, 1)], (47, True): [(38, -1, -1), (46, -1, 0), (54, -1, 1), (39, 0, -1), (55, 0, 1)], (48, True): [(40, 0, -1), (56, 0, 1), (41, 1, -1), (49, 1, 0), (57, 1, 1)], (49, True): [(40, -1, -1), (48, -1, 0), (56, -1, 1), (41, 0, -1), (57, 0, 1), (42, 1, -1), (50, 1, 0), (58, 1, 1)], (50, True): [(41, -1, -1), (49, -1, 0), (57, -1, 1), (42, 0, -1), (58, 0, 1), (43, 1, -1), (51, 1, 0), (59, 1, 1)], (51, True): [(42, -1, -1), (50, -1, 0), (58, -1, 1), (43, 0, -1), (59, 0, 1), (44, 1, -1), (52, 1, 0), (60, 1, 1)], (52, True): [(43, -1, -1), (51, -1, 0), (59, -1, 1), (44, 0, -1), (60, 0, 1), (45, 1, -1), (53, 1, 0), (61, 1, 1)], (53, True): [(44, -1, -1), (52, -1, 0), (60, -1, 1), (45, 0, -1), (61, 0, 1), (46, 1, -1), (54, 1, 0), (62, 1, 1)], (54, True): [(45, -1, -1), (53, -1, 0), (61, -1, 1), (46, 0, -1), (62, 0, 1), (47, 1, -1), (55, 1, 0), (63, 1, 1)], (55, True): [(46, -1, -1), (54, -1, 0), (62, -1, 1), (47, 0, -1), (63, 0, 1)], (56, True): [(48, 0, -1), (49, 1, -1), (57, 1, 0)], (57, True): [(48, -1, -1), (56, -1, 0), (49, 0, -1), (50, 1, -1), (58, 1, 0)], (58, True): [(49, -1, -1), (57, -1, 0), (50, 0, -1), (51, 1, -1), (59, 1, 0)], (59, True): [(50, -1, -1), (58, -1, 0), (51, 0, -1), (52, 1, -1), (60, 1, 0)], (60, True): [(51, -1, -1), (59, -1, 0), (52, 0, -1), (53, 1, -1), (61, 1, 0)], (61, True): [(52, -1, -1), (60, -1, 0), (53, 0, -1), (54, 1, -1), (62, 1, 0)], (62, True): [(53, -1, -1), (61, -1, 0), (54, 0, -1), (55, 1, -1), (63, 1, 0)], (63, True): [(54, -1, -1), (62, -1, 0), (55, 0, -1)]}


RANK_MASKS = {0: (18446744073709551360, 0), 1: (18446744073709486080, 255), 2: (18446744073692774400, 65535), 3: (18446744069414584320, 16777215), 4: (18446742974197923840, 4294967295), 5: (18446462598732840960, 1099511627775), 6: (18374686479671623680, 281474976710655), 7: (0, 72057594037927935)}

# for rank in range(0, 8):
#     ranksAhead = list(range(rank + 1, 8)) 
#     ranksBehind = list(range(0, rank))

#     ranksBehindMasks = list(map(lambda x: chess.BB_RANKS[x], ranksBehind))
#     ranksAheadMasks = list(map(lambda x: chess.BB_RANKS[x], ranksAhead))

#     piecesBehindMask = reduce(lambda x, y: x | y, ranksBehindMasks, 0)
#     piecesAheadMask = reduce(lambda x, y: x | y, ranksAheadMasks, 0)

#     RANK_MASKS[rank] = (piecesAheadMask, piecesBehindMask) 

# print(RANK_MASKS)

ADJACENT_FILES_MASK = {0: 217020518514230019, 1: 506381209866536711, 2: 1012762419733073422, 3: 2025524839466146844, 4: 4051049678932293688, 5: 8102099357864587376, 6: 16204198715729174752, 7: 13889313184910721216}

# for file in range(0, 8):
#     files = [file]
#     if((file - 1) >= 0):
#         files.append(file - 1)

#     if((file + 1) < 8):
#         files.append(file + 1)

#     fileMasks = list(map(lambda x: chess.BB_FILES[x], files))

#     adjacentFilesMask = reduce(lambda x, y: x | y, fileMasks, 0)

#     ADJACENT_FILES_MASK[file] = adjacentFilesMask

# print(ADJACENT_FILES_MASK)