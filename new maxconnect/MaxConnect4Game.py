#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

from copy import copy,deepcopy
import random
import sys

class maxConnect4Game:
    def __init__(self):
        self.gameBoard = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn = 1
        self.player1Score = 0
        self.player2Score = 0
        self.pieceCount = 0
        self.gameFile = None
	self.playerName = 1
	self.alpha =  float('-inf')
	self.beta = float('inf')

    # Count the number of pieces already played
    def checkPieceCount(self):
        self.pieceCount = sum(1 for row in self.gameBoard for piece in row if piece)

    # print game board
    def printGameBoard(self):
        print ' -----------------'
        for i in range(6):
            print ' |',
            for j in range(7):
                print('%d' % self.gameBoard[i][j]),
            print '| '
        print ' -----------------'
	
    # Output current game status to file
    def printGameBoardToFile(self):
        for row in self.gameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r\n')
        self.gameFile.write('%s\r\n' % str(self.currentTurn))

    # Place the current player's piece in the requested column
    def playPiece(self, column):
        if not self.gameBoard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameBoard[i][column]:
                    self.gameBoard[i][column] = self.currentTurn
                    self.pieceCount += 1
                    return 1
    #Change player turn.
    def chagePlayerTurn(self):	
	if self.currentTurn == 1:
		self.currentTurn = 2
	else:
		self.currentTurn = 1

    # The AI section. Currently plays randomly.
    def aiPlay(self, depth, game_mode):
		minmax_state = self.miniMax(depth)
		self.gameBoard = deepcopy(minmax_state.gameBoard)
		self.chagePlayerTurn()
		if game_mode == 'interactive':
			self.gameFile = open('computer.txt', 'w')
			self.printGameBoardToFile()
			self.gameFile.close()

    #Check if the next move is valid or not.
    def ValidMove(self, column):
	move = maxConnect4Game()
	move.gameBoard = deepcopy(self.gameBoard)
	move.currentTurn = deepcopy(self.currentTurn)
	move.playerName =  deepcopy(self.playerName)
	result = move.playPiece(column)
	if result:			
		move.chagePlayerTurn()
		move.checkPieceCount()
		move.countScore()
		return move

    #return utility value for terminal state
    def terminal_test(self):
	if self.pieceCount == 42:
		if (self.playerName == 1) and (self.player1Score > self.player2Score):
			return 1
		elif (self.playerName == 1) and (self.player1Score < self.player2Score):
			return -1
		elif (self.playerName == 2) and (self.player1Score < self.player2Score):
			return 1
		elif(self.playerName == 2) and (self.player1Score > self.player2Score):
			return -1
		else:
			return 0
	else:
		return 2

    #Simple MiniMax algorithm
    def miniMax(self, depthl):
		valid_next_move = self
		self.checkPieceCount()
		if not self.gameBoard[5][3]:
			valid_next_move = self.ValidMove(3)
			return valid_next_move
		elif not self.gameBoard[5][2]:
			valid_next_move = self.ValidMove(2)
			return valid_next_move
		elif not self.gameBoard[5][4]:
			valid_next_move = self.ValidMove(4)
			return valid_next_move

		utility = float('-inf')
		for column in range(7):
			next_move = self.ValidMove(column)
			if not next_move:
				continue
			current_utility = next_move.minValue(1, depthl)
			if current_utility  > utility:
				utility =  current_utility
				self.alpha = max(self.alpha, utility)
				valid_next_move = deepcopy(next_move)
		return valid_next_move

    #Return the minimum value for given state
    def minValue(self, depth, depthl):
		utility = self.terminal_test() 
		if utility < 2:
			return utility
		if depth == depthl:
			return self.evaluation()

		utility = float('inf')
		for column in range(7):
			next_move = self.ValidMove(column)
			if not next_move:
				continue
			current_utility = next_move.maxValue(depth + 1, depthl)
			if current_utility  < utility:
				#print 'In MinValue utility update code'
				utility =  current_utility
			if utility <= self.alpha:
				return utility
			self.beta = min(self.beta, utility)
		return utility

    #Return the maximum value for given state
    def maxValue(self, depth, depthl):
		utility = self.terminal_test() 
		if utility < 2:
			return utility
		if depth == depthl:
					return self.evaluation()

		utility = float('-inf')
		for column in range(7):
			next_move = self.ValidMove(column)
			if not next_move:
				continue
			current_utility = next_move.minValue(depth + 1, depthl)
			if current_utility  > utility:
				utility =  current_utility
			if utility >= self.beta:
				return utility
			self.alpha = max(self.alpha, utility)
		return utility

    #Heuristic function
    def evaluation(self):
		own = 0
		opponent = 0
		own4Count = 0
		own3Count = 0
		own2Count = 0
		opponent4Count = 0
		opponent3Count = 0
		opponent2Count = 0

		self.countScore()
		if self.playerName == 1:
			own = 1
			opponent = 2
			own4Count = self.player1Score
			opponent4Count = self.player2Score
		else:
			own = 2
			opponent = 1
			own4Count = self.player2Score
					opponent4Count = self.player1Score

		own3Count = self.checkForStreak(own, 3)
		own2Count = self.checkForStreak(own, 2)

		opponent3Count = self.checkForStreak(opponent, 3)
		opponent2Count = self.checkForStreak(opponent, 2)
		
		ownValue = (own4Count * 1.1)+(own3Count * 0.7) + (own2Count * 0.3)
		opponentValue = (opponent4Count * 1.1)+(opponent3Count * 0.7) + (opponent2Count * 0.3)
		return (ownValue - opponentValue)

    def checkForStreak(self, player, streak):
		count = 0
		for i in range(6):
				for j in range(7):
						count += self.diagonalCheck(i, j, player, streak)

		count += self.verticalStreak(player, streak)
		count += self.horizontalStreak( player, streak)
			return count

    def verticalStreak(self,  player, streak):
		consecutiveCount = 0
        for j in range(7):
		if streak == 3:
	        	if (self.gameBoard[0][j] == player and self.gameBoard[1][j] == player and
        	        	self.gameBoard[2][j] == player):
				consecutiveCount += 1
	            	if (self.gameBoard[1][j] == player and self.gameBoard[2][j] == player and
        	        	self.gameBoard[3][j] == player):
                		consecutiveCount += 1
	            	if (self.gameBoard[2][j] == player and self.gameBoard[3][j] == player and
        	           	self.gameBoard[4][j] == player):
                		consecutiveCount += 1
			if (self.gameBoard[3][j] == player and self.gameBoard[4][j] == player and
                                self.gameBoard[5][j] == player):
                                consecutiveCount += 1
		elif streak == 2:
			if (self.gameBoard[0][j] == player and self.gameBoard[1][j] == player):
                                consecutiveCount += 1
                        if (self.gameBoard[1][j] == player and self.gameBoard[2][j] == player):
                                consecutiveCount += 1
                        if (self.gameBoard[2][j] == player and self.gameBoard[3][j] == player):
                                consecutiveCount += 1
                        if (self.gameBoard[3][j] == player and self.gameBoard[4][j] == player):
                                consecutiveCount += 1
			if (self.gameBoard[4][j] == player and self.gameBoard[5][j] == player):
                                consecutiveCount += 1
		return consecutiveCount

    def horizontalStreak(self, player, streak):
		consecutiveCount = 0	
		for row in self.gameBoard:
			if streak == 3:
						if row[0:3] == [player]*3:
							consecutiveCount += 1
						if row[1:4] == [player]*3:
							consecutiveCount += 1
						if row[2:5] == [player]*3:
							consecutiveCount += 1
						if row[3:6] == [player]*3:
							consecutiveCount += 1
				if row[4:7] == [player]*3:
									consecutiveCount += 1
			elif streak == 2:
				if row[0:2] == [player]*2:
									consecutiveCount += 1
							if row[1:3] == [player]*2:
									consecutiveCount += 1
							if row[2:4] == [player]*2:
									consecutiveCount += 1
							if row[3:5] == [player]*2:
									consecutiveCount += 1
							if row[4:6] == [player]*2:
									consecutiveCount += 1
				if row[5:7] == [player]*2:
									consecutiveCount += 1
		return consecutiveCount

    def diagonalCheck(self, row, col, player, streak):
        #Check for diagonals with positive slope
		total = 0
        consecutiveCount = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif self.gameBoard[i][j] == player and self.gameBoard[row][col] == player:
                consecutiveCount += 1
            else:
                break
            j += 1
        
		if consecutiveCount >= streak:
            total += 1
        
		# check for diagonals with negative slope
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif self.gameBoard[i][j] == player and self.gameBoard[row][col] == player:
                consecutiveCount += 1
            else:
                break
            j += 1

        if consecutiveCount >= streak:
            total += 1

        return total	
    
	# Calculate the number of 4-in-a-row each player has
    def countScore(self):
        self.player1Score = 0;
        self.player2Score = 0;

        # Check horizontally
        for row in self.gameBoard:
            # Check player 1
            if row[0:4] == [1]*4:
                self.player1Score += 1
            if row[1:5] == [1]*4:
                self.player1Score += 1
            if row[2:6] == [1]*4:
                self.player1Score += 1
            if row[3:7] == [1]*4:
                self.player1Score += 1
            # Check player 2
            if row[0:4] == [2]*4:
                self.player2Score += 1
            if row[1:5] == [2]*4:
                self.player2Score += 1
            if row[2:6] == [2]*4:
                self.player2Score += 1
            if row[3:7] == [2]*4:
                self.player2Score += 1

        # Check vertically
        for j in range(7):
            # Check player 1
            if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                   self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                   self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                   self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                self.player1Score += 1
            # Check player 2
            if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                   self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                   self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                   self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                self.player2Score += 1

        # Check diagonally
			# Check player 1
        if (self.gameBoard[2][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][0] == 1 and self.gameBoard[1][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][1] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][5] == 1 and self.gameBoard[5][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][2] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[4][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[3][6] == 1):
            self.player1Score += 1

        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[3][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][4] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[4][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][5] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][1] == 1 and self.gameBoard[5][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][6] == 1 and self.gameBoard[1][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][6] == 1 and self.gameBoard[2][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1

			# Check player 2
        if (self.gameBoard[2][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][0] == 2 and self.gameBoard[1][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][1] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][1] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][5] == 2 and self.gameBoard[5][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][2] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][5] == 2):
            self.player2Score += 1	
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[4][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[3][6] == 2):
            self.player2Score += 1

        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[3][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][4] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[4][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][5] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][1] == 2 and self.gameBoard[5][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][6] == 2 and self.gameBoard[1][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][6] == 2 and self.gameBoard[2][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1
