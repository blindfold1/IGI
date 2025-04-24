def log_computation(func):

    def wrapper(*args, **kwargs):
        print(f"Starting computation for {func.__name__} with args: {args}")
        result = func(*args, **kwargs)
        print(f"Finished computation. Result: {result}")
        return result

    return wrapper