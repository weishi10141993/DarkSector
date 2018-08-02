import FWCore.ParameterSet.Config as cms
import sys, os, shutil
from optparse import OptionParser

#_*_*_*_*_*_
#Read Inputs
#_*_*_*_*_*_

def FillNumDen(num, den):
    '''Declares the needed selections for a givent numerator, denominator'''

    #Define the mass distribution
    if den == "highptid" or den == "trkhighptid":
        if 'mass_up' in sample:
            process.TnP_Trigger.Variables.pair_newTuneP_mass = cms.vstring("Tag-muon Mass", _mrange, "140", "GeV/c^{2}")
            print 'SISTEMATIC STUDIES: mass_up = 140 GeV'
        elif 'mass_down' in sample:
            process.TnP_Trigger.Variables.pair_newTuneP_mass = cms.vstring("Tag-muon Mass", _mrange, "120", "GeV/c^{2}")
            print 'SISTEMATIC STUDIES: mass_down = 120 GeV'
        else:
            process.TnP_Trigger.Variables.pair_newTuneP_mass = cms.vstring("Tag-muon Mass", _mrange, "130", "GeV/c^{2}")
    else:
        if 'mass_up' in sample:
            process.TnP_Trigger.Variables.mass = cms.vstring("Tag-muon Mass", _mrange, "140", "GeV/c^{2}")
        elif 'mass_down' in sample:
            process.TnP_Trigger.Variables.mass = cms.vstring("Tag-muon Mass", _mrange, "120", "GeV/c^{2}")
        else:
            process.TnP_Trigger.Variables.mass = cms.vstring("Tag-muon Mass", _mrange, "130", "GeV/c^{2}")
        #New selector:


    if num == "TrkMu16NoVtx":
        process.TnP_Trigger.Variables.pt  = cms.vstring("probe pt", "0", "1000", "")
        process.TnP_Trigger.Categories.HLT_TrkMu16NoFiltersNoVtx  = cms.vstring("PassTrkMu16NoVtx", "dummy[pass=1,fail=0]")
        process.TnP_Trigger.Expressions.PassHLTCutHighPt = cms.vstring("PassHLTCutPt", "pt > 16 && HLT_TrkMu16NoFiltersNoVtx == 1", "pt","HLT_TrkMu16NoFiltersNoVtx")
        process.TnP_Trigger.Cuts.HLTTrkMu16  = cms.vstring("HLTTrkMu16", "PassHLTCutHighPt", "0.5")
    elif num == "TrkMu6NoVtx":
        process.TnP_Trigger.Variables.pt  = cms.vstring("probe pt", "0", "1000", "")
        process.TnP_Trigger.Categories.HLT_TrkMu6NoFiltersNoVtx  = cms.vstring("PassTrkMu6NoVtx", "dummy[pass=1,fail=0]")
        process.TnP_Trigger.Expressions.PassHLTCutLowPt = cms.vstring("PassHLTCutPt", "pt > 6 && HLT_TrkMu6NoFiltersNoVtx == 1", "pt","HLT_TrkMu16NoFiltersNoVtx")
        process.TnP_Trigger.Cuts.HLTTrkMu6  = cms.vstring("HLTTrkMu6", "PassHLTCutLowPt", "0.5")


    if den == "pT16":
        process.TnP_Trigger.Variables.pt  = cms.vstring("probe pt", "0", "1000", "")
        process.TnP_Trigger.Expressions.PassHighPtCut = cms.vstring("PassHighPtCut", "pt > 16", "pt")
        process.TnP_Trigger.Cuts.Pt16Cut  = cms.vstring("Pt16Cut", "PassHighPtCut", "0.5")
    elif den == "pT6":
        process.TnP_Trigger.Variables.pt  = cms.vstring("probe pt", "0", "1000", "")
        process.TnP_Trigger.Expressions.PassLowPtCut = cms.vstring("PassLowPtCut", "pt > 6", "pt")
        process.TnP_Trigger.Cuts.Pt6Cut  = cms.vstring("Pt6Cut", "PassLowPtCut", "0.5")

                                    
