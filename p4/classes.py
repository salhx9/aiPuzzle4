#classes.py
"""
CS5400 AI: Puzzle Assignment 4
author: salhx9@mst.edu
Shelby Luttrell
"""
import copy, math

class Action:
    # moveDirection :direction the wriggler shifts
    # partMoved     :head or tail moved
    # wrigglerIndex :indicates which wriggler moved
    # rowH          :head row of the board changed in this action
    # colH          :head column of the board changed in this action
    # rowM          :row the segment was moved to in this action
    # colM          :column the segment was moved to in this action
    def __init__(self, moveDirection, partMoved, wrigglerIndex, rowH = 0, colH = 0, rowM = 0, colM = 0):
        self.moveDirection = moveDirection
        self.partMoved = partMoved
        self.wrigglerIndex = wrigglerIndex
        self.rowH = rowH
        self.colH = colH
        self.rowM = rowM
        self.colM = colM

class Node:
    # state     :2d array grid that is the board
    # parent    :parent of the node
    # action    :action taken to get to this state
    # pathCost  :total actions taken to get to this node
    def __init__(self, state, parent, action=None):
        #def __init__(self, state, parent, pathCost = 0, action = None):
        self.state = state
        self.parent = parent
        self.action = action
        self.pathCost = 0
        self.fValue = 0
        self.stringBoard = self.convertToString()
        if parent:
            self.pathCost = parent.pathCost + 1

    # this needs to return a set of children
    def expand(self, problem):
        childList = []      # list of children made by this node

        # for each possible action for this node, make a state and then apply actions to it
        possibleActions = Problem.findActions(problem, self)
        
        for action in possibleActions:
            # if the childState has a match it will return a new state. If no match it returns None
            childState, action = Problem.generateState(problem, self, action)

            if childState is not None:
                # make a new node out of the state and add it into the list
                childNode = Node(childState,self, action)
                childList.append(childNode)
        return childList
    
    #for the explored set, needs to be a 1d list or a string to quickly check
    def convertToString(self):
        return "".join([j for sub in self.state for j in sub])
    
