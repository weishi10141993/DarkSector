import FWCore.ParameterSet.Config as cms
import sys, os, shutil
from optparse import OptionParser
### USAGE: cmsRun fitMuonID.py TEST tight loose mc mc_all
###_id: tight, loose, medium, soft

#_*_*_*_*_*_
#Read Inputs
#_*_*_*_*_*_

def FillNumDen(num, den):
    '''Declares the needed selections for a givent numerator, denominator'''

    #Define the mass distribution
    #Variables defines all the real variables of the probes available in the input tree and intended for use in the efficiencies
    if den == "highptid" :
        process.TnP_MuonID.Variables.pair_newTuneP_mass = cms.vstring("Tag-muon Mass", _mrange, "3.4", "GeV/c^{2}")
    else:
        process.TnP_MuonID.Variables.mass = cms.vstring("Tag-muon Mass", _mrange, "3.3", "GeV/c^{2}")
    #NUMS:probe parameter definition
    if num == "looseid":
        #Category defines all the discrete variables of the probes available in the input tree and intended for use in the efficiency calculations
        #This reads Loose branch from the TnP tree
        process.TnP_MuonID.Categories.Loose  = cms.vstring("Loose Muon", "dummy[pass=1,fail=0]")
        process.TnP_MuonID.Categories.tag_Mu7p5_Track7_Jpsi_MU = cms.vstring("tag trigger","dummy[pass=1,fail=0]")
        process.TnP_MuonID.Categories.Mu7p5_Track7_Jpsi_TK = cms.vstring("probe trigger","dummy[pass=1,fail=0]")
        #This defines a new variable "Loose_Var" which has value 1 or 0 depending on "Loose==1" or not, 3rd and 4th component indicate the variables used
        process.TnP_MuonID.Expressions.Loose_Var  = cms.vstring("Loose_Var", "Loose==1", "Loose")
        #This defines a dynamical category so simple cut value can be applied, using "above" or "below" in the "EfficiencyCategoryAndState"
        process.TnP_MuonID.Cuts.Loose_Muon = cms.vstring("Loose_Muon", "Loose_Var", "0.5")
    elif num == "mediumid":
        process.TnP_MuonID.Categories.Medium2016  = cms.vstring("Medium Id. Muon (ICHEP version)", "dummy[pass=1,fail=0]")
        process.TnP_MuonID.Expressions.Medium2016_noIPVar= cms.vstring("Medium2016_noIPVar", "Medium2016==1", "Medium2016")
        process.TnP_MuonID.Cuts.Medium2016_noIP= cms.vstring("Medium2016_noIP", "Medium2016_noIPVar", "0.5")
    elif num == "tightid":
        process.TnP_MuonID.Variables.dzPV  = cms.vstring("dzPV", "-1000", "1000", "")
        process.TnP_MuonID.Categories.Tight2012 = cms.vstring("Tight Id. Muon", "dummy[pass=1,fail=0]")
        process.TnP_MuonID.Expressions.Tight2012_zIPCutVar = cms.vstring("Tight2012_zIPCut", "Tight2012 == 1 && abs(dzPV) < 0.5", "Tight2012", "dzPV")#3rd and 4th component shows which variables are used to define this new dynamical category
        process.TnP_MuonID.Cuts.Tight2012_zIPCut = cms.vstring("Tight2012_zIPCut", "Tight2012_zIPCutVar", "0.5")
    elif num == "highptid":
        process.TnP_MuonID.Variables.dzPV  = cms.vstring("dzPV", "-1000", "1000", "")
        process.TnP_MuonID.Categories.HighPt = cms.vstring("High-pT Id. Muon", "dummy[pass=1,fail=0]")
        process.TnP_MuonID.Expressions.HighPt_zIPCutVar = cms.vstring("HighPt_zIPCut", "HighPt == 1 && abs(dzPV) < 0.5", "HighPt", "dzPV")
        process.TnP_MuonID.Cuts.HighPt_zIPCut = cms.vstring("HighPt_zIPCut", "HighPt_zIPCutVar", "0.5")
    elif num == "looseiso":
        process.TnP_MuonID.Variables.combRelIsoPF04dBeta = cms.vstring("dBeta rel iso dR 0.4", "-2", "9999999", "")
        process.TnP_MuonID.Cuts.LooseIso4 = cms.vstring("LooseIso4" ,"combRelIsoPF04dBeta", "0.25")
    elif num == "tightiso":
        process.TnP_MuonID.Variables.combRelIsoPF04dBeta = cms.vstring("dBeta rel iso dR 0.4", "-2", "9999999", "")
        process.TnP_MuonID.Cuts.TightIso4 = cms.vstring("TightIso4" ,"combRelIsoPF04dBeta", "0.15")
    elif num == "tklooseiso":
        process.TnP_MuonID.Variables.relTkIso = cms.vstring("trk rel iso dR 0.3", "-2", "9999999", "")
        process.TnP_MuonID.Cuts.LooseTkIso3 = cms.vstring("LooseTkIso3" ,"relTkIso", "0.10")
    #DEN
    if den == "looseid":
        process.TnP_MuonID.Categories.Loose  = cms.vstring("Loose Muon", "dummy[pass=1,fail=0]")
    elif den == "mediumid":
        process.TnP_MuonID.Categories.Medium2016  = cms.vstring("Medium Id. Muon (ICHEP version)", "dummy[pass=1,fail=0]")
    elif den == "tightid":
        process.TnP_MuonID.Variables.dzPV  = cms.vstring("dzPV", "-1000", "1000", "")
        process.TnP_MuonID.Categories.Tight2012 = cms.vstring("Tight Id. Muon", "dummy[pass=1,fail=0]")
    elif den == "highptid":
        process.TnP_MuonID.Variables.dzPV  = cms.vstring("dzPV", "-1000", "1000", "")
        process.TnP_MuonID.Categories.HighPt = cms.vstring("High-pT Id. Muon", "dummy[pass=1,fail=0]")
        process.TnP_MuonID.Expressions.HighPt_zIPCutVar = cms.vstring("HighPt_zIPCut", "HighPt == 1 && abs(dzPV) < 0.5", "HighPt", "dzPV")
        process.TnP_MuonID.Cuts.HighPt_zIPCut = cms.vstring("HighPt_zIPCut", "HighPt_zIPCutVar", "0.5")


                                    
