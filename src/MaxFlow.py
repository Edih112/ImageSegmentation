
import numpy as np
from copy import copy, deepcopy



class MaxFlow: 
    #@param graph is an input numpy nxn matrix, where the first elementon diagonal is s
    # and the last element on the diagonal is t, 
    # and the rest of the graph is the adjacency matrix of the flow network
    def __init__(self, graph, s, t):
        self.graph = graph
        self.graph_length = graph.shape[0]
        self.s = s #tap node
        self.t = t #sink node
        self.res_graph = deepcopy(graph) #residual graph

    def getMaxFlow(self):
        #find augmenting path from s to t
        augment_paths = self.findAugmentPaths()

        augment_path = []
        if (augment_paths != []):
            augment_path = augment_paths[0]
            for i in range(1, len(augment_paths)):
                if (len(augment_paths[i]) < len(augment_path)):
                    augment_path = augment_paths[i]

        # keep updating residual graph while 
        # an augmenting path still exists
        while (len(augment_path) > 0):
            #find min capacity edge 
            # from found augmenting path
            min_cap = None
            for i in range(len(augment_path) - 1):
                if (min_cap == None or self.res_graph[augment_path[i], augment_path[i+1]] < min_cap):
                    min_cap = self.res_graph[augment_path[i], augment_path[i+1]]
            
            #update residual graph
            for i in range(0, len(augment_path) - 1):
                self.res_graph[augment_path[i], augment_path[i + 1]] = self.res_graph[augment_path[i], augment_path[i + 1]] - min_cap

            #find new augmenting path
            augment_paths = self.findAugmentPaths()

            augment_path = []
            if (augment_paths != []):
                augment_path = augment_paths[0]
                for i in range(1, len(augment_paths)):
                    if (len(augment_paths[i]) < len(augment_path)):
                        augment_path = augment_paths[i]


        cut = [0]*self.graph_length 
        self.getCutEdges(self.s, cut)
        return self.cutEdgeCapacitySum(cut)
    

    #@params cut: the list of all vertices in the S cut,
    #             where cut[i] = 1 if vertex i is in the cut S, else 0
    def cutEdgeCapacitySum(self, cut):
        cut_set = set()
        
        #transfer all vertices in cut to a set
        for i in range(0, len(cut)):
            if (cut[i] == 1):
                cut_set.add(i)

        #find max flow, these are all edges that are reachable within the set S
        max_flow = 0

        for vertex in cut_set:
            for i in range(0, self.graph_length):
                if (not (i in cut_set)):
                    max_flow += self.graph[vertex, i]

        return max_flow


    # searches through residual graph to get all vertices
    # in the cut S in format where cut[i] = 1 if vertex i is in S
    # else cut[i] = 0
    def getCutEdges(self, curr_edge, cut):
        if (cut[curr_edge] == 0):
            cut[curr_edge] = 1

            for i in range(1, self.graph_length):
                if (self.res_graph[curr_edge, i] > 0):
                    self.getCutEdges(i, cut)
    
    # performs a DFS over the residual graph
    # @returns [flow, vert1, vert2,...vertn] if a path from s to t exists, 
    #          []                            if no path exists
    def findAugmentPaths(self):
        # set first element of path as the flow along the path
        paths = []
        path = []
        # set of visited vertices
        visited = set()
        self.augmentPathHelper(self.s, paths, deepcopy(path), visited)
        return paths


    def augmentPathHelper(self, currVertex, paths, path, visited):
    
        if (currVertex == self.t):
            # path to t has been found case
            path.append(self.t)
            paths.append(path)
        else:
            # only keep searching if 
            # currVertex has not been searched yet
            if ((currVertex in visited) == False):
                #recurse down residual looking for a path
                for i in range(1, self.graph_length):
                    # print(path, ", ", currVertex, ", ", i, ", ", self.res_graph[currVertex, i])
                    # if ("" + str(path) +", " + str(currVertex)+ ", "+ str(i)+ ", "+ str(self.res_graph[currVertex, i]) == "[0, 1], 3, 5, 20"):
                    #     print("help")
                    #     x = 10

                    if (self.res_graph[currVertex, i] > 0):

                        copy_visited = deepcopy(visited)
                        copy_visited.add(currVertex)
                        copy_path = deepcopy(path)
                        copy_path.append(currVertex)
                        self.augmentPathHelper(i, paths, copy_path, copy_visited)

    







# matrix = np.array([[0,10,10,0,0,0],
#                        [0,0,2,4,8,0],
#                        [0,0,0,0,9,0],
#                        [0,0,0,0,0,10],
#                        [0,0,0,6,0,10],
#                        [0,0,0,0,0,0]])

# mf = MaxFlow(np.array([[0,10,10,0,0,0],
#                        [0,0,2,4,8,0],
#                        [0,0,0,0,9,0],
#                        [0,0,0,0,0,10],
#                        [0,0,0,6,0,10],
#                        [0,0,0,0,0,0]]))
# print(mf.getMaxFlow())
# mf = MaxFlow(matrix)
# print(mf.getMaxFlow())