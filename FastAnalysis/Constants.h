//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
//!  Common Constants for BKG Estimation!
//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
//Luminosity each year: unit: fb^-1
const double lumi_2017 = 36.734;
const double lumi_2018 = 59.7;

//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
//!  Constants used exclusively in LowMassBKGFit1D  !
//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
TString pT_cut  = "24";//offline high pT cut for 2018 trigger L2Mu23
TString eta_cut = "2.0";
TString iso_cut = "2.3";//isolation cut for dimu

const double       m_min  = 0.2113;
const double       m_max  = 9.;
const double       m_highmax = 60.;
const unsigned int m_bins = 220;

//Used for excluding the J/psi region when constructing 1D/2D template
const double       m_Jpsi_dn = 2.72;
const double       m_Jpsi_up = 3.24;
const double       m_Upsilon_up = 11.;
const unsigned int m_bins_below_Jpsi = 63;//bin size is ~0.04GeV, as above
const unsigned int m_bins_above_Jpsi = 144;
const unsigned int m_bins_above_Upsilon = 98;//bin size is 0.5GeV
const unsigned int m_bins_all = 300;

// Used for smooth pdf with kernel density:
// for width, AN v4 uses 0.9 (down) and 1.1 (up)
// for sys plot range, AN v4 uses -0.45 (min) and 0.45 (max)
const double       width_scale_dn  = 0.9;
const double       width_scale_up  = 1.1;
const double       shape_unc_plot_min  = -0.45;
const double       shape_unc_plot_max  = 0.45;
//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
//!  Constants used exclusively in LowMassBKGPlot2D !
//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
//number of toys used for calibration
int ntoys = 1000000;

//Y axis max in validation plots SetRangeUser: normally don't need to change
const double validate_m1_iso_Ymax_2017    = 35.;
const double validate_m2_iso_Ymax_2017    = 10.;
const double validate_m1_iso_Ymax_2018    = 25.;
const double validate_m2_iso_Ymax_2018    = 20.;

//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
//!  Constants used exclusively in HighMassBKGShape.C  !
//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
//Mass range and bin size at high mass
const double       HM_m_min  = 11.0;
const double       HM_m_max  = 60.0;
const unsigned int HM_m_bins = 14; // bin size 3.5 GeV

const double       HM_Lxy_min  = 0.0;
const double       HM_Lxy_max  = 16.0;
const unsigned int HM_Lxy_bins = 16; // bin size 1 cm

//Directory of histograms
TString store_2017 = "/scratch/user/ws13/SMBKGatHighMass/2017";
TString store_2018 = "/scratch/user/ws13/SMBKGatHighMass/2018/Cut2Segs_FINAL";

//Scale MC events to Data (Xsec*Lumi/tot MC evt), not including SF like trigger, muon id etc
//The order is important here: DY 0J, 1J, 2J, ZZTo4L, TTJets_DiLept, ggHToZZTo4L, ggToZZTo4mu
Float_t MC_ScaleFactors_2017[7] = {2.2149318E+00, 3.7806072E-01, 2.5133039E-01, 3.0278414E-03, 7.0425976E-02, 4.6355268E-04, 6.3245328E-05};
Float_t MC_ScaleFactors_2018[7] = {3.4145686E+00, 6.2974242E-01, 3.5720940E-01, 4.1624890E-03, 1.0998854E-01, 7.6245783E-04, 1.1110732E-04};

Float_t CR_Data_MC_SF_2018 = 1.05; // 1.05+/-0.12

//Color in final legend for each bkg process, same order as above
Color_t MC_Colors[7] = {20, 30, 40, 9, 8, 7, 6};

//The input files below contain histograms from running the cut-flow script (with ModelBKGShape flag on) over each background ntuples
//script: MuJetAnalysis/CutFlowAnalyzer/scripts/cutflow_macros/CutFlow_2018L2Mu23.C
//run command: echo 'gROOT->ProcessLine(".L CutFlow_2018L2Mu23.C++"); analysis("BKGsList*.txt" )' | root -l -b
//Same order as MC_ScaleFactors above
TString MC_files_2017[7] = {
  "CutFlowPlots_2017_DYToLL_0J.root",
  "CutFlowPlots_2017_DYToLL_1J.root",
  "CutFlowPlots_2017_DYToLL_2J.root",
  "CutFlowPlots_2017_ZZTo4L.root",
  "CutFlowPlots_2017_TTJets_DiLept.root",
  "CutFlowPlots_2017_ggHToZZTo4L.root",
  "CutFlowPlots_2017_ggToZZTo4mu.root"
};
TString DATA_files_2017[1] = {
  "CutFlowPlots_2017DoubleMuon_ABCD.root"
};

TString MC_files_2018[7] = {
  "CutFlowPlots_2018_DYToLL_0J.root",
  "CutFlowPlots_2018_DYToLL_1J.root",
  "CutFlowPlots_2018_DYToLL_2J.root",
  "CutFlowPlots_2018_ZZTo4L.root",
  "CutFlowPlots_2018_TTJets_DiLept.root",
  "CutFlowPlots_2018_ggHToZZTo4L.root",
  "CutFlowPlots_2018_ggToZZTo4mu.root"
};
//DoubleMuon dataset
TString DATA_files_2018[1] = {
  "CutFlowPlots_2018DoubleMuon_ABCD.root"
};
