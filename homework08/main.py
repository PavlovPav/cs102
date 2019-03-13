from multiprocessing import Process, cpu_count
import psutil


class Pool():
    def __init__(self, min_workers, max_workers, mem_usage):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.mem_usage = mem_usage

    def map(self, function, args):
        procs = []
        proc = Process(target=function, args=(args.get(),))
        procs.append(proc)
        proc.start()

        proc_info = psutil.Process(proc.pid)
        mem = proc_info.memory_info().rss / 1024 / 1024  #return in Mb
        # print(psutil.cpu_percent(interval=None))

        procs[0].join()

        defer_count = int(self.mem_usage / mem - self.mem_usage / mem / 100 * 10)
        if defer_count == 0: defer_count = 1

        while not args.empty():
            for _ in range(defer_count):
                if args.empty(): break
                proc = Process(target=function, args=(args.get(),))
                procs.append(proc)
                proc.start()
            for proc in procs:
                proc.join()
