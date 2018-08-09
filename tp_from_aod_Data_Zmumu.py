import FWCore.ParameterSet.Config as cms

import subprocess

process = cms.Process("TagProbe")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 10

process.source = cms.Source("PoolSource", 
    fileNames = cms.untracked.vstring(),
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load("Configuration.StandardSequences.Reconstruction_cff")

import os
if "CMSSW_7_4_" in os.environ['CMSSW_VERSION']:

    #run 251168
    process.GlobalTag.globaltag = cms.string('74X_dataRun2_Prompt_v1')
    sourcefilesfolder = "/store/data/Run2015B/SingleMuon/AOD/PromptReco-v1/000/251/168/00000"
    files = subprocess.check_output([ "/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select", "ls", sourcefilesfolder ])
    process.source.fileNames = [ sourcefilesfolder+"/"+f for f in files.split() ]

    #run 251244
    sourcefilesfolder = "/store/data/Run2015B/SingleMuon/AOD/PromptReco-v1/000/251/244/00000"
    files = subprocess.check_output([ "/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select", "ls", sourcefilesfolder ])
    process.source.fileNames.extend( [ sourcefilesfolder+"/"+f for f in files.split() ] )

    #run 251251
    sourcefilesfolder = "/store/data/Run2015B/SingleMuon/AOD/PromptReco-v1/000/251/251/00000"
    files = subprocess.check_output([ "/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select", "ls", sourcefilesfolder ])
    process.source.fileNames.extend( [ sourcefilesfolder+"/"+f for f in files.split() ] )

    #run 251252
    sourcefilesfolder = "/store/data/Run2015B/SingleMuon/AOD/PromptReco-v1/000/251/252/00000"
    files = subprocess.check_output([ "/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select", "ls", sourcefilesfolder ])
    process.source.fileNames.extend( [ sourcefilesfolder+"/"+f for f in files.split() ] )

    # to add following runs: 251491, 251493, 251496, ..., 251500 
    print process.source.fileNames
    #print process.source.fileNames, dataSummary
elif "CMSSW_7_6_" in os.environ['CMSSW_VERSION']:
    process.GlobalTag.globaltag = cms.string('76X_dataRun2_v15')
    process.source.fileNames = [
            '/store/data/Run2015D/SingleMuon/AOD/16Dec2015-v1/10000/00A3E567-75A8-E511-AD0D-0CC47A4D769E.root'
    ]
elif "CMSSW_8_0_"in os.environ['CMSSW_VERSION']:
    process.GlobalTag.globaltag = cms.string('80X_dataRun2_Prompt_v9')

    process.source.fileNames = [
        '/store/data/Run2016C/SingleMuon/AOD/PromptReco-v2/000/276/283/00000/0001E5C0-AE44-E611-9F88-02163E014235.root'
        ]
elif "CMSSW_9_2_" in os.environ['CMSSW_VERSION']:
    process.GlobalTag.globaltag = cms.string('92X_dataRun2_Express_v2')

    process.source.fileNames = [
        '/store/express/Run2017B/ExpressPhysics/FEVT/Express-v1/000/297/101/00000/0C01D9CD-D253-E711-9D2F-02163E013511.root'
    ]  
elif "CMSSW_9_4_" in os.environ['CMSSW_VERSION']:
    process.GlobalTag.globaltag = cms.string('91X_mcRun2_asymptotic_v3')

    process.source.fileNames = [
            '/store/data/Run2017B/SingleMuon/AOD/17Nov2017-v1/40000/0001B172-B9D8-E711-9771-34E6D7E05F1B.root'
    ]
elif "CMSSW_10_1_" in os.environ['CMSSW_VERSION']:
    process.GlobalTag.globaltag = cms.string('101X_dataRun2_Prompt_v11')

    process.source.fileNames = [
        '/store/data/Run2018B/SingleMuon/AOD/PromptReco-v2/000/318/828/00000/B6F906F2-597C-E811-BBAA-FA163E4F3A7C.root',
        '/store/data/Run2018B/SingleMuon/AOD/PromptReco-v2/000/318/828/00000/B6228E42-547C-E811-981A-FA163EBCAB45.root',
        '/store/data/Run2018B/SingleMuon/AOD/PromptReco-v2/000/318/828/00000/ACAA703C-4F7C-E811-A0AD-FA163E3BE999.root'
    ]
    #Only use runs after control triggers are implemented, i.e. after run 317509
else: raise RuntimeError, "Unknown CMSSW version %s" % os.environ['CMSSW_VERSION']

## SELECT WHAT DATASET YOU'RE RUNNING ON
TRIGGER="SingleMu"
#TRIGGER="DoubleMu"

## ==== Fast Filters ====
process.goodVertexFilter = cms.EDFilter("VertexSelector",
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake && ndof > 4 && abs(z) <= 25 && position.Rho <= 2"),
    filter = cms.bool(True),
)
process.noScraping = cms.EDFilter("FilterOutScraping",
    applyfilter = cms.untracked.bool(True),
    debugOn = cms.untracked.bool(False), ## Or 'True' to get some per-event info
    numtrack = cms.untracked.uint32(10),
    thresh = cms.untracked.double(0.25)
)

process.load("HLTrigger.HLTfilters.triggerResultsFilter_cfi")


if TRIGGER == "SingleMu":
    process.triggerResultsFilter.triggerConditions = cms.vstring( 'HLT_IsoMu24_v*' )
elif TRIGGER == "DoubleMu":
    process.triggerResultsFilter.triggerConditions = cms.vstring( 'HLT_Mu8_v*', 'HLT_Mu17_v*',
                                                                  'HLT_Mu8_TrkIsoVVL_v*', 'HLT_Mu17_TrkIsoVVL_v*',
                                                                  'HLT_Mu17_TkMu8_v*', 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v*' )
else:
    raise RuntimeError, "TRIGGER must be 'SingleMu' or 'DoubleMu'"

process.triggerResultsFilter.l1tResults = "gtStage2Digis"
process.triggerResultsFilter.throw = False
process.triggerResultsFilter.hltResults = cms.InputTag("TriggerResults","","HLT")

#decomment when you have it
#process.triggerResultsFilterFake = process.triggerResultsFilter.clone(
#    triggerConditions = cms.vstring( 'HLT_Mu40_v*', 'HLT_Mu5_v*', 'HLT_Mu12_v*', 'HLT_Mu24_v*')
#)

process.fastFilter     = cms.Sequence(process.goodVertexFilter + process.noScraping + process.triggerResultsFilter)
#process.fastFilterFake = cms.Sequence(process.goodVertexFilter + process.noScraping + process.triggerResultsFilterFake)

##    __  __                       
##   |  \/  |_   _  ___  _ __  ___ 
##   | |\/| | | | |/ _ \| '_ \/ __|
##   | |  | | |_| | (_) | | | \__ \
##   |_|  |_|\__,_|\___/|_| |_|___/
##                                 
## ==== Merge CaloMuons and Tracks into the collection of reco::Muons  ====
from RecoMuon.MuonIdentification.calomuons_cfi import calomuons;
process.mergedMuons = cms.EDProducer("CaloMuonMerger",
    mergeTracks = cms.bool(True),
    mergeCaloMuons = cms.bool(False), # AOD
    muons     = cms.InputTag("muons"), 
    caloMuons = cms.InputTag("calomuons"),
    tracks    = cms.InputTag("generalTracks"),
    minCaloCompatibility = calomuons.minCaloCompatibility,
    ## Apply some minimal pt cut
    muonsCut     = cms.string("pt > 3 && track.isNonnull"),
    caloMuonsCut = cms.string("pt > 3"),
    tracksCut    = cms.string("pt > 3"),
)

## ==== Trigger matching
process.load("MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff")
## with some customization
process.muonMatchHLTL2.maxDeltaR = 0.3 # Zoltan tuning - it was 0.5
process.muonMatchHLTL3.maxDeltaR = 0.1
from MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff import *
changeRecoMuonInput(process, "mergedMuons")
useL1Stage2Candidates(process)
appendL1MatchingAlgo(process)
#addHLTL1Passthrough(process)
from MuonAnalysis.TagAndProbe.common_variables_cff import *
process.load("MuonAnalysis.TagAndProbe.common_modules_cff")

process.tagMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string("pt > 24 && "+MuonIDFlags.Tight2012.value()+
                     " && !triggerObjectMatchesByCollection('hltIterL3MuonCandidates').empty()"+
                     " && pfIsolationR04().sumChargedHadronPt/pt < 0.2"),
)

if TRIGGER == "DoubleMu":
    process.tagMuons.cut = ("pt > 6 && (isGlobalMuon || isTrackerMuon) && isPFMuon "+
                            " && !triggerObjectMatchesByCollection('hltL3MuonCandidates').empty()"+
                            " && pfIsolationR04().sumChargedHadronPt/pt < 0.2")

process.oneTag  = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tagMuons"), minNumber = cms.uint32(1))

process.probeMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    #Universal cut for probes following control HLT L3 filter
    #Adding muon ID requirement as from analysis, no muon isolation requirement in analysis
    cut = cms.string("track.isNonnull && pt > 6 && numberOfMatchedStations >= 2 && (isGlobalMuon || isTrackerMuon) && isPFMuon"),  
)

