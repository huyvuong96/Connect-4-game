import random, time
from tkinter import *

class GUI:
    def __init__(self, window):
        self.window = window
        self.frame = Frame(window)
        self.frame.pack()
        self.width = 800
        self.height = 850
        self.row = 6 #height
        self.col = 7 #width
        self.messageSize = 25
        self.diameter = self.width / 7
        self.ox1 = 'RED'
        self.ox2 = 'BLUE'
        self.ox0 = 'BLACK'
        self.watcher = 2
        self.turn = self.watcher %2
        self.gameOVER = False
        self.one= False
        self.two= False

        self.quitButton = Button(self.frame, text='Quit',fg='green', command=self.quitGame)
        self.quitButton.pack(side=LEFT)

        self.OnePlayer = Button(self.frame, text='vs AI', command=self.playwithAi)
        self.OnePlayer.pack(side=RIGHT)

        self.TwoPlayer = Button(self.frame, text='vs another Human', command=self.playwithHuman)
        self.TwoPlayer.pack(side=RIGHT)

        self.scale = Scale(self.frame, orient=HORIZONTAL, from_=0, to=3, length=200, label='IQ for AI')
        self.scale.pack(side=LEFT)

        self.NewGame = Button(self.frame, text='New Game', command=self.clear)
        self.NewGame.pack(side=RIGHT)

        self.draw = Canvas(window, height=self.height, width=self.width)
        self.draw.bind('<Button-1>', self.mouseInput)
        self.draw.pack()

        self.circles = []
        self.colors = []

        y = 0
        for row in range(self.row):
            circleRow = []
            colorRow = []
            x=0
            for col in range(self.col):
                circleRow += [self.draw.create_oval(x, y, x + self.diameter, y + self.diameter, fill='BLACK')]
                colorRow += ['BLACK']
                x += self.diameter

            self.circles += [circleRow]
            self.colors += [colorRow]
            y += self.diameter

        self.message = self.draw.create_text(self.messageSize, self.height - self.messageSize,
                                             text='CHOOSE YOUR OPPONENT!!!',
                                             anchor='w', font='Courier 24')

    def mouseInput(self, event): #mouse input funtion
        # self.window.bell()
        col = int(event.x / self.diameter) #7
        row = int(event.y / self.diameter) #6
        print('board[%s][%s]' % (row, col))
        self.turn = self.watcher %2
        #print("turn is",self.turn)

        if self.one == True: #one player game
            self.humanmove(col)
            if not self.winsFor(self.ox1):
                self.aimove()
            if self.isFull():
                self.draw.itemconfig(self.message, text='TIE!!!')
                self.one = False

        if self.two == True: # 2 player game
            if self.turn == 0:
                ox = self.ox1
                if self.allowsMove(col):
                    self.watcher += 1
                    print('watcher1 is',self.watcher)
                row = self.addMove(col,ox)
                self.draw.itemconfig(self.circles[row][col], fill=self.colors[row][col])
                self.draw.itemconfig(self.message, text='PLAYER 2 MAKE YOUR MOVE')

                if self.winsFor(ox):
                    self.draw.itemconfig(self.message, text='PLAYER 1 WIN!!!')
                    self.two = False

                if self.isFull():
                    self.draw.itemconfig(self.message, text='TIE!!!')
                    self.two = False

            if self.turn == 1:
                ox = self.ox2
                if self.allowsMove(col):
                    self.watcher -= 1
                    print('watcher1 is',self.watcher)
                row = self.addMove(col,ox)
                self.draw.itemconfig(self.circles[row][col], fill=self.colors[row][col])
                self.draw.itemconfig(self.message, text='PLAYER 1 MAKE YOUR MOVE')

                if self.winsFor(ox):
                    self.draw.itemconfig(self.message, text='PLAYER 2 WIN!!!')
                    self.two = False

                if self.isFull():
                    self.draw.itemconfig(self.message, text='TIE!!!')
                    self.two = False

    def playwithAi(self):
        self.one= True
        self.two = False
        self.draw.itemconfig(self.message, text='MAKE YOUR MOVE HUMAN!!!')

    def playwithHuman(self):
        self.two = True
        self.one = False
        self.draw.itemconfig(self.message, text='PLAYER 1 MAKE YOUR MOVE')

    def humanmove(self,col): #move for human
        row = self.addMove(col, self.ox1)
        self.draw.itemconfig(self.circles[row][col], fill=self.colors[row][col])
        self.draw.itemconfig(self.message, text='AI IS THINKING')
        if self.winsFor(self.ox1):
            self.draw.itemconfig(self.message, text='HUMAN WIN!!!')
            self.one = False

    def aimove(self): #move for AI
        col = self.nextMove()
        row = self.addMove(col, self.ox2)
        #self.draw.itemconfig(self.circles[row][col], fill=self.colors[row][col])
        self.draw.after(1000, lambda: self.draw.itemconfig(self.circles[row][col], fill=self.colors[row][col]))
        print('AI move is', col)
        self.draw.after(1000, lambda: self.draw.itemconfig(self.message, text='MAKE YOUR MOVE HUMAN!!!'))
        if self.winsFor(self.ox2):
            self.draw.after(1000, lambda:self.draw.itemconfig(self.message, text='AI WIN!!!'))
            self.one = False

    def allowsMove(self,col): #check if a spot is empty
        if 0 <= col < self.col:
            return self.colors[0][col] == 'BLACK'
        else:
            return False

    def addMove(self,col,ox): #add a move to the board
        if self.allowsMove(col): #check if the column is available to add move
            for row in range(self.row):
                if self.colors[row][col] != 'BLACK':
                    self.colors[row-1][col] = ox
                    return row-1
            self.colors[self.row-1][col] = ox
            return self.row-1

    def clear(self): #clear the board
        self.one = False
        self.two = False
        self.draw.itemconfig(self.message, text='CHOOSE YOUR NEW OPPONENT!!!')
        for row in range(self.row):
            for col in range(self.col):
                self.colors[row][col] = 'BLACK'
                self.draw.itemconfig(self.circles[row][col], fill=self.colors[row][col])

    def isFull(self): #check if the board is full
        for col in range(self.col):
            if self.allowsMove(col):
                return False
        return True

    def winsFor(self,ox):
        for row in range(self.row): #checks for win horizontally
            for col in range(self.col - 3):
                if self.colors[row][col] == ox and \
                    self.colors[row][col+1] == ox and \
                    self.colors[row][col+2] == ox and \
                    self.colors[row][col+3] == ox:
                        return True

        for row in range(self.row-3): #checks for win vertically
            for col in range(self.col):
                if self.colors[row][col] == ox and \
                    self.colors[row+1][col] == ox and \
                    self.colors[row+2][col] == ox and \
                    self.colors[row+3][col] == ox:
                        return True

        for row in range(self.row -3): #checks for win NW to SE
            for col in range(self.col -3):
                if self.colors[row][col] == ox and \
                    self.colors[row+1][col+1] == ox and \
                    self.colors[row+2][col+2] == ox and \
                    self.colors[row+3][col+3] == ox:
                        return True

        for row in range(3,self.row): #checks for win NE to SW
            for col in range(self.col -3):
                if self.colors[row][col] == ox and \
                    self.colors[row-1][col+1] == ox and \
                    self.colors[row-2][col+2] == ox and \
                    self.colors[row-3][col+3] == ox:
                        return True
        return False

    def delMove(self,col): #delete one move
        for row in range(self.row):
            if self.colors[row][col] != 'BLACK':
                self.colors[row][col] = 'BLACK'
                return row

    def quitGame(self):
        self.window.destroy()

    def scoresFor(self, ox, ply):
        if ply == 0 :
            return [50] * 7

        goodMoves = [0] * 7
        for move1 in range(7):
            if not self.allowsMove(move1):
                continue

            col = move1
            row = self.addMove(move1, self.ox2)
            self.draw.itemconfig(self.circles[row][col], fill=self.colors[row][col])

            if self.winsFor(self.ox2):
                # a winning moves get 100
                goodMoves[move1] = 100
                col = move1
                row = self.delMove(move1)
                self.draw.itemconfig(self.circles[row][col], fill='BLACK')
                break #no bother checking other moves if win
            else:
                # counter moves
                if self.isFull():
                    goodMoves[move1] = 0
                else:
                    for move2 in range(7):
                        if not self.allowsMove(move2):
                            continue
                        col = move2
                        row= self.addMove(move2,self.ox1)
                        self.draw.itemconfig(self.circles[row][col], fill=self.colors[row][col])

                        if self.winsFor(self.ox1):
                            # losing moves get -1
                            goodMoves[move1] = -1
                            col = move2
                            row = self.delMove(move2)
                            self.draw.itemconfig(self.circles[row][col], fill='BLACK')
                            break
                        else:
                            # recursive
                            goodMoves[move1] += max(self.scoresFor(ox, ply - 1))
                        col = move2
                        row = self.delMove(move2)
                        self.draw.itemconfig(self.circles[row][col], fill='BLACK')
            col = move1
            row = self.delMove(move1)
            self.draw.itemconfig(self.circles[row][col], fill='BLACK')
        return goodMoves

    def nextMove(self):
        strategy = self.scoresFor(self.ox2, self.scale.get())
        # get the highest scores to set it as a standard to make choice easier
        bestMove = -1
        for i in range(7):
            if strategy[i] > bestMove and self.allowsMove(i):
                bestMove = strategy[i]

        # get the move that has highest score
        execute = [] #list of the column that has good moves
        for i in range(7):
            if strategy[i] == bestMove and self.allowsMove(i):
                execute.append(i)
                print(execute)
        return random.choice(execute) #random because sometimes bestMove is not 100 but only 50

def main():
    root = Tk()
    root.title('Connect 4')
    b= GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
