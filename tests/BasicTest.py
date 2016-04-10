
__author__ = 'sidwagz'

from wagz.sid.x2j.X2J import X2J

if __name__ == '__main__':

    parser = X2J('JustAnotherXmlStyleFile.xml')

    # from textwrap import dedent
    # print(dedent(parser.xml))

    parser.preprocess()

    # for line in parser.data:
    #     # print(line)
    #     print(parser.tokenize(line))

    parser.make_json()