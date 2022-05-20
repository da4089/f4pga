#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 F4PGA Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

# Symbiflow Stage Module

# ----------------------------------------------------------------------------- #

import os
import shutil
from sf_common import *
from sf_module import *

# ----------------------------------------------------------------------------- #

def route_place_file(eblif: str):
    return file_noext(eblif) + '.route'

class RouteModule(Module):
    def map_io(self, ctx: ModuleContext):
        return {
            'route': route_place_file(ctx.takes.eblif)
        }

    def execute(self, ctx: ModuleContext):
        build_dir = os.path.dirname(ctx.takes.eblif)

        vpr_options = []
        if ctx.values.vpr_options:
            vpr_options = options_dict_to_list(ctx.values.vpr_options)


        vprargs = VprArgs(ctx.share, ctx.takes.eblif, ctx.values,
                          sdc_file=ctx.takes.sdc)

        yield 'Routing with VPR...'
        vpr('route', vprargs, cwd=build_dir)

        if ctx.is_output_explicit('route'):
            shutil.move(route_place_file(ctx.takes.eblif), ctx.outputs.route)

        yield 'Saving log...'
        save_vpr_log('route.log', build_dir=build_dir)

    def __init__(self, _):
        self.name = 'route'
        self.no_of_phases = 2
        self.takes = [
            'eblif',
            'place',
            'sdc?'
        ]
        self.produces = [ 'route' ]
        self.values = [
            'device',
            'vpr_options?'
        ] + vpr_specific_values()

ModuleClass = RouteModule
