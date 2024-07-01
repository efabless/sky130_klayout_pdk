# Copyright 2022 Mabrains LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

########################################################################################################################
## BJT Pcells Generators for Klayout of skywater130
########################################################################################################################


import pya
import os
from .globals import *
import gdsfactory as gf
from .pdk import read_component

gds_p_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"fixed_devices/bjt" )#  parent file path 


def draw_npn(cell, device_name):

    '''
    drawing NPN devices 
    '''
    gds_path = f"{gds_p_path}/npn"
    if device_name in BJT_NPN_DEV :
        read_component(f"{gds_path}/{device_name}.gds", device_name, cell)

def draw_pnp(cell, device_name):

    '''
    drawing PNP devices
    '''
    gds_path = f"{gds_p_path}/pnp"
    
    if device_name in BJT_PNP_DEV :
        read_component(f"{gds_path}/{device_name}.gds", device_name, cell)


