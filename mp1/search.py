# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,extra)



#pseudocode retrieved from https://www.youtube.com/watch?v=-L-WgKMFuhE&t=594s for astar algorithms
#refenced https://www.geeksforgeeks.org/prims-minimum-spanning-tree-mst-greedy-algo-5/ for prim's mst algorithm
from queue  import deque
from queue import Queue
from queue import PriorityQueue

import sys

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "extra": extra,
    }.get(searchMethod)(maze)




def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    #TODO: Write your code here
    q = Queue()           #init queue
    v = set()                     #init visited nodes
    prev = {}                       #init previous nodes (dictionary)

    start = maze.getStart()
    dot = maze.getObjectives()
    destination = dot[0]

    path = []


    q.put(start)
    v.add(start)

    while q.empty() == False:
        current = q.get()

        if current == destination:
            break

        for neighbor in maze.getNeighbors(current[0], current[1]):
            if neighbor not in v:
                q.put(neighbor)
                v.add(neighbor)
                prev[neighbor] = current

    #backtrace
    path.append(destination)
    while destination in prev:
        path.append(prev[destination])
        destination = prev[destination]

    path.reverse()
    return path


def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here

    open = {}               #open dictionary with f value
    closed = {}             #closed dictionary
    prev = {}                       #init previous nodes (dictionary)
    g_set = {}


    path= []

    start = maze.getStart()             #tuple of starting point
    dot = maze.getObjectives()          #list of dots
    dest = dot[0]                       #tuple of destination

    open[start] = 0            #set start f value = 0
    g_set[start] = 0
    search =1

    while len(open) != 0 and search == 1:
        minNode = ()
        fmin = min(open.values())
        for key in open:                    #find node with lowest f value
            if open[key] == fmin:
                minNode = key
                del open[minNode]           #pop
                closed[minNode] = fmin
                break

        for neighbor in maze.getNeighbors(minNode[0], minNode[1]):

            if neighbor == dest:
                search = 0
                prev[dest] = minNode
                break

            g = 1 + g_set[minNode]
            g_set[neighbor] = g
            h = abs(neighbor[0] - dest[0]) + abs(neighbor[1] - dest[1])
            f = g+h

            if neighbor in closed.keys():
                continue

            if neighbor not in open.keys() or f < open[neighbor]:
                prev[neighbor] = minNode
                open[neighbor] = f

    path.append(dest)                   #backtrace
    while dest != start:
        path.append(prev[dest])
        dest = prev[dest]

    path.reverse()
    return path

#----------------------------------------------------------------------------------------

class Node: # node class for bookeeping
    def __init__(self, pos ,g ,h , prev):
        self.pos = pos
        self.g = g
        self.h = h
        self.f = g+h
        self.prev = prev
        self.neighbor = []

    def __lt__(self,other):
        return self.f < other.f

    def __eq__(self,other):
        if self.pos == other.pos:
            return True
        else:
            return False

    def printNode(self):
        print("pos:", self.pos, "g:",self.g, " h:",self.h, " g:", self.f)
        print("prev:", self.prev.pos)
        print("neighbor:", self.neighbor)

#use priority queue

def astar_util(maze, start, dot):
    open = {}               #open dictionary with f value
    closed = {}             #closed dictionary
    prev = {}                       #init previous nodes (dictionary)
    g_set = {}
    path= []

    #start = maze.getStart()             #tuple of starting point
    #dot = maze.getObjectives()          #list of dots
    dest = dot                       #tuple of destination

    open[start] = 0            #set start f value = 0
    g_set[start] = 0
    search =1

    while len(open) != 0 and search == 1:
        minNode = ()
        fmin = min(open.values())
        for key in open:                    #find node with lowest f value
            if open[key] == fmin:
                minNode = key
                del open[minNode]           #pop
                closed[minNode] = fmin
                break

        for neighbor in maze.getNeighbors(minNode[0], minNode[1]):

            if neighbor == dest:
                search = 0
                prev[dest] = minNode
                break

            g = 1 + g_set[minNode]
            g_set[neighbor] = g
            h = abs(neighbor[0] - dest[0]) + abs(neighbor[1] - dest[1])
            f = g+h

            if neighbor in closed.keys():
                continue

            if neighbor not in open.keys() or f < open[neighbor]:
                prev[neighbor] = minNode
                open[neighbor] = f

    #path.append(dest)                   #backtrace
    while dest != start:
        path.append(prev[dest])
        dest = prev[dest]

    path.reverse()
    return path


