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
## Guard Ring Pcells Generators for Klayout of skywater130
########################################################################################################################


from .via_generator import *
from .globals import *
from .layers_def import *
import gdsfactory as gf
from .pdk import open_component, take_component

def draw_gr (
    cell,
    in_l : float = 1,
    in_w : float = 1,
    grw : float = 0.17,
    con_lev = "li",
    implant_type = "None"
) :

    '''
    cell : kdb.Cell cell to place layout into
    in_l : float of the inner length of the ring
    in_w : float of the inner width of the ring 
    grw : float of the guard ring width 
    con_lev : connection level of (li, metal1)

    '''

    con_size = (0.17,0.17)
    con_spacing = (0.19, 0.19)
    con_enc = (0.12, 0.12)

    tap_nsdm_enc : float = 0.125
    tap_psdm_enc : float = 0.125

    c = open_component("sky_ring_gen")
    c_temp = gf.Component("temp_store")

    # Choose the implant
    if implant_type == 'nsdm':
        implant_layer = nsdm_layer
    if implant_type == 'psdm':
        implant_layer = psdm_layer
    
    # Add the implant layer
    if implant_type != 'None':
        implant_in = c_temp.add_ref(gf.components.rectangle(size=(in_w - 2*tap_nsdm_enc, in_l - 2*tap_nsdm_enc), layer=implant_layer))
        implant_in.move((tap_nsdm_enc, tap_nsdm_enc))
        implant_out = c_temp.add_ref(gf.components.rectangle(size=(in_w + 2*grw + 2*tap_nsdm_enc, in_l + 2*grw + 2*tap_nsdm_enc), layer=implant_layer))
        implant_out.move((-grw - tap_nsdm_enc, -grw - tap_nsdm_enc))
        implant = c.add_ref(gf.boolean(A=implant_out, B=implant_in, operation="A-B", layer=implant_layer))

    inner = c_temp.add_ref(gf.components.rectangle(size=(in_w, in_l), layer=tap_layer))
    outer = c_temp.add_ref(gf.components.rectangle(size=(inner.xmax - inner.xmin + 2*grw , inner.ymax - inner.ymin + 2*grw), layer=tap_layer))
    outer.move((-grw, -grw))

    gr = c.add_ref(gf.boolean(A=outer, B=inner , operation="A-B", layer=tap_layer))

    if con_lev == "li" or con_lev == "metal1":
        inner = c_temp.add_ref(gf.components.rectangle(size=(in_w, in_l), layer=li_layer))
        outer = c_temp.add_ref(gf.components.rectangle(size=(inner.xmax - inner.xmin + 2*grw , inner.ymax - inner.ymin + 2*grw), layer=li_layer))
        outer.move((-grw, -grw))
    
        li = c.add_ref(gf.boolean(A=outer, B=inner, operation="A-B", layer=li_layer))

        if grw < con_size[0] + 2*con_enc[0]:
            con_range = (inner.xmin, inner.xmax)
        else : 
            con_range = (outer.xmin, outer.xmax)

        licon_l = c.add_ref(via_generator(x_range=(outer.xmin, inner.xmin), y_range=(inner.ymin + 0.17 , inner.ymax - 0.17), via_enclosure=con_enc, via_layer=licon_layer
        , via_size=con_size, via_spacing=con_spacing))
        licon_r = c.add_ref(via_generator(x_range=(inner.xmax, outer.xmax), y_range=(inner.ymin + 0.17 , inner.ymax - 0.17), via_enclosure=con_enc, via_layer=licon_layer
        , via_size=con_size, via_spacing=con_spacing))
        licon_t = c.add_ref(via_generator(x_range=con_range, y_range=(inner.ymax, outer.ymax), via_enclosure=con_enc, via_layer=licon_layer
        , via_size=con_size, via_spacing=con_spacing))
        licon_b = c.add_ref(via_generator(x_range=con_range, y_range=(outer.ymin, inner.ymin), via_enclosure=con_enc, via_layer=licon_layer
        , via_size=con_size, via_spacing=con_spacing))



    if con_lev == "metal1" :
        inner = c_temp.add_ref(gf.components.rectangle(size=(in_w, in_l), layer=m1_layer))
        outer = c_temp.add_ref(gf.components.rectangle(size=(inner.xmax - inner.xmin + 2*grw , inner.ymax - inner.ymin + 2*grw), layer=m1_layer))
        outer.move((-grw, -grw))
    
        m1 = c.add_ref(gf.boolean(A=outer, B=inner, operation="A-B", layer=m1_layer))

        mcon_l = c.add_ref(via_generator(x_range=(outer.xmin, inner.xmin), y_range=(inner.ymin + 0.17 , inner.ymax - 0.17), via_enclosure=con_enc, via_layer=mcon_layer
        , via_size=con_size, via_spacing=con_spacing))
        mcon_r = c.add_ref(via_generator(x_range=(inner.xmax, outer.xmax), y_range=(inner.ymin + 0.17 , inner.ymax - 0.17), via_enclosure=con_enc, via_layer=mcon_layer
        , via_size=con_size, via_spacing=con_spacing))
        mcon_t = c.add_ref(via_generator(x_range=con_range, y_range=(inner.ymax, outer.ymax), via_enclosure=con_enc, via_layer=mcon_layer
        , via_size=con_size, via_spacing=con_spacing))
        mcon_b = c.add_ref(via_generator(x_range=con_range, y_range=(outer.ymin, inner.ymin), via_enclosure=con_enc, via_layer=mcon_layer
        , via_size=con_size, via_spacing=con_spacing))


    take_component(c, cell)
