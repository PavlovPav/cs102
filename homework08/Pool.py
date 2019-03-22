from multiprocessing import Process, cpu_count
import psutil
from time import sleep


class Pool():
    def __init__(self, min_workers=1, max_workers=10, mem_usage=500):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.mem_usage = mem_usage

    def map(self, function, args):
        procs = []
        proc = Process(target=function, args=(args.get(),))
        procs.append(proc)
        proc.start()
        mem_count = []
        while proc.is_alive():
            proc_info = psutil.Process(proc.pid)
            mem_count.append(proc_info.memory_info().rss / 1024 / 1024)  # return in Mb
            sleep(0.0001)
        self.memory = max(mem_count)

        self.worker_count = int(self.mem_usage / (self.memory + self.memory / 100 * 10))
        self.worker_count = 1 if self.worker_count == 0 else self.worker_count

        if self.worker_count > self.max_workers: self.worker_count = self.max_workers
        if self.worker_count < self.min_workers:
            raise MemoryError("The number of required workers is less than the minimum specified.")

        for _ in range(self.worker_count):
            if args.empty():
                for proc in procs:
                    proc.join()
                return self.worker_count, self.memory
            proc = Process(target=function, args=(args.get(),))
            procs.append(proc)
            proc.start()

        while not args.empty():
            for idx, proc in enumerate(procs):
                if args.empty(): break
                if not proc.is_alive():
                    new_proc = Process(target=function, args=(args.get(),))
                    procs[idx] = new_proc
                    new_proc.start()

        for proc in procs:
            proc.join()

        return self.worker_count, self.memory
