# Copyright 2022 Efabless Corporation
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

#=========================================================================
# ---------------------------------- LVS ---------------------------------
#=========================================================================

SHELL            	:= /bin/bash
Testing_DIR      	?= $(shell realpath .)
PDK_ROOT         	:= $(shell realpath ../..)
TESTCASES_DIR    	:= $(shell realpath ./testcases)
SC_TESTCASES_DIR	:= $(shell realpath ./testcases/sc_testcases)
PDK              	:= $(shell basename `realpath ..`)
run_folder       	:= $(shell realpath $$(date +'run_%Y_%m_%d_%H_%M'))
MAIN 		     	:= $(wildcard testcases/pass_cases/*.cdl)
CASES		     	:= $(MAIN:testcases/pass_cases/%.cdl=test_lvs_main_local_%)
MAIN_CONN	     	:= $(wildcard testcases/connectivity_test/*.gds)
CONN_CASES       	:= $(MAIN_CONN:testcases/connectivity_test/%.gds=test_conn_%)
SC_HD	         	:= $(wildcard testcases/sc_testcases/hd/*.cdl)
SC_HD_GHA		 	:= $(SC_HD:testcases/sc_testcases/hd/%.cdl=test_lvs_sc_gha_%)
SC_HD_LOCAL		 	:= $(SC_HD:testcases/sc_testcases/hd/%.cdl=test_lvs_sc_local_%)
SC_HDLL	         	:= $(wildcard testcases/sc_testcases/hdll/*.cdl)
SC_HDLL_GHA	 		:= $(SC_HDLL:testcases/sc_testcases/hdll/%.cdl=test_lvs_sc_gha_%)
SC_HDLL_LOCAL 		:= $(SC_HDLL:testcases/sc_testcases/hdll/%.cdl=test_lvs_sc_local_%)
SC_HS	         	:= $(wildcard testcases/sc_testcases/hs/*.cdl)
SC_HS_GHA		 	:= $(SC_HS:testcases/sc_testcases/hs/%.cdl=test_lvs_sc_gha_%)
SC_HS_LOCAL		 	:= $(SC_HS:testcases/sc_testcases/hs/%.cdl=test_lvs_sc_local_%)
SC_HVL	         	:= $(wildcard testcases/sc_testcases/hvl/*.cdl)
SC_HVL_GHA	 		:= $(SC_HVL:testcases/sc_testcases/hvl/%.cdl=test_lvs_sc_gha_%)
SC_HVL_LOCAL 		:= $(SC_HVL:testcases/sc_testcases/hvl/%.cdl=test_lvs_sc_local_%)
SC_LP	         	:= $(wildcard testcases/sc_testcases/lp/*.cdl)
SC_LP_GHA		 	:= $(SC_LP:testcases/sc_testcases/lp/%.cdl=test_lvs_sc_gha_%)
SC_LP_LOCAL		 	:= $(SC_LP:testcases/sc_testcases/lp/%.cdl=test_lvs_sc_local_%)
SC_LS	         	:= $(wildcard testcases/sc_testcases/ls/*.cdl)
SC_LS_GHA		 	:= $(SC_LS:testcases/sc_testcases/ls/%.cdl=test_lvs_sc_gha_%)
SC_LS_LOCAL		 	:= $(SC_LS:testcases/sc_testcases/ls/%.cdl=test_lvs_sc_local_%)
SC_MS	         	:= $(wildcard testcases/sc_testcases/ms/*.cdl)
SC_MS_GHA		 	:= $(SC_MS:testcases/sc_testcases/ms/%.cdl=test_lvs_sc_gha_%)
SC_MS_LOCAL		 	:= $(SC_MS:testcases/sc_testcases/ms/%.cdl=test_lvs_sc_local_%)

.DEFAULT_GOAL := all

all: test_lvs_main test_lvs_collective test_lvs_connectivity

#=================================
# -------- TEST MAIN LVS ---------
#=================================

.ONESHELL:
$(run_folder):
	@echo "## Our current Run folder: $(run_folder)"
	@mkdir -p $(run_folder)

.phony:
test_lvs_main_gha_%: $(run_folder)
	@$(Testing_DIR)/run_test_case.sh $* $(PDK_ROOT) $(PDK) $(TESTCASES_DIR) $(run_folder) GHA

.ONESHELL:
test_lvs_main_local_%: $(run_folder)
	@$(Testing_DIR)/run_test_case.sh $* $(PDK_ROOT) $(PDK) $(TESTCASES_DIR) $(run_folder) LOCAL

nfet:
	@$(eval SUB_MAIN  := $(wildcard testcases/pass_cases/*nfet*.cdl))
	@$(eval SUB_CASES := $(SUB_MAIN:testcases/pass_cases/%.cdl=test_lvs_main_local_%))
	@$(MAKE) $(SUB_CASES)

pfet:
	@$(eval SUB_MAIN  := $(wildcard testcases/pass_cases/*pfet*.cdl))
	@$(eval SUB_CASES := $(SUB_MAIN:testcases/pass_cases/%.cdl=test_lvs_main_local_%))
	@$(MAKE) $(SUB_CASES)

BJT:
	@$(eval SUB_MAIN  := $(wildcard testcases/pass_cases/*__npn*.cdl))
	@$(eval SUB_MAIN  += $(wildcard testcases/pass_cases/*__pnp*.cdl))
	@$(eval SUB_CASES := $(SUB_MAIN:testcases/pass_cases/%.cdl=test_lvs_main_local_%))
	@$(MAKE) $(SUB_CASES)

# RF_BJT:
# 	@$(eval SUB_MAIN  := $(wildcard testcases/pass_cases/*rf_npn*.cdl))
# 	@$(eval SUB_CASES := $(SUB_MAIN:testcases/pass_cases/%.cdl=test_lvs_main_local_%))
# 	@$(MAKE) $(SUB_CASES)

diode:
	@$(eval SUB_MAIN  := $(wildcard testcases/pass_cases/*diode*.cdl))
	@$(eval SUB_CASES := $(SUB_MAIN:testcases/pass_cases/%.cdl=test_lvs_main_local_%))
	@$(MAKE) $(SUB_CASES)

resistor:
	@$(eval SUB_MAIN  := $(wildcard testcases/pass_cases/*res*.cdl))
	@$(eval SUB_CASES := $(SUB_MAIN:testcases/pass_cases/%.cdl=test_lvs_main_local_%))
	@$(MAKE) $(SUB_CASES)

cap_var:
	@$(eval SUB_MAIN  := $(wildcard testcases/pass_cases/*cap_var*.cdl))
	@$(eval SUB_CASES := $(SUB_MAIN:testcases/pass_cases/%.cdl=test_lvs_main_local_%))
	@$(MAKE) $(SUB_CASES)

cap_mim:
	@$(eval SUB_MAIN  := $(wildcard testcases/pass_cases/*cap_mim*.cdl))
	@$(eval SUB_CASES := $(SUB_MAIN:testcases/pass_cases/%.cdl=test_lvs_main_local_%))
	@$(MAKE) $(SUB_CASES)

inductor:
	@$(eval SUB_MAIN  := $(wildcard testcases/pass_cases/*coil*.cdl))
	@$(eval SUB_CASES := $(SUB_MAIN:testcases/pass_cases/%.cdl=test_lvs_main_local_%))
	@$(MAKE) $(SUB_CASES)

cap_vpp:
	@$(eval SUB_MAIN  := $(wildcard testcases/pass_cases/*cap_vpp*.cdl))
	@$(eval SUB_CASES := $(SUB_MAIN:testcases/pass_cases/%.cdl=test_lvs_main_local_%))
	@$(MAKE) $(SUB_CASES)

sonos:
	@$(eval SUB_MAIN  := $(wildcard testcases/pass_cases/*sonos*.cdl))
	@$(eval SUB_CASES := $(SUB_MAIN:testcases/pass_cases/%.cdl=test_lvs_main_gha_%))
	@$(MAKE) $(SUB_CASES)

.ONESHELL:
test_lvs_main: $(run_folder) $(CASES)
	@echo "Congratulations! Testing main LVS has finished successfully"

#=================================
# ------ TEST COLLISION LVS ------
#=================================

.ONESHELL:
test_lvs_collision: $(run_folder)
	@echo "## Running collision testing"
	@cd $(Testing_DIR)
	@if python3 $(PDK_ROOT)/$(PDK)/run_lvs.py --design=testcases/collision_test/collision.gds --net=collision.cdl --report=$(run_folder)/collision --lvs_sub=SUBSTRATE > $(run_folder)/collision_results.log 2>&1 ; \
		then echo "Congratulations! Testing collision LVS has finished successfully"; else echo "Testing collision LVS has failed."; exit 1 ; fi


#=================================
# ---- TEST CONNECTIVITY LVS -----
#=================================

.ONESHELL:
test_conn_%:
	@echo "## Running connectivity testing for $*"
	@cd $(Testing_DIR)
	@mkdir -p $(run_folder)/connectivity_test
	@file=`readlink -f testcases/connectivity_test/$*.gds`
	@cdl=`readlink -f testcases/connectivity_test/$*.cdl`
	@if python3 $(PDK_ROOT)/$(PDK)/run_lvs.py --design=$$file --net=$*.cdl --report=$(run_folder)/connectivity_test/$* --lvs_sub=SUB_SRC_D1 > $(run_folder)/connectivity_test/$*_run.log 2>&1 ;
		then echo "Congratulations! Connectivity test has finished successfully" ; else echo "Connectivity test has failed"; fi

.ONESHELL:
test_lvs_connectivity: $(CONN_CASES)
	@echo "Congratulations! Testing connectivity LVS is finished successfully"


#=================================
# -------- TEST SC LVS ---------
#=================================

.phony:
test_lvs_sc_gha_%: $(run_folder)
	@$(Testing_DIR)/run_test_case.sh $* $(PDK_ROOT) $(PDK) $(SC_TESTCASES_DIR) $(run_folder) GHA VNB $(word 4,$(subst _, ,$*)) SC

.phony:
test_lvs_sc_local_%: $(run_folder)
	@$(Testing_DIR)/run_test_case.sh $* $(PDK_ROOT) $(PDK) $(SC_TESTCASES_DIR) $(run_folder) LOCAL VNB $(word 4,$(subst _, ,$*)) SC

.ONESHELL:
test_lvs_sc: test_lvs_hd_sc test_lvs_hdll_sc test_lvs_hs_sc test_lvs_hvl_sc test_lvs_lp_sc test_lvs_ls_sc test_lvs_ms_sc
	@echo "Congratulations! Testing All SC LVS has finished successfully"

.ONESHELL:
test_lvs_sc_local: test_lvs_hd_sc_local test_lvs_hdll_sc_local test_lvs_hs_sc_local test_lvs_hvl_sc_local test_lvs_lp_sc_local test_lvs_ls_sc_local test_lvs_ms_sc_local
	@echo "Congratulations! Testing All SC LVS has finished successfully"

.ONESHELL:
test_lvs_hd_sc: $(run_folder) $(SC_HD_GHA)
	@echo "Congratulations! Testing HD SC LVS has finished successfully"

.ONESHELL:
test_lvs_hd_sc_local: $(run_folder) $(SC_HD_LOCAL)
	@echo "Congratulations! Testing HD SC LVS has finished successfully"

.ONESHELL:
test_lvs_hdll_sc: $(run_folder) $(SC_HDLL_GHA)
	@echo "Congratulations! Testing HDLL SC LVS has finished successfully"

.ONESHELL:
test_lvs_hdll_sc_local: $(run_folder) $(SC_HDLL_LOCAL)
	@echo "Congratulations! Testing HDLL SC LVS has finished successfully"

.ONESHELL:
test_lvs_hs_sc: $(run_folder) $(SC_HS_GHA)
	@echo "Congratulations! Testing HS SC LVS has finished successfully"

.ONESHELL:
test_lvs_hs_sc_local: $(run_folder) $(SC_HS_LOCAL)
	@echo "Congratulations! Testing HS SC LVS has finished successfully"

.ONESHELL:
test_lvs_hvl_sc: $(run_folder) $(SC_HVL_GHA)
	@echo "Congratulations! Testing HVL SC LVS has finished successfully"

.ONESHELL:
test_lvs_hvl_sc_local: $(run_folder) $(SC_HVL_LOCAL)
	@echo "Congratulations! Testing HVL SC LVS has finished successfully"

.ONESHELL:
test_lvs_lp_sc: $(run_folder) $(SC_LP_GHA)
	@echo "Congratulations! Testing LP SC LVS has finished successfully"

.ONESHELL:
test_lvs_lp_sc_local: $(run_folder) $(SC_LP_LOCAL)
	@echo "Congratulations! Testing LP SC LVS has finished successfully"

.ONESHELL:
test_lvs_ls_sc: $(run_folder) $(SC_LS_GHA)
	@echo "Congratulations! Testing LS SC LVS has finished successfully"

.ONESHELL:
test_lvs_ls_sc_local: $(run_folder) $(SC_LS_LOCAL)
	@echo "Congratulations! Testing LS SC LVS has finished successfully"

.ONESHELL:
test_lvs_ms_sc: $(run_folder) $(SC_MS_GHA)
	@echo "Congratulations! Testing MS SC LVS has finished successfully"

.ONESHELL:
test_lvs_ms_sc_local: $(run_folder) $(SC_MS_LOCAL)
	@echo "Congratulations! Testing MS SC LVS has finished successfully"

#==========================
# --------- HELP ----------
#==========================

# Help Target
help:
	@echo "\n ==== The following are some of the valid targets for this Makefile ====\n"
	@echo "... all						(the default if no target is provided          			)"
	@echo "... test_lvs_main			(To run main lvs regression for all devices    			)"
	@echo "... test_lvs_collective		(To run collective lvs regression for all devices		)"
	@echo "... test_lvs_connectivity	(To run connectivity lvs regression for all devices		)"
	@echo "... test_lvs_sc				(To run standard cells lvs regression for all devices	)"
