## import skeleton process
#from PhysicsTools.PatAlgos.patTemplate_cfg import *

# verbose flags for the PF2PAT modules
#process.options.allowUnscheduled = cms.untracked.bool(True)
#process.options.allowUnscheduled = cms.untracked.bool(False)

import FWCore.ParameterSet.Config as cms
#process = cms.Process("MuJetProducer")
#process = cms.Process("Demo")
process = cms.Process("CutFlowAnalyzer")

process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("FWCore.MessageService.MessageLogger_cfi")

#process.load("MuJetAnalysis.CutFlowAnalyzer.CutFlowAnalyzer_cfi")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag


#we may need this since in patTemplate_cfg its auto:run2_mc
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2_asymptotic_2016_miniAODv2_v1', '')

### Add MuJet Dataformats
#from MuJetAnalysis.DataFormats.EventContent_version10_cff import *
#process = customizePatOutput(process)

process.load("MuJetAnalysis.DataFormats.miniAODtoPAT_cff")
#process.patMuons.addGenMatch = cms.bool(True)
#process.patMuons.embedGenMatch = cms.bool(True)

## pick latest HLT process
#process.patTrigger.processName = cms.string( "*" )
#process.patTriggerEvent.processName = cms.string( "*" )

process.load("MuJetAnalysis.MuJetProducer.MuJetProducer_cff")
process.load("MuJetAnalysis.CutFlowAnalyzer.CutFlowAnalyzer_cff")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#specify in crab3 file
        "file:out_miniaod_1.root"
       # "file:/fdata/hepx/store/user/bmichlin/DarkSUSY_mH_125_mGammaD_0250_cT_000_Evt_79k_13TeV_MG452_BR224_LHE_pythia8_GEN_SIM_MCRUN2_71_V1_v1/DarkSUSY_mH_125_mGammaD_0250_cT_000_Evt_79k_13TeV_RAW2DIGI_L1Reco_RECO_MCRUN2_74_V9_v1/151026_194054/0000/out_reco_1.root"
    )
)

#process.maxEvents.input = -1
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.p = cms.Path(
    process.patifyMC *
    process.MuJetProducers * 
    process.cutFlowAnalyzers
)

#process.outpath = cms.EndPath(process.out)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string("out_ana_1.root")
)
