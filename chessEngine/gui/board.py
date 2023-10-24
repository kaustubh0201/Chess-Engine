from turtle import position
import pygame as pg
import sys
import chess

from dataclasses import dataclass

class Chessboard:
    def __init__(self,screenHeight, screenWidth, squareHeight, squareWidth):
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth
        self.squareHeight = squareHeight
        self.squareWidth = squareWidth
        self.WHITE= 255, 255, 255
        self.BLACK = 75, 75, 75
        
        self.starting_x = (screenWidth-squareWidth*8)/2; 
        self.starting_y = (screenHeight-squareHeight*8)/2; 
                
    def loadSquarePosition(self):
        squareList = []
        for file in range(0,8):
            for rank in range(0,8):
                isLightSquare = (file + rank) % 2 != 0
                squareColor = self.WHITE if isLightSquare else self.BLACK
                position = (self.starting_x + file*self.squareWidth, self.starting_y + rank*self.squareHeight)
                rect = pg.Rect(position[0],position[1],self.squareWidth,self.squareHeight)
                squareList.append((rect,squareColor))
        # print(squareList)
        return squareList
    
    def drawChessBoard(self,squareList,screen):
        for rect, color in squareList:
            pg.draw.rect(screen,color,rect)
     
    # List of tuples -> position, piece  
    def loadPositionFromFen(self,fen):
        pieceTypeFromSymbol = {
            'k' : chess.KING,
            'p' : chess.PAWN,
            'n' : chess.KNIGHT,
            'b' : chess.BISHOP,
            'r' : chess.ROOK,
            'q' : chess.QUEEN
        }
        
        piecePosition = {}
        fenboard = fen.split(' ')[0]
        file = 0
        rank = 7
        
        for symbol in fenboard:
            if(symbol == '/'):
                file = 0
                rank-=1
            else:
                if(symbol.isdigit()):
                    file += int(symbol)
                else:
                    pieceColor = chess.WHITE if symbol.isupper() else chess.BLACK
                    pieceType = pieceTypeFromSymbol[symbol.lower()]
                    piecePosition[(self.starting_x + file*self.squareWidth,self.starting_y + rank*self.squareHeight)] = (pieceType,pieceColor)
                    file+=1
        return piecePosition
                    
        
                 

