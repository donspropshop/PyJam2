
import sys
import random
import qdarkstyle
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox

from PyTacToeGameUi import Ui_PyTacToeGame

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.gameState = "initializing"

        self.setupUi()
        self.setupGame()

    def setupUi(self):
        self.ui = Ui_PyTacToeGame()
        self.ui.setupUi(self)

        self.ui.gameStartStopButton.clicked.connect(self.startStopGame)
        self.ui.playerSwap.clicked.connect(self.swapPlayers)
        self.ui.enemySelect.currentIndexChanged.connect(self.setEnemyLevel)

        self.game_squares = [
            self.ui.gameSquare00,
            self.ui.gameSquare01,
            self.ui.gameSquare02,

            self.ui.gameSquare10,
            self.ui.gameSquare11,
            self.ui.gameSquare12,

            self.ui.gameSquare20,
            self.ui.gameSquare21,
            self.ui.gameSquare22
        ]

        for gameSquare in self.game_squares:
            gameSquare.clicked.connect(self.gameSquareClicked)


    def alertMessage(self, statusText):
        messageBox = QMessageBox()
        messageBox.setText(statusText)
        messageBox.exec()


    def setupGame(self):
        self.setEnemyLevel(self.ui.enemySelect.currentIndex())
        self.playerToken = "X"
        self.enemyToken = "O"
        self.gameState = "ready"


    def startStopGame(self):
        if self.gameState == "ready":
            self.startGame()
            self.ui.gameStartStopButton.setText("End")
            self.gameState = "playing"

        elif self.gameState == "playing":
            self.playerLoses()


    def startGame(self):
        for gameSquare in self.game_squares:
            gameSquare.setText("")
            gameSquare.setEnabled(True)

        self.ui.enemySelect.setEnabled(False)
        self.ui.playerSwap.setEnabled(False)

        if self.enemyToken == "X":
            self.enemyPlay()


    def stopGame(self):
        for gameSquare in self.game_squares:
            gameSquare.setEnabled(False)

        self.ui.enemySelect.setEnabled(True)
        self.ui.playerSwap.setEnabled(True)

        self.ui.gameStartStopButton.setText("Start")
        self.gameState = "ready"


    def gameSquareClicked(self):
        gameSquare = self.sender()

        if gameSquare.text() == "":
            gameSquare.setText(self.playerToken)
            gameSquare.setEnabled(False)

            if self.checkForWin(self.playerToken):
                self.playerWins()
            elif self.checkForTie():
                self.gameTied()
            else:
                self.enemyPlay()


    def playerWins(self):
        self.alertMessage("You Win!")
        self.stopGame()


    def playerLoses(self):
        self.alertMessage("You Lose!")
        self.stopGame()


    def gameTied(self):
        self.alertMessage("It's A Tie!")
        self.stopGame()


    def swapPlayers(self):
        if self.playerToken == "X":
            self.playerToken = "O"
            self.enemyToken = "X"
            self.ui.playerOneNameLabel.setGeometry(300, 480, 150, 60)
            self.ui.enemySelect.setGeometry(30, 480, 150, 60)

        else:
            self.playerToken = "X"
            self.enemyToken = "O"
            self.ui.playerOneNameLabel.setGeometry(30, 480, 150, 60)
            self.ui.enemySelect.setGeometry(300, 480, 150, 60)


    def setEnemyLevel(self, enemyIndex):
        enemyPlayers = [self.easyEnemyPlay, self.mediumEnemyPlay, self.hardEnemyPlay]
        self.enemyPlay = enemyPlayers[enemyIndex]


    def easyEnemyPlay(self):
        openSquares = list(filter(lambda square: square.text() == "", self.game_squares))
        chosenSquare = random.choice(openSquares)

        self.gameSquareEnemyClicked(chosenSquare)


    def mediumEnemyPlay(self):
        openSquares = list(filter(lambda square: square.text() == "", self.game_squares))
        chosenSquare = random.choice(openSquares)

        enemyWinningMoves = self.getWinningMoves(self.enemyToken)

        if len(enemyWinningMoves) > 0:
            chosenSquare = enemyWinningMoves[0]

        self.gameSquareEnemyClicked(chosenSquare)


    def hardEnemyPlay(self):
        openSquares = list(filter(lambda square: square.text() == "", self.game_squares))
        chosenSquare = random.choice(openSquares)

        enemyWinningMoves = self.getWinningMoves(self.enemyToken)
        playerWinningMoves = self.getWinningMoves(self.playerToken)

        if len(enemyWinningMoves) > 0:
            chosenSquare = enemyWinningMoves[0]
        elif len(playerWinningMoves) > 0:
            chosenSquare = playerWinningMoves[0]

        self.gameSquareEnemyClicked(chosenSquare)


    def gameSquareEnemyClicked(self, gameSquare):
        if gameSquare.text() == "":
            gameSquare.setText(self.enemyToken)
            gameSquare.setEnabled(False)

            if self.checkForWin(self.enemyToken):
                self.playerLoses()
            elif self.checkForTie():
                self.gameTied()
    

    def checkForTie(self):
        openSquares = list(filter(lambda square: square.text() == "", self.game_squares))

        return len(openSquares) == 0


    def checkForWin(self, token):
        isWin = (self.ui.gameSquare00.text() == token and self.ui.gameSquare01.text() == token and self.ui.gameSquare02.text() == token
        ) or (self.ui.gameSquare10.text() == token and self.ui.gameSquare11.text() == token and self.ui.gameSquare12.text() == token
        ) or (self.ui.gameSquare20.text() == token and self.ui.gameSquare21.text() == token and self.ui.gameSquare22.text() == token
        ) or (self.ui.gameSquare00.text() == token and self.ui.gameSquare10.text() == token and self.ui.gameSquare20.text() == token
        ) or (self.ui.gameSquare01.text() == token and self.ui.gameSquare11.text() == token and self.ui.gameSquare21.text() == token
        ) or (self.ui.gameSquare02.text() == token and self.ui.gameSquare12.text() == token and self.ui.gameSquare22.text() == token
        ) or (self.ui.gameSquare00.text() == token and self.ui.gameSquare11.text() == token and self.ui.gameSquare22.text() == token
        ) or (self.ui.gameSquare02.text() == token and self.ui.gameSquare11.text() == token and self.ui.gameSquare20.text() == token)

        return isWin


    def getWinningMoves(self, token):
        winningMoves = []

        winningMoves.append(self.getWinningMove(token, [self.ui.gameSquare00, self.ui.gameSquare01, self.ui.gameSquare02]))
        winningMoves.append(self.getWinningMove(token, [self.ui.gameSquare10, self.ui.gameSquare11, self.ui.gameSquare12]))
        winningMoves.append(self.getWinningMove(token, [self.ui.gameSquare20, self.ui.gameSquare21, self.ui.gameSquare22]))
        winningMoves.append(self.getWinningMove(token, [self.ui.gameSquare00, self.ui.gameSquare10, self.ui.gameSquare20]))
        winningMoves.append(self.getWinningMove(token, [self.ui.gameSquare01, self.ui.gameSquare11, self.ui.gameSquare21]))
        winningMoves.append(self.getWinningMove(token, [self.ui.gameSquare02, self.ui.gameSquare12, self.ui.gameSquare22]))
        winningMoves.append(self.getWinningMove(token, [self.ui.gameSquare00, self.ui.gameSquare11, self.ui.gameSquare22]))
        winningMoves.append(self.getWinningMove(token, [self.ui.gameSquare02, self.ui.gameSquare11, self.ui.gameSquare20]))

        winningMoves = list(filter(lambda square: square is not None, winningMoves))

        return winningMoves


    def getWinningMove(self, token, squares):
        winningMove = None
        pattern = ""

        for square in squares:
            pattern += square.text()

        if pattern == token + token:
            winningMove = list(filter(lambda square: square.text() == "", squares))[0]

        return winningMove


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())

    window.show()

    sys.exit(app.exec_())