def FillVariables(par):
    '''Declares only the parameters which are necessary, no more'''

    if par == 'newpt' or 'newpt_eta':
        process.TnP_MuonID.Variables.pair_newTuneP_probe_pt = cms.vstring("muon p_{T} (tune-P)", "0", "1000", "GeV/c")
    if par == 'eta':
        process.TnP_MuonID.Variables.eta  = cms.vstring("muon #eta", "-2.5", "2.5", "")
    if par == 'pt' or 'pt_eta':
        process.TnP_MuonID.Variables.pt  = cms.vstring("muon p_{T}", "0", "1000", "GeV/c")
    if par == 'pt_eta' or 'newpt_eta':
        process.TnP_MuonID.Variables.abseta  = cms.vstring("muon |#eta|", "0", "2.5", "")
    if par == 'vtx':
        print 'I filled it'
        process.TnP_MuonID.Variables.tag_nVertices   = cms.vstring("Number of vertices", "0", "999", "")

def FillBin(par):
    '''Sets the values of the bin paramters and the bool selections on the denominators'''
    #Parameter 
    if par == 'newpt_eta':
        DEN.pair_newTuneP_probe_pt = cms.vdouble(1,2,3,4,5,6,7,8) 
        DEN.abseta = cms.vdouble( 0., 0.9, 1.2, 2.1, 2.4)
    elif par == 'newpt':
        DEN.pair_newTuneP_probe_pt = cms.vdouble(1,2,3,4,5,6,7,8)
    elif par == 'eta':
        DEN.eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4)
    elif par == 'pt':
        DEN.pt = cms.vdouble(2, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.5, 5, 6, 8, 10, 15, 20, 30, 35, 40)
    elif par == 'pt_eta':
        DEN.pt = cms.vdouble(2, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.5, 5, 6, 8, 10, 15, 20, 30, 35, 40)
        DEN.abseta = cms.vdouble( 0., 0.9, 1.2, 2.1, 2.4)
    elif par == 'vtx':
        print 'I filled it also asdf'
        DEN.tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5)
    #Selections
    if den == "gentrack": pass
    elif den == "looseid": DEN.Loose = cms.vstring("pass")
    elif den == "mediumid": DEN.Medium2016 = cms.vstring("pass")
    elif den == "tightid": 
        DEN.Tight2012 = cms.vstring("pass")
        DEN.dzPV = cms.vdouble(-0.5, 0.5)
    elif den == "highptid":
        DEN.HighPt = cms.vstring("pass")
        DEN.dzPV = cms.vdouble(-0.5, 0.5)


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
    print 'Will use the standard fit functions for the background'