process.tpPairs = cms.EDProducer("CandViewShallowCloneCombiner",
    cut = cms.string("70 < mass < 130"),
    decay = cms.string("tagMuons@+ probeMuons@-")
)
process.onePair = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tpPairs"), minNumber = cms.uint32(1))

from MuonAnalysis.TagAndProbe.muon.tag_probe_muon_extraIso_cff import ExtraIsolationVariables

from MuonAnalysis.TagAndProbe.puppiIso_cfi import load_fullPFpuppiIsolation
process.fullPuppIsolationSequence = load_fullPFpuppiIsolation(process)
from MuonAnalysis.TagAndProbe.puppiIso_cff import PuppiIsolationVariables

process.tpTree = cms.EDAnalyzer("TagProbeFitTreeProducer",
    # choice of tag and probe pairs, and arbitration
    tagProbePairs = cms.InputTag("tpPairs"),
    arbitration   = cms.string("None"),
    # probe variables: all useful ones
    variables = cms.PSet(
        pt  = cms.string("pt"),
        eta = cms.string("eta"),
        phi = cms.string("phi"),
        abseta = cms.string("abs(eta)"),
        tkIso  = cms.string("isolationR03.sumPt"),
        relTkIso  = cms.string("isolationR03.sumPt/pt"),
        combRelIsoPF04dBeta = cms.string("(pfIsolationR04().sumChargedHadronPt + max(pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - pfIsolationR04().sumPUPt/2,0.0))/pt"),
    ),
    flags = cms.PSet(
       MuonIDFlags.Medium2016,
       MuonIDFlags.Tight2012,
       HLT_IsoMu20 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu20_v*',1,0).empty()"),
       HLT_IsoMu24 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu24_v*',1,0).empty()"),
       HLT_IsoMu27 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu27_v*',1,0).empty()"),
       HLT_IsoMu30 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu30_v*',1,0).empty()"),
       HLT_TrkMu16NoFiltersNoVtx = cms.string("!triggerObjectMatchesByPath('HLT_TrkMu16NoFiltersNoVtx_v*',1,0).empty()"),
       HLT_TrkMu6NoFiltersNoVtx = cms.string("!triggerObjectMatchesByPath('HLT_TrkMu6NoFiltersNoVtx_v*',1,0).empty()"),
    ),
    tagVariables = cms.PSet(
        pt  = cms.string("pt"),
        eta = cms.string("eta"),
        phi = cms.string("phi"),
        abseta = cms.string("abs(eta)"),
        tkIso  = cms.string("isolationR03.sumPt"),
        relTkIso  = cms.string("isolationR03.sumPt/pt"),
        combRelIsoPF04dBeta = cms.string("(pfIsolationR04().sumChargedHadronPt + max(pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - pfIsolationR04().sumPUPt/2,0.0))/pt"),
    ),
    tagFlags = cms.PSet(
        MuonIDFlags.Medium2016,
        MuonIDFlags.Tight2012,
        HLT_IsoMu20 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu20_v*',1,0).empty()"),
        HLT_IsoMu24 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu24_v*',1,0).empty()"),
        HLT_IsoMu27 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu27_v*',1,0).empty()"),
        HLT_IsoMu30 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu30_v*',1,0).empty()"),
        HLT_TrkMu16NoFiltersNoVtx = cms.string("!triggerObjectMatchesByPath('HLT_TrkMu16NoFiltersNoVtx_v*',1,0).empty()"),
        HLT_TrkMu6NoFiltersNoVtx = cms.string("!triggerObjectMatchesByPath('HLT_TrkMu6NoFiltersNoVtx_v*',1,0).empty()"),
    ),
    pairVariables = cms.PSet(
        probeMultiplicity = cms.InputTag("probeMultiplicity"),
    ),
    pairFlags = cms.PSet(
        BestZ = cms.InputTag("bestPairByZMass"),
    ),
    isMC           = cms.bool(False),
    addRunLumiInfo = cms.bool(True),
)
if TRIGGER == "DoubleMu":
    for K,F in MuonIDFlags.parameters_().iteritems():
        setattr(process.tpTree.tagFlags, K, F)


