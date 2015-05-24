# -*- coding: utf-8 -*-
"""
Sandbox: Reading CERN data files
Created on Wed Jan 28 11:18:59 2015

@author: kevin
"""
import os
import lxml.etree as ET
import json
import glob
import numpy as np
import matplotlib.pyplot as plt

DATA_PATH = "../data/"
FILE_PATTERN = "*.xml"

def elem_to_json(elem):
    if len(elem) == 0:
        # Leaf node
        return elem.text
    else:
        value = {}
        for child in elem:
            value[child.tag] = elem_to_json(child)
            
        return value

def get_event_json(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    event = elem_to_json(root)
    event['attributes'] = dict(root.items())
    return event

def get_array(root,tag):
    return np.array(root[tag].lstrip().rstrip().split(),dtype=float)

def get_events_iter(directory,pattern):
    filenames = glob.glob(os.path.join(directory,pattern))
    for f in filenames:
        yield get_event_json(f)

def spherical2cart(spherical_coords):
    r,theta,phi = spherical_coords
    x = r*np.sin(theta)*np.cos(phi)
    y = r*np.sin(theta)*np.sin(phi)
    z = r*np.cos(theta)
    return x,y,z

def test():
    # -- Test --
    # Get all data filenames
    events = get_events_iter(DATA_PATH,FILE_PATTERN)
    phis = []
    etas = []
    for event in events:
        if 'Jet' in event:
            jet = event['Jet']
            phi = get_array(jet,'phi')
            eta = get_array(jet,'eta')
            phis.append(phi)
            etas.append(eta)
        else:
            print "Jet not found in Event #" + event['attributes']['eventNumber']
    
    angle_hist, _, _ = np.histogram2d(np.concatenate(phis),np.concatenate(etas))
    plt.close('all')
    plt.hist2d(np.concatenate(phis),np.concatenate(etas),cmap='gray')
    plt.xlabel('$\phi$')
    plt.ylabel('$\eta$')
    plt.title("Sample Histogram")
    plt.colorbar()
    plt.show()
    
if __name__ == "__main__":
    test()