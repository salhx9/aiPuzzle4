#!/usr/bin/env python3
#main.py

"""
CS5400 AI: Puzzle Assignment 4
author: salhx9@mst.edu
Shelby Luttrell
"""
import sys
import classes as cla
import functions as fun
import time, os

def main():
    #starts the timer to record length of run
    start_time = time.time()

    if len(sys.argv) == 1:
        print("No arguments passed. Exiting now.")
        return

    #this sets the file to the one given in the command line
    fileName = sys.argv[1]

    #check for valid file and automatically close file
    if os.path.exists(fileName):
        with open(fileName) as f:
            lines = f.read().split("\n")
    else:
        print("Filename does not exist. Exiting now.")
        return

    #parses the gameboard input
    wrigglerInput = lines[0]
    lineOneList = wrigglerInput.split()

    #check for invalid input
    if len(lineOneList) != 3:
        print("This file has too many inputs for the length width and num of wrigglers. Exiting now.")
        return
    if lineOneList[0].isdigit() == False:
        print("Invalid width puzzle")
        return
    if lineOneList[1].isdigit() == False:
        print("Invalid height puzzle")
        return
    if lineOneList[2].isdigit() == False:
        print("Invalid numWrigglers puzzle")
        return

    widthPuzzle = int(lineOneList[0])
    heightPuzzle = int(lineOneList[1])
    numWrigglers = int(lineOneList[2])

    #initialize the gameboard
    gameBoard = []
    row = []
    for ro in range(heightPuzzle):
        x = lines[1+ro]
        row = x.split()
        gameBoard.append(row)

    #check for invalid characters in board 
    for row in gameBoard:
        for item in range(len(row)):
            if row[item] not in ("v", "D", ">", "R", "^", "U", "<", "L", "e","x"):
                #check if its a number, if not exit
                if row[item].isdigit() == True:
                    continue
                else:
                    print("Invalid character in input. Exiting now.")
                    return
                    

    # for x in gameBoard:
    #     print(*x)

    #the Problem is the bottom right corner
    problem = cla.Problem(gameBoard, widthPuzzle, heightPuzzle, numWrigglers, 20) #50 is max depth

    # perform a*gs on the gameBoard given and returns winning node
    solution1 = fun.astarSearch(problem)
    finalSol1 = fun.findPath(solution1)
    
    # print out the solution
    if solution1:
        for item in finalSol1:
            print(''.join(item))
        
        fun.printBoard(solution1)
        print('{} '.format(time.time() - start_time))
        print(str(fun.getPathCost(solution1)))
    else:
        print('Failure')
        print('{}'.format(time.time() - start_time))

                                                                              
if __name__ == "__main__":
    main()

#end