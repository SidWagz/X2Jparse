
__author__ = 'sidwagz'

class X2J:

    def __init__(self, file_name):
        self.xml = None
        with open(file_name, 'r') as f:
            self.xml = f.read()

