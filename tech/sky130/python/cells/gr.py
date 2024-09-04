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
# Guard Ring Generator for skywater130
########################################################################################################################

import pya
from .draw_guard_ring import *

min_s = 0.27
min_w = 0.17
min_w_m1 = 0.23
min_s_m1 = 0.38

class guard_ring_gen(pya.PCellDeclarationHelper):
    """
    Guard Ring Generator for Skywater130
    """

    def __init__(self):
        # Initialize super class.
        super(guard_ring_gen, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================

        self.param("in_w", self.TypeDouble, "Inner Width", default=min_s, unit="um")
        self.param("in_l", self.TypeDouble, "Inner Length", default=min_s, unit="um")
        self.param("grw", self.TypeDouble, "Guard Ring Width", default=min_w, unit="um")

        
        self.Type_handle  = self.param("con_lev", self.TypeString, "Connection Level")
        self.Type_handle.add_choice("None", "None")
        self.Type_handle.add_choice("li", "li")
        self.Type_handle.add_choice("metal1", "metal1")
        self.Type_handle.default = self.Type_handle.choice_values()[0]
        
        self.Type_handle  = self.param("implant_type", self.TypeString, "Implant Type")
        self.Type_handle.add_choice("None", "None")
        self.Type_handle.add_choice("psdm", "psdm")
        self.Type_handle.add_choice("nsdm", "nsdm")
        self.Type_handle.default = self.Type_handle.choice_values()[0]

    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return f"Guard Ring(Ring Width = {self.grw})"
    
    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the
        # numeric parameter has changed (by comparing against the effective
        # radius ru) and set ru to the effective radius. We also update the
        # numerical value or the shape, depending on which on has not changed.        
        # w,l must be larger or equal than min. values.
        

        if self.con_lev == "metal1":
            if self.grw < min_w_m1 :
                self.grw = min_w_m1

            if self.in_l < min_s_m1 :
                self.in_l = min_s_m1
        
            if self.in_w < min_s_m1 :
                self.in_w  = min_s_m1
        else : 
            if self.grw < min_w :
                self.grw = min_w

            if self.in_l < min_s :
                self.in_l = min_s
        
            if self.in_w < min_s :
                self.in_w  = min_s
    
    def can_create_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we can use any shape which
        # has a finite bounding box
        return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()

    def parameters_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we set r and l from the shape's
        # bounding box width and layer
        self.r = self.shape.bbox().width() * self.layout.dbu / 2
        self.l = self.layout.get_info(self.layer)
    
    def transformation_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol: we use the center of the shape's
        # bounding box to determine the transformation
        return pya.Trans(self.shape.bbox().center())
    
    def produce_impl(self):
        draw_gr(cell=self.cell, in_l=self.in_l, in_w=self.in_w , grw= self.grw , con_lev=self.con_lev, implant_type=self.implant_type)

