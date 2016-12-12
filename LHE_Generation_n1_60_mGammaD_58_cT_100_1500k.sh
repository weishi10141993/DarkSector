#!/usr/bin/expect -f
#This is a script written by Benjamin Michlin for DarkSUSY LHE files generation.
#Add changing n2 mass by Wei Shi for 2016 analysis.
#set n2 mass: 60GeV(n2 is lightest neutralino with id 3000002)
#dark neutralino n1(id 3000001) is still fixed at 1GeV

set timeout 86400
#set dark photon mGammaD mass
set gev [list 58]
set mass [list 58]
#set lightest neutralino n2 mass
set n2gev [list 60]
set n2mass [list 60]
#cT is not large here: 80k events
set lifetimemm [list 100]
set lifetimeString [list 100]
set numevents [list 80000 79000 78000 77000 76000 75000 74000 73000 72000 71000 70000 69000 68000 67000 66000 65000 64000 63000 62000 61000 60000 59000]
set numeventsk [list 80k 79k 78k 77k 76k 75k 74k 73k 72k 71k 70k 69k 68k 67k 66k 65k 64k 63k 62k 61k 60k 59k]
set RANDOMA [list 5457 6294 4358 3762 7549 8732 2344 4765 9356 3277 4885 8374 8294 3857 2938 8278 4626 7346 3545 5792 4628 2488]
set RANDOMB [list 5457 6294 4358 3762 7549 8732 2344 4765 9356 3277 4885 8374 8294 3857 2938 8278 4626 7346 3545 5792 4628 2488]
set RANDOMC [list 54537 62904 43538 37622 75459 87327 23443 47654 93563 32772 48855 83743 82943 38572 29383 82783 46262 73463 35452 57921 46281 24881]
################
spawn ssh -X -Y wshi@lxplus.cern.ch
expect "Password: "
send "????????\r"
expect "$ "
send "tmux\r"
expect "$ "

