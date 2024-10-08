# Copyright 2024 Efabless Corporation
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

import re

templates = [
  {
    # This regex searches for one of the available nfets with the parameters L, W, nf, m in any order
    'regex' : re.compile(r'^.*(?P<type>sky130_fd_pr__nfet_(?:01v8|01v8_lvt|01v8_hvt|g5v0d10v5))(?=.*L=(?P<l>\d+(\.\d+)?))(?=.*W=(?P<w>\d+(\.\d+)?))(?=.*nf=(?P<nf>\d+))(?=.*m=(?P<m>\d+)).*$'),
    'pcell_library': 'skywater130',
    'pcell_name' : 'nfet',
    'params' : [
      {
        'name' : 'type',
        'type' : 'string',
      },
      {
        'name' : 'l',
        'type' : 'float',
      },
      {
        'name' : 'w',
        'type' : 'float',
      },
      {
        'name' : 'nf',
        'type' : 'int',
      },
      {
        'name' : 'm',
        'type' : 'int',
      }
    ],
    'default_params' : {
      'bulk' : 'guard ring', # 'bulk tie', 'None'
      'gate_con_pos' : 'top', # 'bottom', 'alternating'
      'sd_con_col' : 1,
      'inter_sd_l' : 0.5,
      'nf' : 1,
      'grw' : 0.17
    }
  },
  {
    'regex' : re.compile(r'^.*(?P<type>sky130_fd_pr__pfet_(?:01v8|01v8_lvt|01v8_hvt|g5v0d10v5))(?=.*L=(?P<l>\d+(\.\d+)?))(?=.*W=(?P<w>\d+(\.\d+)?))(?=.*nf=(?P<nf>\d+))(?=.*m=(?P<m>\d+)).*$'),
    'pcell_library': 'skywater130',
    'pcell_name' : 'pfet',
    'params' : [
      {
        'name' : 'type',
        'type' : 'string',
      },
      {
        'name' : 'l',
        'type' : 'float',
      },
      {
        'name' : 'w',
        'type' : 'float',
      },
      {
        'name' : 'nf',
        'type' : 'int',
      },
      {
        'name' : 'm',
        'type' : 'int',
      }
    ],
    'default_params' : {
      'bulk' : 'guard ring', # 'bulk tie', 'None'
      'gate_con_pos' : 'top', # 'bottom', 'alternating'
      'sd_con_col' : 1,
      'inter_sd_l' : 0.5,
      'nf' : 1,
      'grw' : 0.17
    }
  },
  {
    'regex' : re.compile(r'^.*(?P<type>sky130_fd_pr__res_(?:x)?high_po_(?:0p35|0p69|1p41|2p85|5p73))(?=.*L=(?P<len>\d+(\.\d+)?))(?=.*m=(?P<m>\d+)).*$'),
    'pcell_library': 'skywater130',
    'pcell_name' : 'res_poly',
    'params' : [
      {
        'name' : 'type',
        'type' : 'string',
      },
      {
        'name' : 'len',
        'type' : 'float',
      },
      {
        'name' : 'm',
        'type' : 'int',
      }
    ],
    'default_params' : {
      'gr' : False # guard ring
    }
  },
  {
    'regex' : re.compile(r'^.*sky130_fd_pr__cap_mim_m3_1(?=.*L=(?P<l>\d+(\.\d+)?))(?=.*W=(?P<w>\d+(\.\d+)?))(?=.*m=(?P<m>\d+)).*$'),
    'pcell_library': 'skywater130',
    'pcell_name' : 'mim_cap',
    'params' : [
      {
        'name' : 'l',
        'type' : 'float',
      },
      {
        'name' : 'w',
        'type' : 'float',
      },
      {
        'name' : 'm',
        'type' : 'int',
      }
    ],
    'default_params' : {
      'type' : 'sky130_fd_pr__model__cap_mim',
    }
  },
  {
    'regex' : re.compile(r'^.*sky130_fd_pr__cap_mim_m3_2(?=.*W=(?P<w>\d+(\.\d+)?))(?=.*L=(?P<l>\d+(\.\d+)?))(?=.*m=(?P<m>\d+)).*$'),
    'pcell_library': 'skywater130',
    'pcell_name' : 'mim_cap',
    'params' : [
      {
        'name' : 'l',
        'type' : 'float',
      },
      {
        'name' : 'w',
        'type' : 'float',
      },
      {
        'name' : 'm',
        'type' : 'int',
      }
    ],
    'default_params' : {
      'type' : 'sky130_fd_pr__model__cap_mim_m4',
    }
  },
  {
    'regex' : re.compile(r'^.*(?P<Type>sky130_fd_pr__photodiode).*$'),
    'pcell_library': 'skywater130',
    'pcell_name' : 'photodiode',
    'params' : [
      {
        'name' : 'Type',
        'type' : 'string',
      },
    ],
    'default_params' : {
    }
  },
  {
    'regex' : re.compile(r'^.*(?P<type>sky130_fd_pr__res_generic_(?:l1|m1|m2|m3|m4|m5))(?=.*W=(?P<w>\d+(\.\d+)?))(?=.*L=(?P<len>\d+(\.\d+)?))(?=.*m=(?P<m>\d+)).*$'),
    'pcell_library': 'skywater130',
    'pcell_name' : 'res_metal',
    'params' : [
      {
        'name' : 'type',
        'type' : 'string',
      },
      {
        'name' : 'len',
        'type' : 'float',
      },
      {
        'name' : 'w',
        'type' : 'float',
      },
      {
        'name' : 'm',
        'type' : 'int',
      }
    ],
    'default_params' : {
      'gr': True,
    }
  },
  {
    'regex' : re.compile(r'^.*sky130_fd_pr__npn_05v5_w1p00l2p00(?=.*m=(?P<m>\d+)).*$'),
    'pcell_library': 'skywater130',
    'pcell_name' : 'npn_bjt',
    'params' : [
      {
        'name' : 'm',
        'type' : 'int',
      }
    ],
    'default_params' : {
        'type': 'sky130_fd_pr__npn_05v5_W1p00L1p00',
    }
  },
  {
    'regex' : re.compile(r'^.*sky130_fd_pr__pnp_05v5_W0p68L0p68(?=.*m=(?P<m>\d+)).*$'),
    'pcell_library': 'skywater130',
    'pcell_name' : 'pnp_bjt',
    'params' : [
      {
        'name' : 'm',
        'type' : 'int',
      }
    ],
    'default_params' : {
        'Type': 'sky130_fd_pr__pnp_05v5_W0p68L0p68',
    }
  },
  {
    'regex' : re.compile(r'^.*(?P<type>sky130_fd_pr__diode_pw2nd_(?:05v5|05v5_lvt|05v5_nvt|11v0)).*$'),
    'pcell_library': 'skywater130',
    'pcell_name' : 'n_diode',
    'params' : [
      {
        'name' : 'type',
        'type' : 'string',
      },
    ],
    'default_params' : {
    }
  },
  {
    'regex' : re.compile(r'^.*(?P<type>sky130_fd_pr__cap_var_(?:lvt|hvt))(?=.*W=(?P<w>\d+(\.\d+)?))(?=.*L=(?P<l>\d+(\.\d+)?))(?=.*m=(?P<m>\d+)).*$'),
    'pcell_library': 'skywater130',
    'pcell_name' : 'cap_var',
    'params' : [
      {
        'name' : 'type',
        'type' : 'string',
      },
      {
        'name' : 'l',
        'type' : 'float',
      },
      {
        'name' : 'w',
        'type' : 'float',
      },
      {
        'name' : 'm',
        'type' : 'int',
      }
    ],
    'default_params' : {
    }
  },
  {
    'regex' : re.compile(r'^.*(?P<Type>sky130_fd_pr__cap_vpp_[^\s]*)(?=.*m=(?P<m>\d+)).*$'),
    'pcell_library': 'skywater130',
    'pcell_name' : 'cap_vpp',
    'params' : [
      {
        'name' : 'Type',
        'type' : 'string',
      },
      {
        'name' : 'm',
        'type' : 'int',
      }
    ],
    'default_params' : {
    }
  },
]
