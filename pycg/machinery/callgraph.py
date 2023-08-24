#
# Copyright (c) 2020 Vitalis Salis.
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
class CallGraph(object):
    def __init__(self, meta_cg = False):
        self.cg = {}
        self.meta_cg = meta_cg
        self.modnames = {}

    def add_node(self, name, lineno = None, modname=""):
        if not isinstance(name, str):
            raise CallGraphError("Only string node names allowed")
        if not name:
            raise CallGraphError("Empty node name")

        if name not in self.cg:
            if self.meta_cg:
                self.cg[name] = {}
                self.modnames[name] = modname
                self.cg[name]["lineno"] = lineno
            else:
                self.cg[name] = set()
                self.modnames[name] = modname


        if name in self.cg and not self.modnames[name]:
            self.modnames[name] = modname

    def add_edge(self, src, dest, lineno = None, col_offset = None):
        if self.meta_cg:
            self.add_node(src,lineno)
            self.add_node(dest, lineno)
            self.cg[src] = {dest: {"lineno" : lineno,
                                    "col_offset" : col_offset }
            }
        else:
            self.add_node(src)
            self.add_node(dest)
            self.cg[src].add(dest)
        

    def get(self):
        return self.cg

    def get_edges(self):
        output = []
        for src in self.cg:
            for dst in self.cg[src]:
                output.append([src, dst])
        return output

    def get_modules(self):
        return self.modnames


class CallGraphError(Exception):
    pass