def FillVariables(par):
    '''Declares only the parameters which are necessary, no more'''

    if par == 'eta':
        process.TnP_Trigger.Variables.eta  = cms.vstring("muon #eta", "-2.5", "2.5", "")
    if par == 'phi':
        process.TnP_Trigger.Variables.phi  = cms.vstring("muon #phi", "-3.2", "3.2", "")   
    if par == 'pt' or 'pt_eta':
        process.TnP_Trigger.Variables.pt  = cms.vstring("muon p_{T}", "0", "1000", "GeV/c")
    if par == 'pt_eta' or 'newpt_eta':
        process.TnP_Trigger.Variables.abseta  = cms.vstring("muon |#eta|", "0", "2.5", "")
    if par == 'tag_instLumi':
        process.TnP_Trigger.Variables.tag_instLumi  = cms.vstring("Inst. Lumi [10E30]", "0", "15", "")
    if par == 'pair_deltaR':
        process.TnP_Trigger.Variables.pair_deltaR  = cms.vstring("deltaR", "0", "4", "")
    if par == 'vtx':
        print 'I filled it'
        process.TnP_Trigger.Variables.tag_nVertices   = cms.vstring("Number of vertices", "0", "999", "")

def FillBin(par):
    '''Sets the values of the bin paramters and the bool selections on the denominators'''
    #Parameter 
    if par == 'newpt_eta':
        DEN.pair_newTuneP_probe_pt = cms.vdouble(10, 15, 20, 25, 30, 40, 50, 60, 120) 
        DEN.abseta = cms.vdouble( 0., 0.9, 1.2, 2.1, 2.4)
    elif par == 'newpt':
        DEN.pair_newTuneP_probe_pt = cms.vdouble(10, 20, 25, 30, 40, 50, 60, 120, 200)
    elif par == 'eta':
        DEN.eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4)
    elif par == 'phi':
        DEN.phi = cms.vdouble(-3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0)
    elif par == 'pt':
        DEN.pt = cms.vdouble(10, 20, 25, 30, 40, 50, 60, 120, 200)
    elif par == 'pair_deltaR':
        DEN.pair_deltaR = cms.vdouble(0., 0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 5.0)
    elif par == 'tag_instLumi':
        DEN.tag_instLumi = cms.vdouble(1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3200, 3400, 3600, 3800, 4000, 4200, 4400, 4600, 4800, 5000, 5200, 5400, 5600, 5800, 6000, 6200, 6400, 6600, 6800, 7000, 7200, 7400, 7600, 7800, 8000, 8200, 8400, 8600, 8800, 9000, 9200, 9400, 9600, 9800, 10000, 10200, 10400, 10600, 10800, 11000) # for runs BCD 
    elif par == 'pt_eta':
        DEN.pt = cms.vdouble(10, 20, 25, 30, 40, 50, 60, 120)
        DEN.abseta = cms.vdouble( 0., 0.9, 1.2, 2.1, 2.4)
    elif par == 'vtx':
        print 'I filled it also asdf'
        DEN.tag_nVertices = cms.vdouble(6.5,10.5,14.5,18.5,22.5,26.5,30.5,34.5,50.5)
 
    #Selections
    if den == "pT16": DEN.Pt16Cut = cms.vstring("pass")
    elif den == "pT6": DEN.Pt6Cut = cms.vstring("pass")


args = sys.argv[1:]
iteration = ''
if len(args) > 1: iteration = args[1]
print "The iteration is", iteration
num = 'tight'
if len(args) > 2: num = args[2]
print 'The num is', num 
den = 'tight'
if len(args) > 3: den = args[3]
print 'The den is', den 
scenario = "data_all"
if len(args) > 4: scenario = args[4]
print "Will run scenario ", scenario
sample = 'data'
if len(args) > 5: sample = args[5]
print 'The sample is', sample
if len(args) > 6: par = args[6]
print 'The binning is', par 
bgFitFunction = 'default'
if len(args) > 7: bgFitFunction = args[7]
if bgFitFunction == 'CMSshape':
    print 'Will use the CMS shape to fit the background'
elif bgFitFunction == 'custom':
    print 'Will experiment with custom fit functions'
else:
    print 'Will use the standard fit functions for the backgroud'


process = cms.Process("TagProbe")
process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

