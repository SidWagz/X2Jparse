
__author__ = 'sidwagz'

from wagz.sid.x2j.X2J import X2J

if __name__ == '__main__':

    parser = X2J('JustAnotherXmlStyleFile.xml')

    parser.preprocess()
    parser.make_json()

    # Pretty print json stlye dictionary
    import pprint
    pprint.pprint(parser.prejson)