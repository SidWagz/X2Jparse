
__author__ = 'sidwagz'

from wagz.sid.x2j.X2J import X2J

if __name__ == '__main__':

    parser = X2J('JustAnotherXmlStyleFile.xml')

    print(parser.xml)