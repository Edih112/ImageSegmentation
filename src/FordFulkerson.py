
import numpy as np
from copy import deepcopy
from collections import deque


class FordFulkerson: 
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
        la = 2048
        while (la >= 1):
            #find augmenting path from s to t
            augment_path = self.findAugmentPaths(la)

            count = 0

            # keep updating residual graph while 
            # an augmenting path still exists
            while (len(augment_path) > 1):
                count += 1
                # get max flow along path which is first element value
                min_cap = augment_path[0]
                
                #update residual graph, augment path vertices are index 1=>end
                for i in range(1, len(augment_path) - 1):
                    self.res_graph[augment_path[i]][augment_path[i + 1]] = self.res_graph[augment_path[i]][augment_path[i + 1]] - min_cap

                augment_path.clear()
                #find new augmenting path
                augment_path = self.findAugmentPaths(la)

            print(la, "lambda done ", count, " paths found")
            la = la // 2
        
        self.cut = self.getCut()
        self.maxFlow = self.cutEdgeCapacitySum(self.cut)

        return self.maxFlow
    
    def getCut(self):
        queue = deque()
        visited = [0]*self.graph_length
        queue.append(self.s)

        while queue:
            vertex = queue.popleft()
            visited[vertex] = 1

            for neighbor, weight in self.res_graph[vertex].items():
                if (weight > 0 and visited[neighbor] == 0):
                    queue.append(neighbor)
        return visited
    

    #@params cut: the list of all vertices in the S cut,
    #             where cut[i] = 1 if vertex i is in the cut S, else 0
    def cutEdgeCapacitySum(self, cut):
        #find max flow, these are all edges that are reachable within the set S
        max_flow = 0
        for i in range(len(cut)):
            if cut[i] == 1:
                for n, w in self.res_graph[i].items():
                    if cut[n] == 0:
                        max_flow += self.graph[i][n]

        return max_flow
    
    # performs a DFS over the residual graph
    # @returns [flow, vert1, vert2,...vertn] if a path from s to t exists, 
    #          []                            if no path exists
    def findAugmentPaths(self, minFlow):
        path = self.augmentPathHelperIterativeBFS(self.s, minFlow)
        #self.augmentPathHelperRecursive(self.s, paths, deepcopy(path), visited)
        return path

    # returns path if one is found, otherwise returns a single elemtn list
    # containing the set of all visited nodes, ie the min cut when no path is found
    def augmentPathHelperIterativeBFS(self, startVertex, minFlow):
        queue = deque()
        searched = {}

        queue.append((startVertex, -1))

        # while queue is not empty
        while queue:
            curr, prev = queue.popleft()
            searched[curr] = prev

            if (curr == self.t):
                # build up augment path, finding maxflow along path at the same time
                min_cap = self.res_graph[prev][curr]
                result = [curr]
                # while a previosu vertex exists
                while prev != -1:
                    # update max flow along path
                    if (min_cap > self.res_graph[prev][curr]):
                        min_cap = self.res_graph[prev][curr]
                    # add previous vertex to list
                    result.append(prev)
                    curr = prev
                    prev = searched[prev]

                # add maxflow to list
                result.append(min_cap)
                # return the reversed list, of [maxFlow, v1, v2, ..., vn]
                return result[::-1]
            else:
                for neighbor, weight in self.res_graph[curr].items():
                    if (weight >= minFlow and (neighbor not in searched.keys())):
                        queue.append((neighbor, curr))
        return []
