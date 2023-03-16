import threading

def foo():
    print("AAA")

t = threading.Timer(2, foo).start()

print("BBB")

