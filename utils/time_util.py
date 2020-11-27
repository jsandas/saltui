import time

def convert_timestamp(epoch_timestamp):
    timestamp = time.strftime("%x %X %z", time.localtime(epoch_timestamp))
    return timestamp