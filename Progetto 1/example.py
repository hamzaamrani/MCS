@profile
def my_func():
    a = [1] * (100 ** 6)
    b = [2] * (20 * 10 ** 7)
    del b
    return a

if __name__ == '__main__':
    my_func()
