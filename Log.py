import inspect

global debug
debug = True

def log(*args):
    if(debug == True):
        s = ''.join(str(i) for i in args)
        print(inspect.stack()[1][3], " :-  ",s)
    return

if __name__ == "__main__":
	log("hello")