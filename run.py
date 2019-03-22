from multiprocessing import Pool

from utils import findWebcam
from core import video

if __name__ == '__main__':

    pool = Pool()
    count = pool.apply(func=findWebcam)

    for i in range(count):
        pool.apply_async(func=video.stream, args=(i,))

    pool.apply(func=video.index, args=(count,))

    pool.close()
    pool.join()
