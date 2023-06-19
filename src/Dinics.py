from copy import deepcopy

class Dinics:

    def __init__(self, graph, s, t):
        self.graph = graph
        self.s = s #tap node
        self.t = t #sink node
        self.res_graph = deepcopy(graph) #residual graph
        self.levels = [0]*(len(self.graph))

    def initiateAlgorithm(self):
        
        self.getLevelGraph()
    
    def sendFlow():
        pass

    def getLevelGraph(self):
        # initially all levels are -1
        for i in range(len(self.levels)):
            self.levels[i] = -1

        # BFS over residual graph assigning levels
        queue = []
        queue.append(self.s)
        prev = {}
        prev[self.s] = None
        
        while queue:
            curr = queue.pop(0)
            # no need to check if curr is unvisited since only unvisited are pushed on
            # set level to +1 on level of parent
            if (prev[curr] == None):
                # if is s node
                self.levels[curr] = 0
            else:
                self.levels[curr] = self.levels[prev[curr]]
            
            for neighbor, weight in self.res_graph[curr].items():
                # if neighbor is unvisited and has positive cap
                if self.levels[neighbor] == -1 and weight > 0:
                    queue.append(neighbor)
                    prev[neighbor] = curr

        return self.levels[self.t] >= 0 # if self.t was reached from self.s

        
