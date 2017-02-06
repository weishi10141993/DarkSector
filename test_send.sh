#!/usr/bin/expect -f

set timeout 86400
set pass "YOUR PASSWORD"
################
spawn ssh -X -Y wshi@lxplus.cern.ch
expect "Password: "
send "$pass\r"
expect "$ "
send "tmux\r"
expect "$ "
send "cd /afs/cern.ch/work/w/wshi/public/DisplacedMuonJetAnalysis_2016/CMSSW_8_0_20/src\r"
expect "$ "
send "cmsenv\r"
expect "$ "
send "source /cvmfs/cms.cern.ch/crab3/crab.sh\r"
expect "$ "

send "sed -i '/Output dataset:/!d' test.txt\r"
expect "$ "
send "sed -i 's/Output dataset://g' test.txt\r"
expect "$ "
send "sed -i 's/\^\[ \\t\]\*//' test.txt\r"
expect "$ "
send "sed -i \"s|/DarkSUSY_mH_125_mGammaD_0250_cT_000_13TeV_MG452_BR224_LHE_pythia8_GEN_SIM_MINIAOD_V2_v1/wshi-DarkSUSY_mH_125_mGammaD_0250_cT_000_13TeV_MG452_BR224_LHE_pythia8_GEN_SIM_MINIAOD_V2_v1-9f24980cc1adfee526c3f4e710f8eab1/USER|\$(cat test.txt)|\" DIGI_RAW_CRAB3_DARKSUSY_mH_125_mGammaD_0250_cT_000_13TeV.py\r"
expect "$ "

send "exit\r"
expect "$ "