class Problem:
    # initialState  :beginning board state
    # winColumn     :holds the index of rightmost column
    # winRow        :holds the index of the bottom row
    def __init__(self, initialState, winColumn, winRow, numWrigglers, maxDepth):
        self.initialState = initialState
        self.winColumn = winColumn
        self.winRow = winRow
        self.numWrigglers = numWrigglers
        self.maxDepth = maxDepth
    
    #heuristic to find the straight line distance from the index 0 wriggler to goal column and row
    def f(self, node):
        #find the zero index wriggler in this state
        headRow, headCol, tailRow, tailCol = self.findZero(node)
        goalRow = self.winRow
        goalCol = self.winColumn
        cost = node.pathCost
        hVal = 0
        
        #calculate distance to goal for both the head and the tail
        distHead = math.sqrt(((goalRow-headRow)**2)+((goalCol-headCol)**2))
        distTail = math.sqrt(((goalRow-tailRow)**2)+((goalCol-tailCol)**2))
        #print("heuristic called")

        #the straight line distance that is smaller will be the one returned
        # distHead and distTail are the h Values in the function f(x) = g(x) + h(x)
        if distHead > distTail:
            hVal = distTail + cost
        else:
            hVal = distHead + cost
        node.fValue = hVal 

    # finds the next segment in the worm and says done when it hits the tail
    def findNextSegment(self, board, currentI, currentJ, endTail):
        if board[currentI][currentJ] in ("v", "D"):
            currentI = currentI+1
        elif board[currentI][currentJ] in (">", "R"):
            currentJ = currentJ+1
        elif board[currentI][currentJ] in ("^", "U"):
            currentI = currentI-1
        elif board[currentI][currentJ]in ("<", "L"):
            currentJ = currentJ-1
        if board[currentI][currentJ] not in ("v", "D", ">", "R", "^", "U", "<", "L"):
            endTail = True
        else:
            endTail = False
        return currentI, currentJ, endTail
    
    ### this should find all the numbers and the letters that aren't e or x
    def findActions(self, node):
        actionList = []
        board = node.state
        heightBoard= len(board)
        widthBoard = len(board[0])
        for row in range(heightBoard):
            for column in range (widthBoard):
                if board[row][column] in ("D", "R", "U", "L"): #found a head
                    endTail = False
                    headRow, headCol= row, column
                    tailRow, tailCol= row, column

                    while (endTail == False): #look for tail
                        tailRow, tailCol, endTail = self.findNextSegment(board, tailRow, tailCol, endTail)
        
                    #found the tail, now record the index of wriggler
                    wIndex = board[tailRow][tailCol]

                    #find the empty tiles around head
                    possibleMovesH = self.findEmpty(heightBoard, widthBoard, board, headRow, headCol)
                    possibleMovesT = self.findEmpty(heightBoard, widthBoard, board, tailRow, tailCol)
                    
                    if len(possibleMovesH) != 0:
                        #make a new action for head moves and adds it to list:
                        for direction in range(len(possibleMovesH)):
                            #makes a new action
                            #print(possibleMovesH[direction])
                            tempAct = Action(possibleMovesH[direction], '0', wIndex, headRow, headCol, 0, 0)
                            actionList.append(tempAct)

                    if len(possibleMovesT) != 0:
                        #make a new action for tail moves and adds it to list:
                        for direction in range(len(possibleMovesT)):
                            #makes a new action
                            #print(possibleMovesT[direction])
                            tempAct = Action(possibleMovesT[direction], '1', wIndex, headRow, headCol, 0, 0)
                            actionList.append(tempAct)
        #return a list actions
        return actionList
    
    def findZero(self, node):
        board = node.state
        heightBoard= len(board)
        widthBoard = len(board[0])
        #find the zero index wriggler
        for row in range(heightBoard):
            for column in range (widthBoard):
                if board[row][column] in ("D", "R", "U", "L"): #found a head and 
                    endTail = False
                    headRow, headCol= row, column
                    tailRow, tailCol= row, column

                    while (endTail == False): #look for tail
                        tailRow, tailCol, endTail = self.findNextSegment(board, tailRow, tailCol, endTail)
        
                    #found the tail, now record the index of wriggler
                    wIndex = board[tailRow][tailCol]

                    #if the 0 wriggler is found, return the coordinates of the head and tail
                    if wIndex == '0':
                        return headRow, headCol, tailRow, tailCol


    def generateState(self, node, action):
        #this should a new board for the action
        newState = copy.deepcopy(node.state)
        #print("PreGenSTATE:")
        # for row in newState:
        #     print(*row)
        # print("Action to be performed:")
        # print("Direction:", action.moveDirection," PartMoved:", action.partMoved," Head Row:", action.rowH," Head Col:", action.colH)
        
        #start at the head of the wriggler to change everything
        tempRow = action.rowH
        tempCol = action.colH

        #this will be used later for changing of the tail
        wrigNum = action.wrigglerIndex

        #this is true when the indices are at the tail
        foundTail = False

        if action.partMoved == "0": # if this action moves the head
            if action.moveDirection == "D":
                newState[tempRow+1][tempCol] = "U"
                tempRow = tempRow + 1

            elif action.moveDirection == "R":
                newState[tempRow][tempCol+1] = "L"
                tempCol = tempCol + 1

            elif action.moveDirection == "U":
                newState[tempRow-1][tempCol] = "D"
                tempRow = tempRow - 1

            elif action.moveDirection == "L":
                newState[tempRow][tempCol-1] = "R"
                tempCol = tempCol - 1
            
            #save in state where the action was performed
            action.rowM = tempRow
            action.colM = tempCol
            
            #print where the action was performed
            #print("Head Action Performed: ",tempRow,tempCol)

            #now we're where the head was
            tempRow, tempCol = action.rowH, action.colH
            prevRow,prevCol = tempRow,tempCol

            #find the next state, if it was a wrig num, change the temp to wrig num
            tempRow,tempCol, foundTail = self.findNextSegment(newState, tempRow, tempCol, foundTail)
            
            #if this was a wriggler of length 2
            if (foundTail == True):
                newState[tempRow][tempCol] = "e"
                newState[prevRow][prevCol] = wrigNum
            else:
                #print("Next Segment:",tempRow,tempCol)
                
                #takes the letters and makes them arrows
                if newState[prevRow][prevCol] in ("D", "R", "U", "L"):
                    character = newState[prevRow][prevCol]
                    newState[prevRow][prevCol] = self.convertHeadToArrow(character)
                    #print("Converted old head to:", newState[prevRow][prevCol],prevRow,prevCol)
                
                foundTail = False
                #now that the old head is an arrow now, find the next segment
                #tempRow, tempCol, foundTail = self.findNextSegment(newState, tempRow, tempCol, foundTail)
                #print("Next Segment:",tempRow,tempCol)
                
                while(foundTail == False):
                    prevRow = tempRow
                    prevCol = tempCol         
                    tempRow, tempCol, foundTail = self.findNextSegment(newState, tempRow, tempCol, foundTail)
                #print("Temps:",tempRow,tempCol)
                # print("Prevs:",prevRow,prevCol)
                if newState[tempRow][tempCol] == wrigNum:   
                    newState[tempRow][tempCol] = "e"
                    newState[prevRow][prevCol] = wrigNum

            #now we will make the previous space the tail, and place an 'e' in current
            

        elif action.partMoved == "1": # if this action is the tail
            #shift everything towards tail until reach the wrignum, then apply action to the tail

            #head space goes to empty
            headRow = tempRow
            headCol = tempCol
            tempRow, tempCol, foundTail = self.findNextSegment(newState, tempRow, tempCol, foundTail)
            newState[headRow][headCol] = "e"
        
            #not 2 segment case
            if(newState[tempRow][tempCol] != wrigNum):
                #next space needs to contain a letter of the arrow it is 
                temp = newState[tempRow][tempCol]
                newState[tempRow][tempCol] = self.convertArrowToLetter(temp)

                #find the tail
                while (foundTail == False):       
                    tempRow, tempCol, foundTail = self.findNextSegment(newState, tempRow, tempCol, foundTail)
        
                #tail is found now perform action on it
                if action.moveDirection == "D":
                    newState[tempRow][tempCol] = "v"
                    newState[tempRow+1][tempCol] = wrigNum
                    tempRow = tempRow + 1
                    
                elif action.moveDirection == "R":
                    newState[tempRow][tempCol] = ">"
                    newState[tempRow][tempCol+1] = wrigNum
                    tempCol = tempCol + 1

                elif action.moveDirection == "U":
                    newState[tempRow][tempCol] = "^"
                    newState[tempRow-1][tempCol] = wrigNum
                    tempRow = tempRow - 1

                elif action.moveDirection == "L":
                    newState[tempRow][tempCol] = "<"
                    newState[tempRow][tempCol-1] = wrigNum
                    tempCol = tempCol-1
                else:
                    print("hmmmmm")
            else:
                #print("here's the tail to be moved: ", str(tempRow),str(tempCol))
                #tail is found now perform action on it
                if action.moveDirection == "D":
                    newState[tempRow][tempCol] = "D"
                    newState[tempRow+1][tempCol] = wrigNum
                    tempRow = tempRow + 1
                    
                elif action.moveDirection == "R":
                    newState[tempRow][tempCol] = "R"
                    newState[tempRow][tempCol+1] = wrigNum
                    tempCol = tempCol + 1

                elif action.moveDirection == "U":
                    newState[tempRow][tempCol] = "U"
                    newState[tempRow-1][tempCol] = wrigNum
                    tempRow = tempRow - 1

                elif action.moveDirection == "L":
                    newState[tempRow][tempCol] = "L"
                    newState[tempRow][tempCol-1] = wrigNum
                    tempCol = tempCol-1
                else:
                    print("hmmmmm")
            #record the space that was moved into

            action.rowM = tempRow
            action.colM = tempCol
            
        else:
            print("done messed up")
        return newState, action


    # finds the empty coordinates around the worms head and tail
    def findEmpty(self, heightBoard, widthBoard, board, currentI, currentJ):
        tH = heightBoard - 1
        tW = widthBoard - 1
        emptySpace = []
        if (currentJ+1 <= tW) and (currentJ >= 0):
            if board[currentI][currentJ+1] == "e":
                emptySpace.append('R')
        if (currentJ <= tW) and (currentJ -1 >= 0):
            if board[currentI][currentJ-1] == "e":
                emptySpace.append('L')    
        if (currentI+1 <= tH) and (currentI >= 0):
            if board[currentI+1][currentJ] == "e":
                emptySpace.append('D')        
        if (currentI <= tH) and (currentI -1 >= 0):
            if board[currentI-1][currentJ] == "e":
                emptySpace.append('U')
        return emptySpace

    #changes the letters on the head to arrows when moved 
    def convertHeadToArrow(self, temp):
        if (temp == "D"):
            val = "v"
        elif (temp == "R"):
            val = ">"
        elif (temp == "U"):
            val = "^"
        else:
            val = "<"
        return val

    #changes arrows to letters when moved
    def convertArrowToLetter(self, temp):
        if (temp == "v"):
            val = "D"
        elif (temp == ">"):
            val = "R"
        elif (temp == "^"):
            val = "U"
        else:
            val = "L"
        return val

    #check for head, then make sure it belongs to index 0 wriggler    
    def checkGoal(self, state):
        if state[self.winRow-1][self.winColumn-1] in ("D", "R", "U", "L"):
            row = self.winRow-1
            col = self.winColumn-1
            foundTail = False
            #find the tail
            while (foundTail == False):
                row, col, foundTail = self.findNextSegment(state, row, col, foundTail)
            #found the goal if the 0 wriggler is in this position
            if (state[row][col]== "0"):
                return True
            else:
                return False
        elif state[self.winRow-1][self.winColumn-1] == "0":
            return True
        else:
            return False
# end