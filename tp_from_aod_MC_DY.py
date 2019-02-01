import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbe")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 10

process.source = cms.Source("PoolSource", 
    fileNames = cms.untracked.vstring(),
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100))

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load("Configuration.StandardSequences.Reconstruction_cff")

import os
if "CMSSW_8_0_" in os.environ['CMSSW_VERSION']:
    process.GlobalTag.globaltag = cms.string('80X_mcRun2_asymptotic_v14')
    process.source.fileNames = [
        '/store/mc/RunIISpring16reHLT80/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/40001/3459A4AB-D85C-E611-81F5-02163E011488.root',
        '/store/mc/RunIISpring16reHLT80/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/40001/8AB9296A-C55C-E611-9291-02163E012E69.root',
        '/store/mc/RunIISpring16reHLT80/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/40001/9A8A076A-C55C-E611-BE5A-02163E012E69.root',
        '/store/mc/RunIISpring16reHLT80/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/40002/4AC3D851-C45C-E611-8BFD-02163E012E69.root',
        '/store/mc/RunIISpring16reHLT80/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/40003/ACAA69A9-D85C-E611-983F-02163E011488.root',
    ]
elif "CMSSW_9_2_" in os.environ['CMSSW_VERSION']:
    process.GlobalTag.globaltag = cms.string('91X_mcRun2_asymptotic_v3')
    process.source.fileNames = [
        '/store/relval/CMSSW_9_2_0/RelValZMM_13/GEN-SIM-RECO/PU25ns_91X_mcRun2_asymptotic_v3-v1/10000/0471AF1A-F53C-E711-A012-0CC47A7C345E.root'
    ] 
elif "CMSSW_9_4_" in os.environ['CMSSW_VERSION']:
    process.GlobalTag.globaltag = cms.string('94X_mc2017_realistic_v17')
    process.source.fileNames = [
        '/store/mc/RunIIFall17DRPremix/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/AODSIM/RECOSIMstep_94X_mc2017_realistic_v10-v1/00000/0019074F-6EF2-E711-B6CD-008CFAC94118.root'
    ] 
elif "CMSSW_10_2_" in os.environ['CMSSW_VERSION']:
    process.GlobalTag.globaltag = cms.string('102X_upgrade2018_realistic_v15')
    process.source.fileNames = [
        '/store/mc/RunIIAutumn18DRPremix/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/AODSIM/102X_upgrade2018_realistic_v15-v1/80002/FF4FB1B8-3C5A-044E-86AD-F93B009222BB.root'
    ]
else: raise RuntimeError, "Unknown CMSSW version %s" % os.environ['CMSSW_VERSION']

## SELECT WHAT DATASET YOU'RE RUNNING ON
TRIGGER="SingleMu"
#TRIGGER="Any"

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
process.fastFilter = cms.Sequence(process.goodVertexFilter + process.noScraping)

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
changeTriggerProcessName(process, "HLT")


from MuonAnalysis.TagAndProbe.common_variables_cff import *
process.load("MuonAnalysis.TagAndProbe.common_modules_cff")

process.tagMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string("pt > 8 && "+MuonIDFlags.Tight2012.value()+
                     " && pfIsolationR04().sumChargedHadronPt/pt < 0.2"),
)
if TRIGGER != "SingleMu":
    process.tagMuons.cut = ("pt > 6 && (isGlobalMuon || isTrackerMuon) && isPFMuon "+
                            " && pfIsolationR04().sumChargedHadronPt/pt < 0.2")

process.oneTag  = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tagMuons"), minNumber = cms.uint32(1))

process.probeMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string("track.isNonnull && pt > 3"),  # no real cut now
)

process.tpPairs = cms.EDProducer("CandViewShallowCloneCombiner",
    cut = cms.string("70 < mass <130"),
    decay = cms.string("tagMuons@+ probeMuons@-")
)
process.onePair = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tpPairs"), minNumber = cms.uint32(1))

