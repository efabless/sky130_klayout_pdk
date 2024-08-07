# Skywater 130nm Technology PDK for KLayout

<p align="center">
    <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/github/license/efabless/sky130_klayout_pdk" alt="License: Apache 2.0"/></a>
</p>

This package contains the Skywater 130nm PDK for KLayout.

## Contents

* `sky130.lyt`   : technology and connections description
* `sky130.lyp`   : layers color and shape description
* `sky130.map`   : layer mapping of def/lef shapes
* DRC          : DRC deck, located at [mpw_precheck](https://github.com/efabless/mpw_precheck/blob/main/checks/tech-files/sky130A_mr.drc)
* LVS          : LVS script, located at `lvs/lvs_sky130.lylvs`
* PCells       : devices generators

## Usage

### Installation

You have two options for using this package:

1. Clone this repository
2. Install the complete sky130 PDK from [open_pdks](https://github.com/RTimothyEdwards/open_pdks) either manually or with [volare](https://github.com/efabless/volare). The PDK also includes this package.

When you start KLayout, you must load this package. This can be done by setting the environment variable `KLAYOUT_PATH`. For example, inside this repository:

```console
KLAYOUT_PATH=./sky130_tech klayout -e
```

### PCells

If you would like to use the PCells, you need to install `gdsfactory` in your system-wide Python package installation.
This can be as simple as running the following:

```console
pip install --upgrade gdsfactory
```

> [!IMPORTANT]  
> If you are using a Linux distribution that discourages the installation of system-wide Python packages through pip, you need to pass `--break-system-packages`.
