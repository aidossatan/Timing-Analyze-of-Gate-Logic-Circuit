from collections import defaultdict 

#CLASS 'NODE' STARTS FROM HERE 
class Node:
    def __init__(self, name, Nodetype, pD, sT=0, hT=0):
        self.name = name
        self.type = Nodetype
        self.propogationDelay = pD
        self.setupTime = sT
        self.holdTime = hT

    def setNodeName(self, name):
        self.name = name
        return True

    def getNodeType(self):
        return self.type

#CLASS 'NETLIST' STARTS FROM HERE 
class netlist:
    def __init__(self):
        self.graph = defaultdict(list) 
        self.type = defaultdict(str) 
        self.pD = defaultdict(int) 
        self.sT = defaultdict(int) 
        self.hT = defaultdict(int) 
        self.nodeDistance = []
    
    # save all parameters of Node object
    def add(self, parent, *nodes):
        self.type[parent.name] = parent.type 
        self.pD[parent.name]= parent.propogationDelay
        self.sT[parent.name] = parent.setupTime 
        # self.hT[parent.name] = parent.holdTime 
        for node in nodes:
            if node.name not in self.graph[parent.name]:
                self.graph[parent.name].append(node.name) 
        return True
    
    #method timingAnalyze
    def timingAnalyze(self, s):
        self.find_path(s)
        max_v = 0
        print(f"Input: ", s)
        print("Outputs: ", end=" ")
        for path in self.nodeDistance:
            print(path[len(path)-1], end=" ")
        print("\n")
        for path in self.nodeDistance:
            res = 0
            n = len(path)
            for i in range(n-1):
                if self.type[path[i]] == "GATE":
                    res += self.pD[path[i]]
                elif self.type[path[i]] == "FF":
                    res += self.pD[path[i]]
            res += self.sT[path[n-1]]  #last FF in path
            if res > max_v:
                max_v = res
            print(f"Path: ", path, end=" ")
            print(f"Delay: ", res, f"Combo_max: ", 0)
        print(f"\nF_max: ", 1/max_v)

    def find_path(self, start, path=[]):
        path = path + [start]
        if self.type[start] == "FF" and len(path) > 1:
            self.nodeDistance.append(path)
        if not self.graph[start]:
            return None
        for node in self.graph[start]:
            if node not in path:
                newpath = self.find_path(node, path)
                if newpath: return newpath

    def show(self):
        print(self.graph)

#main part
node1 = Node("FF1", "FF", 3, 5, 1)
node2 = Node("AND1", "GATE", 2)
node3 = Node("OR1", "GATE", 3)
node4 = Node("OR2", "GATE", 3)
node5 = Node("FF2", "FF", 3, 5, 1)
node6 = Node("FF3", "FF", 3, 5, 1)
graph = netlist()
graph.add(node1, node2)
graph.add(node2, node3, node4, node1)
graph.add(node3, node5, node2)
graph.add(node4, node2, node6)
graph.add(node5, node3)
graph.add(node6, node4)
graph.timingAnalyze('FF1')
# graph.show()