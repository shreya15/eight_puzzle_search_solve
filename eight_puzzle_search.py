from heapq import heappush, heappop 
from math import sqrt
from math import ceil
from functools import total_ordering

# 8-puzzle size
size = 9
limit = int(sqrt(size))

# construct initial puzzle 
def constructInitial(sz):
    global size
    global limit
    size = sz  # size of puzzle, here 9
    limit = int(sqrt(sz))
    return size, limit

# construct the answer
solution = []
def findAnswer(flag = 0):
    global solution
    global size
    solution = []
    if flag:
        solution = list(flag)
        return solution
    for i in range(1, size, 1):
        solution.append(i)
    solution.append(0)
    return solution


# The number of misplaced tiles are returned
def misplacedTiles(state):
    num = 0
    for i in range(0, size, 1):
        if state[i] == 0:
            continue
        if state[i] != solution[i]:
            num += 1
    return num


# manhattan distance calculation
def manhattanDistance(state):
    man_dist = 0
    for i in range(1, size, 1):
        val = state.index(i)
        ans = solution.index(i)
        if val == ans:  # manhattan distance for tile = 0
            continue

        # position of row and answer
        posrow = int(ceil(val/float(limit)))
        arow = int(ceil(ans/float(limit)))
        # check for row 1
        if posrow == 0:
            posrow = 1
        if arow == 0:
            arow = 1

        # position of column and answer
        poscol = (val % limit) + 1
        acol = (ans % limit) + 1

        # manhattan distance is maintained by adding distance of the tile
        man_dist += (abs(posrow-arow) + (abs(poscol - acol)))
    return man_dist


# Information about a state is specified here    
@total_ordering    
class node:
    # Node intitialisation
    def __init__(self, state, parent=None):
        self.STATE = state
        self.MISTILE = None
        self.MANDIST = None
        if parent is None:
            self.PARENT = None
            self.DEPTH = 0
        else:
            self.STATE = state
            self.PARENT = parent 
            self.DEPTH = self.PARENT.DEPTH+1    # depth greater than one from previous traversal
            
    def __index__(self, item):
        return self.STATE.index(item)        

    def __getitem__(self, item):
        return self.STATE[item]

    def misplaced(self):
        if self.MISTILE is None:
            self.MISTILE = misplacedTiles(self.STATE)
        return self.MISTILE

    def manhattan(self):
        if self.MANDIST is None:
            self.MANDIST = manhattanDistance(self.STATE)
        return self.MANDIST

    def swap(self, x, y):
        self.STATE[x], self.STATE[y] = self.STATE[y], self.STATE[x]
        
    # def __eq__(self, other):
    #     return ((self.DEPTH , self.STATE , self.misplaced(), self.manhattan()) == (other.DEPTH, other.STATE, other.misplaced(), other.manhattan()))

    def __lt__(self, other):
        return ((self.DEPTH , self.STATE , self.misplaced(), self.manhattan()) < (other.DEPTH, other.STATE, other.misplaced(), other.manhattan()))    


# Operations are defined. We apply them to the blank. Move feasibilty is checked before it is taken        
def left(state, position):
    if position in range(0, limit*(limit-1)+1, limit):
        return 0
    else:
        child = node(list(state), state)
        child.swap(position, position-1)
        return child


def right(state, position):
    if position in range(limit-1, limit*limit, limit):
        return 0
    else:
        child = node(list(state), state)
        child.swap(position, position+1)
        return child


def up(state, position):
    if position in range(0, limit, 1):
        return 0
    else:
        child = node(list(state), state)
        child.swap(position, position-limit)
        return child


def down(state, position):
    if position in range(limit*(limit-1), limit*limit, 1):
        return 0
    else:
        child = node(list(state), state)
        child.swap(position, position+limit)
        return child


# Check if goal and current state are the same
def isGoal(state):
    if state == solution:
        return 1
    else:
        return 0


# Defining the puzzle        
class eightPuzzle:
    def __init__(self, initialState):
        self.INITIAL_STATE = node(list(initialState))
        self.OPERATORS = [left, right, up, down]
        self.GOAL_TEST = isGoal

    def diffGoal(self, goalState):
        self.ANSWER = list(goalState)


diameter = 31          # diameter of 8 puzzle
MAX_SIZEOF_Q = 0       # queue size 
EXPANDED_NODES = 0     # returns number of nodes expanded 


# printing current state of the puzzle
def currentPuzzle(state):
    j = 0
    for i in range(0, limit):
        print ('      '),
        while j < limit:
            if state[j + limit * i] == 0:
                print ('*', end= ' '),
            else:
                print (state[j + limit * i], end = ' '),
            j += 1
        print ("")
        j = 0


#expand the nodes given the operators
def expandNode(node, operators):
    child_nodes = []
    blankTile = node.STATE.index(0)       # blank tile
    for oper in operators:
        child = oper(node, blankTile)     # applying operator gives child
        if child:                             
            child_nodes.append(child)         # child is added to the list of nodes
    return child_nodes


# the search function
def general_search(problem, qfunction):
    global diameter
    global EXPANDED_NODES
    global MAX_SIZEOF_Q
    if problem.GOAL_TEST(problem.INITIAL_STATE.STATE):
        print ("\n This is the goal state")
        return problem.INITIAL_STATE, EXPANDED_NODES, MAX_SIZEOF_Q
    nodes = []   # initialise priority queue
    costly = {}  # positions will not be visited due to high cost
    heappush(nodes, [float('inf'), problem.INITIAL_STATE])    # root node mounted on queue
    
    while True:
        if not nodes: # state of no solution
            return 0, 0, 0
        MAX_SIZEOF_Q = max(MAX_SIZEOF_Q, nodes.__len__())
        #pop the element with highest priority
        cost, node = heappop(nodes) 
        costly[tuple(node.STATE)] = True
        if qfunction is 2:
                node.misplaced()
        elif qfunction is 3:
                node.manhattan()
# No action if child node visited. If not, it is pushed to the queue                
                      
        for child in expandNode(node, problem.OPERATORS):
            if tuple(child.STATE) not in costly:
                if child.DEPTH <= diameter:
                    if qfunction is 1:
                        heappush(nodes, [child.DEPTH, child])
                    elif qfunction is 2:
                        heappush(nodes, [child.DEPTH + child.misplaced(), child])
                    else:
                        heappush(nodes, [child.DEPTH + child.manhattan(), child])
                    EXPANDED_NODES += 1
            if problem.GOAL_TEST(child.STATE):        # test for goal state of expanded node
                return child, EXPANDED_NODES, MAX_SIZEOF_Q

