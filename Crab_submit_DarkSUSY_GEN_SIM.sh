#!/usr/bin/expect -f
#This is a script written by Wei Shi for private DarkSUSY MC Samples generation.

set timeout 86400
#set lightest neutralino n2 mass
set n2mass [list 10 30 60]

################
spawn ssh -X -Y wshi@lxplus.cern.ch
expect "Password: "
send "???????\r"
expect "$ "
send "tmux\r"
expect "$ "
send "cd /afs/cern.ch/user/w/wshi/public/DisplacedMuonJetAnalysis_2016/CMSSW_8_0_20/src\r"
expect "$ "
send "cmsenv\r"
expect "$ "
send "source /cvmfs/cms.cern.ch/crab3/crab.sh\r"
expect "$ "

for { set m 0 } { $m < [llength $n2mass] } { incr m } {

set N2MASS [lindex $n2mass $m]

if { [string equal $N2MASS 10] } {
set mass [list 0p25 0p4 0p7 1 2 5]
} elseif { [string equal $N2MASS 30] } {
set mass [list 10]
} else {
set mass [list 58]
}

for { set k 0 } { $k < [llength $mass] } { incr k } {

set MASS [lindex $mass $k]

if { [string equal $MASS 0p25] } {
set lifetimeString [list 0 0p05 0p1 0p5 1 2 5 20 100]
} elseif { [string equal $MASS 0p4] } {
set lifetimeString [list 0 0p5 1 2 5 20 100]
} elseif { [string equal $MASS 0p7] } {
set lifetimeString [list 0 0p5 1 5 20 100]
} elseif { [stirng equal $MASS 1] } {
set lifetimeString [list 0 1 20 100]
} elseif { [string equal $MASS 5] } {
set lifetimeString [list 0 1 20 100]
} elseif { [string equal $MASS 10] } {
set lifetimeString [list 0 100]
} else {
set lifetimeString [list 0 100]
}

for { set j 0 } { $j < [llength $lifetimeString] } { incr j } {

set LIFETIMESTRING [lindex $lifetimeString $j]

if { [string equal $LIFETIMESTRING 100] } {
set numevents [list 80000 79000 78000 77000 76000 75000 74000 73000 72000 71000 70000 69000 68000 67000 66000 65000 64000 63000 62000 61000 60000 59000]
set numeventsk [list 80k 79k 78k 77k 76k 75k 74k 73k 72k 71k 70k 69k 68k 67k 66k 65k 64k 63k 62k 61k 60k 59k]
} elseif { [string equal $LIFETIMESTRING 20] } {
set numevents [list 80000 79000 78000 77000 76000 75000 74000 73000 72000 71000 70000 69000 68000 67000]
set numeventsk [list 80k 79k 78k 77k 76k 75k 74k 73k 72k 71k 70k 69k 68k 67k]
} elseif { $LIFETIMESTRING in [list 5 2 1] } {
set numevents [list 47000 48000 49000 51000 52000 53000]
set numeventsk [list 47k 48k 49k 51k 52k 53k]
} else {
set numevents [list 80000 20000]
set numeventsk [list 80k 20k]
}

for { set i 0 } { $i < [llength $numevents] } { incr i } {

set NUMEVENTS [lindex $numevents $i];
set NUMEVENTSK [lindex $numeventsk $i];

#create pset file for each crab, don't need to specify events number for this file, 80000 is upper limit for one crab
send "cmsDriver.py MuJetAnalysis/GenProduction/Pythia8HadronizerFilter_13TeV_cfi -s GEN,SIM --mc --datatier GEN-SIM --beamspot Realistic25ns13TeV2016Collision --conditions 80X_mcRun2_asymptotic_2016_miniAODv2_v1 --eventcontent RAWSIM --era Run2_2016 --python_filename DarkSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_cT_$LIFETIMESTRING\_13TeV_madgraph452_bridge224_LHE_pythia8_cfi_GEN_SIM.py --filetype LHE --filein file:/eos/user/w/wshi/DarkSUSYMC_LHE_Moriond2017_Part2/DarkSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_13TeV_cT_$LIFETIMESTRING\_madgraph452_bridge224_events$NUMEVENTSK\.lhe --fileout file:out_sim.root -n 80000 --no_exec\r"
expect "$ "
#create crab config for each event, need to specify events number!
send "cp GEN_SIM_CRAB3_DARKSUSY_mH_125_mGammaD_0250_cT_000_13TeV.py GEN_SIM_CRAB3_DARKSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_cT_$LIFETIMESTRING\_13TeV_events$NUMEVENTSK\.py\r"
expect "$ "
#change request name
send "sed -i '3s/DarkSUSY_mH_125_mGammaD_0250_cT_000_13TeV_MG452_BR224_LHE_pythia8_GEN_SIM_MINIAOD_V2_v1/DarkSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_cT_$LIFETIMESTRING\_13TeV_$NUMEVENTSK\_MG452_BR224_LHE_pythia8_GEN_SIM_MINIAOD_V2_v1/' GEN_SIM_CRAB3_DARKSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_cT_$LIFETIMESTRING\_13TeV_events$NUMEVENTSK\.py\r"
expect "$ "
#change pset file
send "sed -i '8s/DarkSUSY_mH_125_mGammaD_0250_cT_000_13TeV_madgraph452_bridge224_LHE_pythia8_cfi_GEN_SIM.py/DarkSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_cT_$LIFETIMESTRING\_13TeV_madgraph452_bridge224_LHE_pythia8_cfi_GEN_SIM.py/' GEN_SIM_CRAB3_DARKSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_cT_$LIFETIMESTRING\_13TeV_events$NUMEVENTSK\.py\r"
expect "$ "
#change input file
send "sed -i '10s/DarkSUSY_mH_125_mGammaD_0250_13TeV_cT_000_madgraph452_bridge224_events80k.lhe/DarkSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_13TeV_cT_$LIFETIMESTRING\_madgraph452_bridge224_events$NUMEVENTSK\.lhe/' GEN_SIM_CRAB3_DARKSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_cT_$LIFETIMESTRING\_13TeV_events$NUMEVENTSK\.py\r"
expect "$ "
#change outputPrimaryDataset
send "sed -i '11s/DarkSUSY_mH_125_mGammaD_0250_cT_000_13TeV_MG452_BR224_LHE_pythia8_GEN_SIM_MINIAOD_V2_v1/DarkSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_cT_$LIFETIMESTRING\_13TeV_$NUMEVENTSK\_MG452_BR224_LHE_pythia8_GEN_SIM_MINIAOD_V2_v1/' GEN_SIM_CRAB3_DARKSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_cT_$LIFETIMESTRING\_13TeV_events$NUMEVENTSK\.py\r"
expect "$ "
#change total units to event number
send "sed -i '14s/80000/$NUMEVENTS/' GEN_SIM_CRAB3_DARKSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_cT_$LIFETIMESTRING\_13TeV_events$NUMEVENTSK\.py\r"
expect "$ "
#change output Datatag
send "sed -i '17s/DarkSUSY_mH_125_mGammaD_0250_cT_000_13TeV_MG452_BR224_LHE_pythia8_GEN_SIM_MINIAOD_V2_v1/DarkSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_cT_$LIFETIMESTRING\_13TeV_$NUMEVENTSK\_MG452_BR224_LHE_pythia8_GEN_SIM_MINIAOD_V2_v1/' GEN_SIM_CRAB3_DARKSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_cT_$LIFETIMESTRING\_13TeV_events$NUMEVENTSK\.py\r"
expect "$ "
#submit job
send "crab submit -c GEN_SIM_CRAB3_DARKSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_cT_$LIFETIMESTRING\_13TeV_events$NUMEVENTSK\.py\r"
expect {
"Enter GRID pass phrase for this identity: "
{
send "??????\r"
expect "$ "
sleep 1
}
"$ "
{
sleep 1
}
}

#save file
send "date >> Crab_submit_DarkSUSY_GEN_SIM.log\r"
expect "$ "
send "echo \'User, Mass of N2 (string), Mass of GammaD (string), Lifetime of mGammaD(string), Number of Events, Number of Events (k): \' >> FileCreation_typical_n2_10GeV.log \r"
expect "$ "
send "echo \'wshi, $N2MASS, $MASS, $LIFETIMESTRING, $NUMEVENTS, $NUMEVENTSK  \' >> Crab_submit_DarkSUSY_GEN_SIM.log \r"
expect "$ "
send "echo \'\\n\' >> Crab_submit_DarkSUSY_GEN_SIM.log \r"
expect "$ "
sleep 2

}
}
}
}

send "exit\r"
expect "$ "


