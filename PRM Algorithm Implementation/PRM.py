# Standard Algorithm Implementation
# Sampling-based Algorithms PRM

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import random
from scipy.spatial import KDTree

# Class for PRM
class PRM:
    # Constructor
    def __init__(self, map_array):
        self.map_array = map_array            # map array, 1->free, 0->obstacle
        self.size_row = map_array.shape[0]    # map size
        self.size_col = map_array.shape[1]    # map size

        self.samples = []                     # list of sampled points
        self.graph = nx.Graph()               # constructed graph
        self.path = []                        # list of nodes of the found path


    def check_collision(self, p1, p2):
        '''Check if the path between two points collide with obstacles
        arguments:
            p1 - point 1, [row, col]
            p2 - point 2, [row, col]

        return:
            True if there are obstacles between two points
        '''
        ### YOUR CODE HERE ###
        line_pts=[p1,p2]
        H=self.dis(p1,p2)
        while len(line_pts)<H*2:
            i=0
            j=1
            while j < len(line_pts):
                line_pts.insert(j,self.get_midpoint(line_pts[i][0],line_pts[i][1],line_pts[j][0],line_pts[j][1]))
                i+=2
                j+=2
        for points in line_pts:
            if (self.map_array[round(points[0]),round(points[1])]==0): 
                return True
        return False

    def get_midpoint(self,row1,col1,row2,col2):
        return (row1+row2)/2,(col1+col2)/2


    def dis(self, point1, point2):
        '''Calculate the euclidean distance between two points
        arguments:
            p1 - point 1, [row, col]
            p2 - point 2, [row, col]

        return:
            euclidean distance between two points
        '''
        ### YOUR CODE HERE ###
        dist=np.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
        return dist


    def uniform_sample(self, n_pts):
        '''Use uniform sampling and store valid points
        arguments:
            n_pts - number of points try to sample, 
                    not the number of final sampled points

        check collision and append valide points to self.samples
        as [(row1, col1), (row2, col2), (row3, col3) ...]
        '''
        # Initialize graph
        self.graph.clear()
        ### YOUR CODE HERE ###
        j=0
        i=0
        for i in range(0,self.size_row,int(self.size_row//np.sqrt(n_pts))):
            for j in range(0,self.size_col,int(self.size_col//np.sqrt(n_pts))):
                    if self.map_array[i][j]==1:
                        self.samples.append((i, j))

    def random_sample(self, n_pts):
        '''Use random sampling and store valid points
        arguments:
            n_pts - number of points try to sample, 
                    not the number of final sampled points

        check collision and append valide points to self.samples
        as [(row1, col1), (row2, col2), (row3, col3) ...]
        '''
        # Initialize graph
        self.graph.clear()

        ### YOUR CODE HERE ###
        for i in range(n_pts):
            row=random.randint(0, self.size_row-1)
            col=random.randint(0, self.size_col-1)
            if self.map_array[row][col]==1 and (row,col) not in self.samples:
                self.samples.append((row, col))


    def gaussian_sample(self, n_pts):
        '''Use gaussian sampling and store valid points
        arguments:
            n_pts - number of points try to sample, 
                    not the number of final sampled points

        check collision and append valide points to self.samples
        as [(row1, col1), (row2, col2), (row3, col3) ...]
        '''
        # Initialize graph
        self.graph.clear()
        for i in range(n_pts):
            row1=random.randint(0, self.size_row-1)
            col1=random.randint(0, self.size_col-1)
            #pick point using gaussian
            row2=np.random.normal(row1,10,1)
            col2=np.random.normal(col1,10,1)
            row2=round(abs(row2[0]))
            col2=round(abs(col2[0]))
                
            if(row2<=self.size_row-1 and col2<=self.size_col-1):

                if (self.map_array[row1][col1]==1 and self.map_array[row2][col2]==1) or (self.map_array[row1][col1]==0 and self.map_array[row2][col2]==0):
                    continue
                # Adding the one with collision free
                elif(self.map_array[row1][col1]==1):
                    self.samples.append((row1, col1))
                else:
                    self.samples.append((row2, col2))
        
            


    def bridge_sample(self, n_pts):
        '''Use bridge sampling and store valid points
        arguments:
            n_pts - number of points try to sample, 
                    not the number of final sampled points

        check collision and append valide points to self.samples
        as [(row1, col1), (row2, col2), (row3, col3) ...]
        '''
        # Initialize graph
        self.graph.clear()
        for i in range(n_pts):
            row1=random.randint(0, self.size_row-1)
            col1=random.randint(0, self.size_col-1)
            if(self.map_array[row1][col1]==0):
                #pick point using gaussian
                row2=np.random.normal(row1,20,1)
                col2=np.random.normal(col1,20,1)
                row2=round(abs(row2[0]))
                col2=round(abs(col2[0]))
                if(row2<=self.size_row-1 and col2<=self.size_col-1):
                    if self.map_array[row2][col2]==0:
                        m_row,m_col=self.get_midpoint(row1,col1,row2,col2)
                        m_row=round(m_row)
                        m_col=round(m_col)
                        if(m_row<=self.size_row-1 and m_col<=self.size_col-1):
                            if self.map_array[m_row][m_col]==1:
                                self.samples.append((m_row,m_col))

    def draw_map(self):
        '''Visualization of the result
        '''
        # Create empty map
        fig, ax = plt.subplots()
        img = 255 * np.dstack((self.map_array, self.map_array, self.map_array))
        ax.imshow(img)

        # Draw graph
        # get node position (swap coordinates)
        node_pos = np.array(self.samples)[:, [1, 0]]
        pos = dict( zip( range( len(self.samples) ), node_pos) )
        pos['start'] = (self.samples[-2][1], self.samples[-2][0])
        pos['goal'] = (self.samples[-1][1], self.samples[-1][0])
        
        # draw constructed graph
        nx.draw(self.graph, pos, node_size=3, node_color='y', edge_color='y' ,ax=ax)

        # If found a path
        if self.path:
            # add temporary start and goal edge to the path
            final_path_edge = list(zip(self.path[:-1], self.path[1:]))
            nx.draw_networkx_nodes(self.graph, pos=pos, nodelist=self.path, node_size=8, node_color='b')
            nx.draw_networkx_edges(self.graph, pos=pos, edgelist=final_path_edge, width=2, edge_color='b')

        # draw start and goal
        nx.draw_networkx_nodes(self.graph, pos=pos, nodelist=['start'], node_size=12,  node_color='g')
        nx.draw_networkx_nodes(self.graph, pos=pos, nodelist=['goal'], node_size=12,  node_color='r')

        # show image
        plt.axis('on')
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        plt.show()


    def sample(self, n_pts=1000, sampling_method="random"):
        '''Construct a graph for PRM
        arguments:
            n_pts - number of points try to sample, 
                    not the number of final sampled points
            sampling_method - name of the chosen sampling method

        Sample points, connect, and add nodes and edges to self.graph
        '''
        # Initialize before sampling
        self.samples = []
        self.graph.clear()
        self.path = []

        # Sample methods
        if sampling_method == "uniform":
            self.uniform_sample(n_pts)
        elif sampling_method == "random":
            self.random_sample(n_pts)
        elif sampling_method == "gaussian":
            self.gaussian_sample(n_pts)
        elif sampling_method == "bridge":
            self.bridge_sample(n_pts)

        ### YOUR CODE HERE ###

        # Find the pairs of points that need to be connected
        # and compute their distance/weight.
        # Store them as
        # pairs = [(p_id0, p_id1, weight_01), (p_id0, p_id2, weight_02), 
        #          (p_id1, p_id2, weight_12) ...]
        pairs = []
        self.kdtree=KDTree(self.samples)
        
        for point_idx in range(len(self.samples)):
            _,idx=self.kdtree.query(self.samples[point_idx],10)
            for i in idx:
                if self.samples[point_idx]==self.samples[i]:
                    continue
                if self.check_collision(self.samples[point_idx],self.samples[i]):
                    continue
                if (point_idx,i,self.dis(self.samples[point_idx], self.samples[i])) not in pairs and (i,point_idx,self.dis(self.samples[point_idx], self.samples[i])) not in pairs :
                    pairs.append((point_idx,i,self.dis(self.samples[point_idx], self.samples[i])))
                
        # Use sampled points and pairs of points to build a graph.
        # To add nodes to the graph, use
        # self.graph.add_nodes_from([p_id0, p_id1, p_id2 ...])
        # To add weighted edges to the graph, use
        # self.graph.add_weighted_edges_from([(p_id0, p_id1, weight_01), 
        #                                     (p_id0, p_id2, weight_02), 
        #                                     (p_id1, p_id2, weight_12) ...])
        # 'p_id' here is an integer, representing the order of 
        # current point in self.samples
        # For example, for self.samples = [(1, 2), (3, 4), (5, 6)],
        # p_id for (1, 2) is 0 and p_id for (3, 4) is 1.
        self.graph.add_nodes_from([i for i in range(len(self.samples))])
        self.graph.add_weighted_edges_from(pairs)

        # Print constructed graph information
        n_nodes = self.graph.number_of_nodes()
        n_edges = self.graph.number_of_edges()
        print("The constructed graph has %d nodes and %d edges" %(n_nodes, n_edges))


    def search(self, start, goal):
        '''Search for a path in graph given start and goal location
        arguments:
            start - start point coordinate [row, col]
            goal - goal point coordinate [row, col]

        Temporary add start and goal node, edges of them and their nearest neighbors
        to graph for self.graph to search for a path.
        '''
        # Clear previous path
        self.path = []

        # Temporarily add start and goal to the graph
        self.samples.append(start)
        self.samples.append(goal)
        # start and goal id will be 'start' and 'goal' instead of some integer
        self.graph.add_nodes_from(['start', 'goal'])

        ### YOUR CODE HERE ###

        # Find the pairs of points that need to be connected
        # and compute their distance/weight.
        # You could store them as
        # start_pairs = [(start_id, p_id0, weight_s0), (start_id, p_id1, weight_s1), 
        #                (start_id, p_id2, weight_s2) ...]
        start_pairs = []
        goal_pairs = []
        _,idx=self.kdtree.query(start,20)
        for i in idx:
            if self.check_collision(start,self.samples[i]):
                continue
            start_pairs.append(('start',i,self.dis(start, self.samples[i])))

        _,idx=self.kdtree.query(goal,20)
        for i in idx:
            if self.check_collision(goal,self.samples[i]):
                continue
            goal_pairs.append(('goal',i,self.dis(goal, self.samples[i])))



        # Add the edge to graph
        self.graph.add_weighted_edges_from(start_pairs)
        self.graph.add_weighted_edges_from(goal_pairs)
        
        # Seach using Dijkstra
        try:
            self.path = nx.algorithms.shortest_paths.weighted.dijkstra_path(self.graph, 'start', 'goal')
            path_length = nx.algorithms.shortest_paths.weighted.dijkstra_path_length(self.graph, 'start', 'goal')
            print("The path length is %.2f" %path_length)
        except nx.exception.NetworkXNoPath:
            print("No path found")
        
        # Draw result
        self.draw_map()

        # Remove start and goal node and their edges
        self.samples.pop(-1)
        self.samples.pop(-1)
        self.graph.remove_nodes_from(['start', 'goal'])
        self.graph.remove_edges_from(start_pairs)
        self.graph.remove_edges_from(goal_pairs)
        