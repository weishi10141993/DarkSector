import FWCore.ParameterSet.Config as cms

process = cms.Process("TEST")

process.load("FWCore.Framework.test.cmsExceptionsFatal_cff")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.source = cms.Source("EmptySource")

process.generator = cms.EDFilter("Pythia8EGun",

    maxEventsToPrint = cms.untracked.int32(10),
    pythiaPylistVerbosity = cms.untracked.int32(2),
    pythiaHepMCVerbosity = cms.untracked.bool(True),
#    useEvtGenPlugin = cms.PSet(),
    #evtgenDecFile = cms.string("mydecfile"),
    #evtgenPdlFile = cms.string("mypdlfile"),
#    evtgenUserFile = cms.vstring('GeneratorInterface/Pythia8Interface/test/evtgen_userfile.dec'),
    PGunParameters = cms.PSet(
#       ParticleID = cms.vint32(521),
       ParticleID = cms.vint32(3000022),
       AddAntiParticle = cms.bool(False),
       MinPhi = cms.double(-3.14159265359),
       MaxPhi = cms.double(3.14159265359),
       MinE = cms.double(100.0),
       MaxE = cms.double(200.0),
       MinEta = cms.double(0.0),
       MaxEta = cms.double(2.4)
    ),
#    SLHAFileForPythia8 = cms.string('GeneratorInterface/Pythia8Interface/test/MSSMD_10_5_50.lhe'),
    PythiaParameters = cms.PSet(
        py8Settings = cms.vstring(
          'ParticleDecays:tau0Max = 1000.1',
          'Next:showScaleAndVertex = on',
          '3000022:all = ad void 0 0 0 5.00 0.0001 4.9 5.1 50.0 1 1 0 0 1',
          '3000022:oneChannel = on 1.0 100 13 -13'),
        parameterSets = cms.vstring('py8Settings')
    )
        
)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger = cms.Service("MessageLogger",
    cout = cms.untracked.PSet(
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(2)
        )
    ),
    destinations = cms.untracked.vstring('cout')
)

process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    generator = cms.PSet(
        initialSeed = cms.untracked.uint32(123456789),
        engineName = cms.untracked.string('HepJamesRandom')
    )
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

process.GEN = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('Py8EGun_EvtGen.root')
)


process.p = cms.Path(process.generator)
process.outpath = cms.EndPath(process.GEN)

process.schedule = cms.Schedule(process.p, process.outpath)
