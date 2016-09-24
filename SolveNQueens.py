import time
import unittest
import cProfile
class NQueens(object):

    def solveNQueens(self, n):
        """

        :param int n: number of queens
        :rtype: List[List[str]]
        """
        self.res = []
        self.numQueens = n
        self.placeQueens([],0)
        return self.res
    
    def placeQueens(self, queenPos, queenNum):
        """
        the idea is to palce k-th queen at k-th row and record the column
        positions only

        :param List[int] queenPos: stores the column position of k-th row
        :param int queenNum: the queenNum-th queen, and the row number

        """
        if queenNum == self.numQueens:
            #found the solution
            board = ['.'*self.numQueens] * self.numQueens
            for k in xrange(self.numQueens):
                colPos = queenPos[k]
                board[k] = board[k][:colPos] + 'Q' + board[k][colPos+1:]
            self.res.append(board)
            return True
        for i in xrange(self.numQueens):
            if self.validMove(queenNum, i, queenPos):
                self.placeQueens(queenPos + [i], queenNum + 1)
        return False

    def validMove(self, queenNum, colPos, queenPos):
        """
        check if it is safe/valid to place the queen on colPos

        :param int queenNum: the queenNum-th queen, and the row number
        :param int colPos: the column for the new queen
        :param List[int] queenPos: column positions of the queens
        """
        for i in xrange(queenNum):
            if queenPos[i]==colPos or abs(i-queenNum)==abs(queenPos[i]-colPos):
                #no need to check row, as the new queen is always in new row
                return False
        return True

class NQueensTest(unittest.TestCase):
    """test cases of n-queen solver"""
    def setUp(self):
        self.nq = NQueens()

    def test_n8(self):
        self.assertEqual(len(self.nq.solveNQueens(8)), 92)

    def test_n9(self):
        self.assertEqual(len(self.nq.solveNQueens(9)), 352)

    
if __name__ == "__main__":
    unittest.main()
    nq = NQueens()
    cProfile.runctx('nq.solveNQueens(9)', globals(), locals())
