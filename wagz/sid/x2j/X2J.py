
__author__ = 'sidwagz'

import re

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

        syn = r'</?[\w]+.*?>|[-\"\',\.\w\s\d]+'

        self.data = re.findall(syn, xml_trim)

        print(self.data)
