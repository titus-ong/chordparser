from .chordsheet import Sheet

def create(file_path):
    with open(file_path, 'r') as f:
        contents = f.readlines()
    return Sheet(contents)
