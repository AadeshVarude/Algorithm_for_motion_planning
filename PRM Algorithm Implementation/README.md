# RBE 550 - Standard Search Algorithms Implementation

## Overview

In this assignment, you are going to implement **PRM** algorithm. You are required to implement 4 different sampling methods - **uniform sampling**, **random sampling**, **gaussian sampling** and **bridge sampling**. This template is provided to you as a starting point. After you finish coding, you would be able to run these algorithms to find a path in a map, and visualize the result.

Files included:

**PRM.py** is the file where you will implement a PRM class with four different sampling methods.

**main.py** is the scrip that provides helper functions that load the map from an image and call the classes and functions from **PRM.py**. You are not required to modify anything but you are encouraged to understand the code.

**WPI_map.jpg** is a binary WPI map image with school buildings. You could replace it with some other maps you prefer.

## Instruction

Before starting any coding, please run the code first:

`python main.py`

The **main.py** loads the map image **WPI_map.jpg** and calls classes and functions to run planning tasks. As you haven't written anything yet, there should be no path shown in the graph, but only the map image, start point and end point.

Please keep in mind that, the coordinate system used here is **[row, col]**, which is different from [x, y] in Cartesian coordinates. In README and the code comment, when the word '**point**' is used, it refers to a simple list [row, col]. When the word '**node**' or '**vertex**' is used, it refers to a node/vertex in a graph. 

## PRM

The two main phases of PRM are **Learning Phase** and **Query Phase**. 

#### Learning Phase

You would code **Learning Phase** in the function `sample`, where it samples points in the map according to different strategy, and connect these points to build a graph. In this template, the graph library [Networkx](https://networkx.org/documentation/stable/) is used to store the result graph. 

There are four different sampling methods to be implemented - `uniform_sample`, `random_sample`, `gaussian_sample` and `bridge_sample`. Please refer to the lectures and make sure you understand the ideas behind these sampling methods before coding. 

After sampling, you would need to connect these sampling points to theirs k nearest neighbors. To find their neighbors, you should NOT just use brutal force algorithm (This will take way too long), but use K-D tree as mentioned in the class. Here is an [example](https://stackoverflow.com/questions/13796782/networkx-random-geometric-graph-implementation-using-k-d-trees) of how to use scipy K-D tree structure. 

Finally, you will need to use all the sampled points and their connection with neighbors as nodes and edges to build a Networkx graph.

#### Query Phase

You would code **Query Phase** in the function `search`, where it search for a path in the constructed graph given a start and goal point.

As start and goal points are not connected to the graph, you will first need to add the start and goal node, find their nearest neighbors in the graph and connect them to these two nodes. Practically, as some of the graphs don't have a good connectivity, we will not only connect the start and goal node to their nearest node, but all the nodes within a certain distance, in order to increase the chance of finding a path.

Having connected start and goal node in the graph, we could use Dijkstra algorithm or any other algorithms we learn before to search for a valid path. This part is similar to the first assignment, so is already done by using the Dijkstra function Networkx provided.

Finally, as PRM is a multi-query planning algorithms, one could call `search` with other start and goal point. So the previous start and goal nodes and their edges need to be removed in the end of each query phase. This part is also implemented already.

Read the description of the functions for more details before implementing.

---

Until now, I hope you have a basic understanding of the template code and what to do next. 

This template is only provided as a starting point, feel free to make any modification of the codes or code structures if needed. After you finish coding, your algorithms should produce similar results as the images in **demo** folder.

## Rubrics

- (5 pts) Your PRM is implemented correctly

  - Four sampling methods produce the correct sampling points
  - Connect the sampling points, start and goal into a graph using a proper method
  
  - Given start and goal, find a path if feasible.
  
  ---

- (2 pts) Documentation

  Besides the code, you should also include a documentation with the following content:

  - Briefly answer the following question

    - For PRM, what are the advantages and disadvantages of the four sampling methods in comparison to each other?
    
  - Algorithm results and explanation
    
    Run your code with `python main.py` and **save your results as png images**. Briefly explain why your algorithms would produce these results.
    
  - Reference paper and resources if any
  
  Include the documentation as a pdf file, or if you prefer, a md file.
  
  

