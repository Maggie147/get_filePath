# -*- encoding: utf-8-*-
#================================================
#  __title__ = 'Get filePath'
#  __author__ = 'tx'
#  __mtime__ = '2017-11-12'
#=================================================
#
import io
import sys
import os
import time
from xml.dom import minidom

g_iDEBUG = 1

def DEBUG(*value):
    if g_iDEBUG == 1:
        t = time.strftime("%Y-%m-%d %H:%M:%S")
        filename = sys.argv[0][sys.argv[0].rfind(os.sep)+1:]
        print "[python][%s,%s]:" % (filename, t),
        for i in value:
            print i,
        print ""

def get_attrvalue(node, attrname):
     return node.getAttribute(attrname) if node else ''
def get_nodevalue(node, index = 0):
    return node.childNodes[index].nodeValue if node else ''
def get_xmlnode(node,name):
    return node.getElementsByTagName(name) if node else []

def get_config(filename, module):
    try:
        doc = minidom.parse(filename)
        root = doc.documentElement                      # root Node  filePath_Config
        pathsets = get_xmlnode(root, module.upper())
        PATH = []
        paths = get_xmlnode(pathsets[0], 'Path')
        for path in paths:
            Path = {}
            enable = get_attrvalue(path, "enable")
            name = get_attrvalue(path, "name")
            filepath = get_nodevalue(path).encode('utf-8', 'ignore')
            Path['enable'] = enable
            Path['name'] = name
            Path['filepath'] = filepath

            PATH.append(Path)
        return PATH
    except:
        return None


def get_filePath(filename = "./filePath_Config.xml", module = 'SMTP'):
    try:
        AttPath = None
        AttPath2 = None
        streamPath = None
        PathList = get_config(filename, module)
        if PathList is None:
            DEBUG("GetXmlData failed")
            return -1
        for path in PathList:
            if path['enable'] != '0' and path['filepath']  is not None:
                if path['name'] == "AttPath":
                    AttPath = path['filepath']  + '/' if path['filepath'][-1] != '/' else path['filepath']
                    AttPath = AttPath + "%s/%s/%s/" % (time.strftime("%Y"), time.strftime("%02m"), time.strftime("%02d"))
                if path['name'] == "AttPath2":
                    AttPath2 = path['filepath']  + '/' if path['filepath'][-1] != '/' else path['filepath']
                if path['name'] == "streamPath":
                    streamPath = path['filepath']  + '/' if path['filepath'][-1] != '/' else path['filepath']
                    streamPath = streamPath + "%s%s%s/" % (time.strftime("%Y"), time.strftime("%02m"), time.strftime("%02d"))
        return (AttPath, AttPath2, streamPath)
    except Exception as e:
        DEBUG(e)
        return (None, None, None)


def test():
    module = "smtp"
    filename= "./filePath_Config.xml"
    # PATH = get_config(filename, module)
    # DEBUG(PATH)
    AttPath, AttPath2, streamPath = get_filePath(filename, module)
    # DEBUG(AttPath)
    # DEBUG(AttPath2)
    # DEBUG(streamPath)


if __name__ == "__main__":
    test()
