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

import os
import sys
import re
import pya

def createPCellInstance(pcell_name='CIRCLE', lib_name='Basic', params={}, pos=pya.Trans.R0):
    """
    Create a new instance of a PCell
    and return its width and height
    """

    print(f"Creating PCell '{pcell_name}' with parameters:")
    
    for key, value in params.items():
        print(f' - {key}: {value}')

    # Get PCell Library
    lib = pya.Library.library_by_name(lib_name)

    if not lib:
        print(f'Error: Library not found {lib_name}')
        return (0, 0)

    # The PCell Declaration. This one will create PCell variants.
    pcell_decl = lib.layout().pcell_declaration(pcell_name)

    if not pcell_decl:
        print(f'Error: Pcell not found {pcell_name}')
        return (0, 0)

    layoutview = pya.LayoutView().current()

    cellview = pya.CellView().active()
    view     = cellview.view()
    layout   = cellview.layout()

    # Get the top cell. Assuming only one top cell exists
    top_cell = layout.top_cell()

    # Add a PCell variant
    pcell_var = layout.add_pcell_variant(lib, pcell_decl.id(), params)
    
    width = layout.cell(pcell_var).bbox().width()
    height = layout.cell(pcell_var).bbox().height()
    
    # Insert instance
    top_cell.insert(pya.CellInstArray(pcell_var, pos))
    
    return (width, height)

def sky130_import_netlist():

    # Get the schematic netlist
    netlist_path = pya.FileDialog.ask_open_file_name("Choose the schematic netlist", '.', "SPICE (*.spice)")

    print(f'Info: The netlist importer is still experimental and does not yet support ".subckt" statements.')
    print(f'Please report issues to: https://github.com/efabless/sky130_klayout_pdk/issues')

    # Check whether file exists
    if not netlist_path or not os.path.isfile(netlist_path):
        print(f'Error: {netlist_path} is not a file!')
        sys.exit(0)

    # Get PCell Library
    lib = pya.Library.library_by_name('skywater130')

    if lib == None:
        print(f'Error: Couldn\'t get library "skywater130"')
        return

    layoutview = pya.LayoutView().current()

    if layoutview == None:
        print(f'Error: Couldn\'t get current layout view')
        return

    cellview = pya.CellView().active()
    view     = cellview.view()
    layout   = cellview.layout()

    # Get the top cell. Assuming only one top cell exists
    top_cell = layout.top_cell()

    # Here we store the variants for later instantiation
    variants = {}

    templates = [
      {
        # This regex searches for one of the available nfets with the parameters L, W, nf, m in any order
        'regex' : re.compile(r'^.*(?P<type>sky130_fd_pr__nfet_(?:01v8|01v8_lvt|01v8_hvt|g5v0d10v5))(?=.*L=(?P<l>\d+(\.\d+)?))(?=.*W=(?P<w>\d+(\.\d+)?))(?=.*nf=(?P<nf>\d+))(?=.*m=(?P<m>\d+)).*$'),
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
    ]

    current_x = 0
    spacing = 100

    # Parse the spice netlist
    with open(netlist_path, 'r') as netlist_file:

        line = netlist_file.readline()

        for next_line in netlist_file.readlines():
            #print(f'line {line}', end="")
            
            # This line is a continuation of the previous line
            if next_line.startswith('+'):
              line = line.rstrip('\n') + next_line[1:]
              #print(line)

            # Got a complete line
            else:
              #print(f"Searching for match with '{line}'!")
              for template in templates:
              
                match = template['regex'].match(line)
                if match:
                  params = template['default_params']
                  
                  for param in template['params']:
                    #print(f"Parsing parameter {param['name']}")
                    
                    if param["type"] == "string":
                      params[param['name']] = match.group(param['name'])
                    if param["type"] == "int":
                      params[param['name']] = int(match.group(param['name']))
                    if param["type"] == "float":
                      params[param['name']] = float(match.group(param['name']))
                  
                  # Multiplicity 'm'
                  m = 1
                  if 'm' in params:
                    m = params.pop('m')
                  
                  # Divide 'w' by 'nf' to get individual finger width
                  if 'nf' in params and params['nf'] > 1:
                    if 'w' in params:
                      params['w'] /= params['nf']
                  
                  #print(f'Instantiating Pcell with: {params}')
                  
                  for _ in range(m):
                    (width, height) = createPCellInstance(template['pcell_name'], 'skywater130', params, pya.Trans(current_x, 0))
                    current_x += width + spacing

              # Assign the next line
              line = next_line
