import numpy as np
from typing import Dict


class TTTGame:

    __DEFAULT  : int = 10

    __ZERO     : int = +1
    __CROSS    : int = -1
    __TIE      : int = 00
    __COLS     : int = +3 
    __ROWS     : int = +3
    currPlayer : int = __ZERO

    __DISPLAYCHARS : Dict[int, str] = {__ZERO: 'o', __CROSS: 'x'}

    board : np.ndarray = np.full((__ROWS, __COLS), __DEFAULT)
    
    
    gameResult = None
    gameOver = False

    def __init__(self) -> None:
       pass

    def makeMove(self, move : (int, int)) -> bool:
        x = move[0] 
        y = move[1]
        
        if self.gameOver:
            return self.gameOver 

        if((1 <= x <= 3) and (1 <= y <= 3) and (self.board[x - 1][y - 1] == self.__DEFAULT)):
            self.board[x - 1][y - 1] = self.currPlayer 
            self.currPlayer *= -1 
        else:
            raise Exception(f'Invalid move ({x}, {y})')

        self.gameOver, self.gameResult = self.__terminationCheck()
        return self.gameOver
        
    
    def drawBoard(self) -> None:
        boardStr = ''' ┌─────────┬─────────┬─────────┐
 │         │         │         │
 │ aaaaa11 │ aaaaa12 │ aaaaa13 │
 │         │         │         │
 ├─────────┼─────────┼─────────┤
 │         │         │         │
 │ aaaaa21 │ aaaaa22 │ aaaaa23 │
 │         │         │         │
 ├─────────┼─────────┼─────────┤
 │         │         │         │
 │ aaaaa31 │ aaaaa32 │ aaaaa33 │
 │         │         │         │
 └─────────┴─────────┴─────────┘''' 

        for i in range(0, self.__ROWS):
            for j in range(0, self.__COLS):
                if(self.board[i][j] == self.__DEFAULT):
                    boardStr = boardStr.replace(f'aaaaa{i + 1}{j + 1}', f'({i + 1} , {j + 1})')
                else:
                    boardStr = boardStr.replace(f'aaaaa{i + 1}{j + 1}', f'   {self.__DISPLAYCHARS[self.board[i][j]]}   ')
        
        print(boardStr)

    def currentPlayer(self) -> str:
        return self.__DISPLAYCHARS[self.currPlayer]

    def result(self) -> str:
        if self.gameOver:

            if (self.gameResult == self.__TIE):
                return 'Tie' 

            else:
                return self.__DISPLAYCHARS[self.gameResult]

        raise Exception('No result')
        
    def __terminationCheck(self) -> (bool, int):
        
        # Checking rows
        for i in range(0, self.__ROWS):
            row = self.board[i]
            
            if(self.__checkElements(row)):
                return (True, row[0])

        # Checking columns
        for j in range(0, self.__COLS):
            col = np.full(self.__COLS, -1)

            for i in range(0, self.__ROWS):
                col[i] = self.board[i][j]
            
            if(self.__checkElements(col)):
                return (True, col[0])

        # primary diagonal
        m = min(self.__ROWS, self.__COLS)
        diag = np.full(m, -1)
        for i in range(0, m):
            diag[i] = self.board[i][i]

        if(self.__checkElements(diag)):
            return (True, diag[0])

        # other diagonal
        for i in range(0, m):
            diag[i] = self.board[i][self.__COLS - i - 1]

        if(self.__checkElements(diag)):
            return (True, diag[0])

        # draw

        for i in range(0, self.__ROWS):
            for j in range(0, self.__COLS):

                if(self.board[i][j] == self.__DEFAULT):
                    return (False, self.__DEFAULT)

        return (True, self.__TIE) 



    def __checkElements(self, l : np.ndarray) -> bool:
        n = len(l)
        if(l[0] == self.__DEFAULT):
            return False
    

        for i in range(1, n):
            if l[i] != l[0]:
                return False

        return True




def game():
    tttg = TTTGame()
    
    while(not tttg.gameOver):
        tttg.drawBoard()
        print(f'Player: {tttg.currentPlayer()} ')
        print('Enter the position: ', end = '')
        x, y = map(int, input().strip().split())  

        try:
            tttg.makeMove((x, y))
        except Exception as e:
            print(e)


    print(f'Game Over! result is: {tttg.result()}')
    tttg.drawBoard()



if __name__ == '__main__':
    game()
