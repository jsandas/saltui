import json

def read_in(filename):
    # load from file:
    with open(filename, 'r') as file:
        try:
            data = json.load(file)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            data = {}
    return data

def write_out(filename, data):
    # save to file:
    with open(filename, 'w') as file:
        json.dump(data, file)
    return
