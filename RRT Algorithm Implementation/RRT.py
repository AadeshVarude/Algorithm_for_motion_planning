# Standard Algorithm Implementation
# Sampling-based Algorithms RRT and RRT*

import matplotlib.pyplot as plt
import numpy as np
import math as m


# Class for each tree node
class Node:
    def __init__(self, row, col):
        self.row = row        # coordinate
        self.col = col        # coordinate
        self.parent = None    # parent node
        self.cost = 0.0       # cost


# Class for RRT
class RRT:
    # Constructor
    def __init__(self, map_array, start, goal):
        self.map_array = map_array            # map array, 1->free, 0->obstacle
        self.size_row = map_array.shape[0]    # map size
        self.size_col = map_array.shape[1]    # map size

        self.start = Node(start[0], start[1]) # start node
        self.goal = Node(goal[0], goal[1])    # goal node
        self.vertices = []                    # list of nodes
        self.found = False                    # found flag

    def init_map(self):
        '''Intialize the map before each search
        '''
        self.found = False
        self.vertices = []
        self.vertices.append(self.start)
    
    def dis(self, node1, node2):
        return np.sqrt((node1.row-node2.row)**2+(node1.col-node2.col)**2)
    def get_midpoint(self,row1,col1,row2,col2):
        return (row1+row2)/2,(col1+col2)/2

    def check_collision(self, node1, node2):
        ### YOUR CODE HERE ###
        line_pts=[[node1.row,node1.col],[node2.row,node2.col]]
        H=self.dis(node1,node2)
        while len(line_pts)<H*2:
            i=0
            j=1
            while j < len(line_pts):
                line_pts.insert(j,self.get_midpoint(line_pts[i][0],line_pts[i][1],line_pts[j][0],line_pts[j][1]))
                i+=2
                j+=2
        for points in line_pts:
            if (self.map_array[int(points[0]),int(points[1])]==0): 
                return True
        return False
    def get_new_node_without_collision(self,node1,node2,stepsize=10):
        x1=node1.row
        x2=node2.row
        y1=node1.col
        y2=node2.col
        angle = m.atan2(y2-y1, x2-x1)
        new_x=x1+stepsize*np.cos(angle)
        new_y=y1+stepsize*np.sin(angle)
        if new_x>self.size_row:
            new_x=self.size_row-1
        if new_y>self.size_col:
            new_y=self.size_col-1
        new_node=Node(new_x,new_y)
        # check collision from node to the exploration goal
        # print(new_y,new_x)
        if(self.check_collision(new_node,node1)):

            node_connection=False
        else:
            node_connection=True
        
        # check collision from node to the goal
        if(self.check_collision(new_node,self.goal)):
            goal_connection=False
        else:
            goal_connection=True
        return new_node,node_connection,goal_connection

    def get_new_point(self, goal_bias):
        new_x=np.random.randint(0,self.size_row-1)
        new_y=np.random.randint(0,self.size_col-1)
        new_node=Node(new_x,new_y)
        return new_node

    
    def get_nearest_node(self, point):
        '''Find the nearest node in self.vertices with respect to the new point
        arguments:
            point - the new point

        return:
            the nearest node
        '''
        ### YOUR CODE HERE ###
        min_distance=np.inf
        for i in self.vertices:
            dist=self.dis(point,i)
            if dist<min_distance:
                n_node=i
                min_distance=dist

        return n_node


    def get_neighbors(self, new_node, neighbor_size):
        '''Get the neighbors that are within the neighbor distance from the node
        arguments:
            new_node - a new node
            neighbor_size - the neighbor distance

        return:
            neighbors - a list of neighbors that are within the neighbor distance 
        '''
        ### YOUR CODE HERE ###
        neighbor_nodes=[]
        for i in self.vertices:
            if self.dis(new_node,i)<neighbor_size:
                neighbor_nodes.append(i)
        return neighbor_nodes


    def rewire(self, new_node, neighbors):
        '''Rewire the new node and all its neighbors
        arguments:
            new_node - the new node
            neighbors - a list of neighbors that are within the neighbor distance from the node

        Rewire the new node if connecting to a new neighbor node will give least cost.
        Rewire all the other neighbor nodes.
        '''
        ### YOUR CODE HERE ###
        # print("in rewire")
        for i in neighbors:
            distance=self.dis(i,new_node)
            new_cost=new_node.cost+distance
            if i.cost>new_cost:
                if self.check_collision(i,new_node)==False:
                    # print("changing parent")
                    i.cost=new_cost
                    i.parent=new_node

    
    def draw_map(self):
        '''Visualization of the result
        '''
        # Create empty map
        fig, ax = plt.subplots(1)
        img = 255 * np.dstack((self.map_array, self.map_array, self.map_array))
        ax.imshow(img)

        # Draw Trees or Sample points
        for node in self.vertices[1:-1]:
            plt.plot(node.col, node.row, markersize=3, marker='o', color='y')
            plt.plot([node.col, node.parent.col], [node.row, node.parent.row], color='y')
        
        # Draw Final Path if found
        if self.found:
            cur = self.goal
            while cur.col != self.start.col or cur.row != self.start.row:
                plt.plot([cur.col, cur.parent.col], [cur.row, cur.parent.row], color='b')
                cur = cur.parent
                plt.plot(cur.col, cur.row, markersize=3, marker='o', color='b')

        # Draw start and goal
        plt.plot(self.start.col, self.start.row, markersize=5, marker='o', color='g')
        plt.plot(self.goal.col, self.goal.row, markersize=5, marker='o', color='r')

        # show image
        plt.show()


    def RRT(self, n_pts=1000):
        '''RRT main search function
        arguments:
            n_pts - number of points try to sample, 
                    not the number of final sampled points

        In each step, extend a new node if possible, and check if reached the goal
        '''
        # Remove previous result
        self.init_map()
        
        ### YOUR CODE HERE ###
        for i in range(n_pts):
            exp_node=self.get_new_point(0)
            n_node=self.get_nearest_node(exp_node)
            # print("exp_node",exp_node.row,exp_node.col)
            # print("n_node",n_node.row,n_node.col)
            new_node,node_connection,goal_connection=self.get_new_node_without_collision(n_node,exp_node)
            if(node_connection and goal_connection and self.dis(new_node,self.goal)<=15): # checking collision for the nearest neighbour and the new node
                # print("direct goal found")
                new_node.parent=n_node
                new_node.cost=new_node.parent.cost+self.dis(new_node,n_node)
                self.vertices.append(new_node)
                
                # if(self.found== False): # uncomment this is you wnat ot explore for all the n_pts, otherwise if goal found you can stop the search but for optima path you do it for all n_pts.
                self.goal.parent=new_node
                self.goal.cost=self.goal.parent.cost+self.dis(new_node,self.goal)
                self.vertices.append(self.goal)
                self.found=True
                break 
                    
            elif(node_connection):
                # print("node cosnnection found")
                new_node.parent=n_node
                new_node.cost=new_node.parent.cost+self.dis(new_node,n_node)
                self.vertices.append(new_node)
            else:
                continue
        # self.found=False
        # Output
        if self.found:
            steps = len(self.vertices) - 2
            length = self.goal.cost
            print("It took %d nodes to find the current path" %steps)
            print("The path length is %.2f" %length)
        else:
            print("No path found")
        
        # Draw result
        self.draw_map() 


    def RRT_star(self, n_pts=1000, neighbor_size=20):
        '''RRT* search function
        arguments:
            n_pts - number of points try to sample, 
                    not the number of final sampled points
            neighbor_size - the neighbor distance
        
        In each step, extend a new node if possible, and rewire the node and its neighbors
        '''
        # Remove previous result
        self.init_map()
        ### YOUR CODE HERE ###
        for i in range(n_pts):
            exp_node=self.get_new_point(0)
            n_node=self.get_nearest_node(exp_node)
            new_node,node_connection,goal_connection=self.get_new_node_without_collision(n_node,exp_node)
            if(node_connection and goal_connection and self.dis(new_node,self.goal)<=10): # checking collision for the nearest neighbour and the new node
                #Find the parent node with the least cost in the neighbor hood
                neighbor_nodes=self.get_neighbors(new_node,neighbor_size)
                min_parent_node=n_node
                new_node.parent=min_parent_node
                min_cost=new_node.parent.cost+self.dis(new_node,n_node)
                for i in neighbor_nodes:
                    if self.check_collision(i,new_node)==False:
                        distance=self.dis(i,new_node)
                        new_cost=i.cost+distance
                        if new_cost<min_cost:
                                min_parent_node=i
                                min_cost=new_cost
                new_node.parent=min_parent_node
                new_node.cost=min_cost
                self.vertices.append(new_node)
                self.rewire(new_node, neighbor_nodes)

                if(self.found== False):
                    neighbor_nodes=self.get_neighbors(self.goal,neighbor_size)
                    min_parent_node=new_node
                    self.goal.parent=min_parent_node
                    min_cost=self.goal.parent.cost+self.dis(self.goal,n_node)
                    for i in neighbor_nodes:
                        if self.check_collision(i,self.goal)==False:
                            distance=self.dis(i,self.goal)
                            new_cost=i.cost+distance
                            if new_cost<min_cost:
                                    min_parent_node=i
                                    min_cost=new_cost
                    self.goal.parent=min_parent_node
                    self.goal.cost=min_cost
                    self.vertices.append(self.goal)
                    self.found=True
                    
            elif(node_connection):
                neighbor_nodes=self.get_neighbors(new_node,neighbor_size)
                #Find the parent node with the least cost in the neighbor hood
                min_parent_node=n_node
                new_node.parent=min_parent_node
                min_cost=new_node.parent.cost+self.dis(new_node,n_node)
                for i in neighbor_nodes:
                    if self.check_collision(i,new_node)==False:
                        distance=self.dis(i,new_node)
                        new_cost=i.cost+distance
                        if new_cost<min_cost:
                                min_parent_node=i
                                min_cost=new_cost
                new_node.parent=min_parent_node
                new_node.cost=min_cost
                self.vertices.append(new_node)
                self.rewire(new_node, neighbor_nodes)
            else:
                continue

        # Output
        if self.found:
            steps = len(self.vertices) - 2
            length = self.goal.cost
            print("It took %d nodes to find the current path" %steps)
            print("The path length is %.2f" %length)
        else:
            print("No path found")

        # Draw result
        self.draw_map()
