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
        '/store/data/Run2015D/Charmonium/AOD/16Dec2015-v1/50000/0013A0EA-94AE-E511-9B84-001E67398683.root',
        '/store/data/Run2015D/Charmonium/AOD/16Dec2015-v1/50000/02A9F67F-A2AE-E511-939A-0CC47A4C8EB6.root',
        '/store/data/Run2015D/Charmonium/AOD/16Dec2015-v1/50000/02D39573-BDAE-E511-AF22-00266CF9AF00.root',
        '/store/data/Run2015D/Charmonium/AOD/16Dec2015-v1/50000/0639B2A3-A7AE-E511-887E-A0000420FE80.root',
        '/store/data/Run2015D/Charmonium/AOD/16Dec2015-v1/50000/06C00544-AAAE-E511-831D-00A0D1EE2BBC.root',
        '/store/data/Run2015D/Charmonium/AOD/16Dec2015-v1/50000/06DCCB30-C7AE-E511-A318-0025905A6092.root',
        '/store/data/Run2015D/Charmonium/AOD/16Dec2015-v1/50000/0ADF8F02-94AE-E511-96F0-549F358EB72E.root',
        '/store/data/Run2015D/Charmonium/AOD/16Dec2015-v1/50000/0C78D007-95AE-E511-87A9-0CC47A4DEDCA.root',
        '/store/data/Run2015D/Charmonium/AOD/16Dec2015-v1/50000/10438105-95AE-E511-ADCD-0090FAA59634.root',
        '/store/data/Run2015D/Charmonium/AOD/16Dec2015-v1/50000/1077A155-AAAE-E511-A1C7-0CC47A4DEF3E.root',
    ]
elif "CMSSW_8_0_" in os.environ['CMSSW_VERSION']:
    process.GlobalTag.globaltag = cms.string('80X_dataRun2_2016SeptRepro_v4')
    process.source.fileNames = [
        '/store/data/Run2016G/Charmonium/AOD/23Sep2016-v1/100000/0006BA63-7097-E611-BBE8-001E67E71412.root',
        '/store/data/Run2016G/Charmonium/AOD/23Sep2016-v1/100000/0018FFBA-5B94-E611-AD99-008CFAFBF52E.root',
        '/store/data/Run2016G/Charmonium/AOD/23Sep2016-v1/100000/003343EB-7496-E611-B5EC-848F69FD2997.root',
        '/store/data/Run2016G/Charmonium/AOD/23Sep2016-v1/100000/0060EAA8-9197-E611-9D75-001E67E59BE3.root',
        '/store/data/Run2016G/Charmonium/AOD/23Sep2016-v1/100000/00E2CD87-9798-E611-8CA4-848F69FD4598.root',
        '/store/data/Run2016G/Charmonium/AOD/23Sep2016-v1/100000/020BB297-5B97-E611-82B5-848F69FD4541.root',
        '/store/data/Run2016G/Charmonium/AOD/23Sep2016-v1/100000/04CA2B1A-0897-E611-A716-0025907FD242.root',
        '/store/data/Run2016G/Charmonium/AOD/23Sep2016-v1/100000/06069075-3C97-E611-92D8-008CFA00018C.root',
        '/store/data/Run2016G/Charmonium/AOD/23Sep2016-v1/100000/061698EB-E096-E611-840C-848F69FD3EC9.root',
        '/store/data/Run2016G/Charmonium/AOD/23Sep2016-v1/100000/062B282E-8097-E611-9710-001E67E6F86E.root',
    ]
    #process.source.fileNames = [ 'file:/tmp/gpetrucc/0006BA63-7097-E611-BBE8-001E67E71412.root' ]
    import FWCore.PythonUtilities.LumiList as LumiList
    json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
    process.source.lumisToProcess = LumiList.LumiList(filename = json).getVLuminosityBlockRange()

#elif "CMSSW_9_" in os.environ['CMSSW_VERSION']:
#    process.GlobalTag.globaltag = cms.string('92X_dataRun2_Prompt_v4')
#    # process.source.fileNames = ['root://cms-xrd-global.cern.ch//store/data/Run2017C/Charmonium/AOD/PromptReco-v1/000/299/368/00000/1C041F03-806D-E711-B796-02163E0136CC.root']
#    #process.source.fileNames = ['file:/u/user/kplee/scratch/ROOTFiles_Test/92X/AOD_Charmonium_Run2017Bv1_Run297050.root']
elif "CMSSW_9_4_" in os.environ['CMSSW_VERSION']:
    process.GlobalTag.globaltag = cms.string('91X_mcRun2_asymptotic_v3')
    process.source.fileNames = [
        '/store/data/Run2017C/Charmonium/AOD/17Nov2017-v1/00000/1A315D13-8CF1-E711-8706-1866DA890700.root'
    ] 
elif "CMSSW_10_2_" in os.environ['CMSSW_VERSION']:
    process.GlobalTag.globaltag = cms.string('102X_dataRun2_Prompt_v11')

    process.source.fileNames = [
        '/store/data/Run2018B/SingleMuon/AOD/PromptReco-v2/000/318/828/00000/B6F906F2-597C-E811-BBAA-FA163E4F3A7C.root',
        '/store/data/Run2018B/SingleMuon/AOD/PromptReco-v2/000/318/828/00000/B6228E42-547C-E811-981A-FA163EBCAB45.root',
        '/store/data/Run2018B/SingleMuon/AOD/PromptReco-v2/000/318/828/00000/ACAA703C-4F7C-E811-A0AD-FA163E3BE999.root'
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
process.HLTMu   = process.triggerResultsFilter.clone(triggerConditions = [ 'HLT_Mu7p5_L2Mu2_Jpsi_v*' ])
process.HLTBoth = process.triggerResultsFilter.clone(triggerConditions = [ 'HLT_Mu7p5_L2Mu2_Jpsi_v*', 'HLT_Mu*_Track*_Jpsi*' ])

process.fastFilter = cms.Sequence(process.goodVertexFilter + process.noScraping)

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
    process.HLTBoth    +
    process.fastFilter +
    process.mergedMuons                 *
    process.patMuonsWithTriggerSequence *
    process.tnpSimpleSequence
)

process.TFileService = cms.Service("TFileService", fileName = cms.string("tnpJPsi_Data.root"))
