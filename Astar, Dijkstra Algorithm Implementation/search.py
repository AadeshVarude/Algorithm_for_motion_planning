import numpy as np

# Basic searching algorithms
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

def if_valid(next_x,next_y,n_r,n_c):
    if (next_x>=0 and next_y>=0 and next_x<n_r and next_y<n_c):
        return True
def get_next_node(a,visited,n):
    d=a.copy()
    d[np.where(visited)]=np.Inf
    ind=np.argmin(d)
    x=ind // n
    y=ind % n
    return x,y

# Class for each node in the grid
class Node:
    def __init__(self, row, col, is_obs, h):
        self.row = row        # coordinate
        self.col = col        # coordinate
        self.is_obs = is_obs  # obstacle?
        self.g = None         # cost to come (previous g + moving cost)
        self.h = h            # heuristic
        self.cost = None      # total cost (depend on the algorithm)
        self.parent = None    # previous node

def dijkstra(grid, start, goal):
    '''Return a path found by Dijkstra alogirhm 
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
    >>> dij_path, dij_steps = dijkstra(grid, start, goal)
    It takes 10 steps to find a path using Dijkstra
    >>> dij_path
    [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1]]
    '''
    ### YOUR CODE HERE ###
    # we need to make a new grid where we create a cost map for processing the data
    new_grid=np.array(grid).copy()
    #Make the obstacels with higher values 10000
    new_grid*=10000
    # Make every other node as one
    new_grid=new_grid+np.ones((len(grid),len(grid[0])))

    # now we have a new grid that has the hueristi cost map for processing
    path = []
    steps = 0
    found = False
    # parent array for backtracking
    parent=np.negative(np.ones((len(grid),len(grid[0])),dtype=object))
    # marking the visited nodes
    visited=np.zeros((len(grid),len(grid[0])))
    
    # The distance map
    dist=np.ones((len(grid),len(grid[0])))*np.Inf

    # direction priority for exploration
    r=[[0, 1], [1, 0], [0, -1], [-1, 0]]
    
    # set source as zero
    new_grid[start[0]][start[1]]=0
    dist[start[0]][start[1]]=0
    x,y=start
    while True:
        steps+=1
        if grid[goal[0]][goal[1]]==1 or grid[start[0]][start[1]]==1 :
            break
        if([x,y]==[goal[0],goal[1]]):
            found=True
            break 
        for i in r:
            next_x=x+i[0]
            next_y=y+i[1]
            if(if_valid(next_x,next_y,len(grid),len(grid[0])) and grid[next_x][next_y]==0):
                if(visited[next_x][next_y]==0):
                    distance=dist[x][y]+new_grid[next_x][next_y] # if not visited calculate the distance
                    if distance < dist[next_x][next_y]:
                        dist[next_x][next_y]=distance
                    if(parent[next_x][next_y]==-1):
                        parent[next_x][next_y]=(x,y)
        visited[x][y]=1
        
        #selecting next_x and Next_y
        x,y=get_next_node(dist,visited,new_grid.shape[0])
    if found:
        path=path_finder(start,goal,parent)
        print(f"It takes {steps} steps to find a path using Dijkstra")
    else:
        print("No path found")
    return path, steps


def astar(grid, start, goal):
    '''Return a path found by A* alogirhm 
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
    >>> astar_path, astar_steps = astar(grid, start, goal)
    It takes 7 steps to find a path using A*
    >>> astar_path
    [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1]]
    '''
    new_grid=np.array(grid).copy()
    #Make the obstacels with higher values 10000
    new_grid*=10000
    # Make every other node as one
    new_grid=new_grid+np.ones((len(grid),len(grid[0])))

    # now we have a new grid that has the hueristi cost map for processing
    path = []
    steps = 0
    found = False
    # parent array for backtracking
    parent=np.negative(np.ones((len(grid),len(grid[0])),dtype=object))
    # marking teh visited nodes
    visited=np.zeros((len(grid),len(grid[0])))
    
    # Initialising the g and the f map values
    g=np.ones((len(grid),len(grid[0])))*0
    f=np.ones((len(grid),len(grid[0])))*np.Inf

    # direction priority for exploration
    r=[[0, 1], [1, 0], [0, -1], [-1, 0]]
    
    # set source as zero
    new_grid[start[0]][start[1]]=0
    g[start[0]][start[1]]=0
    f[start[0]][start[1]]=0
    x,y=start
    while True:
        steps+=1
        if grid[goal[0]][goal[1]]==1 or grid[start[0]][start[1]]==1:
            break
        if([x,y]==[goal[0],goal[1]]):
            found=True
            break
        for i in r:
            steps+=1
            next_x=x+i[0]
            next_y=y+i[1]
            if(if_valid(next_x,next_y,len(grid),len(grid[0])) and grid[next_x][next_y]==0):
                if(visited[next_x][next_y]==0 ):
                    g_val=g[x][y]+new_grid[next_x][next_y] # if not visited calculate the distance
                    h_val=abs(next_x-goal[0])+abs(next_y-goal[1])
                    f_val=g_val+h_val # calculate the f value
                    g[next_x][next_y]=g_val # update the g value
                    if f_val < f[next_x][next_y]:
                        f[next_x][next_y]=g_val+h_val # update the f value
                    if(parent[next_x][next_y]==-1):
                        parent[next_x][next_y]=(x,y) # adding the parent node
        visited[x][y]=1
        
        #selecting next_x and Next_y
        x,y=get_next_node(f,visited,new_grid.shape[0])
        
    if found:
        path=path_finder(start,goal,parent)
        print(f"It takes {steps} steps to find a path using A*")
    else:
        print("No path found")
    return path, steps



# Doctest
if __name__ == "__main__":
    # load doc test
    from doctest import testmod, run_docstring_examples
    # Test all the functions
    testmod()