class SpriteSheet:
    def __init__(self, filename):
        """Load the sheet."""

    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pg.image.load(filename).convert_alpha()
            # self.sheet = pg.transform.scale(self.sheet,(500,500))
        except pg.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)


    def image_at(self, rectangle, colorkey = None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pg.Rect(rectangle)
        image = pg.Surface(rect.size, pg.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pg.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey = None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)
    
    def load_grid_images(self, num_rows, num_cols, x_margin = 0, x_padding = 0, y_margin=0, y_padding=0):
        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size
        
        # calculate size of each icon
        x_sprite_size = (sheet_width - 2 * x_margin - (num_cols - 1) * x_padding) / num_cols
        y_sprite_size = (sheet_height - 2 * y_margin - (num_rows - 1) * y_padding) / num_rows
        
        sprite_rects = []
        for row_num in range(num_rows):
            for col_num in range(num_cols):
                x = x_margin + col_num * (x_sprite_size + x_padding)
                y = y_margin + row_num * (y_sprite_size + y_padding)
                sprite_rect = (x, y, x_sprite_size, y_sprite_size)
                sprite_rects.append(sprite_rect)
                
        grid_images = self.images_at(sprite_rects)
        print(f"Loaded {len(grid_images)} grid images.")
        
        return grid_images
        
        

class ChessGame:
    def __init__(self) -> None:   
        self.BACKGROUND = 247, 199, 171, 255
        

        self.SQUARE_HEIGHT = 100
        self.SQUARE_WIDTH = 100

        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 1024
        
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
        self.chess_set = ChessSet(self)
        pg.display.set_caption("Chess")
        
        self.cb = Chessboard(self.SCREEN_HEIGHT,self.SCREEN_WIDTH,self.SQUARE_HEIGHT,self.SQUARE_WIDTH)
        self.squareList = self.cb.loadSquarePosition()
        
        piecePosition = self.cb.loadPositionFromFen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        
        self.chess_set.placePiece(piecePosition)
    def run_game(self):
            
        while True:
            self._check_events()
            self._update_screen()
                
    def _check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
                    
    def _update_screen(self):
        self.screen.fill(self.BACKGROUND)
        self.cb.drawChessBoard(self.squareList,self.screen)
        
        # for rect, color in squareList:
        #     pg.draw.rect(self.screen,color,rect)
        
        # for index, piece in enumerate(self.chess_set.pieces[:6]):
        #     piece.x = index * 100
        #     piece.blitme(self.SQUARE_HEIGHT, self.SQUARE_WIDTH)

        # # white pieces row
        # for index, piece in enumerate(self.chess_set.pieces[6:]):
        #     piece.x = index * 100
        #     piece.y = 100
        #     piece.blitme(self.SQUARE_HEIGHT, self.SQUARE_WIDTH)
        # self.screen = chess_game.screen
        # x_index = 0
        # y_index = 0
        # for entry in self.chess_set.pieces:
        #     for piece in self.chess_set.pieces[entry]:
        #         piece.x = x_index*100
        #         piece.y = y_index*100
        #         piece.blitme(self.SQUARE_HEIGHT,self.SQUARE_WIDTH)
        #         x_index+=1
        #     y_index+=1
        #     x_index = 0
        
        for piece in self.chess_set.finalPiecePositions:
            piece.blitme(self.SQUARE_HEIGHT,self.SQUARE_WIDTH)
        # piecePosition[(rank,file)] = (pieceType,pieceColor)    
        
        
        pg.display.flip()
            
class Piece:
    
    def __init__(self, chess_game):
        self.image = None 
        self.name = ''
        self.color = ''
        self.x, self.y = 0.0, 0.0
        self.screen = chess_game.screen
        # black pieces row
        
    # 
    def blitme(self,squareHeight, squareWidth):
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y
        self.image = pg.transform.scale(self.image,(squareHeight,squareWidth))
        self.screen.blit(self.image, self.rect)
        
        
class ChessSet:
    def __init__(self,chess_game):
         
        self.chess_game = chess_game
        self.pieces = {}
        self._load_pieces()
        self.finalPiecePositions = []
        
    def _load_pieces(self):
        filename = "./output-onlinepngtools.png"
        piece_ss = SpriteSheet(filename)
        
        piece_images = piece_ss.load_grid_images(2, 6, x_margin=0,x_padding=0, y_margin=0, y_padding=0)
        
        colors = [chess.BLACK, chess.WHITE]
        names = [chess.KING, chess.QUEEN, chess.BISHOP, chess.KNIGHT, chess.ROOK, chess.PAWN]
        quantity = {
            chess.KING: 1,
            chess.QUEEN : 1,
            chess.BISHOP : 2,
            chess.KNIGHT : 2,
            chess.ROOK : 2,
            chess.PAWN: 8
        }
        
        piece_num = 0        
        for color in colors:
            for name in names:
                
                for _ in range(quantity[name]):
                    piece = Piece(self.chess_game)
                    piece.name = name
                    piece.color = color
                    piece.image = piece_images[piece_num]

                    if ((color, name) in self.pieces):
                        self.pieces[(color, name)].append(piece)
                    else:
                        self.pieces[(color, name)] = [piece]
                
                piece_num += 1
        
    def placePiece(self,piecePosition):
        for (x,y),(t,c) in piecePosition.items():
            temp_piece = self.pieces[(c,t)][0]
            del self.pieces[(c,t)][0]
            temp_piece.x = x
            temp_piece.y = y
            self.finalPiecePositions.append(temp_piece)
                
                     
if __name__ == '__main__':
    chess_game = ChessGame()
    chess_game.run_game()
                    

# def squares():
#     squareList = []
#     for file in range(8):
#         for rank in range(8):
#             isLightSquare = (file + rank) % 2 != 0
#             squareColor = WHITE if isLightSquare else BLACK
#             position = (STARTING_X + file*SQUARE_WIDTH, STARTING_Y + rank*SQUARE_HEIGHT)
            
#             rect = pg.Rect(position[0],position[1],SQUARE_WIDTH,SQUARE_HEIGHT)
#             squareList.append((rect,squareColor))
            
#     return squareList            
            
            
# def drawBoard(screen, squareList):
#     for rect, color in squareList:
#         pg.draw.rect(screen,color,rect)
    
# def boardGui():
#     pg.init()

#     size = width, height = 1024, 1024
#     speed = [2, 2]
    

#     screen = pg.display.set_mode(size)

#     # ball = pg.image.load("./chessEngine/gui/chesspieces.png")
#     # ballrect = ball.get_rect()
#     squareList = squares()
#     while 1:
#         for event in pg.event.get():
#             if event.type == pg.QUIT: sys.exit()
            
        
#         screen.fill(BACKGROUND)
#         drawBoard(screen,squareList)
#         # screen.blit(ball, ballrect)
#         pg.display.flip()
        
        
# if(__name__=='__main__'):
#     boardGui()
    



