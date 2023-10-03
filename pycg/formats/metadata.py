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
from .base import BaseFormatter
from pycg import utils


class Meta(BaseFormatter):
    def generate(self):
        graph = self.cg_generator.get_as_graph()
        return {
            key: (
                [
                    {"name_pointers": [list(defi.get_name_pointer().get().copy())]},
                    {"points_to": defi.points_to},
                ]
                if defi.def_type in [utils.constants.MOD_DEF, utils.constants.EXT_DEF]
                else [
                    {
                        "defined_at": [
                            d for d in defi.defined_at if d["lineno"] is not None
                        ]
                    },
                    {"points_to": defi.points_to},
                ]
            )
            for key, defi in graph
        }
