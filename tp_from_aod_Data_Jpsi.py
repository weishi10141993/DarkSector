import FWCore.ParameterSet.Config as cms
##new
process = cms.Process("TagProbe")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.source = cms.Source("PoolSource", 
    fileNames = cms.untracked.vstring(),
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )      

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load("Configuration.StandardSequences.Reconstruction_cff")

# process.Tracer = cms.Service('Tracer')
import os
if "CMSSW_7_6_" in os.environ['CMSSW_VERSION']:
    process.GlobalTag.globaltag = cms.string('76X_dataRun2_v15')
    process.source.fileNames = [
        '/store/data/Run2015D/Charmonium/AOD/16Dec2015-v1/50000/0013A0EA-94AE-E511-9B84-001E67398683.root'
    ]
elif "CMSSW_8_0_" in os.environ['CMSSW_VERSION']:
    process.GlobalTag.globaltag = cms.string('80X_dataRun2_2016SeptRepro_v4')
    process.source.fileNames = [
        '/store/data/Run2016G/Charmonium/AOD/23Sep2016-v1/100000/0006BA63-7097-E611-BBE8-001E67E71412.root'
    ]
elif "CMSSW_9_4_" in os.environ['CMSSW_VERSION']:
    process.GlobalTag.globaltag = cms.string('91X_mcRun2_asymptotic_v3')
    process.source.fileNames = [
        '/store/data/Run2017C/Charmonium/AOD/17Nov2017-v1/00000/1A315D13-8CF1-E711-8706-1866DA890700.root'
    ] 
elif "CMSSW_10_2_" in os.environ['CMSSW_VERSION']:
    process.GlobalTag.globaltag = cms.string('102X_dataRun2_Prompt_v11')

    process.source.fileNames = [
        '/store/data/Run2018C/Charmonium/AOD/PromptReco-v1/000/319/347/00000/02675E66-E084-E811-AECA-FA163E092C74.root'
    ]
    #Only use runs after control triggers are implemented, i.e. after run 317509
else: raise RuntimeError, "Unknown CMSSW version %s" % os.environ['CMSSW_VERSION']

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
process.triggerResultsFilter.triggerConditions = cms.vstring( 'HLT_Mu7p5_L2Mu2_Jpsi_v*' ) 
process.triggerResultsFilter.l1tResults = "gtStage2Digis"
process.triggerResultsFilter.throw = False
process.triggerResultsFilter.hltResults = cms.InputTag( "TriggerResults", "", "HLT" )

process.fastFilter = cms.Sequence(process.goodVertexFilter + process.noScraping + process.triggerResultsFilter)

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
    muonsCut     = cms.string("pt > 2 && track.isNonnull"),
    caloMuonsCut = cms.string("pt > 2"),
    tracksCut    = cms.string("pt > 2"),
)

## ==== Trigger matching
process.load("MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff")
## with some customization
from MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff import *
changeRecoMuonInput(process, "mergedMuons")
useL1Stage2Candidates(process)
appendL1MatchingAlgo(process)
#addHLTL1Passthrough(process)


from MuonAnalysis.TagAndProbe.common_variables_cff import *
process.load("MuonAnalysis.TagAndProbe.common_modules_cff")

process.tagMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string("(isGlobalMuon || numberOfMatchedStations > 1) && pt > 5 && !triggerObjectMatchesByCollection('hltIterL3MuonCandidates').empty()"),
)

process.oneTag  = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tagMuons"), minNumber = cms.uint32(1))

process.probeMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string("track.isNonnull && (!triggerObjectMatchesByCollection('hltTracksIter').empty() || !triggerObjectMatchesByCollection('hltMuTrackJpsiEffCtfTrackCands').empty() || !triggerObjectMatchesByCollection('hltMuTrackJpsiCtfTrackCands').empty() || !triggerObjectMatchesByCollection('hltL2MuonCandidates').empty())"),
)

