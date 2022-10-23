# *********************************************************************** #
#                                                                         #
# OBJECTIVE : MAP UAV                     ####       ###    ###    #      #
# AUTHOR :  VICTOR DALET                  #         #      #       #      #
# CREATED : 23 09 2022                    ####      #      #  ##   #      #
# UPDATE  : 23 10 2022                    #         #      #   #   #      #
#                                         ####    ###      #####   #.fr   #
# *********************************************************************** #

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


def main():
	matrix = [
	  [1, 1, 1, 1, 1, 1],
	  [1, 0, 1, 1, 1, 1],
	  [1, 1, 1, 1, 1, 1]]

	grid = Grid(matrix=matrix)

	start = grid.node(0, 0)
	end = grid.node(5, 2)

	finder = AStarFinder(diagonal_movement = DiagonalMovement.always) 

	path, runs = finder.find_path(start, end, grid)



	print(path)

main()