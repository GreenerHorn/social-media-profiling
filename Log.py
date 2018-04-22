import inspect

global debug
debug = True


def log(*args):
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    filename = module.__file__
    file_array = filename.split('/')
    if (debug == True):
        s = ''.join(str(i) for i in args)
        print(file_array[-1], inspect.stack()[1][3], " :-  ", s)
    return


if __name__ == "__main__":
    log("hello")