def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here

    start = maze.getStart()             #tuple of starting point
    dots = maze.getObjectives()          #list of dots
    open = PriorityQueue()
    closed=[]


    # build MST Table and paths
    nodes = maze.getObjectives()
    nodes.insert(0,start)

    mst_table = {}
    path_list = {}

    # edge generation using part one astar
    for st in nodes:
        for dest in nodes:
            if st != dest:
                path_list[(st,dest)] = astar_util(maze,st,dest)
                mst_table[(st,dest)] = len(path_list[(st,dest)])

    #print(mst_table)            #check
    #print("mstLength: ",mstLength(nodes,mst_table))

    emptyNode =Node((-1,-1),0,0,0)
    #print(start)
    startNode = Node(start,0,0,emptyNode) # set f value of start to zero
    for dot in dots:
        startNode.neighbor.append(dot)
    open.put(startNode)


    while open:
        #print("enter while loop")
        currentNode = open.get()            #PriorityQueue
        #closed.append(currentNode)
        #currentNode.printNode()

        if len(currentNode.neighbor)==0:
            break
        for neighbor in currentNode.neighbor:

            if currentNode.pos == neighbor:
                continue

            #if neighbor in closed.keys():
            #    continue

            g = currentNode.g + mst_table[(currentNode.pos, neighbor)]
            h = mstLength(currentNode.neighbor,mst_table)

            #print("g,h,f:", g,h,g+h)
            nextNode = Node(neighbor, g, h, currentNode)
            for neighborNode in currentNode.neighbor:
                if nextNode.pos != neighborNode:
                    nextNode.neighbor.append(neighborNode)

            open.put(nextNode)
            nextNode.prev = currentNode

    #print("at the end:", currentNode.pos)

    #path generation
    final_path = []
    while currentNode != startNode:

        #print(currentNode.pos)

        prevNode = currentNode.prev
        final_path +=path_list[(currentNode.pos,prevNode.pos)]
        currentNode = currentNode.prev
    #print(currentNode.pos)

    final_path.append(startNode.pos)
    final_path.reverse()
    #print("path:",final_path)
    return final_path


def mstLength(dots, mst_table):        #heuristics
    mstLength =0
    startNode = dots[0]
    key={}

    mstSet = {}
    for i in dots:
        mstSet[i] = False

    minNode = startNode
    mstSet[minNode] = True

    #print(mstSet)
    while not all(value == True for value in mstSet.values()):
        for node in dots:
            if node != minNode:
                if mstSet[node] == True:
                    continue
                #print(mst_table[(minNode, node)])
                key[(minNode,node)] = mst_table[(minNode, node)]

        shortestEdge = get_key(key,min(key.values()) )
        if mstSet[shortestEdge[1]] == True:
            del key[shortestEdge]
            continue

        #print("shortestEdge:", shortestEdge)

        mstSet[shortestEdge[1]] = True
        #print("check set:", mstSet)
        #print("check key:", key)

        del key[shortestEdge]

        mstLength += mst_table[shortestEdge]
        minNode = shortestEdge[1]

    return mstLength

def get_key(dict, val):
    for key in dict:
        if dict[key] == val:
            return key

def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    path = astar_corner(maze)
    return path



class Node: # node class for bookeeping
    def __init__(self, pos ,g ,h , prev):
        self.pos = pos
        self.g = g
        self.h = h
        self.f = g+h
        self.prev = prev
        self.neighbor = []

    def __lt__(self,other):
        return self.f < other.f

    def __eq__(self,other):
        if self.pos == other.pos:
            return True
        else:
            return False

def extra(maze):
    """
    Runs extra credit suggestion.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here

    start = maze.getStart()             #tuple of starting point
    destinations = maze.getObjectives()          #list of dots
    prev = {}                       #init previous destiantion (dictionary)
    notVisitied= []                 #dots not visitied

    dots = maze.getObjectives()

    currentNode = start
    prev[currentNode]= (-1,-1)
    while len(dots) !=0:

        nextNode = findClose(currentNode,dots)
    #    print(nextNode)
        prev[nextNode] = currentNode
        dots.remove(nextNode)
        currentNode = nextNode


    path_list = []
    node = nextNode
    while node != (-1,-1):
        #print(node)
        path_list.append(node)
        node = prev[node]


    final_path =[]
    for i in range(0,len(path_list)-1,1):
        #print(i)
        final_path += astar_util(maze,path_list[i],path_list[i+1])

    final_path.append(start)
    final_path.reverse()
    #print(final_path)

    return final_path

def findClose(current, destinations):
    closest = current
    distance = sys.maxsize;
    for dot in destinations:
        h = abs(current[0] - dot[0]) + abs(current[1] - dot[1])
        if h < distance:
            distance = h
            closest = dot
    return closest





#-------utility functions
def m_dist(start, dest):
    return abs(start[0]-dest[0])+abs(start[1]-dest[1])

def fmin(tmp):
    minf = 10000000
    minNode = Node()
    for node in tmp:
        #print("fmin loop check")
        if node.f < minf:
            minf = node.f
            minNode = node

    return minNode

def printNode(tmp):                  #find node with lowest f value
    for d in tmp:
        d.printNode()
