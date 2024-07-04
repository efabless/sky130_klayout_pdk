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
# Skywater 130nm Layers  parameters generation 
########################################################################################################################

from importlib.util import LazyLoader
from gdsfactory.typings import LayerSpec

diff_layer : LayerSpec = (65,20)
diff_lbl : LayerSpec = (65,6)

tap_layer : LayerSpec = (65,44)
tap_lbl : LayerSpec = (65,5)

nwell_layer : LayerSpec = (64,20)

dnwell_layer : LayerSpec = (64,18)

hvtp_layer : LayerSpec = (78,44)  # high_vt PMOS

hvi_layer : LayerSpec = (75,20)  # high voltage layer for voltages higher than 1.8v

lvtn_layer : LayerSpec = (125,44)  # low_vt NMOS 

poly_layer : LayerSpec = (66,20)  

hvntm_layer : LayerSpec = (125,20)  # high voltage n-implant 

nsdm_layer : LayerSpec = (93,44)

psdm_layer : LayerSpec = (94,20)

npc_layer : LayerSpec = (95,20)

licon_layer : LayerSpec = (66,44)

li_layer : LayerSpec = (67,20)
li_lbl : LayerSpec = (67,5)

mcon_layer : LayerSpec = (67,44)

m1_layer : LayerSpec = (68,20)
m1_lbl : LayerSpec = (68,5)

via1_layer : LayerSpec = (68,44)

m2_layer : LayerSpec = (69,20)
m2_lbl : LayerSpec = (69,5)

via2_layer : LayerSpec = (69,44)

m3_layer : LayerSpec = (70,20)
m3_lbl : LayerSpec = (70,5)

via3_layer : LayerSpec = (70,44)

m4_layer : LayerSpec = (71,20)
m4_lbl : LayerSpec = (71,5)

via4_layer : LayerSpec = (71,44)

m5_layer : LayerSpec = (72,20)
m5_lbl : LayerSpec = (72,5)

pr_bound_layer : LayerSpec = (235,4)

areaid_lvn_layer : LayerSpec = (81,60)

areaid_dio_layer : LayerSpec = (81,23)

capm_layer : LayerSpec = (89,44)

cap2m_layer : LayerSpec = (97,44)


######res
diff_res : LayerSpec = (65,13)
poly_res : LayerSpec = (66,13)
rpm_drawing : LayerSpec = (86,20)
rpm_high_drawing : LayerSpec = (79,20)
pwell_res : LayerSpec = (64,13)
li1_res : LayerSpec = (67,13)
met1_res : LayerSpec = (68,13)
met2_res : LayerSpec = (69,13)
met3_res : LayerSpec = (70,13)
met4_res : LayerSpec = (71,13)
met5_res : LayerSpec = (72,13)
