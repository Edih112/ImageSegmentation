import unittest
import numpy as np
from FordFulkerson import FordFulkerson
from Dinics2 import Dinics2

class MaxFlowTest(unittest.TestCase):

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
