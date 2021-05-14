import eight_puzzle_search
import re

samplepuzzle = [[1, 2, 3, 4, 5, 6, 7, 8, 0], # trivial
              [1, 2, 3, 4, 5, 6, 7, 0, 8],  #  very easy
              [1, 2, 0, 4, 5, 3, 7, 8, 6],  #  easy
              [1, 0, 3, 4, 2, 6, 7, 5, 8],  #  test
              [1, 2, 3, 5, 0, 6, 4, 7, 8],  #  depth 4
              [0, 1, 2, 4, 5, 3, 7, 8, 6],  #  doable
              [1, 3, 6, 5, 0, 2, 4, 7, 8],  #  depth 8
              [1, 3, 6, 5, 0, 7, 4, 8, 2],  #  depth 12
              [1, 6, 7, 5, 0, 3, 4, 8, 2],  #  depth 16
              [7, 1, 2, 4, 8, 5, 6, 3, 0],  #  depth 20
              [0, 7, 2, 4, 6, 1, 3, 5, 8],  #  depth 24
              [8, 7, 1, 6, 0, 2, 5, 4, 3]]  #  oh boy
              


# sample puzzle choice input
def chooseSample():
    print ("\n We have the following sample choices:")
    print ("1. Trivial")
    print ("2. Very ease")
    print ("3. Easy")
    print ("4. Test")
    print ("5. Depth 4")
    print ("6. Doable")
    print ("7. Depth 8")
    print ("8. Depth 12")
    print ("9. Depth 16")
    print ("10. Depth 20")
    print ("11. Depth 24")
    print ("12 Oh boy")
    ch = int(input("Enter a number from 1 to 12 to choose a sample puzzle of a certain level: "))
    if ch in range(1, 13):
        default = eight_puzzle_search.eightPuzzle(samplepuzzle[ch-1])
    else:
        print ("Try again")
        return chooseSample()
    return default

# input custom user puzzle
def userPuzzle(x):
    inputPuzzle = []
    print ("    Provide rowise input and use a zero to represent the blank")
    get = input('    Enter the first row, separate the numbers with a space ')
    temp = map(int, re.split(', | ', get))
    for num in temp:
            inputPuzzle.append(num)

    get = input('    Enter the second row, separate the numbers with a space ')
    temp = map(int, re.split(', | ', get))
    for num in temp:
            inputPuzzle.append(num)
    get = input('    Enter the third row, separate the numbers with a space ')
    temp = map(int, re.split(', | ', get))
    for num in temp:
            inputPuzzle.append(num)
    return eight_puzzle_search.eightPuzzle(inputPuzzle)


# option to choose sample or custom puzzle from the user
def puzzleChoice():
    print ("Enter \"1\" to use a sample puzzle and \"2\" to enter a custom puzzle")
    ch = int(input(""))
    if ch == 1:
        return chooseSample()
    elif ch == 2:
        return userPuzzle("puzzle")
    else:
        print ("Try again")
        return puzzleChoice()



# user input for choice of search algorithm
def searchOption(thePuzzle):
    print ("   Enter the corresponding number for your search algorithm:")
    print ("      1. Uniform Cost Search")
    print ("      2. A* with the Misplaced Tile heuristic.")
    print ("      3. A* with the Manhattan distance heuristic.\n")
    option = int(input('         '))
    if not(option > 3) and not(option < 1):
        return option
    else:
        print ("Try again")
        return searchOption(solvePuzzle)

# program starts
print ("You have entered the sliding 8-puzzle")
solvePuzzle = puzzleChoice()
print ("Puzzle to solve: ")

eight_puzzle_search.currentPuzzle(solvePuzzle.INITIAL_STATE)

answer = eight_puzzle_search.findAnswer()
print ("\nThe destination state: ")

eight_puzzle_search.currentPuzzle(answer)

option = searchOption(solvePuzzle)
result, total_nodes, max_nodes_q = eight_puzzle_search.general_search(solvePuzzle, option)
if result == 0:
    print ("Goal can't be reached with this starting state!")
else:
    print ("\n\nDesired goal state has been reached")
    print ("\nNodes expanded: %d" %(total_nodes))
    print ("\nMaximum nodes in queue: %i" %(max_nodes_q))
    print ("\nThe depth of the goal node %d" %(result.DEPTH))
if result.DEPTH:
    print("\n------------------- Solution Trace-------------------------------------")
    solnTrace = []
    solnTrace.append(result)
    node = result.PARENT
    while node.PARENT is not None:
        solnTrace.append(node)
        node = node.PARENT
    solnTrace.append(node)
    solnTrace.reverse()
    for node in solnTrace[:len(solnTrace)-1]:
        print ("Node with g(n) = %d" %(node.DEPTH))
        
        if option == 1:
           print ("h(n) = 0" )
        elif option == 2:
            print ("h(n) = %d" %(node.MISTILE))
        else:
            print ("h(n) = %d" %(node.MANDIST))
        eight_puzzle_search.currentPuzzle(node.STATE)
        print ('...')
    eight_puzzle_search.currentPuzzle(solnTrace[len(solnTrace)-1].STATE)
    print ("\n\nDesired goal state has been reached")
    print ("\nNodes expanded: %d" %(total_nodes))
    print ("\nMaximum nodes in queue: %i" %(max_nodes_q))
    print ("\nThe depth of the goal node %d" %(result.DEPTH))
       

print (' All good')




