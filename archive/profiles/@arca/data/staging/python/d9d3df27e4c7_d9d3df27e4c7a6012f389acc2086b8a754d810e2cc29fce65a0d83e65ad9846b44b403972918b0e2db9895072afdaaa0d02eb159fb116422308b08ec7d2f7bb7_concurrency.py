from concurrent.futures import ThreadPoolExecutor

def parallel_process(files: list, process_func: callable, max_workers: int, **kwargs):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_func, f, **kwargs) for f in files]
        return [f.result() for f in futures if f.exception() is None]