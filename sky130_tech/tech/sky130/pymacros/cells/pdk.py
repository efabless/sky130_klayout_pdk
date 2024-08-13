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

import gdsfactory as gf
import kfactory as kf
import klayout.db as kdb

def open_component(name : str) -> gf.Component:

  """
  Creates a new component for use as KLayout PCell incarnation

  The component is a temporary canvas to create the cell's layout.
  Later it is transferred to KLayout space using "take_component".

  This method will clean the entire gdsfactory space before creating
  the component. This mitigates namespace issue.
  """

  # TODO: have an API for this
  kf.kcell._get_default_kcl().clear()

  c = gf.Component(name)
  return c

def take_component(c : gf.Component, target_cell : kdb.Cell):

  """
  This method will copy the temporary gf.Component into the KLayout native target_cell
  """

  if target_cell is None:
    return

  # TODO: have an API for this
  source_cell = c._kdb_cell
  
  # Since dbu for sky130 is 0.001nm, but the manufacturing grid is 0.005nm
  # snap to 0.005nm grid to prevent offgrid DRC errors
  source_cell.layout().scale_and_snap(source_cell, 5, mult=1, div=1)

  cm = kdb.CellMapping()
  cm.for_single_cell(target_cell, source_cell)
  target_cell.copy_tree_shapes(source_cell, cm)

def read_component(path : str, name : str, target_cell : kdb.Cell):

  """
  Reads a component from a static GDS file
  """

  layout = kdb.Layout()
  layout.read(path)

  # copy into target cell
  source_cell = layout.cell(name)
  if source_cell is not None:
    cm = kdb.CellMapping()
    cm.for_single_cell(target_cell, source_cell)
    target_cell.copy_tree_shapes(source_cell, cm)
