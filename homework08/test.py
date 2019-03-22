import unittest
from Pool import Pool
import random
import queue


class MyTestCase(unittest.TestCase):
    def generate_data(self, len_q, len_list):
        q = queue.Queue()
        for _ in range(len_q):
            array = [random.randint(0, 100) for _ in range(len_list)]
            q.put(array)
        return q

    def task(self, data):
        data.sort()

    def test_count_worker(self):
        worker = Pool()
        self.assertEqual(9, worker.map(self.task, self.generate_data(30, 100000))[0])

    def test_count_worker_max(self):
        worker = Pool(1, 2, 512)
        self.assertEqual(2, worker.map(self.task, self.generate_data(30, 100000))[0])

    def test_count_worker_min(self):
        worker = Pool(15, 20, 512)
        self.assertRaisesRegexp(MemoryError,"The number of required workers is less than the minimum specified.", worker.map,self.task, self.generate_data(30, 100000))

    def test_memory(self):
        worker = Pool()
        self.assertLessEqual(45, int(worker.map(self.task, self.generate_data(30, 100000))[1]))

    def test_max_memory(self):
        worker = Pool()
        count_worker = worker.map(self.task, self.generate_data(30, 100000))[0]
        mem_for_worker = worker.map(self.task, self.generate_data(30, 100000))[1]
        self.assertLessEqual(count_worker * mem_for_worker, 500)


if __name__ == '__main__':
    unittest.main()