process.tagMuonsMCMatch = cms.EDProducer("MCMatcher", # cut on deltaR, deltaPt/Pt; pick best by deltaR
    src     = cms.InputTag("tagMuons"), # RECO objects to match
    matched = cms.InputTag("goodGenMuons"),   # mc-truth particle collection
    mcPdgId     = cms.vint32(13),  # one or more PDG ID (13 = muon); absolute values (see below)
    checkCharge = cms.bool(False), # True = require RECO and MC objects to have the same charge
    mcStatus = cms.vint32(1),      # PYTHIA status code (1 = stable, 2 = shower, 3 = hard scattering)
    maxDeltaR = cms.double(0.3),   # Minimum deltaR for the match
    maxDPtRel = cms.double(0.5),   # Minimum deltaPt/Pt for the match
    resolveAmbiguities = cms.bool(True),    # Forbid two RECO objects to match to the same GEN object
    resolveByMatchQuality = cms.bool(True), # False = just match input in order; True = pick lowest deltaR pair first
)
process.probeMuonsMCMatch = process.tagMuonsMCMatch.clone(src = "probeMuons", maxDeltaR = 0.3, maxDPtRel = 1.0, resolveAmbiguities = False,  resolveByMatchQuality = False)

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
        dxyBS = cms.InputTag("muonDxyPVdzmin","dxyBS"),
        dxyPVdzmin = cms.InputTag("muonDxyPVdzmin","dxyPVdzmin"),
        dzPV = cms.InputTag("muonDxyPVdzmin","dzPV"),
    ),
    flags = cms.PSet(
       Medium2016  = cms.string("isPFMuon && innerTrack.validFraction >= 0.49 && ( isGlobalMuon && globalTrack.normalizedChi2 < 3 && combinedQuality.chi2LocalPosition < 12 && combinedQuality.trkKink < 20 && segmentCompatibility >= 0.303 || segmentCompatibility >= 0.451 )"),
       Tight2012   = cms.string("isPFMuon && numberOfMatchedStations > 1 && muonID('GlobalMuonPromptTight') && abs(dB) < 0.2 && "+
                        "track.hitPattern.trackerLayersWithMeasurement > 5 && track.hitPattern.numberOfValidPixelHits > 0"),
       IsoMu20 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu20_v*',1,0).empty()"),
       IsoMu24 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu24_v*',1,0).empty()"),
       IsoMu27 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu27_v*',1,0).empty()"),
       IsoMu30 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu30_v*',1,0).empty()"),
       Mu8 = cms.string("!triggerObjectMatchesByPath('HLT_Mu8_v*',1,0).empty()"),
       Mu12 = cms.string("!triggerObjectMatchesByPath('HLT_Mu12_v*',1,0).empty()"),
       Mu15 = cms.string("!triggerObjectMatchesByPath('HLT_Mu15_v*',1,0).empty()"),
       Mu17 = cms.string("!triggerObjectMatchesByPath('HLT_Mu17_v*',1,0).empty()"),
       Mu19 = cms.string("!triggerObjectMatchesByPath('HLT_Mu19_v*',1,0).empty()"),
       Mu20 = cms.string("!triggerObjectMatchesByPath('HLT_Mu20_v*',1,0).empty()"),
       Mu27 = cms.string("!triggerObjectMatchesByPath('HLT_Mu27_v*',1,0).empty()"),
       Mu55 = cms.string("!triggerObjectMatchesByPath('HLT_Mu55_v*',1,0).empty()"),
       OldMu100 = cms.string("!triggerObjectMatchesByPath('HLT_OldMu100_v*',1,0).empty()"),
       TkMu100 = cms.string("!triggerObjectMatchesByPath('HLT_TkMu100_v*',1,0).empty()"),
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
        dxyBS = cms.InputTag("muonDxyPVdzminTags","dxyBS"),
        dxyPVdzmin = cms.InputTag("muonDxyPVdzminTags","dxyPVdzmin"),
        dzPV = cms.InputTag("muonDxyPVdzminTags","dzPV"),
    ),
    tagFlags = cms.PSet(
        Medium2016  = cms.string("isPFMuon && innerTrack.validFraction >= 0.49 && ( isGlobalMuon && globalTrack.normalizedChi2 < 3 && combinedQuality.chi2LocalPosition < 12 && combinedQuality.trkKink < 20 && segmentCompatibility >= 0.303 || segmentCompatibility >= 0.451 )"),
        Tight2012   = cms.string("isPFMuon && numberOfMatchedStations > 1 && muonID('GlobalMuonPromptTight') && abs(dB) < 0.2 && "+
                        "track.hitPattern.trackerLayersWithMeasurement > 5 && track.hitPattern.numberOfValidPixelHits > 0"),
        IsoMu20 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu20_v*',1,0).empty()"),
        IsoMu24 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu24_v*',1,0).empty()"),
        IsoMu27 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu27_v*',1,0).empty()"),
        IsoMu30 = cms.string("!triggerObjectMatchesByPath('HLT_IsoMu30_v*',1,0).empty()"),
        Mu8 = cms.string("!triggerObjectMatchesByPath('HLT_Mu8_v*',1,0).empty()"),
        Mu12 = cms.string("!triggerObjectMatchesByPath('HLT_Mu12_v*',1,0).empty()"),
        Mu15 = cms.string("!triggerObjectMatchesByPath('HLT_Mu15_v*',1,0).empty()"),
        Mu17 = cms.string("!triggerObjectMatchesByPath('HLT_Mu17_v*',1,0).empty()"),
        Mu19 = cms.string("!triggerObjectMatchesByPath('HLT_Mu19_v*',1,0).empty()"),
        Mu20 = cms.string("!triggerObjectMatchesByPath('HLT_Mu20_v*',1,0).empty()"),
        Mu27 = cms.string("!triggerObjectMatchesByPath('HLT_Mu27_v*',1,0).empty()"),
        Mu55 = cms.string("!triggerObjectMatchesByPath('HLT_Mu55_v*',1,0).empty()"),
        OldMu100 = cms.string("!triggerObjectMatchesByPath('HLT_OldMu100_v*',1,0).empty()"),
        TkMu100 = cms.string("!triggerObjectMatchesByPath('HLT_TkMu100_v*',1,0).empty()"),
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
        probeMultiplicity = cms.InputTag("probeMultiplicity"),
        ## Gen related variables
        genWeight    = cms.InputTag("genAdditionalInfo", "genWeight"),
        truePileUp   = cms.InputTag("genAdditionalInfo", "truePileUp"),
        actualPileUp = cms.InputTag("genAdditionalInfo", "actualPileUp"),
    ),
    pairFlags = cms.PSet(
        BestZ = cms.InputTag("bestPairByZMass"),
    ),
    isMC           = cms.bool(True),
    addRunLumiInfo = cms.bool(True),
    tagMatches       = cms.InputTag("tagMuonsMCMatch"),
    probeMatches     = cms.InputTag("probeMuonsMCMatch"),
    motherPdgId      = cms.vint32(22, 23),
    makeMCUnbiasTree       = cms.bool(False), 
    checkMotherInUnbiasEff = cms.bool(True),
    allProbes              = cms.InputTag("probeMuons"),
)
if TRIGGER != "SingleMu":
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
    process.goodGenMuons +
    process.tagMuons   * process.tagMuonsMCMatch   +
    process.oneTag     +
    process.probeMuons * process.probeMuonsMCMatch +
    process.tpPairs    +
    process.onePair    +
    process.nverticesModule +
    process.njets30Module +
    process.extraProbeVariablesSeq +
    process.probeMultiplicities + 
    process.bestPairByZMass + 
    process.newTunePVals +
    process.genAdditionalInfo +
    process.muonDxyPVdzminTags +
    process.tpTree
)

process.tagAndProbe = cms.Path( 
    process.fastFilter +
    process.mergedMuons                 *
    process.patMuonsWithTriggerSequence +
    process.tnpSimpleSequence
)

process.TFileService = cms.Service("TFileService", fileName = cms.string("tnpZ_MC.root"))
