from asyncio.windows_events import NULL
from math import floor
import pygame

def checkNatNum(n):
    if n - floor(n) == 0:
        return True


class Game:
    def __init__(self):
        self._window = pygame.display.set_mode((560,560))
        self._running = True
        self._mousepress = False
        self._pieces = [Piece(430, 430, "bishop"), Piece(500, 430, "knight"), Piece(360, 430, "pawn")]
        self._tiles = []
        self._currentPiece = NULL
        self._events = []
        self.generateBoard()
        self._clock = pygame.time.Clock()
        

    def processInput(self):
        self._events = pygame.event.get()
        for e in self._events:
            if e.type == pygame.QUIT:
                self._running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                for i in range (0, len(self._pieces)):
                    if self._pieces[i].isColliding(e.pos):
                        self._mousepress = True
                        self._currentPiece = i

            elif e.type == pygame.MOUSEBUTTONUP:
                self._mousepress = False
            
            elif e.type == pygame.KEYDOWN:
                print(self.getTileNumber(self._pieces[self._currentPiece]))
                print("rank:", self._pieces[self._currentPiece]._rank, " startRank:", self.pieces[self._currentPiece]._startRank)

                
    def update(self):
        
        mousemove = pygame.mouse.get_rel()
        if self._mousepress == True:
            self._pieces[self._currentPiece].move(mousemove)
            
               
        if self._mousepress == False:
            if self.canMove(self._pieces[self._currentPiece]) == True:
                self.align()
            else:
                self.snapBack()

        self._pieces[self._currentPiece].updateTile()
        self.updateStartPos(self._pieces[self._currentPiece])
            
    
    def render (self):    
        for i in range (0, len(self._tiles)):
            self._tiles[i].draw(self._window)

        for i in range (0, len(self._pieces)):
            self._pieces[i].draw(self._window)
        pygame.display.update()

    def run(self):
        while self._running == True:
            self.processInput()
            self.update()
            self.render()
            self._clock.tick(60)

    def generateBoard(self):
        for i in range (0, 8):
            for j in range (0, 8):
                if (i + j) % 2 == 0: 
                    self._tiles.append(Tile(j*70, i*70, (0, 0, 0)))
                else:
                    self._tiles.append(Tile(j*70, i*70, (255, 255, 255)))   

    def align(self):
        for i in range(0, len(self._tiles)):
            if self._pieces[self._currentPiece]._middle[0] >= self._tiles[i]._x and self._pieces[self._currentPiece]._middle[0] < self._tiles[i]._x + self._tiles[i]._side:
                if self._pieces[self._currentPiece]._middle[1] >= self._tiles[i]._y and self._pieces[self._currentPiece]._middle[1] < self._tiles[i]._y + self._tiles[i]._side and self._tiles[i]._isTaken == False: 
                    self._pieces[self._currentPiece]._x = self._tiles[i]._x + 10
                    self._pieces[self._currentPiece]._y = self._tiles[i]._y + 10
                    self._pieces[self._currentPiece]._startx = self._pieces[self._currentPiece]._x
                    self._pieces[self._currentPiece]._starty = self._pieces[self._currentPiece]._y
                    
    def getTileNumber(self, piece):
        for i in range(0, len(self._tiles)):
            if piece._middle[0] >= self._tiles[i]._x and piece._middle[0] < self._tiles[i]._x + self._tiles[i]._side:
                if piece._middle[1] >= self._tiles[i]._y and piece._middle[1] < self._tiles[i]._y + self._tiles[i]._side: 
                    return i   

    def snapBack(self):
        self._pieces[self._currentPiece]._x = self._pieces[self._currentPiece]._startx
        self._pieces[self._currentPiece]._y = self._pieces[self._currentPiece]._starty
                    

    def updateStartPos(self, piece):
        if self._mousepress == False:
            piece._startTile = piece._tile
            piece._startRank = piece._rank
            piece._startFile = piece._file
    
    def canMove(self, piece):
        if piece._type == "pawn":
            if piece._startTile - 8 == self.getTileNumber(piece):
                return True
        elif piece._type == "knight":
            if (piece._startTile - 15 == self.getTileNumber(piece) or 
                piece._startTile - 17  == self.getTileNumber(piece) or
                piece._startTile + 15 == self.getTileNumber(piece) or 
                piece._startTile + 17  == self.getTileNumber(piece) or
                piece._startTile - 10 == self.getTileNumber(piece) or 
                piece._startTile - 6  == self.getTileNumber(piece) or
                piece._startTile + 10 == self.getTileNumber(piece) or 
                piece._startTile + 6  == self.getTileNumber(piece)):
                return True
        elif piece._type == "bishop":
            n = (piece._startTile - self.getTileNumber(piece))/9
            m = (piece._startTile - self.getTileNumber(piece))/7
            if checkNatNum(n) == True or checkNatNum(m) == True:
                return True
        elif piece._type == "rook":
            if (piece._startTile % 8 == self.getTileNumber(piece) % 8 or
                (self.getTileNumber(piece) - (self.getTileNumber(piece) % 8)) /8 == piece._startRank):
                return True
        elif piece._type == "queen":
            pass
        elif piece._type == "king":
            pass
        else:
            return False
    
    def getCurrentPiece(self):
        for e in self._events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                for i in range (0, len(self._pieces)):
                    if self._pieces[i].isColliding:
                        return i

    def checkTiles(self):
        pass


    
class Piece:
    def __init__(self, x, y, type):
        self._type = type
        self._side = 50
        self._x = x
        self._y = y
        self._startx = x
        self._starty = y
        self._color = (241, 236, 115)
        self._middle = (self._x + self._side/2 , self._y + self._side/2)
        self._tile = (self._middle[0] - 35)/70  + ((self._middle[1] - 35)/70)*8
        self._rank = (self._middle[1] - 35)/70
        self._file = (self._middle[0] - 35)/70
        self._startTile = self._tile
        self._startRank = self._rank
        self._startFile = self._file
        

    def draw (self, surface):
        pygame.draw.rect(surface, self._color, (self._x, self._y, self._side, self._side))

    def move (self, d):
        self._x += d[0]       
        self._y += d[1]
        self._middle = (self._x + self._side/2, self._y + self._side/2)
        
    def  isColliding (self, mousepos):
        return pygame.Rect(self._x, self._y, self._side, self._side).collidepoint(mousepos)

    def updateTile(self):
        self._middle = (self._x + self._side/2 , self._y + self._side/2)
        self._tile = (self._middle[0] - 35)/70  + ((self._middle[1] - 35)/70)*8
        self._rank = (self._middle[1] - 35)/70
        self._file = (self._middle[0] - 35)/70

class Tile:
    def __init__(self, x, y, color):
        self._side = 70
        self._x = x
        self._y = y
        self._color = color
        self._middle = (self._x + self._side/2, self._y + self._side/2)
        self._isTaken = NULL

    def draw (self, surface):
        pygame.draw.rect(surface, self._color, (self._x, self._y, self._side, self._side))
        




game = Game()
game.run()