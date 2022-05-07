#! /usr/bin/env python3

import random
import time
import numpy as np
import os.path
from typing import Tuple, List
import logging
import sys
import itertools

log = logging.getLogger(__name__)

class DATAFile:
    #ibmq_guadalupe_calibrations = "../../../data/ibmq_guadalupe_calibrations.csv"
    ibmq_guadalupe_calibrations = "Try-to-finish-the-Qucloud-kit/data/16qubit/ibmq_guadalupe_calibrations.csv"
    
class QCData:
    """ Class for a quantum computer data system.

        It loads data from the IBM(csv),and return two dict Vertex {node:read_error,...} and Edge {(node1,node2):CNOT_error,...}
    Parameters
    -----------
    sys_path
            Path to the data system

    """
    def __init__(self,sys_path: str = None, read_test_data: bool = True):
        self.dataflie = sys_path
        self.vertex_number = 0
        self.edge_number = 0
        self.Vertex_error = {}
        self.Edge_error = {}
        self.data_columns = []
        if read_test_data:
            log.info("read the test data")
            read_test_data = self.read_test_data()
            self.get_Vertex_error(read_test_data)
            self.get_Edge_error(read_test_data)
            log.info(f"the test data qubit number is{self.vertex_number}\n the edge number is {self.edge_number}")
        if sys_path and not read_test_data:
            log.info("loading the data:",sys_path)
            read_data = self.read_datafile(sys_path)
            self.get_Vertex_error(read_data)
            self.get_Edge_error(read_data)
            log.info(f"the test data qubit number is{self.vertex_number}\n the edge number is {self.edge_number}")

    
    def read_test_data(self):
        with open(DATAFile.ibmq_guadalupe_calibrations,'r') as ibmq_guadalupe_calibrations_csv:
            ibmq_guadalupe_calibrations = ibmq_guadalupe_calibrations_csv.read().splitlines()
        return ibmq_guadalupe_calibrations

    def read_datafile(self, file : str):
        self.dataflie = file
        with open(self.dataflie,'r') as ibmq_data_csv:
            ibmq_calibrations = ibmq_data_csv.read().splitlines()
        self.data_columns = ibmq_calibrations[0].split(",")
        return ibmq_calibrations

    def get_Vertex_error(self, read_data):
        Qubit = []
        Readout_assignment_error = []
        self.vertex_number = 0

        for line in read_data[1:]:
            listline = line.split(",")
            Qubit.append(listline[0])
            Readout_assignment_error.append(listline[5])
            self.vertex_number += 1
        self.Vertex_error = dict(zip(Qubit,Readout_assignment_error))
        
    def get_Edge_error(self, read_data):
        self.edge_number = 0

        for line in read_data[1:]:
            listline = line.split(",")
            CNOT_list = listline[12].split(";")
            for edge_error in CNOT_list:
                edge, error = edge_error.split(":")
                edge = tuple(sorted(map(int, edge.split("_"))))
                error = float(error)    # 考虑之后可以修改精度
                if not self.Edge_error.get(edge):
                    self.Edge_error[edge] = error
                    self.edge_number += 1

    def set_All_Random_qcdata(self, n, seed_id : int = 1,minread_error = 0.0001 ,maxread_error = 0.05, minCNOT_error = 0.0001, maxCNOT_error = 0.05):
        """ This is to get a Full connection graph N, 
            the Read error of ont qubit and the CNOT error for 2qubit (one edge)

            params :
            Vertex : [0,1,2,3]
            Edge : like this :list(map(tuple,itertools.combinations(range(4),2))) = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
            Vertex_error : {0:0.001,...,3:0.035}
            Edge_error : {(0,1):0.02....,(2,3):0.012564}
        """
        random.seed(seed_id)

        Vertex = list(range(n))
        Edge = list(map(tuple,itertools.combinations(Vertex,2)))
        Vertex_error = {}
        Edge_error = {}
        for vertex in Vertex:
            Vertex_error[vertex] = random.uniform(minread_error, maxread_error) 
        for edge in Edge:
            Edge_error[edge] = random.uniform(minCNOT_error, maxCNOT_error)
        self.Vertex_error = Vertex_error
        self.vertex_number = len(Vertex)
        self.Edge_error = Edge_error
        self.edge_number = len(Edge)

    def set_Single_Random_qcdata(self, n, seed_id : int = 1,minread_error = 0.0001 ,maxread_error = 0.05, minCNOT_error = 0.0001, maxCNOT_error = 0.05):
        """ This is to get a Full connection graph N, 
            the Read error of ont qubit and the CNOT error for 2qubit (one edge)

            params :
            Vertex : [0,1,2,3]
            Edge : like this Edge : = [(0, 1), (1, 2), (2, 3)], the number of Edge == the number of Vertex
            Vertex_error : {0:0.001,...,3:0.035}
            Edge_error : {(0,1):0.02....,(2,3):0.012564}
        """
        random.seed(seed_id)

        Vertex = list(range(n))
        Edge = [(i,i+1) for i in range(n-1)]
        Edge.append((0,n-1))
        Vertex_error = {}
        Edge_error = {}
        for vertex in Vertex:
            Vertex_error[vertex] = random.uniform(minread_error, maxread_error) 
        for edge in Edge:
            Edge_error[edge] = random.uniform(minCNOT_error, maxCNOT_error)
        self.Vertex_error = Vertex_error
        self.vertex_number = len(Vertex)
        self.Edge_error = Edge_error
        self.edge_number = len(Edge)

