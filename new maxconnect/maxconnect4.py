#!/usr/bin/env python
# Written by Chris Conly based on C++
# code provided by Dr. Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

import sys
import os.path
from MaxConnect4Game import *

def oneMoveGame(currentGame, depthl, game_mode):
    if currentGame.pieceCount == 42:    # Is the board full already?
        print 'BOARD FULL\n\nGame Over!\n'
        sys.exit(0)

    currentGame.aiPlay(depthl, game_mode) # Make a move (only random is implemented)

    print 'Game state after move:'
    currentGame.printGameBoard()

    currentGame.countScore()
    print('Score: Player1 = %d, Player2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    currentGame.printGameBoardToFile()
    currentGame.gameFile.close()

def interactiveGame(currentGame, computer, human, depth, game_mode):
    while(True):
	if currentGame.pieceCount == 42:    # Is the board full already?
	        print 'BOARD FULL\n\nGame Over!\n'
		currentGame.countScore()
		print('Score: Player1 = %d, Player2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
        	sys.exit(0)
	elif currentGame.currentTurn == computer:
		print 'Computer turn is %d'%(currentGame.currentTurn)
		currentGame.aiPlay(depth, game_mode)
		currentGame.checkPieceCount()
                print 'Game state after Computer player move:'
                currentGame.printGameBoard()
                currentGame.countScore()
		print('Score: Player1 = %d, Player2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
	else:
		print 'Human turn is %d'%(currentGame.currentTurn)
                column = input("Please enter the column where you want to play: ")
                result = currentGame.playPiece(column - 1)
		while not result:
			print 'That was not a valid move. Try again.'
			column = input("Please enter valid column where you want to play: ")
                        result = currentGame.playPiece(column - 1)
		currentGame.chagePlayerTurn()
		currentGame.gameFile = open('human.txt', 'w')
		currentGame.printGameBoardToFile()
		currentGame.gameFile.close()
                currentGame.checkPieceCount()
		print 'Game state after Human player move:'
                currentGame.printGameBoard()
                currentGame.countScore()
                print('Score: Player1 = %d, Player2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

def main(argv):
    # Make sure we have enough command-line arguments
    if len(argv) != 5:
        print 'Four command-line arguments are needed:'
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)

    game_mode, inFile = argv[1:3]
    depth = int(argv[4])
    human = 0
    comp = 0
    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an invalid game mode' % game_mode)
        sys.exit(2)

    currentGame = maxConnect4Game() # Create a game
    
    #Game mode is Interactive and input file is given.
    if not inFile == '' and os.path.isfile(inFile):
    	# Try to open the input file
    	try:
        	currentGame.gameFile = open(inFile, 'r')
    	except IOError:
        	sys.exit("\nError opening input file.\nCheck file name.\n")

    	# Read the initial game state from the file and save in a 2D list
    	file_lines = currentGame.gameFile.readlines()
    	currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
    	currentGame.currentTurn = int(file_lines[-1][0])
    	currentGame.playerName = currentGame.currentTurn
    	currentGame.gameFile.close()
    elif game_mode == 'interactive' and (inFile == '' or os.path.isfile(inFile)):
	# Game mode is Interactive and input file is not given.
	if  argv[3] == 'computer-next':
		currentGame.currentTurn = 1
	else:
		currentGame.currentTurn = 1
    elif game_mode == 'one-move' and not os.path.isfile(inFile):
	sys.exit("File does not exists.\n")
	
    print '\nMaxConnect-4 game\n'
    print 'Game state before move:'
    currentGame.printGameBoard()

    # Update a few game variables based on initial state and print the score
    currentGame.checkPieceCount()
    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    # Identify Human and Computer player for Interactive mode.
    if game_mode == 'interactive':
	if  argv[3] == 'computer-next':
                comp = currentGame.currentTurn
		if comp  == 1:
			human = 2
		else:
			human = 1
	else:
		human = currentGame.currentTurn
		if human == 1:
			comp = 2
		else:
			comp = 1
	currentGame.playerName = comp
        interactiveGame(currentGame, comp, human, depth, game_mode) # Be sure to pass whatever else you need from the command line
    else: # game_mode == 'one-move'
        # Set up the output file
        outFile = argv[3]
        try:
            currentGame.gameFile = open(outFile, 'w')
        except:
            sys.exit('Error opening output file.')
        oneMoveGame(currentGame, depth, game_mode) # Be sure to pass any other arguments from the command line you might need.


if __name__ == '__main__':
    main(sys.argv)
