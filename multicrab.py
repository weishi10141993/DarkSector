from WMCore.Configuration import Configuration
import datetime

config = Configuration()

workflow='reco' 
cmssw_version='1015'
extra_info='TnP2018Bv2SingleMu'
era=2018
RunOnMC = False
WriteToTAMU = True
useParent = False
dryRun=False # when True, jobs are not submitted (for testing only)

Nunits=5
if (RunOnMC):
  Nunits=3
else:
  Nunits=80

if workflow == 'reco':
  pSet = 'tp_from_aod_Data_Zmumu.py'
  JOBID = 'CMSSW-'+cmssw_version+extra_info
elif workflow == 'MC':
  pSet = 'l1NtupleAODEMUGEN_RAW2DIGI.py'
  JOBID = 'CMSSW-'+cmssw_version+extra_info
elif workflow == 'reEmu' and era==2015:
  pSet = 'l1Ntuple2015_RAW2DIGI.py'
  JOBID = 'CMSSW-'+cmssw_version+extra_info
elif era==2016 :
  pSet = 'l1NtupleAOD2016_ENDJOB.py'
  JOBID = 'CMSSW-'+cmssw_version+extra_info
elif era==2015 :
  pSet = 'l1Ntuple2015_'+workflow+'.py'
  JOBID = 'CMSSW-'+cmssw_version+workflow+extra_info
else:
  print('%ERR: no workflow found')


## JSON

#regular PPD JSON
if era==2015:
  JSON='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Reprocessing/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON.txt'
elif era==2016:
  JSON = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Final/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt'
elif era==2017:
  #JSON = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
  JSON = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'
elif era==2018:
  #JSON = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PromptReco/Cert_314472-317696_13TeV_PromptReco_Collisions18_JSON.txt'
  JSON = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PromptReco/Cert_314472-318876_13TeV_PromptReco_Collisions18_JSON.txt'
elif era==-1: #custom made JSON
  JSON = './json_DCSONLY.txt'
else:
  sys.exit('%ERROR: Era can be 2015, 2016, 2017, or 2018.')

print('Nutples will appear in the usual location in the subdiretory '+JOBID)


###########

#logbase="Run2016_Skims"
#myJobs={
#  "SingleMuon_Run2016B-ZMu-07Aug17_ver1-v1" :["/SingleMuon/Run2016B-ZMu-07Aug17_ver1-v1/RAW-RECO", Nunits, -1],
#  "SingleMuon_Run2016B-ZMu-07Aug17_ver2-v1" :["/SingleMuon/Run2016B-ZMu-07Aug17_ver2-v1/RAW-RECO", Nunits, -1],
#  "SingleMuon_Run2016C-ZMu-07Aug17-v1"      :["/SingleMuon/Run2016C-ZMu-07Aug17-v1/RAW-RECO", Nunits, -1],
#  "SingleMuon_Run2016D-ZMu-07Aug17-v1"      :["/SingleMuon/Run2016D-ZMu-07Aug17-v1/RAW-RECO", Nunits, -1],
#  "SingleMuon_Run2016E-ZMu-07Aug17-v1"      :["/SingleMuon/Run2016E-ZMu-07Aug17-v1/RAW-RECO", Nunits, -1],
#  "SingleMuon_Run2016F-ZMu-07Aug17-v1"      :["/SingleMuon/Run2016F-ZMu-07Aug17-v1/RAW-RECO", Nunits, -1],
#  "SingleMuon_Run2016G-ZMu-07Aug17-v1"      :["/SingleMuon/Run2016G-ZMu-07Aug17-v1/RAW-RECO", Nunits, -1],
#  "SingleMuon_Run2016H-ZMu-07Aug17-v1"      :["/SingleMuon/Run2016H-ZMu-07Aug17-v1/RAW-RECO", Nunits, -1],
#}

