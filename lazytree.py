import lxml.etree as ET


def elem_to_json(elem):
    if len(elem) == 0:
        return elem.text
    else:
        value = {}
        for child in elem:
            value[child.tag] = elem_to_json(child)

        return value


class LazyTree(object):
    def __init__(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        self.data = elem_to_json(root)
        self.data['attributes'] = dict(root.items())

    def __getattr__(self, attr):
        return self.data[attr]
