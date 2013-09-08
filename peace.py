#!python
# -*- coding: utf-8 -*-

# chess-peace.py
# Joshua Moore
# 2013-09-08

## 
# Board
## 

class Peace(Exception):
    def __init__(self):
        self.message = "We have won!"

class Board:

    """Legend of the Board: None is empty, 't' stands for threatened, and
    objects represent themselves."""

    class Nothing:
  
        next = 0
        
        @staticmethod
        def reset():
            Board.Nothing.next = 0

        def __init__(self):
            self.pos = Board.Nothing.next
            Board.Nothing.next += 1
        
        def __repr__(self):
            return '%02d' % self.pos

    class Threatened:
        def __init__(self):
            self.count = 1

        def inc(self):
            self.count += 1

        def dec(self):
            self.count -= 1

        def __repr__(self):
            return 'tt'


    def __init__(self):
        Board.Nothing.reset()
        self._board = [Board.Nothing() for i in range(64)]
        self.eligible = set(range(64))
        self.pieceCount = 0

    def place(self, piece, pos):

        # first filter
        if not (pos in self.eligible):
            return False

        threatened = piece.threatenedFrom(pos)
        for threat in threatened:
            if isinstance(self._board[threat], Piece):
                return False

        for threatened in piece.threatenedFrom(pos):
            if threatened in self.eligible:
                self.eligible.remove(threatened)

            if isinstance(self._board[threatened], Board.Threatened):
                self._board[threatened].inc()
            elif isinstance(self._board[threatened], Board.Nothing):
                self._board[threatened] = Board.Threatened()

        self.eligible.remove(pos)
        self._board[pos] = piece
        self.pieceCount += 1
        
        return True

    def __repr__(self):

        string = ''
        for i in range(8):
            string += repr(self._board[i*8:i*8+8]) + '\n'

        return string
            

## 
# Pieces
## 
class Piece:
    
    """Abstract Class"""

    def onBoard(self, pos):
        return pos in set(range(64))

    def addAndSubtract(self, pos, numbers):
        targets = []
        for num in numbers:
            targets.append( pos - num )
            targets.append( pos + num )

        return targets

    def multiples(self, factor):
        return [mult * factor for mult in range(1, 8)]

    def threatenedFrom(self, pos):
        return set(filter(self.onBoard, self.moves(pos)))

    def __repr__(self):
        return self.name[:2]

class King(Piece):
    
    amount = 1

    def __init__(self):
        self.name = "King"

    def moves(self, pos):
        targets = set(self.addAndSubtract(pos, (1, 7, 8, 9)))
        return targets

class Queen(Piece):

    amount = 1

    def __init__(self):
        self.name = "Queen"

    def moves(self, pos):
        horizontals = self.addAndSubtract(pos, self.multiples(1))
        verticals = self.addAndSubtract(pos, self.multiples(8))
        diagonals = self.addAndSubtract(pos, self.multiples(7))
        diagonals.extend(self.addAndSubtract(pos, self.multiples(9)))

        horizontals = [p for p in horizontals if (p / 8) == (pos / 8)]

        targets = horizontals
        targets.extend(verticals)
        targets.extend(diagonals)
        return set(targets)
        
class Rook(Piece):
    
    amount = 2

    def __init__(self):
        self.name = "Rook"

    def moves(self, pos):
        horizontals = self.addAndSubtract(pos, self.multiples(1))
        verticals = self.addAndSubtract(pos, self.multiples(8))

        targets = filter(lambda num: (num / 8) == (pos / 8), horizontals)
        targets.extend(verticals)
        return set(targets)


class Bishop(Piece):

    amount = 2

    def __init__(self):
        self.name = "Bishop"

    def moves(self, pos):
        targets = self.addAndSubtract(pos, self.multiples(7))
        targets.extend(self.addAndSubtract(pos, self.multiples(9)))
        
        return set(targets)


class Knight(Piece):

    amount = 2

    def __init__(self):
        self.name = "Knight"
        
    def moves(self, pos):
        return set(self.addAndSubtract(pos, (6, 10, 15, 17)))


class Pawn(Piece):
    amount = 8

    def __init__(self):
        self.name = "Pawn"
    
    def moves(self, pos):
        return set([pos - 7, pos - 9])


from random import randint
        
if __name__ == "__main__":

    # get pieces
    def getPieces():
        pieces = []
        pieceTypes = [ Queen, Rook, Bishop, Knight, King, Pawn ]
        for pieceType in pieceTypes:
            for count in range(pieceType.amount):
                pieces.append(pieceType())
        return pieces
    # 
    def guess():
        pieces = getPieces()
        board = Board()
        
        while len(pieces) > 0 and len(board.eligible) > 0:
            # choice a position
            pos = choice(board.eligible)
            piece = pieces.pop(0)
            
            if not board.place(piece, pos):
                return False, board
        
        return board.pieceCount == 16, board
            
    def choice(iterable):
        target = randint(0, len(iterable)-1)
        count = 0
        for item in iterable:
            count += 1
            if count is target:
                return item
    
    pieceCountCount = dict([[count, 0] for count in range(16 + 1)])
    try:
        count = 0
        while True:
            success, board = guess()
            if success:
                pieceCountCount[board.pieceCount] += 1
                print board
                raise Peace
            else:
                pieceCountCount[board.pieceCount] += 1
                if board.pieceCount > 13:
                    print board
                #print 'Fail. Piece Count: %s' % board.pieceCount
            
            count += 1
            if count % 100 == 0:
                print pieceCountCount
    finally:
        print pieceCountCount
