class Vertex:
    def __init__(self,key,value=0):
        self.id = key
        self.error_value = value
        self.connectedTo = {}
    
    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight
    
    def __str__(self):
        return str(self.id) +': error_value is '+ str(self.error_value) + ' connectedTo: '+str([x.id for x in self.connectedTo])
    
    def getConnections(self):
        return [x.id for x in self.connectedTo]
    
    def getId(self):
        return self.id
    
    def getValue(self):
        return self.error_value
    
    def getWeight(self,nbr):
        return self.connectedTo[nbr]
    
class Graph:
    def __init__(self):
        self.vertList = {}
        self.edgeList = {}
        self.numVertices = 0
        self.numberEdges = 0
        
    def addVertex(self,key,value):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key,value)
        self.vertList[key]=newVertex
        return newVertex
    
    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None
    
    def __contains__(self,n):
        return n in self.vertList
    
    def addEdge(self,f,t,cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t],cost)
        self.vertList[t].addNeighbor(self.vertList[f],cost)
        self.edgeList[(f,t)] = cost
        self.numberEdges += 1
    
    def getVertices(self):
        return self.vertList.keys()
    
    def getEdges(self):
        return self.edgeList.keys()

    def getEdgeWeight(self,f,t):
        return self.vertList[f].getWeight(self.vertList[t])

    def __iter__(self):
        return iter(self.vertList.values())
qubit_number=5               #量子位数
w=0.1                        #权重
value_error_list=[1.4,3.5,3.3,3.3,3.0]
graph=Graph()
for i in range(qubit_number):
    graph.addVertex(i,value_error_list[i])
graph.addEdge(0,1,0.5)
graph.addEdge(1,2,1.2)
graph.addEdge(1,3,1.0)
graph.addEdge(3,4,1.3)
cluster={}
for i in range(5):
    cluster[i]=i
def Q(graph, cluster):
    e = 0.0
    a_2 = 0.0
    cluster_degree_table = {}
    for vtx in graph.getVertices():
        label = cluster[vtx]
        adj = graph.getVertex(vtx).getConnections()
        for neighbor in adj:
            if label == cluster[neighbor]:
                e += 1
        if label not in cluster_degree_table:
            cluster_degree_table[label] =0
        cluster_degree_table[label] += len(adj)
    e /= 2 * graph.numberEdges
    for label, cnt in cluster_degree_table.items():
        a = 0.5 * cnt / graph.numberEdges
        a_2 += a * a
    Q = e - a_2
    return Q