#######
#logbase="Run2016_07Aug17rereco"
#myJobs={
#  "SingleMuon_Run2016B-07Aug17_ver1-v1" : ["/SingleMuon/Run2016B-07Aug17_ver1-v1/AOD", Nunits, -1],
#  "SingleMuon_Run2016B-07Aug17_ver2-v1" : ["/SingleMuon/Run2016B-07Aug17_ver2-v1/AOD", Nunits, -1],
#  "SingleMuon_Run2016C-07Aug17-v1"      : ["/SingleMuon/Run2016C-07Aug17-v1/AOD", Nunits, -1],
#  "SingleMuon_Run2016D-07Aug17-v1"      : ["/SingleMuon/Run2016D-07Aug17-v1/AOD", Nunits, -1],
#  "SingleMuon_Run2016E-07Aug17-v1"      : ["/SingleMuon/Run2016E-07Aug17-v1/AOD", Nunits, -1],
#  "SingleMuon_Run2016F-07Aug17-v1"      : ["/SingleMuon/Run2016F-07Aug17-v1/AOD", Nunits, -1],
#  "SingleMuon_Run2016G-07Aug17-v1"      : ["/SingleMuon/Run2016G-07Aug17-v1/AOD", Nunits, -1],
#  "SingleMuon_Run2016H-07Aug17-v1"      : ["/SingleMuon/Run2016H-07Aug17-v1/AOD", Nunits, -1]
#}

#logbase="Run2017Cv3_DiMuon"
#myJobs={
#  "MuOnia_Run2017C-PromptReco-v3"            :["/MuOnia/Run2017C-PromptReco-v3/AOD", Nunits, -1],
#  "Charmonium_Run2017C-PromptReco-v3"        :["/Charmonium/Run2017C-PromptReco-v3/AOD", Nunits, -1],
#  "DoubleMuon_Run2017C-PromptReco-v3"        :["/DoubleMuon/Run2017C-PromptReco-v3/AOD", Nunits, -1],
#  "DoubleMuonLowMass_Run2017C-PromptReco-v3" :["/DoubleMuonLowMass/Run2017C-PromptReco-v3/AOD", Nunits, -1]
#}

#logbase="Run2017Dv1_DiMuon"
#myJobs={
#  "MuOnia_Run2017D-PromptReco-v1"            :["/MuOnia/Run2017D-PromptReco-v1/AOD", Nunits, -1],
#  "Charmonium_Run2017D-PromptReco-v1"        :["/Charmonium/Run2017D-PromptReco-v1/AOD", Nunits, -1],
#  "DoubleMuon_Run2017D-PromptReco-v1"        :["/DoubleMuon/Run2017D-PromptReco-v1/AOD", Nunits, -1],
#  "DoubleMuonLowMass_Run2017D-PromptReco-v1" :["/DoubleMuonLowMass/Run2017D-PromptReco-v1/AOD", Nunits, -1]
#}

#logbase="Run2017_MET"
#myJobs={
#  "MET_Run2017D-PromptReco-v1"            :["/MET/Run2017D-PromptReco-v1/AOD", Nunits, -1]
#}

#logbase="Run2018_ZMu"
#myJobs={
#  "SingleMuon_Run2018A-ZMu-PromptReco-v1"  :["/SingleMuon/Run2018A-ZMu-PromptReco-v1/RAW-RECO", Nunits, -1],
#}

#logbase="Run2017_ZMu"
#myJobs={
#  "SingleMuon_Run2017B-ZMu-12Sep2017-v1"  :["/SingleMuon/Run2017B-ZMu-12Sep2017-v1/RAW-RECO", Nunits, -1],
#  "SingleMuon_Run2017B-ZMu-PromptReco-v2" :["/SingleMuon/Run2017B-ZMu-PromptReco-v2/RAW-RECO", Nunits, -1],
#  "SingleMuon_Run2017C-ZMu-12Sep2017-v1"  :["/SingleMuon/Run2017C-ZMu-12Sep2017-v1/RAW-RECO", Nunits, -1],
#  "SingleMuon_Run2017C-ZMu-PromptReco-v2" :["/SingleMuon/Run2017C-ZMu-PromptReco-v2/RAW-RECO", Nunits, -1],
#  "SingleMuon_Run2017C-ZMu-PromptReco-v3" :["/SingleMuon/Run2017C-ZMu-PromptReco-v3/RAW-RECO", Nunits, -1],
#  "SingleMuon_Run2017D-ZMu-PromptReco-v1" :["/SingleMuon/Run2017D-ZMu-PromptReco-v1/RAW-RECO", Nunits, -1],
#  "SingleMuon_Run2017E-ZMu-PromptReco-v1" :["/SingleMuon/Run2017E-ZMu-PromptReco-v1/RAW-RECO", Nunits, -1],
#  "SingleMuon_Run2017F-ZMu-PromptReco-v1" :["/SingleMuon/Run2017F-ZMu-PromptReco-v1/RAW-RECO", Nunits, -1]
#}

