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

You have two options for installing this package:

- Clone this repository
- Install the complete sky130 PDK via [open_pdks](https://github.com/RTimothyEdwards/open_pdks) or [volare](https://github.com/efabless/volare). The PDK also contains this package.

For this package to be available in KLayout, you need to set the environment variable `KLAYOUT_PATH` to point to the root directory of this repository. For example, within this repository:

```console
KLAYOUT_PATH=. klayout -e
```

Or at another directory:

```console
KLAYOUT_PATH=/path/to/sky130_klayout_pdk klayout -e
```

### PCells

If you would like to use the PCells, you need to install `gdsfactory` in your system-wide Python package installation.
This can be as simple as running the following:

```console
pip install --upgrade gdsfactory
```

> [!IMPORTANT]  
> If you are using a Linux distribution that discourages the installation of system-wide Python packages through pip, you need to pass `--break-system-packages`.

## Acknowledgement

The XSection and D25 setup are gratefully borrowed from: [sky130A_el](https://github.com/klayoutmatthias/sky130A_el).

## License

If not otherwise noted [The Apache License, version 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt).