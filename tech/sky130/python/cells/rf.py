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
# RF DEVICES Generator for skywater130
########################################################################################################################

import pya
from .draw_rf import *
from .globals import *

class rf_mosfet(pya.PCellDeclarationHelper):
    """
    rf mosfet Generator for Skywater130
    """

    def __init__(self):

        # Important: initialize the super class
        super(rf_mosfet, self).__init__()
        self.Type_handle = self.param("Type", self.TypeString, "Type", default=RF_MOSFET_DEV[0])
       
        for i in RF_MOSFET_DEV :
            self.Type_handle.add_choice(i, i)
        
        
        self.param("Model", self.TypeString, "Model", default="sky130_fd_pr__",readonly=True)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return str(self.Type)

    def produce_impl(self):

        # This is the main part of the implementation: create the layout

        draw_rf_mosfet(cell=self.cell,device_name=self.Type)

class rf_bjt(pya.PCellDeclarationHelper):
    """
    rf bjt Generator for Skywater130
    """
    
    def __init__(self):

        # Important: initialize the super class
        super(rf_bjt, self).__init__()
        self.Type_handle = self.param("Type", self.TypeString, "Type", default=RF_BJT_DEV[0])
        for i in RF_BJT_DEV :
            self.Type_handle.add_choice(i, i)
        
        
        self.param("Model", self.TypeString, "Model", default="sky130_fd_pr__",readonly=True)
    

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return str(self.Type)

    def produce_impl(self):

        # This is the main part of the implementation: create the layout

        draw_rf_bjt(cell=self.cell,device_name=self.Type)


class rf_coils(pya.PCellDeclarationHelper):
    """
    rf coils Generator for Skywater130
    """

    def __init__(self):

        # Important: initialize the super class
        super(rf_coils, self).__init__()
        self.Type_handle = self.param("Type", self.TypeString, "Type", default=RF_COILS_DEV[0])
        for i in RF_COILS_DEV :
            self.Type_handle.add_choice(i, i)
        
        
        self.param("Model", self.TypeString, "Model", default="sky130_fd_pr__",readonly=True)

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return str(self.Type)

    def produce_impl(self):

        # This is the main part of the implementation: create the layout

        draw_rf_coils(cell=self.cell,device_name=self.Type)
