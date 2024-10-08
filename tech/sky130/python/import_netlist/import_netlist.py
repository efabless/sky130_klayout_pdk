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
import pya

from .sky130_pcell_templates import templates

def create_pcell_instance(pcell_name='CIRCLE', lib_name='Basic', params={}, pos=pya.Trans.R0):
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

    # Get the active layout
    cellview = pya.CellView().active()
    layout = cellview.layout()
    if layout == None:
        print(f'Error: Couldn\'t get active layout.')
        return

    # Get the top cell. Assuming only one top cell exists
    top_cell = layout.top_cell()

    # Add a PCell variant
    pcell_var = layout.add_pcell_variant(lib, pcell_decl.id(), params)
    
    bbox = layout.cell(pcell_var).bbox()
    
    # Add an offset to the position to account for the origin
    offset = pya.Trans(pos, x=-bbox.left, y=-bbox.bottom)

    width = bbox.width()
    height = bbox.height()
    
    # Insert instance
    top_cell.insert(pya.CellInstArray(pcell_var, offset))
    
    return (width, height)

current_x = 0
spacing = 100

def create_subckt_instance(name, subckt_definitions):
    global current_x
    global spacing

    print(name)

    for pcell_inst in subckt_definitions[name]['pcells']:
        (width, height) = create_pcell_instance(
            pcell_inst['pcell_name'],
            pcell_inst['pcell_library'],
            pcell_inst['params'],
            pya.Trans(current_x, 0)
        )
        current_x += width + spacing

    for subckt_inst in subckt_definitions[name]['subckts']:
        if not subckt_inst in subckt_definitions:
            print(f'Error: Unknown subckt {subckt_inst}')
        else:
            create_subckt_instance(subckt_inst, subckt_definitions)

def sky130_import_netlist():

    # Get the schematic netlist
    netlist_path = pya.FileDialog.ask_open_file_name("Choose the schematic netlist", '.', "SPICE (*.spice)")

    print(f'Info: The netlist importer is still experimental.')
    print(f'Please report issues to: https://github.com/efabless/sky130_klayout_pdk/issues')

    # Check whether file exists
    if not netlist_path or not os.path.isfile(netlist_path):
        print(f'Error: {netlist_path} is not a file!')
        sys.exit(0)

    # Parse the spice netlist
    with open(netlist_path, 'r') as netlist_file:
        netlist_content = netlist_file.read()

    # Continue lines starting with '+'
    netlist_content = netlist_content.replace('\n+', '')
    
    # Split lines
    lines = netlist_content.split('\n')

    subckt_definitions = {'root': {'subckts': [], 'pcells': [], 'references': 0}}
    active_subckt = None

    # Scan for subckts
    for line in lines:
        # Ignore comments
        if line.startswith('*'):
            continue

        # Find start of subckt definitions
        if line.startswith('.subckt') or line.startswith('.SUBCKT'):
            active_subckt = line.split(' ')[1]
            subckt_definitions[active_subckt] = {'subckts': [], 'pcells': [], 'references': 0}

    print(subckt_definitions)

    for line in lines:
        # Ignore comments
        if line.startswith('*'):
            continue

        # Find start of subckt definitions
        if line.startswith('.subckt') or line.startswith('.SUBCKT'):
            active_subckt = line.split(' ')[1]
            
            if not active_subckt in subckt_definitions:
                print(f'Error: Unknown subckt {active_subckt}')

        # Find end of subckt definitions
        if line.startswith('.ends') or line.startswith('.ENDS'):
            active_subckt = None

        # Subckt instantiation
        if line.startswith('x') or line.startswith('X'):
            subckt = line.split(' ')[-1]
            subckt_definitions[active_subckt]['subckts'].append(subckt)
            
            if not subckt in subckt_definitions:
                print(f'Error: Unknown subckt {active_subckt}')
            else:
                subckt_definitions[subckt]['references'] += 1

        #print(f"Searching for match with '{line}'!")
        for template in templates:
      
            match = template['regex'].match(line)
            if match:
                params = template['default_params']
              
                # Parse parameters
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
                    subckt_definitions[active_subckt]['pcells'].append({
                        'pcell_name':       template['pcell_name'],
                        'pcell_library':    template['pcell_library'],
                        'params':           params.copy(),
                    })

    print(subckt_definitions)

    # Instanciate all top-level subckts
    for name in subckt_definitions.keys():
        if subckt_definitions[name]['references'] == 0:
            create_subckt_instance(name, subckt_definitions)
