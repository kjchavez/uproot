import lxml.etree as ET
import numpy as np
import glob


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


class Event(object):
    def __init__(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        self.data = elem_to_json(root)
        self.attributes = LazyNode(root.items())

    @staticmethod
    def iterator(filenames):
        """ An iterator over events by filenames. """
        if isinstance(filenames, str):
            filenames = glob.glob(filenames)

        for filename in filenames:
            yield Event(filename)
