import lxml.etree as ET
import numpy as np
from StringIO import StringIO

class LazyNode(dict):
    def __getattr__(self, attr):
        return self[attr]

    def __repr__(self):
        return "<LazyNode: " + ", ".join(key for key in self.keys()) + ">"

def elem_to_json(elem):
    if len(elem) == 0:

        return np.fromstring(elem.text.replace('\n', ' '), sep=' ')
    else:
        value = LazyNode()
        for child in elem:
            value[child.tag] = elem_to_json(child)

        return value


class LazyTree(object):
    def __init__(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        self.data = elem_to_json(root)
        self.data['attributes'] = LazyNode(root.items())

    def __getattr__(self, attr):
        return self.data[attr]

    def keys(self):
        return self.data.keys()