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
# VPP CAP Generator for skywater130 
########################################################################################################################


import pya
from .draw_vpp import *
from .globals import *

class cap_vpp(pya.PCellDeclarationHelper):
    """
    VPP Cap Generator for Skywater130
    """

    def __init__(self):

        # Important: initialize the super class
        super(cap_vpp, self).__init__()
        self.Type_handle = self.param("Type", self.TypeString, "Type", default=VPP_CAP_DEV[0])
        

        for i in range(len(VPP_CAP_DEV)) :
            self.Type_handle.add_choice(VPP_CAP_DEV[i], VPP_CAP_DEV[i])
        
        
        self.param("Model", self.TypeString, "Model", default="sky130_fd_pr__cap_vpp",readonly=True)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return str(self.Type)

    def produce_impl(self):

        # This is the main part of the implementation: create the layout

        draw_vpp(cell=self.cell,device_name=self.Type)
