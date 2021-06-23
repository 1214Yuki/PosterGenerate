from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing import cpu_count


tp_executor = ThreadPoolExecutor(max_workers=cpu_count())


def get_column_attrs(k):
    return ''.join(k.split('_')[0])