process = cms.Process("TagProbe")
process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

if not num  in ['looseid', 'mediumid', 'tightid', 'highptid', 'looseiso', 'tightiso', 'tklooseiso']:
    print '@ERROR: num should be in ',['looseid', 'mediumid', 'tightid', 'highptid', 'looseiso', 'tightiso', 'tklooseiso'], 'You used', num, '.Abort'
    sys.exit()
if not den in ['looseid', 'mediumid', 'tightid', 'highptid', 'gentrack']:
    print '@ERROR: den should be',['looseid', 'mediumid', 'tightid', 'highptid'], 'You used', den, '.Abort'
    sys.exit()
if not par in  ['pt', 'eta', 'vtx', 'pt_eta', 'newpt', 'newpt_eta']:
    print '@ERROR: par should be', ['pt', 'eta', 'vtx', 'pt_eta', 'newpt', 'newpt_eta'], 'You used', par, '.Abort'

#_*_*_*_*_*_*_*_*_*_*_*_*
#Prepare variables, den, num and fit funct
#_*_*_*_*_*_*_*_*_*_*_*_*

#Set-up the lower mass range needed in FillNumDen 
_mrange = "2.9"
if 'iso' in num:
    _mrange = "2.9"
print 'mass range is', _mrange
mass_ ="mass"
if den == "highptid" : mass_ = "pair_newTuneP_mass"



