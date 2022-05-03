# python3
import json
from lib2to3.pytree import Leaf
import logging
import sys
import time
import os
from typing import Dict, List, Optional, Any
sys.path.insert(0,"C:\\Users\\86178\\Desktop\\Sophomore_work\\Quantum Computer\\QuCloud-kit\\Try-to-finish-the-Qucloud-kit")

from QuCloud.src.data.qcdata import QCData
from QuCloud.src.data.coluping_graph import Graph,change_Graph_to_List
from QuCloud.src.Fast_man import fast_newman
from QuCloud.src.Bplustree import Bptree,KeyValue

__all__ = ["init_mapping"]


log = logging.getLogger(__name__)

def init_mapping(path_file : str=None,
                output : str="output",
                loglevel : int=None, 
                log_path : str="logging"):
    """
        this is the first step, you can give the IBM system data (calibration data) path in your local environment.
        you can download in the https://quantum-computing.ibm.com/services?services=systems.
        parament:
            path_fline : input data path , you can see the detail in the ./data/qcdata.py.
            ouput : ouput file path.
            loglever : the logging's level
            log_path : the logging's output path
    """
    if path_file:
        qcdata = QCData(path_file)
    else:
        qcdata = QCData()
    w=1
    HT = construct_HT(qcdata=qcdata, w=w)
    # BPTdict = HT2dict(HT.root)
    # qubit_n = list(BPTdict.keys())
    # for i in qubit_n:
    #     print(BPTdict[i])
    searchHT_test(HT)

    BPT = HT2BPT(HT)
    searchBPF_test(BPT)



def get_graph(Vertex_error, Edge_error):
    graph=Graph()
    for vertex in Vertex_error:
        vertex_id = int(vertex[1:])
        graph.addVertex(vertex_id,Vertex_error[vertex])
    for edge in Edge_error:
        node0,node1 = edge
        graph.addEdge(node0,node1,Edge_error[edge])
    return graph

def construct_HT(qcdata,w:float):
    Vertex_error = qcdata.Vertex_error
    qubit_number = qcdata.vertex_number
    Edge_error = qcdata.Edge_error

    graph = get_graph(Vertex_error, Edge_error)
    List, List_edge, List_node, node_list = change_Graph_to_List(graph)
    log.info("----------------input fast_newman data---------------")
    log.info("List",List)
    log.info("List_edge",List_edge)
    log.info("List_node",List_node)
    log.info("node_list",node_list)
    log.info("qubit_number",qubit_number)
    HT = fast_newman(node_list, List,List_edge,List_node, qubit_number, w=w)
    return HT

def Qubit_partitioning(HT,program):
    Initialize_candidate_nodes = []
    pass

def HT2dict(root)->Dict:
    """
    广度遍历 利用队列实现树的层次遍历,并且生成一个dict {n:[[...],[...]]}
    类似于一个散列表：
    {1 : [[0],[1],[2].....[n]]
    2 : [[0,1],.....[i,j]]
    .....
    n : [[0,1,2,...n]]}
    """
    if not root:
        return
    queue = []
    dict = {}
    queue.append(root)
    while queue:
        node = queue.pop(0)
        n = len(node.data)
        node_value = node.data
        if not dict.get(n,False):
            dict[n] = [node_value]
        else:
            new_node_value = dict.get(n)
            new_node_value.append(node_value)
            dict[n] = new_node_value
        if node.lchild:
            queue.append(node.lchild)
        if node.rchild:
            queue.append(node.rchild)
    return dict

def HT2BPT(HT, show_print : bool = False):
    BPTdict = HT2dict(HT.root)
    qubit_n = list(BPTdict.keys())
    BPT = Bptree(4,4)
    for i in qubit_n:
        BPT.insert(KeyValue(i, list(BPTdict[i])))
    if show_print:
        show_some_BPF_detial(BPT,qubit_n)
    return BPT

def show_some_BPF_detial(BPT,qubit_n):
    print("-----------查看全部可选比特数: -------------")
    print("size: ", BPT.Size)
    print("qubit_ns: ",qubit_n)
    print("--------------search all leaf-------------------")
    for i in BPT.search(1,None):
        print("BPT[i]:", i)
    print("------展示所有的树结构-----------")
    BPT.show()

def searchBPF_test(BPT):
    print("-----------选择查看比特数为j-的可选:-----------")
    total_time = time.time()
    for i in range(10000): #  /10 ms 0.0026
        for j in range (1,17):
        # first = time.time()
            BPT.search(j,None)
        # print(j, "search time", (time.time()-first))
    print("total_time", time.time() - total_time, "aver-time", (time.time() - total_time)/16)

def searchHT_test(HT):
    condition = []
    print("-----------选择查看比特数为j-的可选:-----------")
    total_time = time.time()
    for qnumber in range(1,17):
        for i in range(1000): #  ms 0.0125
            for node in HT.leaf_node:
                while node:
                    if len(node.data)>=qnumber:
                        condition.append(node.data)
                    node = node.parent
            # print(j, "search time", (time.time()-first))
    print("total_time", time.time() - total_time,"ave_time", (time.time() - total_time)/16)

if __name__ == "__main__":
    init_mapping()
