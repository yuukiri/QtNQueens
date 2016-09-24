from PyQt5.QtWidgets import QGraphicsView, QGraphicsItem, QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QFont, QPixmap
from PyQt5.QtCore import QRect, QRectF, QPoint, Qt
from PyQt5.QtSvg import QSvgRenderer
import sys
import os
from Chessboard import Ui_MainWindow
from SolveNQueens import NQueens

class Chessboard(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Chessboard, self).__init__()
        self.setupUi(self)
        self._pieces = self.__createPieces()
        self._boardOrigin = QPoint(20, 10)
        self._boardMargin = 20
        self._boardSize = 600 # length of the board
        self._nLen = 8 # number of squares in the board in each row/col
        self._solver = NQueens() # the n-queen solver
        self.queens = [] # solutions for n-queen
        self._board = [] # a specific solution, the board positions
        self.spinBox.valueChanged.connect(self.getNQueens)
        # set the limit for spinBox
        self.spinBox.setMaximum(self._nLen)
        self.spinBox.setMinimum(0)
        self.spinBox_2.valueChanged.connect(self.displayNQueens)

    def __createPieces(self):
        path = "pieces"
        pieces = {}
        markers = "ld"
        #upper case for dark, lower for light
        for symbol in "KQRBNPkqrbnp":
            marker = markers[symbol.isupper()]
            filename = os.path.join(path, "Chess_{symbol}{marker}t45.svg")
            renderer = QSvgRenderer(filename.format(symbol=symbol.lower(), marker=marker))
            pieces[symbol] = renderer
        return pieces

    def renderBoard(self, painter):
        """render chessboard, with no piece

        :param QPainter painter: the painter object to paint the board
        """
        lightColor = QColor(255, 250, 240) # floral white
        darkColor = QColor(51, 161, 201) # peacock

        lightBColor = QColor(0, 178, 238) # deepskyblue 2
        darkBColor = QColor(0, 104, 139) # deepskyblue 4
        edgeColor = QColor(0, 154, 205) # deepskyblue 3
        lightPen = QPen(QBrush(lightBColor), 3)
        darkPen = QPen(QBrush(darkBColor), 3)
        coordColor = QColor(191, 239, 255) # lightblue 1
        medPen = QPen(QBrush(coordColor), 1)
        x = self._boardMargin + self._boardOrigin.x()
        y = self._boardMargin + self._boardOrigin.y()
        start = QPoint(x, y)
        squareSize = self._boardSize/self._nLen

        #fill the whole board with
        size = self._boardSize + 2 * self._boardMargin
        x, y = self._boardOrigin.x(), self._boardOrigin.y()
        painter.fillRect(QRect(x, y, size, size), QBrush(edgeColor))
        # draw the frame boarder
        # determine the ends of the frame
        topLeft = self._boardOrigin
        topRight = QPoint(topLeft.x()+self._boardMargin*2+self._boardSize, topLeft.y())
        botLeft = QPoint(topLeft.x(), topLeft.y()+self._boardMargin*2+self._boardSize)
        botRight = QPoint(topRight.x(), botLeft.y())
        painter.setPen(lightPen)
        painter.drawLine(topLeft, topRight)
        painter.drawLine(topLeft, botLeft)
        painter.setPen(darkPen)
        painter.drawLine(topRight, botRight)
        painter.drawLine(botLeft, botRight)

        # positions for the squares
        squarePos = [[] for x in xrange(self._nLen)]

        # draw the square
        brushes = [QBrush(lightColor),QBrush(darkColor)]
        for i in xrange(self._nLen):
            for j in xrange(self._nLen):
                xPos = start.x() + i * squareSize
                yPos = start.y() + j * squareSize
                rect = QRect(xPos, yPos, squareSize, squareSize)
                squarePos[i].append(rect.topLeft()) # same as QPoint(xPos, yPos)
                painter.fillRect(rect, brushes[(i-j)%2])

        # draw boarder
        # determine the ends of the board
        topBLeft = QPoint(topLeft.x() + self._boardMargin, topLeft.y() + self._boardMargin)
        topBRight = QPoint(topRight.x() - self._boardMargin, topRight.y() + self._boardMargin)
        botBLeft = QPoint(botLeft.x() + self._boardMargin, botLeft.y() - self._boardMargin)
        botBRight = QPoint(topBRight.x(), botBLeft.y())
        painter.setPen(darkPen)
        painter.drawLine(topBLeft, topBRight)
        painter.drawLine(topBLeft, botBLeft)
        painter.setPen(lightPen)
        painter.drawLine(topBRight, botBRight)
        painter.drawLine(botBLeft, botBRight)

        # show coordinates
        # setup font properties
        font = QFont()
        font.setPixelSize(self._boardMargin * 0.5)
        painter.setFont(font)
        painter.setPen(medPen)

        for i, val in enumerate("87654321"):
            pos = QRect(topLeft.x(), topBLeft.y()+squareSize*i, self._boardMargin, squareSize).center()
            # save current painter position, so that it can translate
            painter.save()
            painter.translate(pos.x(), pos.y())
            painter.drawText(QRect(-self._boardMargin/2, -self._boardMargin/2, self._boardMargin, self._boardMargin), \
                             Qt.AlignCenter, val)
            # restore to previous location
            painter.restore()

        for i, val in enumerate("abcdefgh"):
            pos = QRect(botBLeft.x()+squareSize*i, botBLeft.y(), squareSize, self._boardMargin).center()
            # same as above
            painter.save()
            painter.translate(pos.x(), pos.y())
            painter.drawText(QRect(-self._boardMargin/2, -self._boardMargin/2, self._boardMargin, self._boardMargin), \
                             Qt.AlignCenter, val)
            painter.restore()
        #return squarePos
        self.squares = squarePos

    def paintEvent(self, event):
        """override the paintEvent func from QWidget

        :param QPaintEvent event: the region
        """
        painter = QPainter()
        painter.begin(self)
        self.renderBoard(painter)
        if self._board:
            nRow = len(self._board)
            nCol = len(self._board[0])
            for i in xrange(nRow):
                for j in xrange(nCol):
                    symbol = self._board[i][j]
                    if symbol=='.':
                        continue
                    self.placePiece(painter, symbol, i, j)
        painter.end()

    def placePiece(self, painter, symbol, row, col):
        """place a chess piece on the board

        :param QPainter painter: the QPainter object to render piece
        :param str symbol: symbol for chess piece, one of "KQRBNPkqrbnp"
        :param int row: row number of the piece in board
        :param int col: column number of the piece in board
        """
        pos = self.squares[row][col]
        piece = self._pieces[symbol]
        size = self._boardSize/self._nLen
        piece.render(painter, QRectF(pos.x(), pos.y(), size, size))

    def getNQueens(self):
        """set up the result once the value has been changed in spinBox"""
        self.repaint()
        n = self.spinBox.value()
        self.label.setText("calculating...")
        self.queens = self._solver.solveNQueens(n)
        self.label.setText("{nSol} solution(s) in total.".format(nSol=len(self.queens)))
        self.spinBox_2.setRange(0, 0) # reset the spinbox
        self.spinBox_2.setRange(0, len(self.queens))

    def displayNQueens(self):
        """display the queens once the comboBox has been updated"""
        index = self.spinBox_2.value()-1#self.comboBox.currentIndex()
        if -1 < index < len(self.queens):
            self._board = self.queens[index]
        else:
            self._board = []
        self.repaint()



def main():
    app = QApplication(sys.argv)
    cb = Chessboard()
    cb.show()
    cb.raise_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
