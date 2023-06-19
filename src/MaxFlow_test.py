import unittest
import numpy as np
from FordFulkerson import FordFulkerson, MaxFlowAdjMatrix
from Dinics2 import Dinics2

class MaxFlowTest(unittest.TestCase):

    def test_getMaxFlow1(self):
        matrix = np.array([[0,10,10,0,0,0],
                       [0,0,2,4,8,0],
                       [0,0,0,0,9,0],
                       [0,0,0,0,0,10],
                       [0,0,0,6,0,10],
                       [0,0,0,0,0,0]])
        mf = MaxFlowAdjMatrix(matrix, 0, 5)
        self.assertEqual(mf.getMaxFlow(), 19)

    def test_getMaxFlow2(self):
        matrix = np.array([[0,16,13,0,0,0],
                            [0,0,10,12,0,0],
                            [0,4,0,0,14,0],
                            [0,0,9,0,0,20],
                            [0,0,0,7,0,4],
                            [0,0,0,0,0,0]])
        mf = MaxFlowAdjMatrix(matrix, 0, 5)
        self.assertEqual(mf.getMaxFlow(), 23)

    def test_getMaxFlow3(self):
        matrix = np.array([[0,0,0,0,0,0],
                           [0,0,41,0,0,0],
                           [0,0,0,3,11,0],
                           [0,0,0,0,0,0],
                           [0,0,0,4,0,15],
                           [0,0,4,21,0,0]])
        mf = MaxFlowAdjMatrix(matrix, 1, 3)
        self.assertEqual(mf.getMaxFlow(), 14)

    def test_getMaxFlowAdj1(self):
        adj_list = [{1:10, 2:10},
                    {2:2, 3:4, 4:8},
                    {4:9},
                    {5:10},
                    {3:6, 5:10},
                    {}]
        mf = FordFulkerson(adj_list, 0, 5)
        self.assertEqual(mf.getMaxFlow(), 19)

    def test_getMaxFlowAdj2(self):
        adj_list = [{1:16, 2:13},
                    {2:10, 3:12},
                    {1:4, 4:14},
                    {2:9, 5:20},
                    {3:7, 5:4},
                    {}]
        mf = FordFulkerson(adj_list, 0, 5)
        self.assertEqual(mf.getMaxFlow(), 23)

    def test_getMaxFlowAdj3(self):
        adj_list = np.array([{},
                           {2:41},
                           {3:3, 4:11},
                           {},
                           {3:4, 5:15},
                           {2:4, 3:21}])
        mf = FordFulkerson(adj_list, 1, 3)
        self.assertEqual(mf.getMaxFlow(), 14)

    def test_getMaxFlowDinic1(self):
        adj_list = [{1:10, 2:10},
                    {2:2, 3:4, 4:8},
                    {4:9},
                    {5:10},
                    {3:6, 5:10},
                    {}]
        mf = Dinics2(adj_list, 0, 5)
        self.assertEqual(mf.getMaxFlow(), 19)

    def test_getMaxFlowDinic2(self):
        adj_list = [{1:16, 2:13},
                    {2:10, 3:12},
                    {1:4, 4:14},
                    {2:9, 5:20},
                    {3:7, 5:4},
                    {}]
        mf = Dinics2(adj_list, 0, 5)
        self.assertEqual(mf.getMaxFlow(), 23)

    def test_getMaxFlowDinic3(self):
        adj_list = np.array([{},
                           {2:41},
                           {3:3, 4:11},
                           {},
                           {3:4, 5:15},
                           {2:4, 3:21}])
        mf = Dinics2(adj_list, 1, 3)
        self.assertEqual(mf.getMaxFlow(), 14)

if __name__ == '__main__':
    unittest.main()
