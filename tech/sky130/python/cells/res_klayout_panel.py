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

# res Generator for skywater130

import pya


class res(pya.PCellDeclarationHelper):
    """parent class for the front end of the res (klayout panel)
    Args:
        l_min(float): minimum length of the resistor
        w_min(float): minimum width of the resistor
    """

    def __init__(self, l_min, w_min):
        # Initialize super class.
        super(res, self).__init__()

        # ===================== PARAMETERS DECLARATIONS =====================

        self.Type_handle = self.param("type", self.TypeString, "Device Type")

        self.param("len", self.TypeDouble, "Length", default=l_min, unit="um")
        self.param("w", self.TypeDouble, "Width", default=w_min, unit="um")

        self.param("gr", self.TypeBoolean, "Guard Ring", default=1)
        self.param(
            "area", self.TypeDouble, "Area", readonly=True, unit="um^2"
        )
        self.param(
            "res_value",
            self.TypeDouble,
            "Res Value",
            readonly=True,
            unit="ohms",
        )

    def display_text_impl(self):
        """Provide a descriptive text for the cell
        Return:
            (str):the res name with len and w
        """

        # Provide a descriptive text for the cell
        return (
            "Resistor_"
            + str(self.type)
            + "(L="
            + ("%.3f" % self.len)
            + ",W="
            + ("%.3f" % self.w)
            + ")"
        )

    def coerce_parameters_impl(self, l_min, w_min):
        """check the minimum values of l and w

            decide whether the handle or the numeric parameter has
            changed (by comparing against the effective
            radius ru) and set ru to the effective radius. We also update the
            numerical value or the shape, depending on which on has not changed
        Args:
            l_min(float): minimum length of the resistor
            w_min(float): minimum width of the resistor

        """

        self.area = self.w * self.len

        if self.len < l_min:
            self.len = l_min

        if self.w < w_min:
            self.w = w_min

    def can_create_from_shape_impl(self):
        """Implement the Create PCell

        we can use any shape which has a finite bounding box
        """

        return (
            self.shape.is_box()
            or self.shape.is_polygon()
            or self.shape.is_path()
        )

    def parameters_from_shape_impl(self):
        """Implement the "Create PCell from shape" protocol:

        we set r and l from the shape's bounding box width and layer
        """
        self.r = self.shape.bbox().width() * self.layout.dbu / 2
        self.len = self.layout.get_info(self.layer)

    def transformation_from_shape_impl(self):
        """Implement the "Create PCell from shape" protocol:

        we use the center of the shape's bounding box
        to determine the transformation
        """
        return pya.Trans(self.shape.bbox().center())
