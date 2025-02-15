import time

# create function 
def push_up_counter(countDown):
    while countDown > 0:
        print(countDown)
        countDown -= 1
        time.sleep(1)
        if countDown == 0:
            break
    return countDown


def start_timer(timeStart):
    global timeUp
    timeUp = push_up_counter(timeStart)