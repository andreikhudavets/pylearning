#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tictactoe.py
#  
#  Copyright 2015 andrusik <andrusik@andrusik-dell>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import sys
import terminalsize
import getch

def print_game_help():
    print '''
Welcome to Tic-Tac-Toe (c) Andrei Khudavets, 2015
"Enter" or "Space" | "n"      | "e"       | Arrow Keys
make a move        | new game | Exit Game | Select cell
Note: you can only run this program in LINUX ONLY or in terminal that supports ANSI codes. 
    '''
def go_to_cell(game_matrix, x, y):
    '''
    Move cursor to specified position of game matrix
    Arguments:
        game_matrix
        x - x position in matrix
        y - y position in matrix
    Return: none
    '''
    sys.stdout.write("\033[{};{}H".format(game_matrix[y][y]['y'],game_matrix[x][x]['x']))
    sys.stdout.flush()

def reset_screen():
    '''
    Flush screen and move cursor to 0, 0
    Input: none
    Return: none
    '''
    sys.stdout.write("\033[2J")
    sys.stdout.write("\033[0;0H")
    sys.stdout.flush()
    
def print_game_field():
    '''
    Function prints game field.
    Arguments: none
    Return: 
        game_matrix - array with screen coordinates
    '''
    cols, rows = terminalsize.get_terminal_size()
    start_x = cols/2-5
    start_y = rows/2-5
    sys.stdout.write("\033[{}H".format(start_y))
    sys.stdout.write("\033[{}G   |   |   \n".format(start_x))
    sys.stdout.write("\033[{}G---+---+---\n".format(start_x))
    sys.stdout.write("\033[{}G   |   |   \n".format(start_x))
    sys.stdout.write("\033[{}G---+---+---\n".format(start_x))
    sys.stdout.write("\033[{}G   |   |   \n".format(start_x))
    sys.stdout.flush()
    
    game_matrix = []
    for x in range(3):
        game_matrix.append([])
        for y in range(3):
            game_matrix[x].append({'x':(start_x+1+x*4),'y':(start_y+y*2)})
    
    return game_matrix

def print_notification(text):
    '''
    Function prints notification about current game status.
    Input: 
        text - text string
    Return: none
    '''
    cols, rows = terminalsize.get_terminal_size()
    sys.stdout.write("\033[{};{}H".format(rows,0))
    sys.stdout.write(text)
    sys.stdout.flush()
    
def print_move(char):
	'''
	Funcation just prints player's move
	Input:
		char - what to print
	Output:
		none
	'''
	sys.stdout.write(char)
	sys.stdout.flush()
	
# -= LOGICAL FUNCTIONS =-
def find_empty_cell(game_matrix, x, y, x_shift, y_shift):
	'''
	Finds next available cell in game matrix
	Input:
		game_matrix
		x int
		y int
		x_shift int
		y_shift int
	Return:
		tuple (new_x, new_y)
	'''
	m_size = len(game_matrix)
	
	new_x = x+x_shift
	if new_x < 0:
		new_x = m_size-1
	elif new_x >= m_size:
		new_x =0
	new_y = y+y_shift
	if new_y < 0:
		new_y = m_size-1
	elif new_y >= m_size:
		new_y =0
	return (new_x, new_y)

def find_winner(game_matrix):
	'''
	Function checks if there is a win or draw situation on the board
	Input:
		game_matrix
	Output:
		winner sign
		or
		None if game can be continued
		or
		Draw if there is a draw
	'''
	m_size = len(game_matrix)
	
	def check_lines(game_matrix):
		'''
		Checks if nested list has all the same elements.
		Input:
			game_matrix
		Output:
			None - if elements are different
			Element - if all the same
		'''
		for x in range(m_size):
			if all( c.has_key('sign') and c['sign'] == game_matrix[x][0]['sign'] for c in game_matrix[x]):
				return game_matrix[x][0]['sign']		
		return None

	# Check vertical lines
	result = check_lines(game_matrix)
	if result != None:
		return result
		
	# Transpose matrix and check again 	
	result = check_lines(zip (*game_matrix))
	if result != None:
		return result
	
	# Check diagonals
	if all (game_matrix[i][i].has_key('sign') and game_matrix[i][i]['sign'] == game_matrix[0][0]['sign'] for i in range(m_size)):
		return game_matrix[0][0]['sign']

	if all (game_matrix[i][m_size-i-1].has_key('sign') and game_matrix[i][m_size-i-1]['sign'] == game_matrix[0][m_size-1]['sign'] for i in range(m_size)):
		return game_matrix[0][m_size-1]['sign']
	
	# Check if threre is a draw
	signs_count = 0
	for i in range(m_size):
		for j in range(m_size):
			if game_matrix[i][j].has_key('sign'):
				signs_count+=1
				
	if signs_count == m_size**2:
		return "Draw"
		
	return None
	

# CONSTANTS
CONST_COMMAND_EXIT = 0
CONST_COMMAND_START = 1
CONST_COMMAND_NEW_GAME = 2
CONST_COMMAND_WIN = 3
CONST_COMMAND_DRAW = 4

def main():
	game_matrix = []
	game_command = CONST_COMMAND_START

	players = [{'name':'First Player', 'sign':'x'},{'name':'Second Player', 'sign':'0'}]

	pos_x = 1
	pos_y = 1
	player = 0
	while (game_command != CONST_COMMAND_EXIT):
		# Reset game field in the beginning of the game
		if game_command == CONST_COMMAND_START or game_command == CONST_COMMAND_NEW_GAME:
			reset_screen()
			print_game_help()
			game_matrix = print_game_field()
			game_command = None
			
		# Print notification about next move
		if game_command != CONST_COMMAND_DRAW and game_command != CONST_COMMAND_WIN:
			print_notification("{} ({}), please make a move.".format(players[player]['name'], players[player]['sign']))

		# Position cursor inside the game field
		go_to_cell(game_matrix, pos_x, pos_y)

		# Capture user input
		key_pressed = ord(getch.getch())

		# Decide what to do next
		if key_pressed == 65:   # Go up
			pos_x, pos_y = find_empty_cell(game_matrix, pos_x, pos_y, 0, -1)
		elif key_pressed == 67: # Go right
			pos_x, pos_y = find_empty_cell(game_matrix, pos_x, pos_y, 1, 0)
		elif key_pressed == 66: # Go down
			pos_x, pos_y = find_empty_cell(game_matrix, pos_x, pos_y, 0, 1)
		elif key_pressed == 68: # Go left
			pos_x, pos_y = find_empty_cell(game_matrix, pos_x, pos_y, -1, 0)
		elif key_pressed == 101: # Exit game
			game_command = CONST_COMMAND_EXIT
		elif key_pressed == 110: # New game
			game_command = CONST_COMMAND_NEW_GAME
		elif key_pressed == 32 or key_pressed == 13: # Make a move
			if not game_matrix[pos_x][pos_y].has_key('sign') and not (game_command == CONST_COMMAND_WIN or game_command == CONST_COMMAND_WIN):
				game_matrix[pos_x][pos_y]['sign'] = players[player]['sign']
				print_move(players[player]['sign'])
				winner = find_winner(game_matrix)
				if winner == players[player]['sign']:
					print_notification("{}, Congratulations, you win!".format(players[player]['name']))
					game_command = CONST_COMMAND_WIN
				elif winner == "Draw":
					print_notification("There is a draw, guys! Please try again.")
					game_command = CONST_COMMAND_DRAW	
				else:
					player = 0 if player==1 else 1

		
	reset_screen()
	return 0

if __name__ == '__main__':
	main()

