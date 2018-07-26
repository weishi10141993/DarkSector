#!/usr/bin/expect -f

set timeout 86400
################
spawn sh
expect "$ "
send "export EOS_MGM_URL=root://eoscms.cern.ch\r"
expect "$ "

for { set i 1 } { $i < 761 } { incr i } {

send "xrdcp root://cms-xrd-global.cern.ch//store/user/dildick/DarkSUSY_mH_125_mGammaD_0400_cT_0_14TeV/DarkSUSY_mH_125_mGammaD_0400_cT_0_13TeV_RECO/171018_214203/0000/out_reco_$i\.root .\r"
expect "$ "
sleep 2
}

send "exit\r"
expect "$ "