#logbase="Run2017_ZMu_17NovReReco"
#myJobs={
#  "SingleMuon_Run2017B-ZMu-17Nov2017-v1" :["/SingleMuon/Run2017B-ZMu-17Nov2017-v1/RAW-RECO", Nunits, -1],
#  "SingleMuon_Run2017C-ZMu-17Nov2017-v1" :["/SingleMuon/Run2017C-ZMu-17Nov2017-v1/RAW-RECO", Nunits, -1],
#  "SingleMuon_Run2017D-ZMu-17Nov2017-v1" :["/SingleMuon/Run2017D-ZMu-17Nov2017-v1/RAW-RECO", Nunits, -1],
#  "SingleMuon_Run2017E-ZMu-17Nov2017-v1" :["/SingleMuon/Run2017E-ZMu-17Nov2017-v1/RAW-RECO", Nunits, -1],
#  "SingleMuon_Run2017F-ZMu-17Nov2017-v1" :["/SingleMuon/Run2017F-ZMu-17Nov2017-v1/RAW-RECO", Nunits, -1]
#}

#logbase="Run2017_SingleMuon"
#myJobs={
#  "SingleMuon_Run2017B-PromptReco-v1" :["/SingleMuon/Run2017B-PromptReco-v1/AOD", Nunits, -1],
#  "SingleMuon_Run2017B-PromptReco-v2" :["/SingleMuon/Run2017B-PromptReco-v2/AOD", Nunits, -1],
#  "SingleMuon_Run2017C-PromptReco-v1" :["/SingleMuon/Run2017C-PromptReco-v1/AOD", Nunits, -1],
#  "SingleMuon_Run2017C-PromptReco-v2" :["/SingleMuon/Run2017C-PromptReco-v2/AOD", Nunits, -1],
#  "SingleMuon_Run2017C-PromptReco-v3" :["/SingleMuon/Run2017C-PromptReco-v3/AOD", Nunits, -1],
#  "SingleMuon_Run2017D-PromptReco-v1" :["/SingleMuon/Run2017D-PromptReco-v1/AOD", Nunits, -1],
#  "SingleMuon_Run2017E-PromptReco-v1" :["/SingleMuon/Run2017E-PromptReco-v1/AOD", Nunits, -1],
#  "SingleMuon_Run2017F-PromptReco-v1" :["/SingleMuon/Run2017F-PromptReco-v1/AOD", Nunits, -1]
#}

#logbase="Run2017_SingleMuon_17NovReReco"
#myJobs={
#  "SingleMuon_Run2017B-17Nov2017-v1" :["/SingleMuon/Run2017B-17Nov2017-v1/AOD", Nunits, -1],
#  "SingleMuon_Run2017C-17Nov2017-v1" :["/SingleMuon/Run2017C-17Nov2017-v1/AOD", Nunits, -1],
#  "SingleMuon_Run2017D-17Nov2017-v1" :["/SingleMuon/Run2017D-17Nov2017-v1/AOD", Nunits, -1],
#  "SingleMuon_Run2017E-17Nov2017-v1" :["/SingleMuon/Run2017E-17Nov2017-v1/AOD", Nunits, -1],
#  "SingleMuon_Run2017F-17Nov2017-v1" :["/SingleMuon/Run2017F-17Nov2017-v1/AOD", Nunits, -1]
#}

#logbase="Run2017_JetHT_17NovReReco"
#myJobs={
#  "JetHT_Run2017B-17Nov2017-v1" :["/JetHT/Run2017B-17Nov2017-v1/AOD", Nunits, -1],
#  "JetHT_Run2017C-17Nov2017-v1" :["/JetHT/Run2017C-17Nov2017-v1/AOD", Nunits, -1],
#  "JetHT_Run2017D-17Nov2017-v1" :["/JetHT/Run2017D-17Nov2017-v1/AOD", Nunits, -1],
#  "JetHT_Run2017E-17Nov2017-v1" :["/JetHT/Run2017E-17Nov2017-v1/AOD", Nunits, -1],
#  "JetHT_Run2017F-17Nov2017-v1" :["/JetHT/Run2017F-17Nov2017-v1/AOD", Nunits, -1]
#}

