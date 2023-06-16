
import numpy as np
from copy import deepcopy

# will need to create a class to abstract away the representation of a flow network
class FlowNetGraph:
    pass


class MaxFlowAdjList: 
    #@param graph is an input adjacency list, where graph[i] is a pair (vertex_j, w) 
    #             that defines the edge i->j with weight w
    #             Additionally, for simplicity no numpy arrays are used for this representation, 
    #             and each adjacency list index should store a dictionary
    #
    # and the last element on the diagonal is t, 
    # and the rest of the graph is the adjacency matrix of the flow network
    # s and t must correspond to existing index  (vertex) in the adjacency list
    def __init__(self, graph, s, t):
        self.graph = graph
        self.graph_length = len(graph)
        self.s = s #tap node
        self.t = t #sink node
        self.res_graph = deepcopy(graph) #residual graph
        self.cut  = []
        self.maxFlow = None

    def getMinCut(self):
        if (self.cut == []):
            self.getMaxFlow()
        return self.cut

    # NEED to make this capcity scaling, otherwise runtime is painful
    def getMaxFlow(self):
        if (self.maxFlow == None):
            #find augmenting path from s to t
            augment_path = self.findAugmentPaths()

            # keep updating residual graph while 
            # an augmenting path still exists
            while (len(augment_path) > 0):
                # find min capacity edge 
                # from found augmenting path
                
                min_cap = None
                for i in range(len(augment_path) - 1):
                    if (min_cap == None or self.res_graph[augment_path[i]][augment_path[i+1]] < min_cap):
                        min_cap = self.res_graph[augment_path[i]][augment_path[i+1]]

                # print(augment_path)
                # print("")

                #update residual graph
                for i in range(0, len(augment_path) - 1):
                    self.res_graph[augment_path[i]][augment_path[i + 1]] = self.res_graph[augment_path[i]][augment_path[i + 1]] - min_cap

                #find new augmenting path
                augment_path = self.findAugmentPaths()

            self.cut = [0]*self.graph_length 
            self.getCutEdgesIterative(self.cut)
            self.maxFlow = self.cutEdgeCapacitySum(self.cut)
        return self.maxFlow

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
            for i, w in self.res_graph[vertex].items():
                if (not (i in cut_set)):
                    max_flow += self.graph[vertex][i]

        return max_flow


    def getCutEdgesIterative(self, cut):
        queue = [self.s]

        while queue:
            vert = queue.pop(0)
            if (cut[vert] == 0):
                cut[vert] = 1
                for neighbor, weight in self.res_graph[vert].items():
                    if (weight > 0):
                        queue += [neighbor]

    # searches through residual graph to get all vertices in 
    # the cut S in format where cut[i] = 1 if vertex i is in S
    # else cut[i] = 0
    def getCutEdgesRecursive(self, curr_edge, cut):
        if (cut[curr_edge] == 0):
            cut[curr_edge] = 1

            for j, w in self.res_graph[curr_edge].items():
                if (w > 0):
                    self.getCutEdgesRecursive(j, cut)

            # for i in range(1, self.graph_length):
            #     if (self.res_graph[curr_edge, i] > 0):
            #         self.getCutEdges(i, cut)

    
    # performs a DFS over the residual graph
    # @returns [flow, vert1, vert2,...vertn] if a path from s to t exists, 
    #          []                            if no path exists
    def findAugmentPaths(self):
        paths = self.augmentPathHelperIterativeBFS(self.s)
        #self.augmentPathHelperRecursive(self.s, paths, deepcopy(path), visited)
        return paths
    
    def augmentPathHelperRecursive(self, currVertex, paths, path, visited):
    
        if (currVertex == self.t):
            # path to t has been found case
            path.append(self.t)
            paths.append(path)
        else:
            # only keep searching if 
            # currVertex has not been searched yet
            if ((currVertex in visited) == False):
                #recurse down residual looking for a path
                for j, w in self.res_graph[currVertex].items():
                    edge_weight = w
                    dest_vert = j
                    if (edge_weight > 0):
                        copy_visited = deepcopy(visited)
                        copy_visited.add(currVertex)
                        copy_path = deepcopy(path)
                        copy_path.append(currVertex)
                        self.augmentPathHelperRecursive(dest_vert, paths, copy_path, copy_visited)

    def augmentPathHelperIterativeBFS(self, startVertex):
        visited = set()
        queue = []
        searched = {}

        queue.append((startVertex, None))
        visited.add(startVertex)

        # while queue is not empty
        while queue:
            curr, prev = queue.pop(0)
            if curr not in searched:
                searched[curr] = prev

                if (curr == self.t):
                    result = [curr]
                    while prev is not None:
                        result.append(prev)
                        prev = searched[prev]
                    return result[::-1]
                else:
                    # if (curr >= len(self.res_graph)):
                    #     #print(curr, ", " , len(self.res_graph))
                    #     break
    
                    for neighbor, weight in self.res_graph[curr].items():
                        if (weight > 0):
                            queue += [(neighbor, curr)]
        return []




class MaxFlowAdjMatrix: 
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
                    max_flow += self.graph[vertex][i]

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
                    if (self.res_graph[currVertex, i] > 0):
                        copy_visited = deepcopy(visited)
                        copy_visited.add(currVertex)
                        copy_path = deepcopy(path)
                        copy_path.append(currVertex)
                        self.augmentPathHelper(i, paths, copy_path, copy_visited)


    
