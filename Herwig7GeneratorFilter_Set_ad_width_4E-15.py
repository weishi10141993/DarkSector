import FWCore.ParameterSet.Config as cms

#externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
#    args = cms.vstring('/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/TT_hvq/TT_hdamp_NNPDF31_NNLO_inclusive.tgz'),
#    nEvents = cms.untracked.uint32(5000),
#    numberOfParameters = cms.uint32(1),
#    outputFile = cms.string('cmsgrid_final.lhe'),
#    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
#)

generator = cms.EDFilter("Herwig7GeneratorFilter",
    configFiles = cms.vstring(),
    crossSection = cms.untracked.double(-1),
    dataLocation = cms.string('${HERWIGPATH:-6}'),
    eventHandlers = cms.string('/Herwig/EventHandlers'),
    filterEfficiency = cms.untracked.double(1.0),
    generatorModule = cms.string('/Herwig/Generators/EventGenerator'),    
    hw_lhe = cms.vstring(
        '##################################################',
        '# Example generator based on LHC parameters',
        '# usage: Herwig read LHE.in',
        '##################################################',
        'read snippets/PPCollider.in',
        '##################################################',
        '# Technical parameters for this run',
        '##################################################',
        'cd /Herwig/Generators',
        '#set EventGenerator:NumberOfEvents 10000000',
        '#set EventGenerator:RandomNumberGenerator:Seed 31122001',
        '#set EventGenerator:DebugLevel 0',
        '#set EventGenerator:PrintEvent 10',
        '#set EventGenerator:MaxErrors 10000',
        '##################################################',
        '#   Create the Les Houches file handler and reader',
        '##################################################',
        'cd /Herwig/EventHandlers',
        'library LesHouches.so',
        '# create the event handler',
        'create ThePEG::LesHouchesEventHandler LesHouchesHandler',
        '# set the various step handlers',
        'set LesHouchesHandler:PartonExtractor /Herwig/Partons/PPExtractor',
        'set LesHouchesHandler:CascadeHandler /Herwig/Shower/ShowerHandler',
        'set LesHouchesHandler:DecayHandler /Herwig/Decays/DecayHandler',
        'set LesHouchesHandler:HadronizationHandler /Herwig/Hadronization/ClusterHadHandler',
        '# set the weight option (e.g. for MC@NLO)',
        'set LesHouchesHandler:WeightOption VarNegWeight',
        '# set event hander as one to be used',
        'set /Herwig/Generators/EventGenerator:EventHandler /Herwig/EventHandlers/LesHouchesHandler',
        '# Set up an EMPTY CUTS object',
        '# Normally you will have imposed any cuts you want',
        '# when generating the event file and do not want any more',
        '# in particular for POWHEG and MC@NLO you must not apply cuts on the',
        '# the extra jet',
        'create ThePEG::Cuts /Herwig/Cuts/NoCuts',
        '# You may wish to use the same PDF as the events were generated with',
        'create ThePEG::LHAPDF /Herwig/Partons/LHAPDF ThePEGLHAPDF.so',
        'set /Herwig/Partons/LHAPDF:PDFName NNPDF31_nnlo_as_0118',
        'set /Herwig/Partons/LHAPDF:RemnantHandler /Herwig/Partons/HadronRemnants',
        'set /Herwig/Particles/p+:PDF /Herwig/Partons/LHAPDF',
        'set /Herwig/Particles/pbar-:PDF /Herwig/Partons/LHAPDF',
        'set /Herwig/Partons/PPExtractor:FirstPDF  /Herwig/Partons/LHAPDF',
        'set /Herwig/Partons/PPExtractor:SecondPDF /Herwig/Partons/LHAPDF',
        '# We would recommend the shower uses the default PDFs with which it was tuned.',
        '# However it can be argued that the same set as for the sample should be used for',
        '# matched samples, i.e. MC@NLO (and less so POWHEG)',
        '#set /Herwig/Shower/ShowerHandler:PDFA /Herwig/Partons/LHAPDF',
        '#set /Herwig/Shower/ShowerHandler:PDFB /Herwig/Partons/LHAPDF',
        '# You can in principle also change the PDFs for the remnant extraction and',
        '# multiple scattering. As the generator was tuned with the default values',
        '# this is STRONGLY DISCOURAGED without retuning the MPI parameters',
        '# create the reader and set cuts',
        'create ThePEG::LesHouchesFileReader LesHouchesReader',
        'set LesHouchesReader:FileName MSSMD_10_5_0.lhe',
        'set LesHouchesReader:AllowedToReOpen No',
        'set LesHouchesReader:InitPDFs 0',
        'set LesHouchesReader:Cuts /Herwig/Cuts/NoCuts',
        '# option to ensure momentum conservation is O.K. due rounding errors (recommended)',
        'set LesHouchesReader:MomentumTreatment RescaleEnergy',
        '# set the pdfs',
        'set LesHouchesReader:PDFA /Herwig/Partons/LHAPDF',
        'set LesHouchesReader:PDFB /Herwig/Partons/LHAPDF',
        '# if using BSM models with QNUMBER info',
        '#set LesHouchesReader:QNumbers Yes',
        '#set LesHouchesReader:Decayer /Herwig/Decays/Mambo',
        '# and add to handler',
        'insert LesHouchesHandler:LesHouchesReaders 0 LesHouchesReader',
        '##################################################',
        '#  Shower parameters',
        '##################################################',
        '# normally, especially for POWHEG, you want',
        '# the scale supplied in the event files (SCALUP)',
        '# to be used as a pT veto scale in the parton shower',
        'set /Herwig/Shower/ShowerHandler:MaxPtIsMuF Yes',
        'set /Herwig/Shower/ShowerHandler:RestrictPhasespace Yes',
        '# Shower parameters',
        '# treatment of wide angle radiation',
        'set /Herwig/Shower/PartnerFinder:PartnerMethod Random',
        'set /Herwig/Shower/PartnerFinder:ScaleChoice Partner',
        '# fix issue before 7.0.5 (not needed after this)',
        'set /Herwig/Shower/GtoQQbarSplitFn:AngularOrdered Yes',
        'set /Herwig/Shower/GammatoQQbarSplitFn:AngularOrdered Yes',
        '# with MC@NLO these parameters are required for consistency of the subtraction terms',
        '# suggested parameters (give worse physics results with POWHEG)',
        '#set /Herwig/Shower/KinematicsReconstructor:InitialInitialBoostOption LongTransBoost',
        '#set /Herwig/Shower/KinematicsReconstructor:ReconstructionOption General',
        '#set /Herwig/Shower/KinematicsReconstructor:FinalStateReconOption Default',
        '#set /Herwig/Shower/KinematicsReconstructor:InitialStateReconOption Rapidity',
        '#set /Herwig/Shower/ShowerHandler:SpinCorrelations No',
        '##################################################',
        '# LHC physics parameters (override defaults here) ',
        '##################################################',
        '# e.g if different top mass used',
        'set /Herwig/Particles/t:NominalMass 172.5',
        '##################################################',
        '# Save run for later usage with `Herwig run`',
        '##################################################',
        'cd /Herwig/Generators',
        'saverun LHE EventGenerator'
    ),    
    hw_com = cms.vstring(
        'cd /Herwig/Generators', 
        'set EventGenerator:EventHandler:LuminosityFunction:Energy 13000.0', 
        'cd /'
    ),
    hw_nnpdf31 = cms.vstring(
        'cd /Herwig/Partons', 
        'create ThePEG::LHAPDF PDFSet_nnlo ThePEGLHAPDF.so', 
        'set PDFSet_nnlo:PDFName NNPDF31_nnlo_as_0118.LHgrid', 
        'set PDFSet_nnlo:RemnantHandler HadronRemnants', 
        'set /Herwig/Particles/p+:PDF PDFSet_nnlo', 
        'set /Herwig/Particles/pbar-:PDF PDFSet_nnlo', 
	
        'set /Herwig/Partons/PPExtractor:FirstPDF  PDFSet_nnlo', 
        'set /Herwig/Partons/PPExtractor:SecondPDF PDFSet_nnlo', 
	
        'set /Herwig/Shower/ShowerHandler:PDFA PDFSet_nnlo', 
        'set /Herwig/Shower/ShowerHandler:PDFB PDFSet_nnlo', 
	
        'create ThePEG::LHAPDF PDFSet_lo ThePEGLHAPDF.so', 
        'set PDFSet_lo:PDFName NNPDF31_lo_as_0130.LHgrid', 
        'set PDFSet_lo:RemnantHandler HadronRemnants', 
	
        'set /Herwig/Shower/ShowerHandler:PDFARemnant PDFSet_lo', 
        'set /Herwig/Shower/ShowerHandler:PDFBRemnant PDFSet_lo', 
        'set /Herwig/Partons/MPIExtractor:FirstPDF PDFSet_lo', 
        'set /Herwig/Partons/MPIExtractor:SecondPDF PDFSet_lo', 
        'cd /'
    ),    
    hw_alphas = cms.vstring(
        'cd /Herwig/Shower', 
        'set AlphaQCD:AlphaMZ 0.118', 
        'cd /'
    ),
    hw_tuning = cms.vstring(
        'read snippets/SoftTune.in', 
        'set /Herwig/Hadronization/ColourReconnector:ReconnectionProbability 0.4712', 
        'set /Herwig/UnderlyingEvent/MPIHandler:pTmin0 3.04', 
        'set /Herwig/UnderlyingEvent/MPIHandler:InvRadius 1.284', 
        'set /Herwig/UnderlyingEvent/MPIHandler:Power 0.1362',
	    'set /Herwig/Partons/RemnantDecayer:ladderPower -0.08',
        'set /Herwig/Partons/RemnantDecayer:ladderNorm 0.95'
    ),      
    hw_stableParticles = cms.vstring(
        'set /Herwig/Decays/DecayHandler:MaxLifeTime 1000*mm', 
        'set /Herwig/Decays/DecayHandler:LifeTimeOption Average'
    ),     
    hw_np = cms.vstring(
        'cd /Herwig/Particles',
        'create ThePEG::ParticleData n1',
        'setup n1 1000022 n1 10.0 0.00001 0.0 0.0 0 0 2 0',
        'create ThePEG::ParticleData nD',
        'setup nD 3000001 nD 1.0 0.0 0.0 0.0 0 0 2 1',
        'create ThePEG::ParticleData ad',
        'setup ad 3000022 ad 5.0 4e-15 0.0 0.0 0 0 3 0',
        'cd /'
    ), 
    parameterSets = cms.vstring(
        'hw_np',
        'hw_lhe',	
        'hw_com',
        'hw_nnpdf31', 
        'hw_alphas', 
        'hw_tuning', 
        'hw_stableParticles'
    ),
    repository = cms.string('${HERWIGPATH}/HerwigDefaults.rpo'),
    run = cms.string('InterfaceMatchboxTest'),
    runModeList = cms.untracked.string('read,run'),
)