#logbase="Run2017_MET_17NovReReco"
#myJobs={
#  "MET_Run2017B-17Nov2017-v1" :["/MET/Run2017B-17Nov2017-v1/AOD", Nunits, -1],
#  "MET_Run2017C-17Nov2017-v1" :["/MET/Run2017C-17Nov2017-v1/AOD", Nunits, -1],
#  "MET_Run2017D-17Nov2017-v1" :["/MET/Run2017D-17Nov2017-v1/AOD", Nunits, -1],
#  "MET_Run2017E-17Nov2017-v1" :["/MET/Run2017E-17Nov2017-v1/AOD", Nunits, -1],
#  "MET_Run2017F-17Nov2017-v1" :["/MET/Run2017F-17Nov2017-v1/AOD", Nunits, -1]
#}

#logbase="TSG_928_mc"
#myJobs={
#  "SingleNeutrino"                                    :["/SingleNeutrino/RunIISummer17DRStdmix-NZSFlatPU28to62_92X_upgrade2017_realistic_v10_ext1-v1/AODSIM", Nunits, -1],
#  "DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8"             :["/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v1/AODSIM", Nunits, -1],
#  "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8"            :["/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/AODSIM", Nunits, -1],
#  "JPsiToMuMu_Pt20to120_EtaPhiRestricted-pythia8-gun" :["/JPsiToMuMu_Pt20to120_EtaPhiRestricted-pythia8-gun/RunIISummer17DRStdmix-NZSNoPU_92X_upgrade2017_realistic_v10-v2/AODSIM", Nunits, -1],
#  "SingleMu_Pt1To1000_FlatRandomOneOverPt"            :["/SingleMu_Pt1To1000_FlatRandomOneOverPt/RunIISummer17DRStdmix-NZSNoPU_92X_upgrade2017_realistic_v10-v2/AODSIM", Nunits, -1],
#  "WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" :["/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_SUS01_92X_upgrade2017_realistic_v10-v1/AODSIM", Nunits, -1],
#}

#logbase="Run2017F_ZeroBiasX"
#myJobs={
#  "ZeroBias_Run2017F-v1" :["/ZeroBias/Run2017F-v1/RAW", Nunits, -1],
#  "ZeroBias1_Run2017F-v1" :["/ZeroBias1/Run2017F-v1/RAW", Nunits, -1],
#  "ZeroBias2_Run2017F-v1" :["/ZeroBias2/Run2017F-v1/RAW", Nunits, -1],
#  "ZeroBias3_Run2017F-v1" :["/ZeroBias3/Run2017F-v1/RAW", Nunits, -1],
#  "ZeroBias4_Run2017F-v1" :["/ZeroBias4/Run2017F-v1/RAW", Nunits, -1],
#  "ZeroBias5_Run2017F-v1" :["/ZeroBias5/Run2017F-v1/RAW", Nunits, -1],
#  "ZeroBias6_Run2017F-v1" :["/ZeroBias6/Run2017F-v1/RAW", Nunits, -1],
#  "ZeroBias7_Run2017F-v1" :["/ZeroBias7/Run2017F-v1/RAW", Nunits, -1],
#  "ZeroBias8_Run2017F-v1" :["/ZeroBias8/Run2017F-v1/RAW", Nunits, -1]
#}

logbase="Run2018B_PR_v2_SingleMuon"
myJobs={
  # "ZeroBias_Run2018B-v1" :["/ZeroBias/Run2018B-v1/RAW", Nunits, -1],
  "SingleMu_2018B-PR-v2" :["/SingleMuon/Run2018B-PromptReco-v2/AOD", Nunits, -1],
}

