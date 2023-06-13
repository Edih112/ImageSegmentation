import unittest
import numpy as np
from MaxFlow import MaxFlow

class MaxFlowTest(unittest.TestCase):

    def test_getMaxFlow1(self):
        matrix = np.array([[0,10,10,0,0,0],
                       [0,0,2,4,8,0],
                       [0,0,0,0,9,0],
                       [0,0,0,0,0,10],
                       [0,0,0,6,0,10],
                       [0,0,0,0,0,0]])
        mf = MaxFlow(matrix)
        self.assertEqual(mf.getMaxFlow(), 19)

    def test_getMaxFlow2(self):
        matrix = np.array([[0,16,13,0,0,0],
                            [0,0,10,12,0,0],
                            [0,4,0,0,14,0],
                            [0,0,9,0,0,20],
                            [0,0,0,7,0,4],
                            [0,0,0,0,0,0]])
        mf = MaxFlow(matrix)
        self.assertEqual(mf.getMaxFlow(), 23)

    def test_getMaxFlow3(self):
        matrix = np.array([])


if __name__ == '__main__':
    unittest.main()