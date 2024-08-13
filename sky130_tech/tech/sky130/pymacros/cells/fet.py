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
# MOSFET (PFET) Generator for skywater130
########################################################################################################################

from select import select
import pya
from .draw_fet import *

fet_01v8_l = 0.15
fet_g5v0_l = 0.5

fet_w = 0.42

fet_ld = 0.3
fet_inter_ld = 0.3
fet_01v8_grw = 0.17
pfet_g5v0_grw = 0.3

pfet_01v8_lvt_l = 0.35
nfet_g5v0_nvt_l = 0.9 


class pfet(pya.PCellDeclarationHelper):
    """
    PMOS Generator for Skywater130
    """

    def __init__(self):
        # Initialize super class.
        super(pfet, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================

        self.param("con_bet_fin", self.TypeBoolean, "Contact Between Fingers", default=1)
        
        self.Type_handle  = self.param("type", self.TypeString, "Device Type")
        self.Type_handle.add_choice("sky130_fd_pr__pfet_01v8", "sky130_fd_pr__pfet_01v8")
        self.Type_handle.add_choice("sky130_fd_pr__pfet_01v8_lvt", "sky130_fd_pr__pfet_01v8_lvt")
        self.Type_handle.add_choice("sky130_fd_pr__pfet_01v8_hvt", "sky130_fd_pr__pfet_01v8_hvt")
        self.Type_handle.add_choice("sky130_fd_pr__pfet_g5v0d10v5", "sky130_fd_pr__pfet_g5v0d10v5")
        self.Type_handle.default = self.Type_handle.choice_values()[0]

        self.Type_handle  = self.param("bulk", self.TypeString, "Bulk Type")
        self.Type_handle.add_choice("None", "None")
        self.Type_handle.add_choice("bulk tie", "bulk tie")
        self.Type_handle.add_choice("guard ring", "guard ring")
        self.Type_handle.default = self.Type_handle.choice_values()[0]

        self.Type_handle  = self.param("gate_con_pos", self.TypeString, "Gate Contact Position")
        self.Type_handle.add_choice("top", "top")
        self.Type_handle.add_choice("bottom", "bottom")
        self.Type_handle.add_choice("alternating", "alternating")
        self.Type_handle.default = self.Type_handle.choice_values()[0]

        

        self.param("l", self.TypeDouble, "Length", default=fet_01v8_l, unit="um")
        self.param("w", self.TypeDouble, "Width", default=fet_w, unit="um")
        self.param("sd_con_col", self.TypeInt, "Diffusion Contacts Columns", default=1)
        self.param("inter_sd_l", self.TypeDouble, "Between Fingers Diffusion Length", default=fet_inter_ld, unit="um")
        self.param("nf", self.TypeInt, "Number of Fingers", default=1)
        self.param("grw", self.TypeDouble, "Guard Ring Width", default=fet_01v8_grw, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")

        self.param("interdig", self.TypeBoolean, "Interdigitation", default=0)
        self.param("patt", self.TypeString,"Pattern in case of Interdigitation", default= "")

        #self.param("n", self.TypeInt, "inst_num", default=1)
    
    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "pfet(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"
    
    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the
        # numeric parameter has changed (by comparing against the effective
        # radius ru) and set ru to the effective radius. We also update the
        # numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if self.type    == "sky130_fd_pr__pfet_g5v0d10v5":
            if (self.l) < fet_g5v0_l:
                self.l  = fet_g5v0_l
            if (self.w) < fet_w:
                self.w = fet_w
            if (self.grw) < pfet_g5v0_grw :
                self.grw = pfet_g5v0_grw 
        else :
            if (self.l) < fet_01v8_l:
                self.l  = fet_01v8_l
            if (self.w) < fet_w:
                self.w = fet_w
            if (self.grw) < fet_01v8_grw :
                self.grw = fet_01v8_grw 
        
            if self.type  == "sky130_fd_pr__pfet_01v8_lvt":
                if (self.l) < pfet_01v8_lvt_l :
                    self.l  = pfet_01v8_lvt_l 
            else :
                if (self.l) < fet_01v8_l :
                    self.l  = fet_01v8_l 

        if (self.sd_con_col) < 1 :
            self.sd_con_col = 1 
        
        if (self.inter_sd_l) < fet_inter_ld and self.con_bet_fin == 1: 
            self.inter_sd_l = fet_inter_ld
        elif (self.inter_sd_l) < 0.21 and self.con_bet_fin == 0: 
            self.inter_sd_l = 0.21

        if self.interdig == 1 and self.gate_con_pos != "alternating":
            self.inter_sd_l = 0.5 
        
        
    
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
        draw_pfet(cell= self.cell , l=self.l, w=self.w, sd_con_col=self.sd_con_col, inter_sd_l=self.inter_sd_l, nf=self.nf, grw=self.grw
                    , type = self.type, bulk=self.bulk, con_bet_fin=self.con_bet_fin,gate_con_pos= self.gate_con_pos, interdig=self.interdig, patt=self.patt)

        
class nfet(pya.PCellDeclarationHelper):
    """
    NMOS Generator for Skywater130
    """

    def __init__(self):
        # Initialize super class.
        super(nfet, self).__init__()

        #===================== PARAMETERS DECLARATIONS =====================

        self.param("con_bet_fin", self.TypeBoolean, "Contact Between Fingers", default=1)

        self.Type_handle  = self.param("type", self.TypeString, "Device Type")
        self.Type_handle.add_choice("sky130_fd_pr__nfet_01v8", "sky130_fd_pr__nfet_01v8")
        self.Type_handle.add_choice("sky130_fd_pr__nfet_01v8_lvt", "sky130_fd_pr__nfet_01v8_lvt")
        self.Type_handle.add_choice("sky130_fd_pr__nfet_03v3_nvt","sky130_fd_pr__nfet_03v3_nvt")
        self.Type_handle.add_choice("sky130_fd_pr__nfet_05v0_nvt","sky130_fd_pr__nfet_05v0_nvt")
        self.Type_handle.add_choice("sky130_fd_pr__nfet_g5v0d10v5","sky130_fd_pr__nfet_g5v0d10v5")
        self.Type_handle.default = self.Type_handle.choice_values()[0]

        self.Type_handle  = self.param("bulk", self.TypeString, "Bulk Type")
        self.Type_handle.add_choice("None", "None")
        self.Type_handle.add_choice("bulk tie", "bulk tie")
        self.Type_handle.add_choice("guard ring", "guard ring")
        self.Type_handle.default = self.Type_handle.choice_values()[0]

        self.Type_handle  = self.param("gate_con_pos", self.TypeString, "Gate Contact Position")
        self.Type_handle.add_choice("top", "top")
        self.Type_handle.add_choice("bottom", "bottom")
        self.Type_handle.add_choice("alternating", "alternating")
        
        self.param("l", self.TypeDouble, "length", default=fet_01v8_l, unit="um")
        self.param("w", self.TypeDouble, "Width", default=fet_w, unit="um")
        self.param("sd_con_col", self.TypeDouble, "Diffusion Contacts Columns", default=fet_ld, unit="um")
        self.param("inter_sd_l", self.TypeDouble, "Between Fingers Diffusion Length", default=fet_inter_ld, unit="um")
        self.param("nf", self.TypeInt, "Number of Fingers", default=1)
        self.param("grw", self.TypeDouble, "Guard Ring Width", default=fet_01v8_grw, unit="um")
        self.param("area", self.TypeDouble,"Area", readonly=True, unit="um^2")
        self.param("perim", self.TypeDouble,"Perimeter", readonly=True, unit="um")   

        self.param("interdig", self.TypeBoolean, "Interdigitation", default=0)
        self.param("patt", self.TypeString,"Pattern in case of Interdigitation", default= "") 

        #self.param("n", self.TypeInt, "inst_num", default=1)
    
    def display_text_impl(self):
        # Provide a descriptive text for the cell
        return "nfet(L=" + ('%.3f' % self.l) + ",W=" + ('%.3f' % self.w) + ")"

    def coerce_parameters_impl(self):
        # We employ coerce_parameters_impl to decide whether the handle or the
        # numeric parameter has changed (by comparing against the effective
        # radius ru) and set ru to the effective radius. We also update the
        # numerical value or the shape, depending on which on has not changed.
        self.area  = self.w * self.l
        self.perim = 2*(self.w + self.l)
        # w,l must be larger or equal than min. values.
        if self.type == "sky130_fd_pr__nfet_03v3_nvt" or self.type == "sky130_fd_pr__nfet_05v0_nvt" or self.type == "sky130_fd_pr__nfet_g5v0d10v5":
            if (self.l) < fet_g5v0_l:
                self.l  = fet_g5v0_l
            if (self.w) < fet_w:
                self.w = fet_w
            if (self.grw) < pfet_g5v0_grw :
                self.grw = pfet_g5v0_grw 

            if self.type == "sky130_fd_pr__nfet_05v0_nvt":
                if (self.l) < nfet_g5v0_nvt_l:
                    self.l  = nfet_g5v0_nvt_l

        else :
            if (self.l) < fet_01v8_l:
                self.l  = fet_01v8_l
            if (self.w) < fet_w:
                self.w = fet_w
            if (self.grw) < fet_01v8_grw :
                self.grw = fet_01v8_grw 
        

        if (self.sd_con_col) < 1 :
            self.sd_con_col = 1 
        
        if (self.inter_sd_l) < fet_inter_ld and self.con_bet_fin == 1: 
            self.inter_sd_l = fet_inter_ld
        elif self.inter_sd_l < 0.21 and self.con_bet_fin == 0 :
            self.inter_sd_l = 0.21
        
        if self.interdig == 1 and self.gate_con_pos != "alternating":
            self.inter_sd_l = 0.5 
        
        
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
        draw_nfet(cell= self.cell , l=self.l, w=self.w, sd_con_col=self.sd_con_col, inter_sd_l=self.inter_sd_l, nf=self.nf, grw=self.grw
                    , type= self.type , bulk=self.bulk, con_bet_fin=self.con_bet_fin,gate_con_pos= self.gate_con_pos, interdig=self.interdig, patt=self.patt)

