import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
#Adapted from HIN-18-003: https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/HIN-pPb816Spring16GS-00108

generator = cms.EDFilter("Pythia8GeneratorFilter",
  maxEventsToPrint = cms.untracked.int32(0),
  pythiaPylistVerbosity = cms.untracked.int32(0),
  filterEfficiency = cms.untracked.double(1),
  pythiaHepMCVerbosity = cms.untracked.bool(False),
  comEnergy = cms.double(13000.0),
  PythiaParameters = cms.PSet(
    pythia8CommonSettingsBlock,
    pythia8CP5SettingsBlock,
    processParameters = cms.vstring(
    'ParticleDecays:limitTau0 = off',
    'ParticleDecays:limitCylinder = on',
    'ParticleDecays:xyMax = 2000',
    'ParticleDecays:zMax = 4000',
    'HardQCD:all = on',
    'PhaseSpace:pTHatMin = 20',
    'PhaseSpace:pTHatMax = 9999',
    '130:mayDecay = on',
    '211:mayDecay = on',
    '321:mayDecay = on'
    ),
    parameterSets = cms.vstring('pythia8CommonSettings',
      'pythia8CP5Settings',
      'processParameters',
    )
  )
)

mugenfilter = cms.EDFilter("MCSmartSingleParticleFilter",
      MinPt = cms.untracked.vdouble(8., 8., 8., 8.),
      MinEta = cms.untracked.vdouble(-2.4, -2.4, -2.4, -2.4),
      MaxEta = cms.untracked.vdouble(2.4, 2.4, 2.4, 2.4),
      ParticleID = cms.untracked.vint32(13, -13, 13, -13),
      Status = cms.untracked.vint32(1, 1, 1, 1),
      MaxDecayRadius = cms.untracked.vdouble(2000., 2000., 2000., 2000.),
      MinDecayZ = cms.untracked.vdouble(-4000., -4000., -4000., -4000.),
      MaxDecayZ = cms.untracked.vdouble(4000., 4000., 4000., 4000.),
)

configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('PYTHIA 8 QCD in pp (pt-hat 20 GeV) at sqrt(s) = 13 TeV')
)

ProductionFilterSequence = cms.Sequence(generator*mugenfilter)
