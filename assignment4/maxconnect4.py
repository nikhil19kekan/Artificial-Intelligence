#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Dr. Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

import sys
from MaxConnect4Game import	 *

def oneMoveGame(currentGame):
    if currentGame.pieceCount == 42:    # Is the board full already?
        print 'BOARD FULL\n\nGame Over!\n'
        sys.exit(0)

    currentGame.aiPlay() # Make a move (only random is implemented)

    print 'Game state after move:\n'
    currentGame.printGameBoard()

    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    currentGame.printGameBoardToFile()
    currentGame.gameFile.close()


def interactiveGame(currentGame,move):
    # Fill me in
	computerIndicator=0
	humanIndicator=0
	if(move=='computer-next'):
		computerIndicator=currentGame.currentTurn
	else:
		humanIndicator=currentGame.currentTurn
	while(currentGame.pieceCount!=42):
		print('Current move of:%s\n'%move)
		if(move=='computer-next'):
			try:
				currentGame.gameFile=open('computer.txt','w')
				oneMoveGame(currentGame)
			except:
				print('error while opening file computer.txt in write mode')
				sys.exit(0)
			move='human-next'
		if(move=='human-next'):
			col=input('Enter column number to put coin in:')
			while(currentGame.gameBoard[0][col-1]!=0):
				col=input('Column full,make another move:')
			currentGame.playPiece(col-1)
			print('\n\nmove %d: Player %d, column %d\n' % (currentGame.pieceCount, currentGame.currentTurn, col))
			currentGame.printGameBoard()
			currentGame.countScore()
			print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
			try:
				currentGame.gameFile=open('human.txt','w')
			except:
				print('error in opening file human.txt in write mode')
				sys.exit(0)
			currentGame.printGameBoardToFile()
			if currentGame.currentTurn==1:
				currentGame.currentTurn=2
			else:
				currentGame.currentTurn=1
			move='computer-next'
	if(currentGame.player1Score>currentGame.player2Score):
		if(computerIndicator==1):
			print('Computer Win')
		else:
			print('You Win')
	if(currentGame.player1Score<currentGame.player2Score):
		if(computerIndicator==2):
			print('Computer Win')
		else:
			print('You Win')
	sys.exit(0)
def main(argv):
    # Make sure we have enough command-line arguments
    if len(argv) != 5:
        print 'Four command-line arguments are needed:'
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)

    game_mode, inFile = argv[1:3]

    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)

    currentGame = maxConnect4Game() # Create a game
    currentGame.depth=int(argv[-1])
    # Try to open the input file
    try:
        currentGame.gameFile = open(inFile, 'r')
    except IOError:
        sys.exit("\nError opening input file.\nCheck file name.\n")

    # Read the initial game state from the file and save in a 2D list
    file_lines = currentGame.gameFile.readlines()
    currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
    currentGame.currentTurn = int(file_lines[-1][0])
    currentGame.gameFile.close()

    print '\nMaxConnect-4 game\n'
    print 'Game state before move:'
    currentGame.printGameBoard()

    # Update a few game variables based on initial state and print the score
    currentGame.checkPieceCount()
    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    if game_mode == 'interactive':
		interactiveGame(currentGame,argv[-2]) # Be sure to pass whatever else you need from the command line
    else: # game_mode == 'one-move'
        # Set up the output file
        outFile = argv[3]
        try:
            currentGame.gameFile = open(outFile, 'w')
        except:
            sys.exit('Error opening output file.')
        oneMoveGame(currentGame) # Be sure to pass any other arguments from the command line you might need.


if __name__ == '__main__':
    main(sys.argv)




