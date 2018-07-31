#!/usr/bin/env python
# Author: poikilos (Jacob Gustafson)
# License: MIT
# Purpose: Flat-file drop-in replacement for jsonstore
# Usage: only works if you use strings in dict (no deeper nor shallower)
# Example:
'''
    from flatstore import FlatStore
    store = FlatStore('fs_shader.json')  # formerly JsonStore
    newline_delimited_string = to_one_line(["//type shader here"])
    if self.store.exists('shader'):
        newline_delimited_string = self.store.get('shader')['fragment']
    else:
        self.store.put('shader',fragment=newline_delimited_string)
        # result: 'fs_shader/shader/fragment' textfile is created&cached
'''
import os

def to_one_line(lines, separator="\n", rstrip_enable=True):
    ret = ""
    if rstrip_enable:
        for line in lines:
            ret += line.rstrip() + separator
    else:
        for line in lines:
            ret += line + separator
    return ret

class FlatStore:

    # db_name: put all dicts as folders in the parent folder db_name
    def __init__(self, db_name):
        self.db_name = db_name
        last_dot = db_name.rfind(".")
        last_slash = db_name.rfind("/")
        # if has at least one character before dot, remove extension:
        if last_dot > 0 and (last_slash==-1 or (last_dot>last_slash+1)):
            db_name = db_name[0:last_dot]
            self.db_name = db_name
        self.data = {}
        db_path = self.db_name
        if os.path.isdir(db_path):
            for folder_name in os.listdir(db_path):
                folder_path = os.path.join(db_path, folder_name)
                self.data[folder_name] = {}
                for sub_name in os.listdir(folder_path):
                    sub_path = os.path.join(folder_path, sub_name)
                    if os.path.isfile(sub_path):
                        #if sub_name[:1] != ".":
                        ins = open(sub_path, "r")
                        self.data[folder_name][sub_name] = \
                            to_one_line(ins.readlines())
                        ins.close()
                        # print("done reading " + sub_path)
                    else:
                        if os.path.isdir(sub_path):
                            print("WARNING In FlatStore get: " +
                                  " unexpected directory '" +
                                  sub_path +
                                  "' (expected only files).")
                        else:
                            print("WARNING In FlatStore get:" +
                                  " unexpected link or mount '" +
                                  sub_path + "' (expected only files).")

    def exists(self, folder_name):
        return folder_name in self.data

    def get(self, folder_name):
        ret = None
        sub = self.data.get(folder_name)
        if sub is not None:
            ret = {}
            for k,v in sub.items():
                ret[k] = v
        return ret

    def _put_s(self, folder_name, file_name, s):
        folder_path = os.path.join(self.db_name, folder_name)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
        sub_path = os.path.join(folder_path, file_name)
        if folder_name not in self.data:
            self.data[folder_name] = {}
        self.data[folder_name][file_name] = s
        outs = open(sub_path, 'w')
        outs.write(s)
        outs.close()

    # where kwargs is file_name=str(s)
    def put(self, folder_name, **kwargs):
        for file_name,s in kwargs.items():
            self._put_s(folder_name, file_name, s)

