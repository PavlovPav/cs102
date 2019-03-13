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
        self.mem = proc_info.memory_info().rss / 1024 / 1024  #return in Mb
        # print(psutil.cpu_percent(interval=None))

        procs[0].join()

        self.defer_count = int(self.mem_usage / self.mem - self.mem_usage / self.mem / 100 * 10)
        self.defer_count = 1 if self.defer_count==0 else self.defer_count

        while not args.empty():
            for _ in range(self.defer_count):
                if args.empty(): break
                proc = Process(target=function, args=(args.get(),))
                procs.append(proc)
                proc.start()
            for proc in procs:
                proc.join()
        return self.defer_count,self.mem