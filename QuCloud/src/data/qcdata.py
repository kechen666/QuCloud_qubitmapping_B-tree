#! /usr/bin/env python3

import time
import numpy as np
import os.path
from typing import Tuple, List
import logging

log = logging.getLogger(__name__)

class DATAFile:
    ibmq_guadalupe_calibrations = "../../../data/ibmq_guadalupe_calibrations.csv"

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
            self.read_test_data()
            self.get_Vertex_error()
            self.get_Edge_error()
            log.info(f"the test data qubit number is{self.vertex_number}\n the edge number is {self.edge_number}")
    
    def read_test_data(self):
        with open(DATAFile.ibmq_guadalupe_calibrations,'r') as ibmq_guadalupe_calibrations_csv:
            ibmq_guadalupe_calibrations = ibmq_guadalupe_calibrations_csv.read().splitlines()
        return ibmq_guadalupe_calibrations

    def read_datafile(self, file : str):
        self.dataflie = file
        with open(self.dataflie,'r') as ibmq_guadalupe_calibrations_csv:
            ibmq_guadalupe_calibrations = ibmq_guadalupe_calibrations_csv.read().splitlines()
        self.data_columns = ibmq_guadalupe_calibrations[0].split(",")
        return ibmq_guadalupe_calibrations

    def get_Vertex_error(self):
        Qubit = []
        Readout_assignment_error = []
        self.vertex_number = 0

        read_data = self.read_test_data()
        for line in read_data[1:]:
            listline = line.split(",")
            Qubit.append(listline[0])
            Readout_assignment_error.append(listline[5])
            self.vertex_number += 1
        self.Vertex_error = dict(zip(Qubit,Readout_assignment_error))
        
    def get_Edge_error(self):
        self.edge_number = 0

        read_data = self.read_test_data()
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