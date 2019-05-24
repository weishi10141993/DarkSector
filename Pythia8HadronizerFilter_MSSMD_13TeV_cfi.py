## Pythia8 fragment for 13TeV collisions
import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    crossSection = cms.untracked.double(0.0),
    comEnergy = cms.double(13000.0),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'SLHA:allowUserOverride = on',
            'ParticleDecays:tau0Max = 1000.1',
            'LesHouches:setLifetime = 2', #Ignore lifetime setting in LHE
            '3000022:all = ad void 3 0 0 5.0 0.00001 0.0 0.0 50.0' #Set lifetime in Pythia8
            #Could use SLHA:readFrom and SLHA:file to replace the last line, chose not to take the risk in central production
        ),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CP5Settings',
            'processParameters',
        )
    )
)
