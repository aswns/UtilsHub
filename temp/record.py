# 临时记录

def log_function(func):
    def wrapper(*args, **kwargs):
        print(f"Calling function '{func.__name__}' with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"Function '{func.__name__}' returned: {result}")
        return result
    return wrapper

@log_function
def add(a, b):
    return a + b

result = add(a=3, b=5)
print("Result of add function:", result)

result = add(3, 5)
print("Result of add function:", result)
# ----------------------测试装饰器