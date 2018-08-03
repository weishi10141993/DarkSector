import FWCore.ParameterSet.Config as cms
import sys, os, shutil
from optparse import OptionParser

#_*_*_*_*_*_
#Read Inputs
#_*_*_*_*_*_

def FillNumDen(num, den):
    '''Declares the needed selections for a givent numerator, denominator'''
    process.TnP_Trigger.Variables.mass = cms.vstring("Tag-muon Mass", _mrange, "130", "GeV/c^{2}")

    if num == "TrkMu16NoVtx":
        process.TnP_Trigger.Categories.HLT_TrkMu16NoFiltersNoVtx  = cms.vstring("Control HLT16", "dummy[pass=1,fail=0]")
        process.TnP_Trigger.Expressions.HLT16CutPt16 = cms.vstring("HLT16CutPt16", "pt > 16 && HLT_TrkMu16NoFiltersNoVtx == 1", "pt","HLT_TrkMu16NoFiltersNoVtx")
        process.TnP_Trigger.Cuts.PassHLT16CutPt16  = cms.vstring("PassHLT16CutPt16", "HLT16CutPt16", "0.5")
    elif num == "TrkMu6NoVtx":
        process.TnP_Trigger.Categories.HLT_TrkMu6NoFiltersNoVtx  = cms.vstring("Control HLT6", "dummy[pass=1,fail=0]")
        process.TnP_Trigger.Expressions.HLT6CutPt6 = cms.vstring("HLT6CutPt6", "pt > 6 && HLT_TrkMu6NoFiltersNoVtx == 1", "pt","HLT_TrkMu6NoFiltersNoVtx")
        process.TnP_Trigger.Cuts.PassHLT6CutPt6 = cms.vstring("PassHLT6CutPt6", "HLT6CutPt6", "0.5")

    if den == "pT16":
        process.TnP_Trigger.Expressions.CutPt16 = cms.vstring("CutPt16", "pt > 16", "pt")
        process.TnP_Trigger.Cuts.PassCutPt16  = cms.vstring("PassCutPt16", "CutPt16", "0.5")
    elif den == "pT6":
        process.TnP_Trigger.Expressions.CutPt6 = cms.vstring("CutPt6", "pt > 6", "pt")
        process.TnP_Trigger.Cuts.PassCutPt6  = cms.vstring("PassCutPt6", "CutPt6", "0.5")
                                    
def FillVariables(par):
    '''Declares only the parameters which are necessary, no more'''
    '''Always fill pt'''
    process.TnP_Trigger.Variables.pt  = cms.vstring("muon p_{T}", "0.0", "1000.0", "GeV/c")
    if par == 'eta':
        process.TnP_Trigger.Variables.eta  = cms.vstring("muon #eta", "-2.5", "2.5", "")
    if par == 'phi':
        process.TnP_Trigger.Variables.phi  = cms.vstring("muon #phi", "-3.2", "3.2", "")   
    if par == 'pt_eta' or 'newpt_eta':
        process.TnP_Trigger.Variables.abseta  = cms.vstring("muon |#eta|", "0", "2.5", "")
    if par == 'pair_deltaR':
        process.TnP_Trigger.Variables.pair_deltaR  = cms.vstring("deltaR", "0", "4", "")
    if par == 'vtx':
        print 'I filled it'
        process.TnP_Trigger.Variables.tag_nVertices   = cms.vstring("Number of vertices", "0", "999", "")

def FillBin(par):
    '''Sets the values of the bin paramters and the bool selections on the denominators'''
    #Parameter 
    if par == 'eta':
        DEN.eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4)
    elif par == 'phi':
        DEN.phi = cms.vdouble(-3.15, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.15)
    elif par == 'pt':
        DEN.pt = cms.vdouble(6, 10, 16, 20, 25, 30, 40, 50, 60, 120, 1000)
    elif par == 'pair_deltaR':
        DEN.pair_deltaR = cms.vdouble(0., 0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 5.0)
    elif par == 'pt_eta':
        DEN.pt = cms.vdouble(20, 25, 30, 40, 50, 60, 120, 1000)
        DEN.abseta = cms.vdouble(0., 0.9, 1.2, 2.1, 2.4)
    elif par == 'vtx':
        DEN.tag_nVertices = cms.vdouble(6.5, 10.5, 14.5, 18.5, 22.5, 26.5, 30.5, 34.5, 50.5)
 
    #Selections
    if den == "pT16": DEN.pt = cms.vdouble(16.0, 1000.0)
    elif den == "pT6": DEN.pt = cms.vdouble(6.0, 1000.0)