#logbase="Commissioning2018_ZeroBiasX"
#myJobs={
#  "ZeroBias_Commissioning2018-v1"   :["/ZeroBias/Commissioning2018-v1/RAW", Nunits, -1],
#  "ZeroBias1_Commissioning2018-v1"  :["/ZeroBias1/Commissioning2018-v1/RAW", Nunits, -1],
#  "ZeroBias2_Commissioning2018-v1"  :["/ZeroBias2/Commissioning2018-v1/RAW", Nunits, -1],
#  "ZeroBias3_Commissioning2018-v1"  :["/ZeroBias3/Commissioning2018-v1/RAW", Nunits, -1],
#  "ZeroBias4_Commissioning2018-v1"  :["/ZeroBias4/Commissioning2018-v1/RAW", Nunits, -1],
#  "ZeroBias5_Commissioning2018-v1"  :["/ZeroBias5/Commissioning2018-v1/RAW", Nunits, -1],
#  "ZeroBias6_Commissioning2018-v1"  :["/ZeroBias6/Commissioning2018-v1/RAW", Nunits, -1],
#  "ZeroBias7_Commissioning2018-v1"  :["/ZeroBias7/Commissioning2018-v1/RAW", Nunits, -1],
#  "ZeroBias8_Commissioning2018-v1"  :["/ZeroBias8/Commissioning2018-v1/RAW", Nunits, -1],
#  "ZeroBias9_Commissioning2018-v1"  :["/ZeroBias9/Commissioning2018-v1/RAW", Nunits, -1],
#  "ZeroBias10_Commissioning2018-v1" :["/ZeroBias10/Commissioning2018-v1/RAW", Nunits, -1],
#}

#logbase="Commissioning2018_L1Accept"
#myJobs={
#  "L1Accept_Commissioning2018-v1"   :["/L1Accept/Commissioning2018-v1/RAW", Nunits, -1],
#}

#logbase="Commissioning2018_HLTPhysics"
#myJobs={
#  "HLTPhysics_Commissioning2018-v1"   :["/HLTPhysics/Commissioning2018-v1/RAW", Nunits, -1],
#  "HLTPhysics1_Commissioning2018-v1"   :["/HLTPhysics1/Commissioning2018-v1/RAW", Nunits, -1],
#  "HLTPhysics2_Commissioning2018-v1"   :["/HLTPhysics2/Commissioning2018-v1/RAW", Nunits, -1],
#  "HLTPhysics3_Commissioning2018-v1"   :["/HLTPhysics3/Commissioning2018-v1/RAW", Nunits, -1],
#  "HLTPhysics4_Commissioning2018-v1"   :["/HLTPhysics4/Commissioning2018-v1/RAW", Nunits, -1],
#}


####################################

splitting   = 'LumiBased'
if RunOnMC :
    splitting   = 'FileBased'

if WriteToTAMU:
    StorageSite = 'T3_US_TAMU'
    output      = '/store/user/wshi/' + JOBID 
else:
    sys.exit("%ERROR: If you don't want to store at CERN you need to specify an alternative storage place.")

#############################################
### common for all jobs  ####################
#############################################
config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
#config.General.workArea = logbase + '_' + str(datetime.date.today())
config.General.workArea = logbase + '_' + str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
#config.General.instance = 'preprod' ## Workaround for failing crab in CMSSW_10_1_0

config.section_('JobType')
config.JobType.psetName = pSet
config.JobType.pluginName = 'Analysis'
config.JobType.maxMemoryMB = 2500
config.JobType.outputFiles = ['tnpZ_Data.root']
## config.JobType.inputFiles = ['../../data/Jet_Stage1_2015_v2.txt']

config.section_('Data')

## ccla
# Set to True to allow the jobs to run at any site. Suggested by Lucia if we want to runon data at CERN pre-publication on DAS.
#config.Data.ignoreLocality = True

config.Data.inputDBS = 'global'
config.Data.splitting = splitting
config.Data.unitsPerJob = 1
## config.Data.totalUnits = 1
config.Data.useParent = useParent
config.Data.outLFNDirBase = output
config.Data.runRange = '317640'

# apply lumi json file
if (not(RunOnMC)) :
    config.Data.lumiMask = JSON
    
config.section_('Site')
config.Site.storageSite = StorageSite

## ccla
#config.Site.whitelist = ["T2_CH*"]
config.Site.blacklist = ["T3_US_UCR"]

if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException
    from multiprocessing import Process

    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)

    #############################################################################################
    ## From now on that's what users should modify: this is the a-la-CRAB2 configuration part. ##
    #############################################################################################

    for job in myJobs.keys():

        jobPars=myJobs[job]
        print job, jobPars        
        config.General.requestName = JOBID + "__" + job  
        config.Data.inputDataset = jobPars[0]
        config.Data.unitsPerJob = jobPars[1]
        if jobPars[2] != -1:
            config.Data.runRange = str(jobPars[2])
        
        # print config
        if not dryRun:
            p = Process(target=submit, args=(config,))
            p.start()
            p.join()
