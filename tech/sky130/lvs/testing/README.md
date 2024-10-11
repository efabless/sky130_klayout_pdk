# Skywater 130nm LVS rule deck testing Documentation

Explains how to test the runset.

## Folder Structure

```text
📦runset
 ┣ 📜README.md
 ┣ 📜Makefile
 ┣ 📜run_test_case.sh
 ┗ 📦testcases
    ┣ 📦collision_test
    ┣ 📦connectivity_test
    ┣ 📦fail_cases
    ┣ 📦pass_cases
    ┣ 📦sc_testcases
 ```

## Rule Deck Testing

The `Makefile` and the `run_test_case.sh` script makes multiple tests of the LVS rule deck of SKY technology.

### **Tests**

### Usage

```bash
    make <target>

    targets:
        "all                   (the default if no target is provided                 )"
        "test_lvs_main         (To run main lvs regression for all devices           )"
        "test_lvs_collective   (To run collective lvs regression for all devices     )"
        "test_lvs_connectivity (To run connectivity lvs regression for all devices   )"
        "test_lvs_sc           (To run standard cells lvs regression for all devices )"
```

Example:

```bash
    make test_lvs_main
```

### Options

all                   (the default if no target is provided, runs the below )
test_lvs_main         (To run main lvs regression for all devices           )
test_lvs_collective   (To run collective lvs regression for all devices     )
test_lvs_connectivity (To run connectivity lvs regression for all devices   )
test_lvs_sc           (To run standard cells lvs regression for all devices )

### **Testing Outputs**

Final results will appear at the end of the run folder.

The output files are :

1. All extracted netlist (`<tested_circuit>.cir`).

2. Database file (`<tested_circuit>.lvdb`) for comparison results. you could view it on your file using klayout.

3. Log file of each circuit that had run.

4. May contain `.cdl` and `.gds` if `test_lvs_sc` target is used.
