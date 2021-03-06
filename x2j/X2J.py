
__author__ = 'sidwagz'

import re

class InvalidTagError(Exception):
    """
    Invalid tag error raised when xml tags aren't formed as expected
    """
    pass

class X2Jparser:

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

        inline_re = '\n[ ]*<'
        xml_trim = re.sub(inline_re, '<', self.xml)

        comment_re = '<!--(<?[-!,?\/\.\w\d\s=\"\']>?)*?-->'
        xml_trim = re.sub(comment_re, '', xml_trim.strip())

        syntax = r'</?\s*\w[-!\w\s\d]+.*?>|[-!\"\',\.\w\s\d]+'
        self.data = re.findall(syntax, xml_trim.strip())


    def tokenize(self, line):
        """
        Splits the individual xml tags and tag-values into
        granular tokens for used for key-value mapping
        :param line:
        :return:
        """

        quoted_kv_pair_re = '[-\.\w\d_]+\s*=\s*[\"\'][-,\.\w\d\s]+[\"\']'
        simple_value_re = '[-,!\.\w\d_]+'
        comment_value_re = '!--[-,!\.\w\d_]+--'
        syntax = '|'.join((comment_value_re, quoted_kv_pair_re, simple_value_re))

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

        map = {'__id__': tokens.pop(0), '__type__': __type__}
        for token in tokens:
            if '=' in token:
                lhs, rhs = token.split('=')
                map[lhs] = rhs

        return map

    def make_json(self):
        """
        Parse preprocessed and tokenized xml data into a json like dictionary
        :return:
        """

        self.prejson = dict()
        keys = []

        def get_innerdict(keys):
            """
            Generates nested dictionary for inner json elements
            :param keys:
            :return:
            """

            inner_dict = self.prejson
            for key in keys:
                if key not in inner_dict:
                    inner_dict[key] = dict()
                inner_dict = inner_dict[key]

            return inner_dict

        for line in self.data:

            map = self.tokenize(line)

            if map['__type__'] == 'start':
                keys.append(map['__id__'])
                del map['__id__']
                del map['__type__']
                inner_dict = get_innerdict(keys)
                for k, v in map.items():
                    inner_dict[k] = v

            elif map['__type__'] == 'end':
                keys.pop()

            elif map['__type__'] == 'value':
                del map['__type__']
                inner_dict = get_innerdict(keys)
                if inner_dict.get('value', None) is None:
                    inner_dict['value'] = map['__id__']
                else:
                    inner_dict['value'] = [inner_dict['value'], map['__id__']]

            else:
                del map['__type__']
                inner_dict = get_innerdict(keys)
                temp_key = map['__id__']
                del map['__id__']
                temp_dict = dict()
                for k, v in map.items():
                    temp_dict[k] = v
                if inner_dict.get(temp_key, None) is None:
                    inner_dict[temp_key] = temp_dict
                else:
                    if isinstance(inner_dict[temp_key], list):
                        inner_dict[temp_key] += [temp_dict]
                    else:
                        inner_dict[temp_key] = [inner_dict[temp_key], temp_dict]
