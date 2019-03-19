from multiprocessing import Process, cpu_count
import psutil


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

        proc_info = psutil.Process(proc.pid)
        self.memory = proc_info.memory_info().rss / 1024 / 1024  # return in Mb
        # print(psutil.cpu_percent(interval=None))

        procs[0].join()

        self.worker_count = int(self.mem_usage / (self.memory + self.memory / 100 * 10))
        self.worker_count = 1 if self.worker_count == 0 else self.worker_count

        if self.worker_count > self.max_workers: self.worker_count = self.max_workers
        if self.worker_count < self.min_workers:
            raise Exception("The number of required workers is less than the minimum specified.")

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
