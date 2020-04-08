import time

def count_time(func):
    def int_time(*args, **kwargs):
        start_time = time.time()
        func()
        over_time = time.time()
        return over_time - start_time
    return int_time

@count_time
def run():
    res = []
    for i in range(10000000):
        res.append(i)
    del res

if __name__ == "__main__":
    print(time.time())
    t = 10
    all = 0
    for i in range(t):
        all += run()
    print(all/t)
