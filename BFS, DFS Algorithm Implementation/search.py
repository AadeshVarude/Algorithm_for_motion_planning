import numpy as np

# Basic searching algorithms

# Class for each node in the grid
class Node:
    def __init__(self, row, col, is_obs, h):
        self.row = row        # coordinate
        self.col = col        # coordinate
        self.is_obs = is_obs  # obstacle?
        self.cost = None      # total cost (depend on the algorithm)
        self.parent = None    # previous node

def if_valid(next_x,next_y,n_r,n_c):
    if (next_x>=0 and next_y>=0 and next_x<n_r and next_y<n_c):
        return True
    return False
def path_finder(start,goal,parent):
    path=[]
    x=goal[0]
    y=goal[1]
    path.append(goal)
    # print("goal pose",goal)
    while parent[x][y]!=(start[0],start[1]):
        # print("values appending in path",[parent[x][y][0],parent[x][y][1]])
        path.append([parent[x][y][0],parent[x][y][1]])
        # print(parent)
        x1=parent[x][y][0]
        y=parent[x][y][1]
        x=x1

    path.append(start)
    path.reverse()
    return path


def bfs(grid, start, goal):
    '''Return a path found by BFS alogirhm 
       and the number of steps it takes to find it.

    arguments:
    grid - A nested list with datatype int. 0 represents free space while 1 is obstacle.
           e.g. a 3x3 2D map: [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    start - The start node in the map. e.g. [0, 0]
    goal -  The goal node in the map. e.g. [2, 2]

    return:
    path -  A nested list that represents coordinates of each step (including start and goal node), 
            with data type int. e.g. [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]]
    steps - Number of steps it takes to find the final solution, 
            i.e. the number of nodes visited before finding a path (including start and goal node)

    >>> from main import load_map
    >>> grid, start, goal = load_map('test_map.csv')
    >>> bfs_path, bfs_steps = bfs(grid, start, goal)
    It takes 10 steps to find a path using BFS
    >>> bfs_path
    [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1]]
    '''
    ### YOUR CODE HERE ###
    path = []
    steps = 0
    found = False
    queue=[]
    parent=np.negative(np.ones((len(grid),len(grid[0])),dtype=object))
    visited=np.zeros((len(grid),len(grid[0])))
    r=[[0, 1], [1, 0], [0, -1], [-1, 0]]
    queue.append(start)

    # if the start position is an obstale it will return no path found
    if grid[start[0]][start[1]]==1:
        queue.pop(0)
    while len(queue)>0:
        x,y=queue.pop(0)
        if (visited[x][y]==0):
            visited[x][y]=1
            steps+=1
            if(visited[x][y]==visited[goal[0]][goal[1]]):
                found=True
                break
            
            for i in r:
                next_x=x+i[0]
                next_y=y+i[1]
                if(if_valid(next_x,next_y,len(grid),len(grid[0]))):
                    if(grid[next_x][next_y]==0 and visited[next_x][next_y]==0):
                        queue.append([next_x,next_y])
                        if(parent[next_x][next_y]==-1):
                            parent[next_x][next_y]=(x,y)

    

    if found:
        path=path_finder(start,goal,parent)
        print(f"It takes {steps} steps to find a path using BFS")
    else:
        print("No path found")
    return path, steps


def dfs(grid, start, goal):
    '''Return a path found by DFS alogirhm 
       and the number of steps it takes to find it.

    arguments:
    grid - A nested list with datatype int. 0 represents free space while 1 is obstacle.
           e.g. a 3x3 2D map: [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    start - The start node in the map. e.g. [0, 0]
    goal -  The goal node in the map. e.g. [2, 2]

    return:
    path -  A nested list that represents coordinates of each step (including start and goal node), 
            with data type int. e.g. [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]]
    steps - Number of steps it takes to find the final solution, 
            i.e. the number of nodes visited before finding a path (including start and goal node)

    >>> from main import load_map
    >>> grid, start, goal = load_map('test_map.csv')
    >>> dfs_path, dfs_steps = dfs(grid, start, goal)
    It takes 9 steps to find a path using DFS
    >>> dfs_path
    [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [2, 3], [3, 3], [3, 2], [3, 1]]
    '''
    ### YOUR CODE HERE ###
    path = []
    steps = 0
    found = False
    stack=[]
    parent=np.negative(np.ones((len(grid),len(grid[0])),dtype=object))
    visited=np.zeros((len(grid),len(grid[0])))
    r=[[-1, 0],[0, -1],[1, 0],[0, 1]]
    stack.append(start)
    # if the start position is an obstale it will return no path found
    if grid[start[0]][start[1]]==1:
        stack.pop()

    while len(stack)>0:
        x,y=stack.pop()
        if (visited[x][y]==0):
            visited[x][y]=1
            steps+=1
            if(visited[x][y]==visited[goal[0]][goal[1]]):
                found=True
                break
            
            for i in r:
                next_x=x+i[0]
                next_y=y+i[1]
                if(if_valid(next_x,next_y,len(grid),len(grid[0]))):
                    if(grid[next_x][next_y]==0 and visited[next_x][next_y]==0):
                        stack.append([next_x,next_y])
                        parent[next_x][next_y]=(x,y)

    if found:
        path=path_finder(start,goal,parent)
        print(f"It takes {steps} steps to find a path using DFS")
    else:
        print("No path found")
    return path, steps


# Doctest
if __name__ == "__main__":
    # load doc test
    from doctest import testmod, run_docstring_examples
    # Test all the functions
    testmod()
