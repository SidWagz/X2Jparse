
__author__ = 'sidwagz'

import re

class InvalidTagError(Exception):
    pass

class X2J:

    def __init__(self, file_name):
        self.xml = None
        with open(file_name, 'r') as f:
            self.xml = f.read()

    def preprocess(self):
        """
        Splits the xml file based only on '<' and '>'
        No support for '<' and '>' in file other than that
        :return:
        """
        xml_trim = re.sub('\n[ ]*<', '<', self.xml)

        syntax = r'</?[\w]+.*?>|[-\"\',\.\w\s\d]+'
        self.data = re.findall(syntax, xml_trim)

        # print(self.data)

    def tokenize(self, line):

        syntax = r'[-,\.\w\d]+\s*=\s*[-,\.\w\d]+|[\"\'][-,\.\w\d\s]+[\"\']\s*=\s*[\"\'][-,\.\w\d\s]+[\"\']|[-,\.\w\d]+\s*=\s*[\"\'][-,\.\w\d\s]+[\"\']|[-,\.\w\d]+'

        if line[0] == '<' and line[-1] == '>':
            line = line[1:-1]

            if line[0] == '/':
                line = line[1:]
                __type__ = 'end'

            elif line[-1] == '/':
                line = line[:-1]
                __type__ = 'single'

            else:
                __type__ = 'start'

        elif line[0] == '<' or line[-1] == '>':
            raise InvalidTagError('Bad tag formation : ' + line)

        else:
            __type__ = 'value'


        tokens = re.findall(syntax, line)
        # print(tokens)

        map = {'__name__': tokens.pop(0), '__type__': __type__}
        for token in tokens:
            lhs, rhs = token.split('=')
            map[lhs] = rhs

        return map