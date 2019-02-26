#functions.py

"""
CS5400 AI: Puzzle Assignment 4
author: salhx9@mst.edu
Shelby Luttrell
"""
import copy
import classes as cla

#def astar_search(problem, h=None):
def astarSearch(problem):
    #A* search is best-first graph search with f(n) = g(n)+h(n).
    return beFGS(problem)


def beFGS(problem):
    """Searches the nodes with the lowest f scores first.
    The function f(node) is the heuristic estimate to the goal in this case
    """
    node = cla.Node(problem.initialState, None, None)

    frontier = []
    frontier.append(node)
    
    #explored set is an unordered collection with no duplicate elements. 
    explored = set()

    while frontier:
        node = frontier.pop()
        if problem.checkGoal(node.state):   # return the end state if goal is reached
            return node
        explored.add(node.stringBoard)      # otherwise add it to the explored set
        for child in node.expand(problem):  
            #if child.stringBoard not in explored and child not in frontier: # add child to frontier if not there or in explored
            if child.stringBoard not in explored:

                #here we loop through frontier and look for the board
                foundState = False      #this will stop iterating through the frontier
                currentState = None     #this is a copy of the current node
                iterFrontier = 0        #this saves where the node is in the frontier so it can be deleted later
                for frontNode in frontier:
                    
                    if (frontNode.stringBoard == child.stringBoard):
                        #print("Found the board in frontier")
                        #print("frontNode.stringboard:", frontNode.stringBoard)
                        #print("iterFrontier:", iterFrontier)
                        foundState = True
                        currentState = frontNode
                        break
                    iterFrontier+= 1

                #if the board is not in the frontier
                if foundState == False: 
                    
                    #f applies the heuristic + pathcost and adds this value to the node class. f(x) = g(x) + h(x)
                    problem.f(child)
                    frontier.append(child)
                    frontier.sort(key=lambda x: x.fValue, reverse=True) #this should sort the list in order of small to large heuristic value
                
                else :# if the state was already in the frontier, then check the heuristic value
                    #print("Already in the frontier, looking to change val")
                    
                    if child.fValue < currentState.fValue:
                        #print('better option found')
                        #del frontier[currentState] #? does not delete this node. need to iterate through frontier
                        del frontier[iterFrontier] #proper way of deleting the node from the frontier
                        frontier.append(child)
                        frontier.sort(key=lambda x: x.fValue, reverse=True) #this should sort the list in order of small to large heuristic value

            # if already explored do nothing
    return None

def findPath(node):
    #this holds the solution to the puzzle
    solutionList=[]
    subList=[]
    #prints from end state to beginning states
    while (node.parent is not None):
        #printBoard(node)
        #print('**********************************')
        prettyFormatAction = '{} {} {} {}'.format(node.action.wrigglerIndex, node.action.partMoved, node.action.colM, node.action.rowM)
        node = node.parent
        solutionList.insert(0, prettyFormatAction)
        subList.clear()
    return solutionList

def printBoard(node):
    for row in node.state:
        print(*row)

def getPathCost(node):
    return node.pathCost