if not num  in ['looseid', 'mediumid', 'mediumidprompt', 'tightid', 'tightidhww', 'puppiIso', 'puppiIsoNoLep', 'combpuppiIso','muCleanerIII', 'muCleanerIV', 'highptid', 'trkhighptid', 'softid', 'softmvaid', 'mvaloose', 'mvamedium', 'mvatight', 'looseiso', 'tightiso', 'tklooseiso', 'tktightiso', 'mediumiso', 'miniisotight', 'trackermuons']:
    print '@ERROR: num should be in ',['looseid', 'mediumid', 'tightid', 'tightidhww', 'puppiIso', 'puppiIsoNoLep', 'combpuppiIso', 'muCleanerIII', 'muCleanerIV', 'highptid', 'looseiso', 'tightiso', 'tklooseiso', 'mediumiso'], 'You used', num, '.Abort'
    sys.exit()
if not den in ['looseid', 'mediumid', 'tightid', 'tightidhww', 'highptid', 'gentrack', 'trkhighptid', 'trackermuons']:
    print '@ERROR: den should be',['looseid', 'mediumid', 'tightid', 'tightidhww', 'highptid'], 'You used', den, '.Abort'
    sys.exit()
if not par in  ['pt', 'eta', 'vtx', 'pt_eta', 'newpt', 'newpt_eta', 'tag_instLumi', 'pair_deltaR']:
    print '@ERROR: par should be', ['pt', 'eta', 'vtx', 'pt_eta', 'newpt', 'newpt_eta', 'tag_instLumi', 'pair_deltaR'], 'You used', par, '.Abort'

#_*_*_*_*_*_*_*_*_*_*_*_*
#Prepare variables, den, num and fit funct
#_*_*_*_*_*_*_*_*_*_*_*_*

#Set-up the mass range
_mrange = "70"
if 'iso' in num:
    _mrange = "77"
print '_mrange is', _mrange
mass_ =" mass"
if den == "highptid" or den == "trkhighptid": mass_ = "pair_newTuneP_mass"

