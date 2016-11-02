## import skeleton process
#from PhysicsTools.PatAlgos.patTemplate_cfg import *
import FWCore.ParameterSet.Config as cms
process = cms.Process("MuJetProducer")

process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("FWCore.MessageService.MessageLogger_cfi")

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag


#we may need this since in patTemplate_cfg its auto:run2_mc
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2_asymptotic_2016_miniAODv2_v1', '')

# verbose flags for the PF2PAT modules
#process.options.allowUnscheduled = cms.untracked.bool(False)

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
#process.load("MuJetAnalysis.CutFlowAnalyzer.CutFlowAnalyzer_cff")

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
		'file:out_miniaod_1.root'
  )
)

#process.maxEvents.input = -1
process.maxEvents = cms.untracked.PSet( 
    input = cms.untracked.int32(-1) 
)

#process.MessageLogger = cms.Service("MessageLogger", 
#    destinations = cms.untracked.vstring("cout"), 
#    cout = cms.untracked.PSet(threshold = cms.untracked.string("ERROR"))
#)

process.p = cms.Path(
	process.patifyMC *
        process.MuJetProducers 
)

#process.outpath = cms.EndPath(process.out)

#process.TFileService = cms.Service("TFileService",
 #   fileName = cms.string("out_ana.root")
#)
