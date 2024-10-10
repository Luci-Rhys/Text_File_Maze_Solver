# Calen Jones
# Dr. Nicholson
# Maze Solver (Assignment 1)
# CSCI 4560-19 (Robotics I)
#
# The objective of this program is to solve a maze by finding a path from a robot's initial position to the exit of the
# maze, which the robot will find by following the rightmost wall of the maze. Once a path is found, the program prints
# the maze with the newfound path solution, along with the source and exit coordinates, the printed path between the

#read_maze method takes file path for file breaks each line into individual, one-string characters for the maze
def read_maze() -> list:
    file_found = False #flag to break loop requesting file name
    maze = [] #empty maze

    #loops until user enters an existing text file name
    while not file_found:
        maze_file = input(f"Enter the name (without .txt) of the maze text file: ") + ".txt"
        print("")

        try:
            with open(maze_file, "r") as file_data:
                for line in file_data:
                    line = line.strip()
                    maze.append([ch for ch in line]) #breaks the string into individual one-string characters
            file_found = True
        #Exception if filename entered does not exist
        except FileNotFoundError:
            print(f"You gotta give it a file that exists. Your file: {maze_file} does not do that."
                  f" That's okay. Let's try again! \n")
    return maze

#takes a maze as a parameter and prints it in a pretty manner
def pretty_print_maze(maze):
    for row in maze:
        print(" ".join(row))

#Function prints maze with path solution, steps designated by *
def generate_path(maze: list, path: list, source: tuple, end: tuple):
    #Adds * to tuples in path
    for node in path:
        if node != source and node != end:
            maze[node[0]][node[1]] = "*"
    pretty_print_maze(maze)

#Function changes wall orientation to true for wall facing the robot and changes remaining orientations to false
def change_orientation(wall_orientation, new_orientation):
    for o in wall_orientation:
        if o == new_orientation:
            wall_orientation[o] = True
        else:
            wall_orientation[o] = False


