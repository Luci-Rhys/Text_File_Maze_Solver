# Calen Jones
# Dr. Nicholson
# Maze Solver (Assignment 1)
# CSCI 4560-19
# The objective of this maze solver program is to "read" a maze map from a file, find a path from the source to the exit,
# and display this map and newfound path to the console

#read_maze method takes file path for file breaks each line into individual, one-string characters for the maze
def read_maze(maze_file: str) -> list:
    maze = []
    with open(maze_file, "r") as file_data:
        for line in file_data:
            line = line.strip()
            maze.append([ch for ch in line]) #breaks the string into individual one-string characters
    return maze