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
## RF Devices Pcells Generators for Klayout of skywater130
########################################################################################################################


import pya
import os
from .globals import *
from .pdk import read_component

 

gds_p_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"fixed_devices/rf" )  # parent file path 



def draw_rf_mosfet(cell, device_name):

    '''
    drawing rf mosfet devices 
    '''
    gds_path = f"{gds_p_path}/rf_mosfet"   # gds file path
    read_component(f"{gds_path}/{device_name}.gds", device_name, cell)

def draw_rf_bjt(cell, device_name):
    '''
    drawing rf mosfet devices 
    '''

    gds_path = f"{gds_p_path}/rf_bjt"   # gds file path 
    if device_name in RF_BJT_DEV :
        read_component(f"{gds_path}/{device_name}.gds", device_name, cell)


def draw_rf_coils(cell, device_name):
    '''
    drawing rf coils devices 
    '''

    gds_path = f"{gds_p_path}/rf_coils"   # gds file path 
    if device_name in RF_COILS_DEV :
        read_component(f"{gds_path}/{device_name}.gds", device_name, cell)