for { set m 0 } { $m < [llength $n2mass] } { incr m } {

set N2MASS [lindex $n2mass $m]
set N2GEV [lindex $n2gev $m]

for { set k 0 } { $k < [llength $mass] } { incr k } {

set MASS [lindex $mass $k];
set GEV [lindex $gev $k];

for { set i 0 } { $i < [llength $numevents] } { incr i } {


set NUMEVENTS [lindex $numevents $i];
set NUMEVENTSK [lindex $numeventsk $i];
set randomA [lindex $RANDOMA $i];
set randomB [lindex $RANDOMB $i];
set randomC [lindex $RANDOMC $i];


send "cd /afs/cern.ch/user/w/wshi/public/DisplacedMuonJetAnalysis_2016/CMSSW_8_0_20/src\r"
expect "$ "
send "cmsenv\r"
expect "$ "
send "cd DarkSUSY_LHE_COPY/MG_ME_V4.5.2\r"
expect "$ "
send "rm -rf Models/usrmod_DarkSusy_mH_125_mN1_$N2MASS\_mGammaD_$MASS\r"
expect "$ "
send "sed -i '/= iseed   ! rnd seed (0=assigned automatically=default))/c \\ $randomA    = iseed   ! rnd seed (0=assigned automatically=default)) ' pp_to_Higgs_HEFT_Model/Cards/run_card.dat\r"
expect "$ "
send "sed -i '/= nevents ! Number of unweighted events requested/c \\ $NUMEVENTS    = nevents ! Number of unweighted events requested' pp_to_Higgs_HEFT_Model/Cards/run_card.dat\r"
expect "$ "
send "cd pp_to_Higgs_HEFT_Model/bin\r"
expect "$ "
send "./generate_events\r"
expect "Enter 2 for multi-core, 1 for parallel, 0 for serial run"
send "0\r"
expect "Enter run name"
send "ggToHiggs_mH_125_13TeV_madgraph452_events$NUMEVENTSK\r"
expect "$ "
send "cd ../Events\r"
expect "$ "
sleep 2
send "gunzip -d ggToHiggs_mH_125_13TeV_madgraph452_events$NUMEVENTSK\_unweighted_events.lhe.gz\r"
sleep 2
#Begin section 3
expect "$ "
send "cd ../../ \r"
expect "$ "
send "cp -r Models/usrmod Models/usrmod_DarkSusy_mH_125_mN1_$N2MASS\_mGammaD_$MASS\r"
expect "$ "
send "sed -i 's/#MODEL EXTENSION/#MODEL EXTENSION\\nn1      n1        F        S      MN1   WN1     S    n1   3000001\\nn2      n2        F        S      MN2   WN2     S    n2   3000002\\nzd      zd        V        W      MZD   WZD     S    zd   3000022\\nmu1-    mu1+      F        S      MMU1  WMU1    S    mu1  3000013\\n/g' Models/usrmod_DarkSusy_mH_125_mN1_$N2MASS\_mGammaD_$MASS/particles.dat\r"
expect "$ "
#Model interactions are also already defined
send "cd Models/usrmod_DarkSusy_mH_125_mN1_$N2MASS\_mGammaD_$MASS\r"
expect "$ "
send "sed -i 's/#   USRVertex/#   USRVertex\\nn2   n2   h    GHN22   QED\\nn2   n1   zd   GZDN12  QED\\nmu1- mu1- zd   GZDL    QED/g' interactions.dat\r"
expect "$ "
send "sed -i 's/ta- ta- h GHTAU QED/#ta- ta- h GHTAU QED/g' interactions.dat\r"
expect "$ "
send "sed -i 's/b   b   h GHBOT QED/#b   b   h GHBOT QED/g' interactions.dat\r"
expect "$ "
send "sed -i 's/t   t   h GHTOP QED/#t   t   h GHTOP QED/g' interactions.dat\r"
expect "$ "
send "sed -i 's/w- w+ h  GWWH  QED/#w- w+ h  GWWH  QED/g' interactions.dat\r"
expect "$ "
send "sed -i 's/z  z  h  GZZH  QED/#z  z  h  GZZH  QED/g' interactions.dat\r"
expect "$ "
#Redefine Model Couplings
send "./ConversionScript.pl\r"
expect "Need to keep old couplings.f and param_card.dat? yes or no: "
send "yes\r"
expect "$ "
send "sed -i 's/GHN22(1)=dcmplx(1d0,Zero)/GHN22(1)=dcmplx(1d-3,Zero)/g' couplings.f\r"
expect "$ "
send "sed -i 's/GHN22(2)=dcmplx(1d0,Zero)/GHN22(2)=dcmplx(1d-3,Zero)/g' couplings.f\r"
expect "$ "
send "sed -i 's/GZDN12(1)=dcmplx(1d0,Zero)/GZDN12(1)=dcmplx(1d-3,Zero)/g' couplings.f\r"
expect "$ "
send "sed -i 's/GZDN12(2)=dcmplx(1d0,Zero)/GZDN12(2)=dcmplx(1d-3,Zero)/g' couplings.f\r"
expect "$ "
send "sed -i 's/GZDL(1)=dcmplx(1d0,Zero)/GZDL(1)=dcmplx(1d-3,Zero)/g' couplings.f\r"
expect "$ "
send "sed -i 's/GZDL(2)=dcmplx(1d0,Zero)/GZDL(2)=dcmplx(1d-3,Zero)/g' couplings.f\r"
expect "$ "
send "sed -i 's/25     1.20000000E+02   # H        mass/25     1.25000000E+02   # H        mass/g' param_card.dat\r"
expect "$ "
send "sed -i 's/3000001     1.00000000e+02   # MN1/3000001     1.00000000e+00   # MN1/g' param_card.dat\r"
expect "$ "
#change n2 mass here to 60GeV
#send "sed -i 's/3000002     1.00000000e+02   # MN2/3000002     6.00000000e+01   # MN2/g' param_card.dat\r"
send "sed -i 's/3000002     1.00000000e+02   # MN2/3000002     $N2GEV   # MN2/g' param_card.dat\r"
expect "$ "
send "sed -i 's/3000022     1.00000000e+02   # MZD/3000022     $GEV   # MZD/g' param_card.dat\r"
expect "$ "
send "sed -i 's/3000013     1.00000000e+02   # MMU1/3000013     1.05000000e-01   # MMU1/g' param_card.dat\r"
expect "$ "
send "sed -i 's/DECAY   3000001     1.00000000e+00   # WN1/DECAY   3000001     0.00000000e+00   # WN1/g' param_card.dat\r"
expect "$ "
send "sed -i 's/DECAY   3000013     1.00000000e+00   # WMU1/DECAY   3000013     0.00000000e+00   # WMU1/g' param_card.dat\r"
expect "$ "
send "sed -i 's/DECAY        25     6.79485838E-03   # H   width/DECAY        25     1.00000000e+00   # H   width/g' param_card.dat\r"
expect "$ "
#interact
send "make couplings\r"
expect "$ "
send "./couplings\r"
expect "$ "
send "cd ../../BRIDGE/\r"
expect "$ "
send "./runBRI.exe\r"
expect "Would you like to run from a MadGraph Model directory? (Y/N) "
send "Y\r"
expect "What is the name of the model directory(assuming that it is a subdirectory of Models/): "
send "usrmod_DarkSusy_mH_125_mN1_$N2MASS\_mGammaD_$MASS\r"
expect "Do you wish to generate decay tables for all particles listed above or a subset?(type 1 for all, 2 for subset)"
send "2\r"
expect "Please enter particles you wish to create decay tables for, you must explicitly enter antiparticles if you want BRI to generate their decay tables, otherwise use antigrids.pl: (type 'done' when finished)"
send "h\r"
sleep 2
send "n2\r"
sleep 2
send "zd\r"
sleep 2
send "done\r"
expect "Please enter a random number seed or write 'time' to use the time"
send "$randomB\r"
expect "The default number of Vegas calls is 50000. Would you like to change this? (Y/N) "
send "n\r"
expect "The default max. number of Vegas iterations is 5. Would you like to change this? (Y/N) "
send "n\r"
expect "Would you like to calculate three-body widths even for particles with open 2-body channels? (Y/N) "
send "n\r"
#expect "Decay table appears to already exist. Should we recreate it? Type 'yes' if so, otherwise we will exit."
#send "yes\r"
#expect "Decay table appears to already exist. Should we recreate it? Type 'yes' if so, otherwise we will exit."
#send "yes\r"
#expect "Decay table appears to already exist. Should we recreate it? Type 'yes' if so, otherwise we will exit."
#send "yes\r"
expect "Do you wish to replace the values of the param_card.dat widths, with the values stored in slha.out?(Y/N)"
send "y\r"
expect "Do you wish to keep a copy of the old param_card.dat?(Y/N) "
send "y\r"
expect "$ "
send "./runDGE.exe\r"
expect "Would you like to run from a MadGraph Model directory? (Y/N) "
send "Y\r"
expect "What is the name of the model directory(assuming that it is a subdirectory of Models/): "
send "usrmod_DarkSusy_mH_125_mN1_$N2MASS\_mGammaD_$MASS\r"
expect "What is the name of the input event file(include path if directory is different from where DGE is running)? "
send "/afs/cern.ch/user/w/wshi/public/DisplacedMuonJetAnalysis_2016/CMSSW_8_0_20/src/DarkSUSY_LHE_COPY/MG_ME_V4.5.2/pp_to_Higgs_HEFT_Model/Events/ggToHiggs_mH_125_13TeV_madgraph452_events$NUMEVENTSK\_unweighted_events.lhe\r"
expect "What is the name of the output event file(include path if directory is different from where DGE is running)? "
send "/afs/cern.ch/work/w/wshi/public/DarkSUSYMC_LHE_Moriond2017_Part2/DarkSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_13TeV-madgraph452_bridge224_events$NUMEVENTSK\.lhe\r"
expect "Please enter a random number seed or write 'time' to use the time"
send "$randomC\r"
expect "Which mode? "
send "2\r"
expect "Which mode? "
send "2\r"
expect "Enter a final-state particle name, or \"END\" to finish: "
send "mu1+\r"
expect "Enter a final-state particle name, or \"END\" to finish: "
send "mu1-\r" 
expect "Enter a final-state particle name, or \"END\" to finish: "
send "END\r"
expect "Would you like to save the list of final-state particles? (Y/N) "
send "Y\r"
expect "What file name do you want to save to?"
sleep 1
send "/afs/cern.ch/work/w/wshi/public/DarkSUSYMC_LHE_Moriond2017_Part2/DarkSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_13TeV-madgraph452_bridge224_ListFinalStateParticles.txt\r"
expect "$ "
sleep 1
send "sed -i 's/3000013 /13 /g' /afs/cern.ch/work/w/wshi/public/DarkSUSYMC_LHE_Moriond2017_Part2/DarkSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_13TeV-madgraph452_bridge224_events$NUMEVENTSK\.lhe\r"
expect "$ "
sleep 1
send "sed -i '/filename =/c \\filename = \"/afs/cern.ch/work/w/wshi/public/DarkSUSYMC_LHE_Moriond2017_Part2/DarkSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_13TeV-madgraph452_bridge224_events$NUMEVENTSK\.lhe\"' replace_lifetime_in_LHE.py\r"
sleep 1

for { set j 0 } { $j < [llength $lifetimemm] } { incr j } {

set LIFETIME [lindex $lifetimemm $j];
set LIFETIMESTRING [lindex $lifetimeString $j];

expect "$ "
send "sed -i 's/ctau_mean_mm = 5.0/ctau_mean_mm = $LIFETIME/g' replace_lifetime_in_LHE.py\r"
expect "$ "
send "python replace_lifetime_in_LHE.py > /afs/cern.ch/work/w/wshi/public/DarkSUSYMC_LHE_Moriond2017_Part2/DarkSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_13TeV_cT_$LIFETIMESTRING\_madgraph452_bridge224_events$NUMEVENTSK\.lhe\r"
expect "$ "
send "sed -i 's/ctau_mean_mm = $LIFETIME/ctau_mean_mm = 5.0/g' replace_lifetime_in_LHE.py\r"

}

expect "$ "
send "date >> FileCreation_typical_n2_10GeV.log\r"
expect "$ "
send "echo \'User, Mass of N2 (string), Mass of N2 (GeV), Mass of GammaD (string), Mass of GammaD (GeV), Number of Events, Number of Events (k), RandomSeed (MADGRAPH), RandomSeed (BRIDGE 1), RandomSeed (BRIDGE 2): \' >> FileCreation_typical_n2_10GeV.log \r"
expect "$ "
send "echo \'wshi, $N2MASS, $N2GEV, $MASS, $GEV, $NUMEVENTS, $NUMEVENTSK, $randomA, $randomB, $randomC  \' >> FileCreation_typical_n2_10GeV.log \r"
expect "$ "
send "echo \'\\n\' >> FileCreation_typical_n2_10GeV.log \r"
expect "$ "
}
}
}

send "exit\r"
expect "$ "