process.tpPairs = cms.EDProducer("CandViewShallowCloneCombiner",
    cut = cms.string('2.8 < mass < 3.4 && abs(daughter(0).vz - daughter(1).vz) < 1'),
    decay = cms.string('tagMuons@+ probeMuons@-')
)
process.onePair = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tpPairs"), minNumber = cms.uint32(1))

from MuonAnalysis.TagAndProbe.muon.tag_probe_muon_extraIso_cff import ExtraIsolationVariables

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
       Medium2016  = cms.string("isPFMuon && innerTrack.validFraction >= 0.49 && ( isGlobalMuon && globalTrack.normalizedChi2 < 3 && combinedQuality.chi2LocalPosition < 12 && combinedQuality.trkKink < 20 && segmentCompatibility >= 0.303 || segmentCompatibility >= 0.451 )"),
       Tight2012   = cms.string("isPFMuon && numberOfMatchedStations > 1 && muonID('GlobalMuonPromptTight') && abs(dB) < 0.2 && "+
                        "track.hitPattern.trackerLayersWithMeasurement > 5 && track.hitPattern.numberOfValidPixelHits > 0"),
       IsoMu20 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu20_v*',1,0).empty()"),
       IsoMu24 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu24_v*',1,0).empty()"),
       IsoMu27 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu27_v*',1,0).empty()"),
       IsoMu30 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu30_v*',1,0).empty()"),
       Control16ByPathLastFilter = cms.string("!triggerObjectMatchesByPath('HLT_TrkMu16NoFiltersNoVtx_v*',1,0).empty()"),
       Control16ByPathL3Filter = cms.string("!triggerObjectMatchesByPath('HLT_TrkMu16NoFiltersNoVtx_v*',0,1).empty()"),
       Control16ByFilterL3 = cms.string("!triggerObjectMatchesByFilter('hltL3fL1sSingleMu7L1f0L2f10OneMuL3Filtered16NoVtx').empty()"),
       Control16ByFilterL1 = cms.string("!triggerObjectMatchesByFilter('hltL1fL1sSingleMu7L1Filtered0').empty()"),
       #Test the known trigger Mu50 efficiency
       Mu50ByPathLastFilter = cms.string("!triggerObjectMatchesByPath('HLT_Mu50_v*',1,0).empty()"),
       Mu50ByPathL3Filter = cms.string("!triggerObjectMatchesByPath('HLT_Mu50_v*',0,1).empty()"),
       Mu50ByFilterL3 = cms.string("!triggerObjectMatchesByFilter('hltL3fL1sMu22Or25L1f0L2f10QL3Filtered50Q').empty()"),
       Mu50ByFilterL1 = cms.string("!triggerObjectMatchesByFilter('hltL1fL1sMu22or25L1Filtered0').empty()"),
       Control6ByPathLastFilter = cms.string("!triggerObjectMatchesByPath('HLT_TrkMu6NoFiltersNoVtx_v*',1,0).empty()"),
       Control6ByPathL3Filter = cms.string("!triggerObjectMatchesByPath('HLT_TrkMu6NoFiltersNoVtx_v*',0,1).empty()"),
       Control6ByFilterL3 = cms.string("!triggerObjectMatchesByFilter('hltL3fL1sSingleMu3L1f0L2f10OneMuL3Filtered6NoVtx').empty()"),
       Control6ByFilterL1 = cms.string("!triggerObjectMatchesByFilter('hltL1fL1sSingleMu3L1Filtered0').empty()"),
       #Jpsi tagging
       Mu7p5_L2Mu2_Jpsi = cms.string("!triggerObjectMatchesByPath('HLT_Mu7p5_L2Mu2_Jpsi_v*',1,0).empty()"),
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
    tagFlags     = cms.PSet(
        Medium2016  = cms.string("isPFMuon && innerTrack.validFraction >= 0.49 && ( isGlobalMuon && globalTrack.normalizedChi2 < 3 && combinedQuality.chi2LocalPosition < 12 && combinedQuality.trkKink < 20 && segmentCompatibility >= 0.303 || segmentCompatibility >= 0.451 )"),
        Tight2012   = cms.string("isPFMuon && numberOfMatchedStations > 1 && muonID('GlobalMuonPromptTight') && abs(dB) < 0.2 && "+
                        "track.hitPattern.trackerLayersWithMeasurement > 5 && track.hitPattern.numberOfValidPixelHits > 0"),
        IsoMu20 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu20_v*',1,0).empty()"),
        IsoMu24 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu24_v*',1,0).empty()"),
        IsoMu27 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu27_v*',1,0).empty()"),
        IsoMu30 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu30_v*',1,0).empty()"),
        Control16ByPathLastFilter = cms.string("!triggerObjectMatchesByPath('HLT_TrkMu16NoFiltersNoVtx_v*',1,0).empty()"),
        Control16ByPathL3Filter = cms.string("!triggerObjectMatchesByPath('HLT_TrkMu16NoFiltersNoVtx_v*',0,1).empty()"),
        Control16ByFilterL3 = cms.string("!triggerObjectMatchesByFilter('hltL3fL1sSingleMu7L1f0L2f10OneMuL3Filtered16NoVtx').empty()"),  
        Control16ByFilterL1 = cms.string("!triggerObjectMatchesByFilter('hltL1fL1sSingleMu7L1Filtered0').empty()"),
        #Test the known trigger Mu50 efficiency
        Mu50ByPathLastFilter = cms.string("!triggerObjectMatchesByPath('HLT_Mu50_v*',1,0).empty()"),
        Mu50ByPathL3Filter = cms.string("!triggerObjectMatchesByPath('HLT_Mu50_v*',0,1).empty()"),
        Mu50ByFilterL3 = cms.string("!triggerObjectMatchesByFilter('hltL3fL1sMu22Or25L1f0L2f10QL3Filtered50Q').empty()"),
        Mu50ByFilterL1 = cms.string("!triggerObjectMatchesByFilter('hltL1fL1sMu22or25L1Filtered0').empty()"),
        Control6ByPathLastFilter = cms.string("!triggerObjectMatchesByPath('HLT_TrkMu6NoFiltersNoVtx_v*',1,0).empty()"),
        Control6ByPathL3Filter = cms.string("!triggerObjectMatchesByPath('HLT_TrkMu6NoFiltersNoVtx_v*',0,1).empty()"),
        Control6ByFilterL3 = cms.string("!triggerObjectMatchesByFilter('hltL3fL1sSingleMu3L1f0L2f10OneMuL3Filtered6NoVtx').empty()"),
        Control6ByFilterL1 = cms.string("!triggerObjectMatchesByFilter('hltL1fL1sSingleMu3L1Filtered0').empty()"),
        #Jspi tagging
        Mu7p5_L2Mu2_Jpsi = cms.string("!triggerObjectMatchesByPath('HLT_Mu7p5_L2Mu2_Jpsi_v*',1,0).empty()"),
    ),
    pairVariables = cms.PSet(
        dz  = cms.string("daughter(0).vz - daughter(1).vz"),
        probeMultiplicity = cms.InputTag("probeMultiplicity"),
    ),
    pairFlags = cms.PSet(),
    isMC           = cms.bool(False),
    addRunLumiInfo = cms.bool(True),
)


process.load("MuonAnalysis.TagAndProbe.muon.tag_probe_muon_extraIso_cfi")

process.tnpSimpleSequence = cms.Sequence(
    process.tagMuons +
    process.oneTag     +
    process.probeMuons +
    process.tpPairs    +
    process.onePair    +
    process.muonDxyPVdzmin +
    process.nverticesModule +
    process.tagProbeSeparation +
    process.computeCorrectedIso + 
    process.probeMultiplicity + 
    process.splitTrackTagger +
    process.addEventInfo +
    process.l1rate +
    process.tpTree
)

process.tagAndProbe = cms.Path( 
    process.fastFilter +
    process.mergedMuons                 *
    process.patMuonsWithTriggerSequence *
    process.tnpSimpleSequence
)

process.TFileService = cms.Service("TFileService", fileName = cms.string("tnpJPsi_Data.root"))
