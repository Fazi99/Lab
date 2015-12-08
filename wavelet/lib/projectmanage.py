# -*- coding: utf-8 -*-
# 2014.07.25 K. Kuwata
# projectmanage.py

import os, glob

class Manage:
    def __init__(self, name):
        self.name = name
        self.present = os.path.abspath(".")
        self.projectpath = self.present.replace("/%s/src" % (self.name), "")
        self.nmpypath = self.projectpath + "/numpy/"

    def GetProjectPath(self):
        present = os.path.abspath(".")
        present = present.replace("/lib", "")
        propath = present.replace("/src", "")
        return propath

    def CheckFiles(self, path):
        check = glob.glob(path)
        if len(check) > 0:
            for fl in check:
                if os.path.isfile(fl):
                    os.remove(fl)

    def Datapath(self, DATA):
        home = os.environ['HOME']
        datapath = os.path.abspath(home + "/Data/" + DATA)
        return datapath