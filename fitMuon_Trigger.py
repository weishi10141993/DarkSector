import FWCore.ParameterSet.Config as cms
import sys, os, shutil
from optparse import OptionParser

#_*_*_*_*_*_
#Read Inputs
#_*_*_*_*_*_

def FillNumDen(num, den):
    '''Declares the needed selections for a givent numerator, denominator'''

    #Define the mass distribution
    if 'mass_up' in sample:
        process.TnP_Trigger.Variables.mass = cms.vstring("Tag-muon Mass", _mrange, "140", "GeV/c^{2}")
    elif 'mass_down' in sample:
        process.TnP_Trigger.Variables.mass = cms.vstring("Tag-muon Mass", _mrange, "120", "GeV/c^{2}")
    else:
        process.TnP_Trigger.Variables.mass = cms.vstring("Tag-muon Mass", _mrange, "130", "GeV/c^{2}")

    if num == "TrkMu16NoVtx":
        process.TnP_Trigger.Variables.pt  = cms.vstring("probe pt", "0", "1000", "")
        process.TnP_Trigger.Categories.HLT_TrkMu16NoFiltersNoVtx  = cms.vstring("PassTrkMu16NoVtx", "dummy[pass=1,fail=0]")
        process.TnP_Trigger.Expressions.HLT16CutPt16 = cms.vstring("HLT16CutPt16", "pt > 16 && HLT_TrkMu16NoFiltersNoVtx == 1", "pt","HLT_TrkMu16NoFiltersNoVtx")
        process.TnP_Trigger.Cuts.PassHLT16CutPt16  = cms.vstring("PassHLT16CutPt16", "HLT16CutPt16", "0.5")
    elif num == "TrkMu6NoVtx":
        process.TnP_Trigger.Variables.pt  = cms.vstring("probe pt", "0", "1000", "")
        process.TnP_Trigger.Categories.HLT_TrkMu6NoFiltersNoVtx  = cms.vstring("PassTrkMu6NoVtx", "dummy[pass=1,fail=0]")
        process.TnP_Trigger.Expressions.HLT6CutPt6 = cms.vstring("HLT6CutPt6", "pt > 6 && HLT_TrkMu6NoFiltersNoVtx == 1", "pt","HLT_TrkMu16NoFiltersNoVtx")
        process.TnP_Trigger.Cuts.PassHLT6CutPt6 = cms.vstring("PassHLT6CutPt6", "HLT6CutPt6", "0.5")

    if den == "pT16":
        process.TnP_Trigger.Variables.pt  = cms.vstring("probe pt", "0", "1000", "")
        process.TnP_Trigger.Expressions.CutPt16 = cms.vstring("CutPt16", "pt > 16", "pt")
        process.TnP_Trigger.Cuts.PassCutPt16  = cms.vstring("PassCutPt16", "CutPt16", "0.5")
    elif den == "pT6":
        process.TnP_Trigger.Variables.pt  = cms.vstring("probe pt", "0", "1000", "")
        process.TnP_Trigger.Expressions.CutPt6 = cms.vstring("CutPt6", "pt > 6", "pt")
        process.TnP_Trigger.Cuts.PassCutPt6  = cms.vstring("PassCutPt6", "CutPt6", "0.5")
                                    
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
        DEN.pt = cms.vdouble(3, 6, 10, 16, 20, 25, 30, 40, 50, 60, 120, 200)
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
    if den == "pT16": DEN.pt = cms.vdouble(16, 1000)
    elif den == "pT6": DEN.pt = cms.vdouble(6, 1000)

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
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

if not num  in ['TrkMu16NoVtx', 'TrkMu6NoVtx']:
    print '@ERROR: num should be in ',['TrkMu16NoVtx', 'TrkMu6NoVtx'], 'You used', num, '.Abort'
    sys.exit()
if not den in ['pT16', 'pT6']:
    print '@ERROR: den should be',['pT16', 'pT6'], 'You used', den, '.Abort'
    sys.exit()
if not par in  ['pt', 'eta', 'phi', 'vtx', 'pt_eta', 'newpt', 'newpt_eta', 'tag_instLumi', 'pair_deltaR']:
    print '@ERROR: par should be', ['pt', 'eta', 'phi', 'vtx', 'pt_eta', 'newpt', 'newpt_eta', 'tag_instLumi', 'pair_deltaR'], 'You used', par, '.Abort'

#_*_*_*_*_*_*_*_*_*_*_*_*
#Prepare variables, den, num and fit funct
#_*_*_*_*_*_*_*_*_*_*_*_*

#Set-up the mass range
_mrange = "70"
if 'iso' in num:
    _mrange = "77"
print '_mrange is', _mrange
mass_ = "mass"

Template = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    NumCPU = cms.uint32(1),
    SaveWorkspace = cms.bool(True),
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


if sample == "2018B":
    process.TnP_Trigger = Template.clone(                                                                                                 
       InputFileNames = cms.vstring(                            
            '/afs/cern.ch/work/w/wshi/public/2018DataControlHLT/CMSSW_10_1_7/src/MuonAnalysis/TagAndProbe/test/zmumu/'
            ),     
        InputDirectoryName = cms.string("tpTree"), 
        InputTreeName = cms.string("fitter_tree"),                                                                                     
        OutputFileName = cms.string("TnP_Trigger_%s.root" % scenario),                                                                   
        Efficiencies = cms.PSet(),                                                                                                       
        ) 

if scenario == "mc_all":
    print "Including the weight for MC"
    process.TnP_Trigger.WeightVariable = cms.string("weight")
    process.TnP_Trigger.Variables.weight = cms.vstring("weight","0","10","")


BIN = cms.PSet()

print 'debug1'
Num_dic = {'TrkMu16NoVtx':'HLT_TrkMu16NoFiltersNoVtx', 'TrkMu6NoVtx':'HLT_TrkMu6NoFiltersNoVtx'}
Den_dic = {'pT16':'Pt16Cut','pT6':'Pt6Cut'}
Sel_dic = {'TrkMu16NoVtx':'PassHLT16CutPt16', 'TrkMu6NoVtx':'PassHLT6CutPt6'}
print 'debugSel'

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
    module = process.TnP_Trigger.clone(OutputFileName = cms.string(_output + "/TnP_Trigger_%s.root" % (X)))
    #save the fitconfig in the plot directory
    shutil.copyfile(os.getcwd()+'/fitMuon_Trigger.py',_output+'/fitMuon_Trigger.py')
    #DEFAULT FIT FUNCTION
    shape = cms.vstring("voigtPlusExpo")
    print 'default fit func'

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