process.load("MuonAnalysis.TagAndProbe.muon.tag_probe_muon_extraIso_cfi")
process.load("PhysicsTools.PatAlgos.recoLayer0.pfParticleSelectionForIso_cff")

process.miniIsoSeq = cms.Sequence(
    process.pfParticleSelectionForIsoSequence +
    process.muonMiniIsoCharged + 
    process.muonMiniIsoPUCharged + 
    process.muonMiniIsoNeutrals + 
    process.muonMiniIsoPhotons 
)

process.extraProbeVariablesSeq = cms.Sequence(
    process.probeMuonsIsoSequence +
    process.computeCorrectedIso + 
    process.splitTrackTagger +
    process.muonDxyPVdzmin + 
    process.probeMetMt + process.tagMetMt +
    process.miniIsoSeq +
    process.ak4PFCHSL1FastL2L3CorrectorChain * process.AddLeptonJetRelatedVariables +
    process.fullPuppIsolationSequence 
)

process.tnpSimpleSequence = cms.Sequence(
    process.tagMuons +
    process.oneTag     +
    process.probeMuons +
    process.tpPairs    +
    process.onePair    +
    process.nverticesModule +
    process.njets30Module +
    process.extraProbeVariablesSeq +
    process.probeMultiplicities + 
    process.addEventInfo +
    process.l1rate +
    #process.l1hltprescale + 
    process.bestPairByZMass + 
    process.newTunePVals +
    process.muonDxyPVdzminTags +
    process.tpTree
)

process.tagAndProbe = cms.Path( 
    process.fastFilter +
    process.mergedMuons                 *
    process.patMuonsWithTriggerSequence +
    process.tnpSimpleSequence
)

process.TFileService = cms.Service("TFileService", fileName = cms.string("tnpZ_Data.root"))