Template = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    NumCPU = cms.uint32(1),
    SaveWorkspace = cms.bool(False),
    Variables = cms.PSet(),
    Categories = cms.PSet(),
    Expressions = cms.PSet(),
    Cuts = cms.PSet(),
    PDFs = cms.PSet(
        voigtPlusExpo = cms.vstring(
            "Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])".replace("mass",mass_),
            "Exponential::backgroundPass(mass, lp[0,-5,5])".replace("mass",mass_),
            "Exponential::backgroundFail(mass, lf[0,-5,5])".replace("mass",mass_),
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusExpo = cms.vstring(
            "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])".replace("mass",mass_),
            "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,2,10])".replace("mass",mass_),
            "SUM::signal(vFrac[0.8,0,1]*signal1, signal2)",
            "Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])".replace("mass",mass_),
            "Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])".replace("mass",mass_),
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusExpoMin70 = cms.vstring(
            "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])".replace("mass",mass_),
            "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])".replace("mass",mass_),
            "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
            "Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])".replace("mass",mass_),
            "Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])".replace("mass",mass_),
            "efficiency[0.9,0.7,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusCheb = cms.vstring(
            "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])".replace("mass",mass_),
            "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])".replace("mass",mass_),
            "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
            #par3
            "RooChebychev::backgroundPass(mass, {a0[0.25,0,0.5], a1[-0.25,-1,0.1],a2[0.,-0.25,0.25]})".replace("mass",mass_),
            "RooChebychev::backgroundFail(mass, {a0[0.25,0,0.5], a1[-0.25,-1,0.1],a2[0.,-0.25,0.25]})".replace("mass",mass_),
            "efficiency[0.9,0.7,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusCMS = cms.vstring(
            "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])".replace("mass",mass_),
            "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])".replace("mass",mass_),
            "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
            "RooCMSShape::backgroundPass(mass, alphaPass[70.,60.,90.], betaPass[0.02, 0.01,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])".replace("mass",mass_),
            "RooCMSShape::backgroundFail(mass, alphaFail[70.,60.,90.], betaFail[0.02, 0.01,0.1], gammaFail[0.001, 0.,0.1], peakPass)".replace("mass",mass_),
            "efficiency[0.9,0.7,1]",
            "signalFractionInPassing[0.9]"
        ),
        voigtPlusCMS = cms.vstring(
            "Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])".replace("mass",mass_),
            "RooCMSShape::backgroundPass(mass, alphaPass[70.,60.,90.], betaPass[0.02, 0.01,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])".replace("mass",mass_),
            "RooCMSShape::backgroundFail(mass, alphaFail[70.,60.,90.], betaFail[0.02, 0.01,0.1], gammaFail[0.001, 0.,0.1], peakPass)".replace("mass",mass_),
            "efficiency[0.9,0.7,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusCMS10_20 = cms.vstring(
            "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[1.5,1,2])".replace("mass",mass_),
            "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,7])".replace("mass",mass_),
            "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
            "RooCMSShape::backgroundPass(mass, alphaPass[70.,60.,90.], betaPass[0.02, 0.01,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])".replace("mass",mass_),
            "RooCMSShape::backgroundFail(mass, alphaFail[70.,60.,90.], betaFail[0.02, 0.01,0.1], gammaFail[0.001, 0.,0.1], peakPass)".replace("mass",mass_),
            "efficiency[0.9,0.7,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusCMSbeta0p2 = cms.vstring(
            "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])".replace("mass",mass_),
            "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])".replace("mass",mass_),
            "RooCMSShape::backgroundPass(mass, alphaPass[70.,60.,90.], betaPass[0.001, 0.,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])".replace("mass",mass_),
            "RooCMSShape::backgroundFail(mass, alphaFail[70.,60.,90.], betaFail[0.03, 0.02,0.1], gammaFail[0.001, 0.,0.1], peakPass)".replace("mass",mass_),
            #"RooCMSShape::backgroundPass(mass, alphaPass[70.,60.,90.], betaPass[0.001, 0.01,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])".replace("mass",mass_),
            #"RooCMSShape::backgroundFail(mass, alphaFail[70.,60.,90.], betaFail[0.001, 0.01,0.1], gammaFail[0.001, 0.,0.1], peakPass)".replace("mass",mass_),
            "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
            "efficiency[0.9,0.7,1]",
            "signalFractionInPassing[0.9]"
        ),
        voigtPlusCMSbeta0p2 = cms.vstring(
            "Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])".replace("mass",mass_),
            "RooCMSShape::backgroundPass(mass, alphaPass[70.,60.,90.], betaPass[0.001, 0.,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])".replace("mass",mass_),
            "RooCMSShape::backgroundFail(mass, alphaFail[70.,60.,90.], betaFail[0.03, 0.02,0.1], gammaFail[0.001, 0.,0.1], peakPass)".replace("mass",mass_),
            "efficiency[0.9,0.7,1]",
            "signalFractionInPassing[0.9]"
        )
    ),
    binnedFit = cms.bool(True),
    binsForFit = cms.uint32(40),
    saveDistributionsPlot = cms.bool(False),
    Efficiencies = cms.PSet(), # will be filled later
)


if sample == "dataidF_test_TM":
    process.TnP_Trigger = Template.clone(                                                                                                 
       InputFileNames = cms.vstring(                            
            '/eos/cms/store/group/phys_muon/fernanpe/TnPTrees/test/TnPTree_17Nov2017_SingleMuon_Run2017Fv1_Full_GoldenJSON_skimmedID.root'
            ),                                                                                                                           
        InputTreeName = cms.string("fitter_tree"),                                                                                       
        InputDirectoryName = cms.string("tpTree"),                                                                                       
        OutputFileName = cms.string("TnP_MuonISO_%s.root" % scenario),                                                                   
        Efficiencies = cms.PSet(),                                                                                                       
        )  



if sample == "mctest":
    process.TnP_Trigger = Template.clone(                                                                                                 
       InputFileNames = cms.vstring(                            
            '/eos/cms/store/group/phys_muon/fernanpe/TnPTrees/94X/mctest.root'
            #'/afs/cern.ch/work/g/gaperrin/public/ForPedro/ForMorion2018SF/tnpZ_MC.root'
            ),                                                                                                                           
        InputTreeName = cms.string("fitter_tree"),                                                                                       
        InputDirectoryName = cms.string("tpTree"),                                                                                       
        OutputFileName = cms.string("TnP_MuonISO_%s.root" % scenario),                                                                   
        Efficiencies = cms.PSet(),                                                                                                       
        )  


if scenario == "mc_all":
    print "Including the weight for MC"
    process.TnP_Trigger.WeightVariable = cms.string("weight")
    process.TnP_Trigger.Variables.weight = cms.vstring("weight","0","10","")


BIN = cms.PSet()

print 'debug1'
Num_dic = {'looseid':'LooseID', 'mediumid':'MediumID', 'mediumidprompt':'MediumPromptID', 'tightid':'TightID', 'trkhighptid':'TrkHighPtID', 'softid':'SoftID', 'softmvaid':'SoftMVAID', 'mvaloose':'MVALoose', 'mvamedium':'MVAMedium', 'mvatight':'MVATight', 'tightidhww':'TightIDHWW','puppiIso':'PuppiIso','puppiIsoNoLep':'PuppiIsoNoLep','combpuppiIso':'combPuppiIso', 'muCleanerIII':'MuonCleanerIII', 'muCleanerIV':'MuonCleanerIV', 'highptid':'HighPtID','looseiso':'LooseRelIso', 'mediumiso':'MediumISO', 'miniisotight':'MiniISOTight', 'tightiso':'TightRelIso','tklooseiso':'LooseRelTkIso', 'tktightiso':'TightRelTkIso', 'mediumiso':'MediumIso', 'trackermuons':'TrackerMuons'}
Den_dic = {'gentrack':'genTracks','looseid':'LooseID','mediumid':'MediumID', 'tightid':'TightIDandIPCut','tightidhww':'TightIDHWW','highptid':'HighPtIDandIPCut', 'trkhighptid':'TrkHighPtID', 'trackermuons':'TrackerMuons'}
Sel_dic = {'looseid':'LooseCutid','mediumid':'MediumCutid','mediumidprompt':'MediumCutidPrompt', 'tightid':'TightCutid','tightidhww':'Tight2012_zIPdBCut','puppiIso':'puppiIsoCut', 'puppiIsoNoLep':'puppiIsoNoLepCut','combpuppiIso':'combpuppiIsoCut','muCleanerIII':'TM_cleanMuonIIICut', 'muCleanerIV':'TM_cleanMuonIVCut', 'highptid':'HighptCutid','looseiso':'LooseCutiso','tightiso':'TightCutiso','tklooseiso':'TrkLooseCutiso', 'tktightiso':'TrkTightCutiso', 'mediumiso':'MediumCutiso', 'trkhighptid':'trkHighptCutid', 'softid':'SoftCutid', 'softmvaid':'SoftMVACutid', 'mvaloose':'MVALooseCut', 'mvamedium':'MVAMediumCut', 'mvatight':'MVATightCut', 'miniisotight':'MiniTightCutiso', 'tightiso':'TightCutiso', 'trackermuons':'TMCut'}
print 'debugSel'
#Par_dic = {'eta':'eta', 'pt':}

FillVariables(par)
FillNumDen(num,den)
print 'debugFill'

print 'den is', den,'dic',Den_dic[den]
print 'num is', num,'dic',Num_dic[num]
print 'par is', par

ID_BINS = [(Sel_dic[num],("NUM_%s_DEN_%s_PAR_%s"%(Num_dic[num],Den_dic[den],par),BIN))]
print 'debug5'

print Sel_dic[num]
print ("NUM_%s_DEN_%s_PAR_%s"%(Num_dic[num],Den_dic[den],par),BIN)

#_*_*_*_*_*_*_*_*_*_*_*
#Launch fit production
#_*_*_*_*_*_*_*_*_*_*_*

for ID, ALLBINS in ID_BINS:
    print 'debug1'
    X = ALLBINS[0]
    B = ALLBINS[1]
    _output = os.getcwd() + '/Efficiency' + iteration
    if not os.path.exists(_output):
        print 'Creating', '/Efficiency' + iteration,', the directory where the fits are stored.'
        os.makedirs(_output)
    if scenario == 'data_all':
        _output += '/DATA' + '_' + sample
    elif scenario == 'mc_all':
        _output += '/MC' + '_' + sample
    if not os.path.exists(_output):
        os.makedirs(_output)
    module = process.TnP_Trigger.clone(OutputFileName = cms.string(_output + "/TnP_MC_%s.root" % (X)))
    #save the fitconfig in the plot directory
    shutil.copyfile(os.getcwd()+'/fitMuon2.py',_output+'/fitMuon2.py')
    if 'signalvar' in sample:
        shape = cms.vstring("voigtPlusExpo")
        print 'debug2'
        print 'SYSTEMATIC STUDIES: the signal function will be ONE voigtian + CMSshape'
    else:
    # DEFAULT FIT FUNCTION: two voingtians + Exponential
        shape = cms.vstring("vpvPlusExpo")
        print 'debug2'



    DEN = B.clone(); num_ = ID;
    FillBin(par)

    if not "iso" in num: #customize only for ID
        if bgFitFunction == 'default':
            
            # SYSTEMATIC STUDIES: signal function variation
            if 'signalvar' in sample:
                if ('pt' in X):
                    print 'SYSTEMATIC STUDIES: the signal function will be ONE voigtian + CMSshape'
                    print 'den is', den 
                    print 'num_ is ', num
                    if den == "highptid" or num == "highptid" or den == "trkhighptid" or num == "trkhighptid":
                        if (len(DEN.pair_newTuneP_probe_pt)==9 or len(DEN.pair_newTuneP_probe_pt)==8 or len(DEN.pair_newTuneP_probe_pt)==10):
                            shape = cms.vstring("voigtPlusCMS","*pt_bin0*","voigtPlusCMS","*pt_bin1*","voigtPlusCMS","*pt_bin2*","voigtPlusCMS","*pt_bin3*","voigtPlusCMSbeta0p2","*pt_bin4*","voigtPlusCMSbeta0p2","*pt_bin5*","voigtPlusCMSbeta0p2","*pt_bin6*","voigtPlusCMSbeta0p2","*pt_bin7*","voigtPlusCMSbeta0p2", "*pt_bin8*","voigtPlusCMSbeta0p2")
                        if scenario == "mc_all":
                            if (len(DEN.pair_newTuneP_probe_pt)==9 or len(DEN.pair_newTuneP_probe_pt)==8 or len(DEN.pair_newTuneP_probe_pt)==10):
                                shape = cms.vstring("voigtPlusCMSbeta0p2","*pt_bin0*","voigtPlusExpo","*pt_bin1*","voigtPlusExpo","*pt_bin2*","voigtPlusExpo","*pt_bin3*","voigtPlusExpo","*pt_bin4*","voigtPlusCMSbeta0p2","*pt_bin5*","voigtPlusCMSbeta0p2","*pt_bin6*","voigtPlusCMSbeta0p2","*pt_bin7*","voigtPlusCMSbeta0p2", "*pt_bin8*","voigtPlusCMSbeta0p2")

                    else:
                        if (len(DEN.pt)==26):
                            shape = cms.vstring("voigtPlusCMSbeta0p2")
                        if scenario == "mc_all":
                            shape = cms.vstring("voigtPlusCMSbeta0p2")

                        if (len(DEN.pt)==9 or len(DEN.pt)==8 or len(DEN.pt)==10):
                            shape = cms.vstring("voigtPlusCMS","*pt_bin0*","voigtPlusCMS","*pt_bin1*","voigtPlusCMS","*pt_bin2*","voigtPlusCMS","*pt_bin3*","voigtPlusCMSbeta0p2","*pt_bin4*","voigtPlusCMSbeta0p2","*pt_bin5*","voigtPlusCMSbeta0p2","*pt_bin6*","voigtPlusCMSbeta0p2","*pt_bin7*","voigtPlusCMSbeta0p2","*pt_bin8*","voigtPlusCMSbeta0p2")

            #NOMINAL CASE: ID vs pT fit funtion by default -> two voigtians + CMSshape
            else:
                if ('pt' in X):
                    print 'den is', den 
                    print 'num_ is ', num
                    if den == "highptid" or num == "highptid" or den == "trkhighptid" or num == "trkhighptid":
                        if (len(DEN.pair_newTuneP_probe_pt)==9 or len(DEN.pair_newTuneP_probe_pt)==8 or len(DEN.pair_newTuneP_probe_pt)==10):
                            shape = cms.vstring("vpvPlusCMS","*pt_bin0*","vpvPlusCMS","*pt_bin1*","vpvPlusCMS","*pt_bin2*","vpvPlusCMS","*pt_bin3*","vpvPlusCMSbeta0p2","*pt_bin4*","vpvPlusCMSbeta0p2","*pt_bin5*","vpvPlusCMSbeta0p2","*pt_bin6*","vpvPlusCMSbeta0p2","*pt_bin7*","vpvPlusCMSbeta0p2", "*pt_bin8*","vpvPlusCMSbeta0p2")
                        if scenario == "mc_all":
                            if (len(DEN.pair_newTuneP_probe_pt)==9 or len(DEN.pair_newTuneP_probe_pt)==8 or len(DEN.pair_newTuneP_probe_pt)==10):
                                shape = cms.vstring("vpvPlusCMSbeta0p2","*pt_bin0*","vpvPlusExpo","*pt_bin1*","vpvPlusExpo","*pt_bin2*","vpvPlusExpo","*pt_bin3*","vpvPlusExpo","*pt_bin4*","vpvPlusCMSbeta0p2","*pt_bin5*","vpvPlusCMSbeta0p2","*pt_bin6*","vpvPlusCMSbeta0p2","*pt_bin7*","vpvPlusCMSbeta0p2", "*pt_bin8*","vpvPlusCMSbeta0p2")

                    else:
                        if (len(DEN.pt)==26):
                            shape = cms.vstring("vpvPlusCMSbeta0p2")
                        if scenario == "mc_all":
                            shape = cms.vstring("vpvPlusCMSbeta0p2")

                        if (len(DEN.pt)==9 or len(DEN.pt)==8 or len(DEN.pt)==10):
                            shape = cms.vstring("vpvPlusCMS","*pt_bin0*","vpvPlusCMS","*pt_bin1*","vpvPlusCMS","*pt_bin2*","vpvPlusCMS","*pt_bin3*","vpvPlusCMSbeta0p2","*pt_bin4*","vpvPlusCMSbeta0p2","*pt_bin5*","vpvPlusCMSbeta0p2","*pt_bin6*","vpvPlusCMSbeta0p2","*pt_bin7*","vpvPlusCMSbeta0p2","*pt_bin8*","vpvPlusCMSbeta0p2")

        elif bgFitFunction == 'CMSshape':
            if den == "highpt":
                if (len(DEN.pair_newTuneP_probe_pt)==9):
                    shape = cms.vstring("vpvPlusExpo","*pt_bin4*","vpvPlusCMS","*pt_bin5*","vpvPlusCMS","*pt_bin6*","vpvPlusCheb","*pt_bin7*","vpvPlusCheb")
            else:
                if (len(DEN.pt)==9):
                    shape = cms.vstring("vpvPlusExpo","*pt_bin4*","vpvPlusCMS","*pt_bin5*","vpvPlusCheb","*pt_bin6*","vpvPlusCheb", "*pt_bin7*","vpvPlusCheb")

    print 'd3'
    mass_variable ="mass"
    print 'den is', den
    if den == "highptid" or den == "trkhighptid":
        mass_variable = "pair_newTuneP_mass"
    #compute isolation efficiency
    if scenario == 'data_all':
        if num_.find("Iso4") != -1 or num_.find("Iso3") != -1:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num_,"below"),
                UnbinnedVariables = cms.vstring(mass_variable),
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        else:
            print 'd4'
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num_,"above"),
                UnbinnedVariables = cms.vstring(mass_variable),
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        setattr(process, "TnP_Trigger_"+ID+"_"+X, module)
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))
        if num_.find("puppiIso") != -1:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                    EfficiencyCategoryAndState = cms.vstring(num_,"below"),
                    UnbinnedVariables = cms.vstring(mass_variable),
                    BinnedVariables = DEN,
                    BinToPDFmap = shape
                    ))
    elif scenario == 'mc_all' and par=='vtx':
        print 'MC sample as function of nVertices -> the PU reweighting will not be applied'
        if num_.find("Iso4") != -1 or num_.find("Iso3") != -1:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num_,"below"),
                UnbinnedVariables = cms.vstring(mass_variable),
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        else:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num_,"above"),
                UnbinnedVariables = cms.vstring(mass_variable),
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        setattr(process, "TnP_Trigger_"+ID+"_"+X, module)
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))
        if num_.find("puppiIso") != -1:
             setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                    EfficiencyCategoryAndState = cms.vstring(num_,"below"),
                    UnbinnedVariables = cms.vstring(mass_variable),
                        BinnedVariables = DEN,
                    BinToPDFmap = shape
                    ))
    elif scenario == 'mc_all' and par!='vtx':
        # PU reweighting applied for MC when par != vtx
        print 'the PU reweighting will be applied'
        if num_.find("Iso4") != -1 or num_.find("Iso3") != -1:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num_,"below"),
                UnbinnedVariables = cms.vstring(mass_variable, "weight"),
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        else:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num_,"above"),
                UnbinnedVariables = cms.vstring(mass_variable, "weight"),
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        setattr(process, "TnP_Trigger_"+ID+"_"+X, module)
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))
        if num_.find("puppiIso") != -1:
             setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                    EfficiencyCategoryAndState = cms.vstring(num_,"below"),
                    UnbinnedVariables = cms.vstring(mass_variable,"weight"),
                        BinnedVariables = DEN,
                    BinToPDFmap = shape
                    ))