'''
Function solves maze by moving the robot one step, either up, down, left, or right one step depending on where the right
wall of the maze is facing the robot.
'''
def solve(maze : list):
    previous : dict = {} #Dict holds the previous coordinates from each step
    source = None #Tuple to hold robot's initial position once found
    end = None #Tuple to hold exit/robot's final position once found
    steps = 0 #Tracks total number of steps robot takes to find the exit
    path = [] #List of tuples of holding path from source to end
    num_of_rows = len(maze) #Number of rows in maze

    #Dictionary of booleans to keep track of the wall's position in relation to the robot
    wall_orientation = {
        "north_of_r" : False,
        "east_of_r" : False,
        "south_of_r" :False,
        "west_of_r" : False,
    }

    #Finds initial position (source) of robot
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == "R":
                source = (row, col)

    #Assigns current row and column of robot to variables and adds to path list
    curr_row, curr_col = source
    path.append((curr_row, curr_col))

    #Robot moves as right as possible to reach an east wall
    while maze[curr_row][curr_col + 1] != "#":
        curr_col += 1
        previous[(curr_row,curr_col)] = (curr_row, curr_col - 1)
        path.append((curr_row, curr_col))
        steps += 1

    #Updates east wall orientation to True since wall is now to the right of the robot.
    wall_orientation["east_of_r"] = True

    #Loop continues until robot occupies the same position as E
    while maze[curr_row][curr_col] != "E":

        #Conditions for if the robot was/is next to the east-oriented wall in the previous or current step
        if wall_orientation["east_of_r"]:
            #Robot is currently next to east-oriented wall
            if maze[curr_row][curr_col + 1] == "#":
                #Next step is not a wall and robot will move up a step
                if maze[curr_row - 1][curr_col] != "#":
                    curr_row -= 1
                    previous[(curr_row,curr_col)] = (curr_row + 1, curr_col)
                #Robot is in a north-east corner, robot will move left, wall orientation changed to north of robot
                elif maze[curr_row -1][curr_col] == "#":
                    curr_col -= 1
                    previous[(curr_row, curr_col)] = (curr_row, curr_col + 1)
                    change_orientation(wall_orientation, "north_of_r")
            #Wall has turned corner to the right, robot will move right, wall orientation changed to south of robot
            elif maze[curr_row][curr_col + 1] != "#":
                curr_col += 1
                previous[(curr_row, curr_col)] = (curr_row, curr_col - 1)
                change_orientation(wall_orientation, "south_of_r")

        # Conditions for if the robot was/is next to the south-oriented wall in the previous or current step
        elif wall_orientation["south_of_r"]:
            # Robot is currently next to south-oriented wall
            if maze[curr_row + 1][curr_col] == "#":
                # Next step is not a wall and robot will move right a step
                if maze[curr_row][curr_col + 1] != "#":
                    curr_col += 1
                    previous[(curr_row, curr_col)] = (curr_row, curr_col - 1)
                # Robot is in a south-east corner, robot will move up, wall orientation changed to east of robot
                elif maze[curr_row][curr_col + 1] == "#":
                    curr_row -= 1
                    previous[(curr_row, curr_col)] = (curr_row + 1, curr_col)
                    change_orientation(wall_orientation, "east_of_r")
            # Wall has turned corner going down, robot will move down, wall orientation changed to west of robot
            elif maze[curr_row + 1][curr_col] != "#":
                curr_row += 1
                previous[(curr_row, curr_col)] = (curr_row - 1, curr_col)
                change_orientation(wall_orientation, "west_of_r")

        # Conditions for if the robot was/is next to the west-oriented wall in the previous or current step
        elif wall_orientation["west_of_r"]:
            # Robot is currently next to west-oriented wall
            if maze[curr_row][curr_col - 1] == "#":
                # Next step is not a wall and robot will move down a step
                if maze[curr_row + 1][curr_col] != "#":
                    curr_row += 1
                    previous[(curr_row, curr_col)] = (curr_row - 1, curr_col)
                # Robot is in a west-south corner, robot will move right, wall orientation changed to south of robot
                elif maze[curr_row + 1][curr_col] == "#" and curr_row + 1 <= num_of_rows - 1:
                    curr_col += 1
                    previous[(curr_row, curr_col)] = (curr_row, curr_col + 1)
                    change_orientation(wall_orientation, "south_of_r")
            # Wall has turned corner to the left, robot will move left, wall orientation changed to north of robot
            elif maze[curr_row][curr_col - 1] != "#":
                curr_col -= 1
                previous[(curr_row, curr_col)] = (curr_row, curr_col + 1)
                change_orientation(wall_orientation, "north_of_r")

        # Conditions for if the robot was/is next to the north-oriented wall in the previous or current step
        elif wall_orientation["north_of_r"]:
            # Robot is currently next to north-oriented wall
            if maze[curr_row - 1][curr_col] == "#":
                # Next step is not a wall and robot will move left a step
                if maze[curr_row][curr_col - 1] != "#":
                    curr_col -= 1
                    previous[(curr_row, curr_col)] = (curr_row, curr_col + 1)
                # Robot is in a north-west corner, robot will move down, wall orientation changed to west of robot
                elif maze[curr_row][curr_col - 1] == "#":
                    curr_row += 1
                    previous[(curr_row, curr_col)] = (curr_row - 1, curr_col)
                    change_orientation(wall_orientation, "west_of_r")
            # Wall has turned corner going up, robot will move up, wall orientation changed to east of robot
            elif maze[curr_row - 1][curr_col] != "#":
                curr_row -= 1
                previous[(curr_row, curr_col)] = (curr_row + 1, curr_col)
                change_orientation(wall_orientation, "east_of_r")

        steps += 1
        path.append((curr_row, curr_col)) #Adds new step to path list

    #Assigns exit location to end variable
    if maze[curr_row][curr_col] == "E":
        end = (curr_row, curr_col)

    #Prints source and end coordinates, the path taken, and the number of steps
    print(f"Source : {source}")
    print(f"Path : {path}")
    print(f"End : {end}")
    print(f"Number of steps: {steps}")
    print("")

    #Prints the maze with the solution path
    generate_path(maze, path, source, end)

#Main method reads maze text file, stores data in maze variable, and passes maze to solve method
def main():
    maze : list = read_maze()
    solve(maze)

if __name__ == '__main__':
    main()