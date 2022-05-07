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
        This is the first step, you can give the IBM system data (calibration data) path in your local environment.
        you can download in the https://quantum-computing.ibm.com/services?services=systems.
        parament:
            path_fline : input data path , you can see the detail in the ./data/qcdata.py.
            ouput : ouput file path.
            loglever : the logging's level
            log_path : the logging's output path
    """
    if path_file:
        qcdata = QCData(path_file, read_test_data=False)
    else:
        qcdata = QCData(None,read_test_data=True)
    print("vertex number", qcdata.vertex_number, "edge number", qcdata.edge_number)
    w = 1
    HT,spand_time = construct_HT(qcdata=qcdata, w=w)
    HT.breadth_travel(HT.root)
    print("------------HT-search----------")
    searchHT_test(HT, qcdata.vertex_number)
    BPT = HT2BPT(HT)
    print("------------BPT-search----------")
    searchBPF_test(BPT,qcdata.vertex_number)
    # print("------完全图性能测试并输出---------")
    # HT_BPT_time_test(qcdata,w)

def HT_BPT_time_test(qcdata,w):
    """
        使用随机生成的图结构，来统计使用HT以及BPT进行可靠候选区域搜索所需的时间对比。
        HT_TIME : 存放HT树搜索所需平均时间
        BPT_TIME : 存放BPT树搜索所需时间
        Qubits : 存放对应的qubit数
    """
    HT_TIME = []
    BPT_TIME = []
    Qubits = []
    Ftime = []
    for n in range(2,60):
        print(f"第{n}个量子比特是搜索速度:")
        qcdata.set_All_Random_qcdata(n)
        HT,fast_newman_time = construct_HT(qcdata=qcdata, w=w)
        print("------------HT-search----------")
        HT_TIME.append(searchHT_test(HT, qcdata.vertex_number))
        BPT = HT2BPT(HT)
        print("------------BPT-search----------")
        BPT_TIME.append(searchBPF_test(BPT, qcdata.vertex_number))
        Qubits.append(n)
        Ftime.append(fast_newman_time)
    # with open("./Try-to-finish-the-Qucloud-kit/output/fast_newman_singlegraph_time.txt","w") as Ftime_out:
    #     for i in range(len(Qubits)):
    #         Ftime_out.write(str(Qubits[i])+":"+str(Ftime[i])+"\n")
    # with open("./Try-to-finish-the-Qucloud-kit/output/fast_newman_allgrpah_time.txt","w") as Ftime_out:
    #     for i in range(len(Qubits)):
    #         Ftime_out.write(str(Qubits[i])+":"+str(Ftime[i])+"\n")
    # with open("./Try-to-finish-the-Qucloud-kit/output/search_time_2_80","w") as search_out:
    #     for i in range(len(Qubits)):
    #         search_out.write(str(Qubits[i])+":"+str(HT_TIME[i])+"_"+str(BPT_TIME[i])+"\n")
    return 

def get_graph(Vertex_error, Edge_error):
    graph=Graph()
    for vertex in Vertex_error:
        if type(vertex) == str:
            vertex_id = int(vertex[1:])
        elif type(vertex) == int:
            vertex_id = vertex
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
    
    log.info("---------------------Fast_newman------------------ ")
    first =time.time()
    HT = fast_newman(node_list, List, List_edge, List_node, qubit_number, w=w)
    fast_newman_time = time.time() - first
    log.info("Community detection spend time is :",fast_newman_time)
    return HT,fast_newman_time

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

def HT2BPT(HT, show_print : bool = True):
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

def searchHT_test(HT,q_num):
    condition = []
    print("-----------按照HT进行查询候选节点")
    total_time = time.time()
    for qnumber in range(1,q_num+1):
        for i in range(10): #  ms 0.0125
            for node in HT.leaf_node:
                while node:
                    if len(node.data) >= qnumber:
                        condition.append(node.data)
                    node = node.parent
            # print(j, "search time", (time.time()-first))
    aver_time = (time.time() - total_time)/q_num
    print("total_time", time.time() - total_time, "aver-time", aver_time)
    return aver_time

def searchBPF_test(BPT, q_num):
    BPF_TIME = []
    print(f"-----------按照BPT进行查询候选节点")
    total_time = time.time()
    for i in range(1000): # 100 - *10 ms  10 - *10 s
        for j in range (1,q_num+1):
        # first = time.time()
            BPT.search(j,None)
        # print(j, "search time", (time.time()-first))
    aver_time = (time.time() - total_time)/q_num
    print("total_time", time.time() - total_time, "aver-time", aver_time)
    return aver_time


if __name__ == "__main__":
    qubit7_data_path = "Try-to-finish-the-Qucloud-kit/data/7qubit/ibm_perth_calibrations.csv"
    qubit16_data_path = "Try-to-finish-the-Qucloud-kit/data/16qubit/ibmq_guadalupe_calibrations.csv"
    qubit27_data_path = "Try-to-finish-the-Qucloud-kit/data/27qubit/ibmq_kolkata_calibrations.csv"
    qubit65_data_path = "Try-to-finish-the-Qucloud-kit/data/65qubit/ibmq_brooklyn_calibrations.csv"
    qubit127_data_path = "Try-to-finish-the-Qucloud-kit/data/127qubit/ibm_washington_calibrations.csv"
    init_mapping(qubit7_data_path)
