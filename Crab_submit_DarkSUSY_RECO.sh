#!/usr/bin/expect -f

set timeout 86400
set pass "LXPLUS PASS"
set gridpass "GRIDPASS"
set n2mass [list 10 30 60]
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

for { set m 0 } { $m < [llength $n2mass] } { incr m } {

set N2MASS [lindex $n2mass $m]

if { $N2MASS in [list 10] } {
set mass [list 0p25 0p4 0p7 1 5]
} elseif { $N2MASS in [list 30] } {
set mass [list 10]
} elseif { $N2MASS in [list 60] } {
set mass [list 58]
} else {
sleep 1
}

for { set k 0 } { $k < [llength $mass] } { incr k } {

set MASS [lindex $mass $k]

if { $MASS in [list 0p25] } {
set lifetimeString [list 0 0p05 0p1 0p5 1 2 5 20 100]
} elseif { $MASS in [list 0p4] } {
set lifetimeString [list 0 0p5 1 2 5 20 100]
} elseif { $MASS in [list 0p7] } {
set lifetimeString [list 0 0p5 1 5 20 100]
} elseif { $MASS in [list 1] } {
set lifetimeString [list 0 1 20 100]
} elseif { $MASS in [list 5] } {
set lifetimeString [list 0 1 20 100]
} elseif { $MASS in [list 10] } {
set lifetimeString [list 0 100]
} elseif { $MASS in [list 58] } {
set lifetimeString [list 0 100]
} else {
sleep 1
}

for { set j 0 } { $j < [llength $lifetimeString] } { incr j } {

set LIFETIMESTRING [lindex $lifetimeString $j]

if { $LIFETIMESTRING in [list 100] } {
set numevents [list 80000 79000 78000 77000 76000 75000 74000 73000 72000 71000 70000 69000 68000 67000 66000 65000 64000 63000 62000 61000 60000 59000]
set numeventsk [list 80k 79k 78k 77k 76k 75k 74k 73k 72k 71k 70k 69k 68k 67k 66k 65k 64k 63k 62k 61k 60k 59k]
} elseif { $LIFETIMESTRING in [list 20] } {
set numevents [list 80000 79000 78000 77000 76000 75000 74000 73000 72000 71000 70000 69000 68000 67000]
set numeventsk [list 80k 79k 78k 77k 76k 75k 74k 73k 72k 71k 70k 69k 68k 67k]
} elseif { $LIFETIMESTRING in [list 5 2 1] } {
set numevents [list 47000 48000 49000 51000 52000 53000]
set numeventsk [list 47k 48k 49k 51k 52k 53k]
} elseif { $LIFETIMESTRING in [list 0p5 0p1 0p05 0]} {
set numevents [list 80000 20000]
set numeventsk [list 80k 20k]
} else {
sleep 1
}

for { set i 0 } { $i < [llength $numevents] } { incr i } {

set NUMEVENTS [lindex $numevents $i]
set NUMEVENTSK [lindex $numeventsk $i]

send "crab status -d crab_projects/crab_DarkSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_cT_$LIFETIMESTRING\_13TeV_$NUMEVENTSK\_DIGI_L1_DIGI2RAW_HLT_PU_MINIAOD_V2_v1\r"
expect {
"Enter GRID pass phrase for this identity:" {
send "$gridpass\r"
}
"$ " {
send "\r"
}
}
expect "$ "
send "crab status -d crab_projects/crab_DarkSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_cT_$LIFETIMESTRING\_13TeV_$NUMEVENTSK\_DIGI_L1_DIGI2RAW_HLT_PU_MINIAOD_V2_v1 > Output_DIGI_RAW_DarkSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_cT_$LIFETIMESTRING\_13TeV_$NUMEVENTSK\.txt\r"
expect {
"Enter GRID pass phrase for this identity:" {
send "$gridpass\r"
}
"$ " {
send "\r"
}
}
expect "$ "
send "sed -i '/Output dataset:/!d' Output_DIGI_RAW_DarkSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_cT_$LIFETIMESTRING\_13TeV_$NUMEVENTSK\.txt\r"
expect "$ "
send "sed -i 's/Output dataset://g' Output_DIGI_RAW_DarkSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_cT_$LIFETIMESTRING\_13TeV_$NUMEVENTSK\.txt\r"
expect "$ "
send "sed -i 's/\^\[ \\t\]\*//' Output_DIGI_RAW_DarkSUSY_mH_125_mN1_$N2MASS\_mGammaD_$MASS\_cT_$LIFETIMESTRING\_13TeV_$NUMEVENTSK\.txt\r"

expect "$ "
send "date >> Crab_submit_DarkSUSY_RECO.log\r"
expect "$ "
send "echo \'User, Mass of N2 (string), Mass of GammaD (string), Lifetime of mGammaD(string), Number of Events, Number of Events (k): \' >> Crab_submit_DarkSUSY_RECO.log \r"
expect "$ "
send "echo \'wshi, $N2MASS, $MASS, $LIFETIMESTRING, $NUMEVENTS, $NUMEVENTSK  \' >> Crab_submit_DarkSUSY_RECO.log \r"
expect "$ "
send "echo \'\\n\' >> Crab_submit_DarkSUSY_RECO.log \r"
expect "$ "
}

}

}

}

send "exit\r"
expect "$ "