args = sys.argv[1:]

if len(args) > 1: iteration = args[1]
print "The iteration is", iteration

if len(args) > 2: num = args[2]
print 'The num is', num 

if len(args) > 3: den = args[3]
print 'The den is', den 

if len(args) > 4: scenario = args[4]
print "Will run scenario ", scenario

if len(args) > 5: sample = args[5]
print 'The sample is', sample

if len(args) > 6: par = args[6]
print 'The binning is', par 

bgFitFunction = 'default'
if len(args) > 7: bgFitFunction = args[7]
if bgFitFunction == 'custom':
    print 'Will experiment with custom fit functions'
else:
    print 'Will use the deault fit functions for the backgroud'

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
if not par in  ['pt', 'eta', 'phi', 'vtx', 'pt_eta', 'newpt', 'newpt_eta', 'pair_deltaR']:
    print '@ERROR: par should be', ['pt', 'eta', 'phi', 'vtx', 'pt_eta', 'newpt', 'newpt_eta', 'pair_deltaR'], 'You used', par, '.Abort'

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
            "Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])",
            "Exponential::backgroundPass(mass, lp[0,-5,5])",
            "Exponential::backgroundFail(mass, lf[0,-5,5])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
        voigtPlusCMSbeta0p2 = cms.vstring(
            "Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])",
            "RooCMSShape::backgroundPass(mass, alphaPass[70.,60.,90.], betaPass[0.001, 0.,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])",
            "RooCMSShape::backgroundFail(mass, alphaFail[70.,60.,90.], betaFail[0.03, 0.02,0.1], gammaFail[0.001, 0.,0.1], peakPass)",
            "efficiency[0.9,0.7,1]",
            "signalFractionInPassing[0.9]"
        )
    ),
    binnedFit = cms.bool(True),
    binsForFit = cms.uint32(40),
    saveDistributionsPlot = cms.bool(False),
    Efficiencies = cms.PSet(), # will be filled later
)

if sample == "2018":
    process.TnP_Trigger = Template.clone(                                                                                                 
        InputFileNames = cms.vstring(                            
            '/afs/cern.ch/work/w/wshi/public/2018DataControlHLT/CMSSW_10_1_7/src/MuonAnalysis/TagAndProbe/test/zmumu/tnpZ_Data_All_Skim.root'
            ),     
        InputDirectoryName = cms.string("tpTree"), 
        InputTreeName = cms.string("fitter_tree"),                                                                                     
        OutputFileName = cms.string("TnP_Trigger_%s.root" % scenario),                                                                   
        Efficiencies = cms.PSet(),                                                                                                       
    )

BIN = cms.PSet()

print 'BIN: ' + BIN
Num_dic = {'TrkMu16NoVtx':'HLT_TrkMu16NoFiltersNoVtx', 'TrkMu6NoVtx':'HLT_TrkMu6NoFiltersNoVtx'}
Den_dic = {'pT16':'Pt16Cut','pT6':'Pt6Cut'}
Sel_dic = {'TrkMu16NoVtx':'PassHLT16CutPt16', 'TrkMu6NoVtx':'PassHLT6CutPt6'}

FillVariables(par)
FillNumDen(num,den)

print 'den is ', den,' dic ',Den_dic[den]
print 'num is ', num,' dic ',Num_dic[num]
print 'par is ', par

ID_BINS = [(Sel_dic[num],("NUM_%s_DEN_%s_PAR_%s"%(Num_dic[num],Den_dic[den],par),BIN))]
print 'ID_BINS: ', ID_BINS

print 'Sel_dic[num]: ', Sel_dic[num]
print ("NUM_%s_DEN_%s_PAR_%s"%(Num_dic[num],Den_dic[den],par),BIN)

#_*_*_*_*_*_*_*_*_*_*_*
#Launch fit production
#_*_*_*_*_*_*_*_*_*_*_*

for ID, ALLBINS in ID_BINS:
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
    print 'Default fit func: voigtPlusExpo'

    DEN = B.clone(); num_ = ID;
    FillBin(par)
    
    if bgFitFunction == 'default':          
        if ('pt' in X):
            print 'par is pt'
            shape = cms.vstring("voigtPlusCMSbeta0p2")
            print 'Fit func updated: ' + shape
                    
    mass_variable ="mass"
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
            print 'Fitting'
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num_,"above"),
                UnbinnedVariables = cms.vstring(mass_variable),
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        setattr(process, "TnP_Trigger_"+ID+"_"+X, module)
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))
