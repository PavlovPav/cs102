import unittest
from main import Pool
import os
import random
import queue


class MyTestCase(unittest.TestCase):
    def generate_data(self):
        q = queue.Queue()
        for _ in range(30):
            array = [random.randint(0, 100) for _ in range(100000)]
            q.put(array)
        return q

    def task(self, data):
        data.sort()

    def test_count_worker(self):
        worker = Pool(0, 0, 500)
        self.assertEqual(9, worker.map(self.task,self.generate_data())[0])


if __name__ == '__main__':
    unittest.main()
