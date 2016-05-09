
__author__ = 'sidwagz'

from x2j.X2J import X2Jparser

if __name__ == '__main__':

    # Enter xml name here to test if file in class/search path
    parser = X2Jparser('JustAnotherXmlStyleFile.xml')

    parser.preprocess()
    parser.make_json()

    # Pretty print json stlye dictionary
    import pprint
    pprint.pprint(parser.prejson)