Template = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    #numbrer of CPUs to use for fitting
    NumCPU = cms.uint32(1),
    # specifies wether to save the RooWorkspace containing the data for each bin and
    # the pdf object with the initial and final state snapshots
    SaveWorkspace = cms.bool(True),


    Variables = cms.PSet(
        #essential for all den/num
        #mass = cms.vstring("Tag-muon Mass", _mrange, "130", "GeV/c^{2}"),
        #Jeta    = cms.vstring("muon #eta", "-2.5", "2.5", ""),
        ),

    Categories = cms.PSet(),
    Expressions = cms.PSet(),
    Cuts = cms.PSet(),

    # defines all the PDFs that will be available for the efficiency calculations; uses RooFit's "factory" syntax;
    # each pdf needs to define "signal", "backgroundPass", "backgroundFail" pdfs, "efficiency[0.9,0,1]" and "signalFractionInPassing[0.9]" are used for initial values
    PDFs = cms.PSet(
        voigtPlusExpo = cms.vstring(
            "Voigtian::signal(mass, mean[3.1, 3.0, 3.2], width[0.1], sigma[0.05,0.02,0.1])".replace("mass",mass_),
            "Exponential::backgroundPass(mass, lp[0,-5,5])".replace("mass",mass_),
            "Exponential::backgroundFail(mass, lf[0,-5,5])".replace("mass",mass_),
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusExpo = cms.vstring(#default shape
            "Voigtian::signal1(mass, mean1[3.1,3.0,3.2], width[0.1], sigma1[0.005, 0.002, 0.01])".replace("mass",mass_),
            "Voigtian::signal2(mass, mean2[3.1,3.0,3.2], width[0.1], sigma2[0.001, 0.0005, 0.004])".replace("mass",mass_),
            "SUM::signal(vFrac[0.8,0,1]*signal1, signal2)",
            "Exponential::backgroundPass(mass, lp[0, -5, 5])".replace("mass",mass_),
            "Exponential::backgroundFail(mass, lf[0, -5, 5])".replace("mass",mass_),
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusExpoMin70 = cms.vstring(
            "Voigtian::signal1(mass, mean1[3,2,4], width[0.4], sigma1[0.2,0.1,0.3])".replace("mass",mass_),
            "Voigtian::signal2(mass, mean2[3,2,4], width,        sigma2[0.4,0.3,1])".replace("mass",mass_),
            "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
            "Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])".replace("mass",mass_),
            "Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])".replace("mass",mass_),
            "efficiency[0.9,0.7,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusCheb = cms.vstring(
            "Voigtian::signal1(mass, mean1[3,2,4], width[0.4], sigma1[0.2,0.1,0.3])".replace("mass",mass_),
            "Voigtian::signal2(mass, mean2[3,2,4], width,        sigma2[0.4,0.3,1])".replace("mass",mass_),
            "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
            #par3
            "RooChebychev::backgroundPass(mass, {a0[0.25,0,0.5], a1[-0.25,-1,0.1],a2[0.,-0.25,0.25]})".replace("mass",mass_),
            "RooChebychev::backgroundFail(mass, {a0[0.25,0,0.5], a1[-0.25,-1,0.1],a2[0.,-0.25,0.25]})".replace("mass",mass_),
            "efficiency[0.9,0.7,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusCMS = cms.vstring( 
            "Voigtian::signal1(mass, mean1[3.1, 3.0, 3.2], width[0.1], sigma1[0.005, 0.002, 0.01])".replace("mass",mass_),
            "Voigtian::signal2(mass, mean2[3.1, 3.0, 3.2], width[0.1], sigma2[0.001, 0.0005, 0.004])".replace("mass",mass_),
            "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
            "RooCMSShape::backgroundPass(mass, alphaPass[2., 1., 3.], betaPass[0.02, 0.01,0.1], gammaPass[0.001, 0., 0.1], peakPass[3.0])".replace("mass",mass_),
            "RooCMSShape::backgroundFail(mass, alphaFail[2., 1., 3.], betaFail[0.02, 0.01,0.1], gammaFail[0.001, 0., 0.1], peakPass)".replace("mass",mass_),
            "efficiency[0.9,0.7,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusCMSbeta0p2 = cms.vstring(
            "Voigtian::signal1(mass, mean1[3.1,3.0,3.2], width[0.1], sigma1[0.005, 0.002, 0.01])".replace("mass",mass_),
            "Voigtian::signal2(mass, mean2[3.1,3.0,3.2], width[0.1], sigma2[0.001, 0.0005, 0.004])".replace("mass",mass_),
            "RooCMSShape::backgroundPass(mass, alphaPass[2.,1.,3.], betaPass[0.001, 0.,0.1], gammaPass[0.001, 0.,0.1], peakPass[3.0])".replace("mass",mass_),
            "RooCMSShape::backgroundFail(mass, alphaFail[2.,1.,3.], betaFail[0.03, 0.02,0.1], gammaFail[0.001, 0.,0.1], peakPass)".replace("mass",mass_),
            #"RooCMSShape::backgroundPass(mass, alphaPass[70.,60.,90.], betaPass[0.001, 0.01,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])".replace("mass",mass_),
            #"RooCMSShape::backgroundFail(mass, alphaFail[70.,60.,90.], betaFail[0.001, 0.01,0.1], gammaFail[0.001, 0.,0.1], peakPass)".replace("mass",mass_),
            "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
            "efficiency[0.9,0.7,1]",
            "signalFractionInPassing[0.9]"
        ),
        gaussPlusExpo = cms.vstring(
            #"CBShape::signal(mass, mean[3.1,3.0,3.2], sigma[0.05,0.02,0.06], alpha[3., 0.5, 5.], n[1, 0.1, 100.])",
            #"Chebychev::backgroundPass(mass, {cPass[0,-0.5,0.5], cPass2[0,-0.5,0.5]})",
            #"Chebychev::backgroundFail(mass, {cFail[0,-0.5,0.5], cFail2[0,-0.5,0.5]})",
            "Gaussian::signal(mass, mean[3.1,3.0,3.2], sigma[0.05,0.02,0.1])",
            "Exponential::backgroundPass(mass, lp[0,-5,5])",
            "Exponential::backgroundFail(mass, lf[0,-5,5])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
        CBPlusExpo = cms.vstring(
            "CBShape::signal(mass, mean[3.1,3.0,3.2], sigma[0.05,0.02,0.06], alpha[3., 0.5, 5.], n[1, 0.1, 100.])",
            #"Chebychev::backgroundPass(mass, {cPass[0,-0.5,0.5], cPass2[0,-0.5,0.5]})",
            #"Chebychev::backgroundFail(mass, {cFail[0,-0.5,0.5], cFail2[0,-0.5,0.5]})",
            #"Gaussian::signal(mass, mean[3.1,3.0,3.2], sigma[0.05,0.02,0.1])",
            "Exponential::backgroundPass(mass, lp[0,-5,5])",
            "Exponential::backgroundFail(mass, lf[0,-5,5])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        )
    ),

    binnedFit = cms.bool(True),
    binsForFit = cms.uint32(40),
    saveDistributionsPlot = cms.bool(False),
    Efficiencies = cms.PSet(), # will be filled later
)
#End Template

if sample == "data_J_Psi":
    process.TnP_MuonID = Template.clone(
        InputFileNames = cms.vstring(
            'tnpJPsi_Data_Run2016.root',
            ),
        InputTreeName = cms.string("fitter_tree"),
        InputDirectoryName = cms.string("tpTree"),
        OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
        Efficiencies = cms.PSet(),
        )

if sample == "mc_J_Psi":
    process.TnP_MuonID = Template.clone(
        InputFileNames = cms.vstring(
            'tnp_withNVtxWeights.root',
            ),
        InputTreeName = cms.string("fitter_tree"),
        InputDirectoryName = cms.string("tpTree"),
        OutputFileName = cms.string("TnP_MuonID_%s.root" % scenario),
        Efficiencies = cms.PSet(),
        )

if scenario == "mc_all":
    print "Including the weight for MC"
    process.TnP_MuonID.WeightVariable = cms.string("weight")
    process.TnP_MuonID.Variables.weight = cms.vstring("weight","0","20","")

#flag for trigger match
BIN = cms.PSet(
    tag_Mu7p5_Track7_Jpsi_MU = cms.vstring("pass"),
    Mu7p5_Track7_Jpsi_TK = cms.vstring("pass")
        )

print 'Creating dictionary...'
#This is just for naming file use
Num_dic = {'looseid':'LooseID','mediumid':'MediumID','tightid':'TightID','highptid':'HighPtID','looseiso':'LooseRelIso','tightiso':'TightRelIso','tklooseiso':'LooseRelTkIso'}
Den_dic = {'gentrack':'genTracks','looseid':'LooseID','mediumid':'MediumID','tightid':'TightIDandIPCut','highptid':'HighPtIDandIPCut'}
#This need to be same as the variable name in the Tree or defined probe parameters
Sel_dic = {'looseid':'Loose_Muon','mediumid':'Medium2016_noIP','tightid':'Tight2012_zIPCut','highptid':'HighPt_zIPCut','looseiso':'LooseIso4','tightiso':'TightIso4','tklooseiso':'LooseTkIso3'}

#Par_dic = {'eta':'eta', 'pt':}

FillVariables(par)
FillNumDen(num,den)

#process.TnP_MuonID.Categories = cms.PSet(
#    PF  = cms.vstring("PF Muon", "dummy[pass=1,fail=0]")
#    )
#process.TnP_MuonID.Expressions = cms.PSet(
#    Loose_noIPVar  = cms.vstring("Loose_noIPVar", "PF==1", "PF")
#    )
#process.TnP_MuonID.Cuts = cms.PSet(
#    Loose_noIP = cms.vstring("Loose_noIP", "Loose_noIPVar", "0.5")
#    )

#process.TnP_MuonID.Categories.PF  = cms.vstring("PF Muon", "dummy[pass=1,fail=0]")
#process.TnP_MuonID.Expressions.Loose_noIPVar  = cms.vstring("Loose_noIPVar", "PF==1", "PF")
#process.TnP_MuonID.Cuts.Loose_noIP = cms.vstring("Loose_noIP", "Loose_noIPVar", "0.5")
    
   

#Template.Categories.PF  = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),
#Template.Expression.Loose_noIPVar  = cms.vstring("Loose_noIPVar", "PF==1", "PF")
#Template.Cuts.Loose_noIP = cms.vstring("Loose_noIP", "Loose_noIPVar", "0.5")

print 'den is', den,'dic',Den_dic[den]
print 'num is', num,'dic',Num_dic[num]
print 'par is', par

ID_BINS = [(Sel_dic[num],("NUM_%s_DEN_%s_PAR_%s"%(Num_dic[num],Den_dic[den],par),BIN))]
print 'Dictionary mapped.'

print Sel_dic[num]
print ("NUM_%s_DEN_%s_PAR_%s"%(Num_dic[num],Den_dic[den],par),BIN)

#_*_*_*_*_*_*_*_*_*_*_*
#Launch fit production
#_*_*_*_*_*_*_*_*_*_*_*

for ID, ALLBINS in ID_BINS:
    print 'Launch fit production...'
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
    module = process.TnP_MuonID.clone(OutputFileName = cms.string(_output + "/TnP_%s.root" % (X)))
    #save the fitconfig in the plot directory
    shutil.copyfile(os.getcwd()+'/fitMuon.py',_output+'/fitMuon.py')
    #default signal shape
    shape = cms.vstring("CBPlusExpo")
    print 'Saving the fit config in the plot directory...'



    DEN = B.clone(); num_ = ID;
    FillBin(par)
    print 'X is', X
    print 'B is', B
    print 'num_ is', num_

    #customize only for ID
    if not "iso" in num: 
        print 'Customize only for ID...'
        if bgFitFunction == 'default':
            print 'Input background fit function is default...'
            if ('pt' in X):
                print 'den is', den 
                print 'num is ', num
                if den == "highptid" or num == "highptid":
                    if (len(DEN.pair_newTuneP_probe_pt)==11):
                        #first string is the default followed by binRegExp - PDFname pair
                        shape = cms.vstring("vpvPlusCMS","*pt_bin3*","vpvPlusCMSbeta0p2","*pt_bin4*","vpvPlusCMSbeta0p2","*pt_bin5*","vpvPlusCMSbeta0p2","*pt_bin6*","vpvPlusCMSbeta0p2","*pt_bin7*","vpvPlusCMS")
                    if (len(DEN.pair_newTuneP_probe_pt)==8):
                        shape = cms.vstring("vpvPlusCMS","*pt_bin3*","vpvPlusCMSbeta0p2","*pt_bin4*","vpvPlusCMSbeta0p2","*pt_bin5*","vpvPlusCMSbeta0p2","*pt_bin6*","vpvPlusCMSbeta0p2")
                else:
                    #Select fit function for signal and bkg
                    print 'Low pT...'
                    if (len(DEN.pt)==18):
                        print 'len of DEN.pt is 18, assign fit function for all pT bins...'
                        print 'DEN.pt is', DEN.pt
                        shape = cms.vstring("CBPlusExpo")
                    if (len(DEN.pt)==7):
                        print 'len of DEN.pt is 7'
                        print 'DEN.pt is', DEN.pt
                        shape = cms.vstring("vpvPlusCMS","*pt_bin3*","vpvPlusCMSbeta0p2","*pt_bin4*","vpvPlusCMSbeta0p2","*pt_bin5*","vpvPlusCMSbeta0p2")
        elif bgFitFunction == 'CMSshape':
            print 'Input background fit function is CMSshape...'
            if den == "highpt":
                if (len(DEN.pair_newTuneP_probe_pt)==9):
                    shape = cms.vstring("vpvPlusExpo","*pt_bin4*","vpvPlusCMS","*pt_bin5*","vpvPlusCMS","*pt_bin6*","vpvPlusCheb","*pt_bin7*","vpvPlusCheb")
            else:
                if (len(DEN.pt)==8):
                    shape = cms.vstring("vpvPlusExpo","*pt_bin4*","vpvPlusCMS","*pt_bin5*","vpvPlusCheb","*pt_bin6*","vpvPlusCheb")

    print 'Background shape determined...'
    print 'Computing isolation efficiency...'
    mass_variable ="mass"
    print 'Denominator is', den
    if den == "highptid" :
        mass_variable = "pair_newTuneP_mass"
    #compute isolation efficiency
    ## defines a set of efficiency calculations, what PDF to use for fitting and how to bin the data;
    # there will be a separate output directory for each calculation that includes a simultaneous fit, side band subtraction and counting. 
    if scenario == 'data_all':
        if num_.find("Iso4") != -1 or num_.find("Iso3") != -1:
            print 'muon Isolation...'
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                #specifies the efficiency of which category and state to measure 
                EfficiencyCategoryAndState = cms.vstring(num_,"below"),
                #specifies what unbinned variables to include in the dataset, the mass is needed for the fit
                UnbinnedVariables = cms.vstring(mass_variable),
                #specifies the binning of parameters
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        else:
            print 'muon ID...'
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num_,"above"),
                UnbinnedVariables = cms.vstring(mass_variable),
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        #unspecified binToPDFmap means no fitting
        setattr(process, "TnP_MuonID_"+ID+"_"+X, module)
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))
    elif scenario == 'mc_all':
        if num_.find("Iso4") != -1 or num_.find("Iso3") != -1:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num_,"below"),
                UnbinnedVariables = cms.vstring(mass_variable,"weight"),
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        else:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num_,"above"),
                UnbinnedVariables = cms.vstring(mass_variable,"weight"),
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        setattr(process, "TnP_MuonID_"+ID+"_"+X, module)
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))
