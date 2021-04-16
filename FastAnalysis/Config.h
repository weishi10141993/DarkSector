#include <iostream>
#include <fstream>
#include <algorithm>    // std::max
#include <stdlib.h>
#include <iomanip>
#include "TSystemDirectory.h"

//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
//!  USER Configure Below        !
//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

const int year = 2018;//Configure which year ntuples to run, options: 2017, 2018

//CB fitted mean mass [GeV] for prompt signals
double mean[11] = {0.2560, 0.4012, 0.7003, 1.0000, 1.9990, 4.9980, 8.4920, 14.990, 24.980, 34.970, 57.930};

//80% signal eff needed mass window size for prompt signals
//double window[11] = {0.030922364, 0.0201698988, 0.02337757474, 0.0275968, 0.04615657165, 0.124742502, 0.2110350916, 0.3849085576, 0.67586519, 0.914118934, 1.860449598};

//85% signal eff needed mass window size for prompt signals
//double window[11] = {0.0359823872, 0.0252123735, 0.02787326219, 0.0326656, 0.056518251, 0.1538490858, 0.2586881768, 0.46940068, 0.849659096, 1.102319891, 2.524895883};

//90% signal eff needed mass window size from above prompt signals
double window[11] = {0.0438535344, 0.0336164980, 0.0359654996, 0.0428032000, 0.0753576680, 0.2037460866, 0.3539943472, 0.7041010200, 1.1972469080, 1.6131510600, 3.9866777100};

//95% signal eff needed mass window size for prompt signals
//double window[11] = {0.0629691776, 0.05176940692, 0.05574652438, 0.0664576, 0.1224562105, 0.3617532558, 0.748834196, 1.40820204, 2.70346076, 2.6885851, 9.523730085};

//Background pdf for high mass: Interpolation between consective bins
double MCBinCenterMass[14] = {12.75, 16.25, 19.75, 23.25, 26.75, 30.25, 33.75, 37.25, 40.75, 44.25, 47.75, 51.25, 54.75, 58.25};

double MCBinContentm1[14] = {0.0260007, 0.070103, 0.457687, 0.161783, 0.157428, 0.62272, 0.599198, 0.887516, 1.56432, 2.07059, 0.707749, 1.12067, 2.29358, 0.954618};
double MCBinErrm1[14] = {0.00764504, 0.0148186, 0.357686, 0.0232653, 0.0228677, 0.160303, 0.117906, 0.195744, 0.530653, 0.765715, 0.117726, 0.224549, 0.773769, 0.375918};

double MCBinContentm2[14] = {0.0263188, 0.0750433, 0.462819, 0.149645, 0.17395, 0.482848, 0.851617, 0.792001, 1.40641, 2.22213, 0.8121, 1.09374, 1.93753, 1.20782};
double MCBinErrm2[14] = {0.00767975, 0.0153949, 0.357711, 0.0224435, 0.0240383, 0.116155, 0.195536, 0.162129, 0.518903, 0.773695, 0.16106, 0.224314, 0.563703, 0.640463};

//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
//!  USER Configure Above        !
//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
//!  Initialize variables for macros  !
//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Float_t luminosity;//Luminosity of a year
TString headertpl = "";//header of template 1D
TString headerfit = "";//header of fit low mass
TString headertpl2 = "";//header of template 2D
TString headervld = "";//header of template validation plots
TString header1 = "";//header of CR plots with pulls
TString header = "";//header of SR plots without pulls

TString inputFile1;//Run 2 data Ntuples used for HighMassBKGABCD and LowMassBKGFit1D
TString outFileLM = "";//output file of LowMassBKGFit1D, will also be used in limit calculation
TString inputFile2;//input workSpace file to LowMassBKGPlot2D, that's also the output file of LowMassBKGFit1D

//Run 2 BKG Ntuples used for kernel density estimation in LowMassBKGFit1D
TString DY1JFile;
TString DY2JFile;
TString qqToZZFile;
TString TTJetsFile;
TString ggHToZZFile;
TString ggToZZFile;

Float_t validate_m1_iso_Ymax;//Max y in validation plots
Float_t validate_m2_iso_Ymax;
Float_t CR_Data_MC_SF; // data-MC scale factor from CR, need to apply to SR MC

TString store;//Input directory for HighMassBKGShape
TString outFileHMShape = "";//output file of HighMassBKGShape
Float_t MC_ScaleFactors[7];//MC-Data SF for HighMassBKGShape
TString MC_files[7];//Input MC shape for HighMassBKGShape
TString DATA_files[1];//Input DATA shape for HighMassBKGShape

TString outFileHMABCD = "";//output file of HighMassBKGABCD

namespace BKG_cfg {

  inline void ConfigureInput( const int year ) {

    std::cout << "\nConfiguring inputs for year " << year << std::endl;

    if (year == 2017) {
      luminosity = lumi_2017;
      inputFile1 = "Input_2017CDEF_2SAmu_NoVtxProbCut.txt";
      inputFile2 = "ws_2017_FINAL.root";
      store      = store_2017;
      validate_m1_iso_Ymax    = validate_m1_iso_Ymax_2017;
      validate_m2_iso_Ymax    = validate_m2_iso_Ymax_2017;
      for(int i = 0; i < 7; i++){
        MC_ScaleFactors[i] = MC_ScaleFactors_2017[i];
        MC_files[i]        = MC_files_2017[i];
      }
      for(int j = 0; j < 1; j++){
        DATA_files[j] = DATA_files_2017[j];
      }
    }//end 2017
    else if (year == 2018) {
      luminosity = lumi_2018;
      inputFile1 = "Input_2018ABCD_2SAmu_NoVtxProbCut_4HLT.txt";
      inputFile2 = "ws_2018_FINAL.root";
      store      = store_2018;
      validate_m1_iso_Ymax    = validate_m1_iso_Ymax_2018;
      validate_m2_iso_Ymax    = validate_m2_iso_Ymax_2018;
      CR_Data_MC_SF = CR_Data_MC_SF_2018;
      for(int i = 0; i < 7; i++){
        MC_ScaleFactors[i] = MC_ScaleFactors_2018[i];
        MC_files[i]        = MC_files_2018[i];
      }
      for(int j = 0; j < 1; j++){
        DATA_files[j] = DATA_files_2018[j];
      }
      DY1JFile    = "Input_2018_DY1J_MC.txt";
      DY2JFile    = "Input_2018_DY2J_MC.txt";
      qqToZZFile  = "Input_2018_qqToZZ_MC.txt";
      TTJetsFile  = "Input_2018_TTJets_MC.txt";
      ggHToZZFile = "Input_2018_ggHToZZ_MC.txt";
      ggToZZFile  = "Input_2018_ggToZZ_MC.txt";
    }//end 2018
    else{
      std::cout << "*** User input year is unknown! Please check. ***" << std::endl;
    }

    //for low mass data 1D template
    headertpl      = headertpl + "#bf{CMS} #it{Preliminary}             " + Form("%.1f", luminosity) + "fb^{-1} (13 TeV)";
    //for low mass fit overlay data
    headerfit      = headerfit + "#bf{CMS} #it{Preliminary}                                             " + Form("%.1f", luminosity) + "fb^{-1} (13 TeV)";
    //for low mass data 2D template
    headertpl2     = headertpl2 + "#bf{CMS} #it{Preliminary}              " + Form("%.1f", luminosity) + "fb^{-1} (13 TeV)";
    //for low mass data 2D template validation
    headervld      = headervld + "#bf{CMS} #it{Preliminary}             " + Form("%.1f", luminosity) + "fb^{-1} (13 TeV)";
    //For high mass CR with lower panel
    header1        = header1 + "#bf{CMS} #it{Preliminary}                                                                                       " + Form("%.1f", luminosity) + "fb^{-1} (13 TeV)";
    //For high mass SR without lower panel
    header         = header +    "#bf{CMS} #it{Preliminary}                                             " + Form("%.1f", luminosity) + "fb^{-1} (13 TeV)";
    outFileLM      = outFileLM + "ws_" + Form("%d", year) + "_FINAL.root";
    outFileHMABCD  = outFileHMABCD + "ABCD_" + Form("%d", year) + "_FINAL.root";
    outFileHMShape = outFileHMShape + "HighMassBKGShape_" + Form("%d", year) + "_FINAL.root";

  } // End ConfigureInput function

  double My_MassWindow(double m1, double m2) {
    //return this mass window size given m1 and m2
    double mysize = 0.0;

    //Interpolation by drawing staight line, we use (m1+m2)/2 here
    //mass window size = y1 + (x-x1)*(y2-y1)/(x2-x1), x = (m1+m2)/2
    //Start and end with 0.2113 and 60GeV to match bkg analysis
    if ( (m1+m2)/2 >= 0.2113   && (m1+m2)/2 < mean[1] ) mysize = window[0] + ( (m1+m2)/2 - mean[0] )*( window[1]  - window[0] )/( mean[1]  - mean[0] );
    if ( (m1+m2)/2 >= mean[1]  && (m1+m2)/2 < mean[2] ) mysize = window[1] + ( (m1+m2)/2 - mean[1] )*( window[2]  - window[1] )/( mean[2]  - mean[1] );
    if ( (m1+m2)/2 >= mean[2]  && (m1+m2)/2 < mean[3] ) mysize = window[2] + ( (m1+m2)/2 - mean[2] )*( window[3]  - window[2] )/( mean[3]  - mean[2] );
    if ( (m1+m2)/2 >= mean[3]  && (m1+m2)/2 < mean[4] ) mysize = window[3] + ( (m1+m2)/2 - mean[3] )*( window[4]  - window[3] )/( mean[4]  - mean[3] );
    if ( (m1+m2)/2 >= mean[4]  && (m1+m2)/2 < mean[5] ) mysize = window[4] + ( (m1+m2)/2 - mean[4] )*( window[5]  - window[4] )/( mean[5]  - mean[4] );
    if ( (m1+m2)/2 >= mean[5]  && (m1+m2)/2 < mean[6] ) mysize = window[5] + ( (m1+m2)/2 - mean[5] )*( window[6]  - window[5] )/( mean[6]  - mean[5] );
    if ( (m1+m2)/2 >= mean[6]  && (m1+m2)/2 < mean[7] ) mysize = window[6] + ( (m1+m2)/2 - mean[6] )*( window[7]  - window[6] )/( mean[7]  - mean[6] );
    if ( (m1+m2)/2 >= mean[7]  && (m1+m2)/2 < mean[8] ) mysize = window[7] + ( (m1+m2)/2 - mean[7] )*( window[8]  - window[7] )/( mean[8]  - mean[7] );
    if ( (m1+m2)/2 >= mean[8]  && (m1+m2)/2 < mean[9] ) mysize = window[8] + ( (m1+m2)/2 - mean[8] )*( window[9]  - window[8] )/( mean[9]  - mean[8] );
    if ( (m1+m2)/2 >= mean[9]  && (m1+m2)/2 < 60.000  ) mysize = window[9] + ( (m1+m2)/2 - mean[9] )*( window[10] - window[9] )/( mean[10] - mean[9] );

    return mysize;
  }

  //BKG Shape above 11GeV
  double My_BKGShapem1(double m1) {
    //return this mass window size given m1
    double mybkg = 0.0;

    //Interpolation by drawing staight line, we use (m1+m2)/2 here
    //mass window size = y1 + (x-x1)*(y2-y1)/(x2-x1), x = (m1+m2)/2
    //Start and end with 11 and 60GeV to match bkg analysis
    //ATTENTION: simple interpolation is negative at 11 and 60 boundaries, use flat profile of bin content for the first half bin and the last half bin
    if ( m1 >= 11.000              && m1 < MCBinCenterMass[0] )   mybkg = MCBinContentm1[0];//use flat profile of bin content for the first half bin
    if ( m1 >= MCBinCenterMass[0]  && m1 < MCBinCenterMass[1] )   mybkg = MCBinContentm1[0]  + ( m1 - MCBinCenterMass[0] )*( MCBinContentm1[1] - MCBinContentm1[0] )/( MCBinCenterMass[1] - MCBinCenterMass[0] );
    if ( m1 >= MCBinCenterMass[1]  && m1 < MCBinCenterMass[2] )   mybkg = MCBinContentm1[1]  + ( m1 - MCBinCenterMass[1] )*( MCBinContentm1[2] - MCBinContentm1[1] )/( MCBinCenterMass[2] - MCBinCenterMass[1] );
    if ( m1 >= MCBinCenterMass[2]  && m1 < MCBinCenterMass[3] )   mybkg = MCBinContentm1[2]  + ( m1 - MCBinCenterMass[2] )*( MCBinContentm1[3] - MCBinContentm1[2] )/( MCBinCenterMass[3] - MCBinCenterMass[2] );
    if ( m1 >= MCBinCenterMass[3]  && m1 < MCBinCenterMass[4] )   mybkg = MCBinContentm1[3]  + ( m1 - MCBinCenterMass[3] )*( MCBinContentm1[4] - MCBinContentm1[3] )/( MCBinCenterMass[4] - MCBinCenterMass[3] );
    if ( m1 >= MCBinCenterMass[4]  && m1 < MCBinCenterMass[5] )   mybkg = MCBinContentm1[4]  + ( m1 - MCBinCenterMass[4] )*( MCBinContentm1[5] - MCBinContentm1[4] )/( MCBinCenterMass[5] - MCBinCenterMass[4] );
    if ( m1 >= MCBinCenterMass[5]  && m1 < MCBinCenterMass[6] )   mybkg = MCBinContentm1[5]  + ( m1 - MCBinCenterMass[5] )*( MCBinContentm1[6] - MCBinContentm1[5] )/( MCBinCenterMass[6] - MCBinCenterMass[5] );
    if ( m1 >= MCBinCenterMass[6]  && m1 < MCBinCenterMass[7] )   mybkg = MCBinContentm1[6]  + ( m1 - MCBinCenterMass[6] )*( MCBinContentm1[7] - MCBinContentm1[6] )/( MCBinCenterMass[7] - MCBinCenterMass[6] );
    if ( m1 >= MCBinCenterMass[7]  && m1 < MCBinCenterMass[8] )   mybkg = MCBinContentm1[7]  + ( m1 - MCBinCenterMass[7] )*( MCBinContentm1[8] - MCBinContentm1[7] )/( MCBinCenterMass[8] - MCBinCenterMass[7] );
    if ( m1 >= MCBinCenterMass[8]  && m1 < MCBinCenterMass[9] )   mybkg = MCBinContentm1[8]  + ( m1 - MCBinCenterMass[8] )*( MCBinContentm1[9] - MCBinContentm1[8] )/( MCBinCenterMass[9] - MCBinCenterMass[8] );
    if ( m1 >= MCBinCenterMass[9]  && m1 < MCBinCenterMass[10]  ) mybkg = MCBinContentm1[9]  + ( m1 - MCBinCenterMass[9] )*( MCBinContentm1[10] - MCBinContentm1[9] )/( MCBinCenterMass[10] - MCBinCenterMass[9] );
    if ( m1 >= MCBinCenterMass[10]  && m1 < MCBinCenterMass[11] ) mybkg = MCBinContentm1[10] + ( m1 - MCBinCenterMass[10] )*( MCBinContentm1[11] - MCBinContentm1[10] )/( MCBinCenterMass[11] - MCBinCenterMass[10] );
    if ( m1 >= MCBinCenterMass[11]  && m1 < MCBinCenterMass[12] ) mybkg = MCBinContentm1[11] + ( m1 - MCBinCenterMass[11] )*( MCBinContentm1[12] - MCBinContentm1[11] )/( MCBinCenterMass[12] - MCBinCenterMass[11] );
    if ( m1 >= MCBinCenterMass[12]  && m1 < MCBinCenterMass[13] ) mybkg = MCBinContentm1[12] + ( m1 - MCBinCenterMass[12] )*( MCBinContentm1[13] - MCBinContentm1[12] )/( MCBinCenterMass[13] - MCBinCenterMass[12] );
    if ( m1 >= MCBinCenterMass[13]  && m1 <= 60.000             ) mybkg = MCBinContentm1[13];//use flat profile of bin content for the last half bin

    return mybkg;
  }

  double My_BKGShapem1SigmaUp(double m1) {
    double mybkg = 0.0;

    if ( m1 >= 11.000              && m1 < MCBinCenterMass[0] )   mybkg = MCBinContentm1[0] + MCBinErrm1[0];
    if ( m1 >= MCBinCenterMass[0]  && m1 < MCBinCenterMass[1] )   mybkg = MCBinContentm1[0] + MCBinErrm1[0] + ( m1 - MCBinCenterMass[0] )*( MCBinContentm1[1] + MCBinErrm1[1] - MCBinContentm1[0] - MCBinErrm1[0] )/( MCBinCenterMass[1] - MCBinCenterMass[0] );
    if ( m1 >= MCBinCenterMass[1]  && m1 < MCBinCenterMass[2] )   mybkg = MCBinContentm1[1] + MCBinErrm1[1] + ( m1 - MCBinCenterMass[1] )*( MCBinContentm1[2] + MCBinErrm1[2] - MCBinContentm1[1] - MCBinErrm1[1] )/( MCBinCenterMass[2] - MCBinCenterMass[1] );
    if ( m1 >= MCBinCenterMass[2]  && m1 < MCBinCenterMass[3] )   mybkg = MCBinContentm1[2] + MCBinErrm1[2] + ( m1 - MCBinCenterMass[2] )*( MCBinContentm1[3] + MCBinErrm1[3] - MCBinContentm1[2] - MCBinErrm1[2] )/( MCBinCenterMass[3] - MCBinCenterMass[2] );
    if ( m1 >= MCBinCenterMass[3]  && m1 < MCBinCenterMass[4] )   mybkg = MCBinContentm1[3] + MCBinErrm1[3] + ( m1 - MCBinCenterMass[3] )*( MCBinContentm1[4] + MCBinErrm1[4] - MCBinContentm1[3] - MCBinErrm1[3] )/( MCBinCenterMass[4] - MCBinCenterMass[3] );
    if ( m1 >= MCBinCenterMass[4]  && m1 < MCBinCenterMass[5] )   mybkg = MCBinContentm1[4] + MCBinErrm1[4] + ( m1 - MCBinCenterMass[4] )*( MCBinContentm1[5] + MCBinErrm1[5] - MCBinContentm1[4] - MCBinErrm1[4] )/( MCBinCenterMass[5] - MCBinCenterMass[4] );
    if ( m1 >= MCBinCenterMass[5]  && m1 < MCBinCenterMass[6] )   mybkg = MCBinContentm1[5] + MCBinErrm1[5] + ( m1 - MCBinCenterMass[5] )*( MCBinContentm1[6] + MCBinErrm1[6] - MCBinContentm1[5] - MCBinErrm1[5] )/( MCBinCenterMass[6] - MCBinCenterMass[5] );
    if ( m1 >= MCBinCenterMass[6]  && m1 < MCBinCenterMass[7] )   mybkg = MCBinContentm1[6] + MCBinErrm1[6] + ( m1 - MCBinCenterMass[6] )*( MCBinContentm1[7] + MCBinErrm1[7] - MCBinContentm1[6] - MCBinErrm1[6] )/( MCBinCenterMass[7] - MCBinCenterMass[6] );
    if ( m1 >= MCBinCenterMass[7]  && m1 < MCBinCenterMass[8] )   mybkg = MCBinContentm1[7] + MCBinErrm1[7] + ( m1 - MCBinCenterMass[7] )*( MCBinContentm1[8] + MCBinErrm1[8] - MCBinContentm1[7] - MCBinErrm1[7] )/( MCBinCenterMass[8] - MCBinCenterMass[7] );
    if ( m1 >= MCBinCenterMass[8]  && m1 < MCBinCenterMass[9] )   mybkg = MCBinContentm1[8] + MCBinErrm1[8] + ( m1 - MCBinCenterMass[8] )*( MCBinContentm1[9] + MCBinErrm1[9] - MCBinContentm1[8] - MCBinErrm1[8] )/( MCBinCenterMass[9] - MCBinCenterMass[8] );
    if ( m1 >= MCBinCenterMass[9]  && m1 < MCBinCenterMass[10]  ) mybkg = MCBinContentm1[9] + MCBinErrm1[9] + ( m1 - MCBinCenterMass[9] )*( MCBinContentm1[10] + MCBinErrm1[10] - MCBinContentm1[9] - MCBinErrm1[9] )/( MCBinCenterMass[10] - MCBinCenterMass[9] );
    if ( m1 >= MCBinCenterMass[10]  && m1 < MCBinCenterMass[11] ) mybkg = MCBinContentm1[10] + MCBinErrm1[10] + ( m1 - MCBinCenterMass[10] )*( MCBinContentm1[11] + MCBinErrm1[11] - MCBinContentm1[10] - MCBinErrm1[10] )/( MCBinCenterMass[11] - MCBinCenterMass[10] );
    if ( m1 >= MCBinCenterMass[11]  && m1 < MCBinCenterMass[12] ) mybkg = MCBinContentm1[11] + MCBinErrm1[11] + ( m1 - MCBinCenterMass[11] )*( MCBinContentm1[12] + MCBinErrm1[12] - MCBinContentm1[11] - MCBinErrm1[11] )/( MCBinCenterMass[12] - MCBinCenterMass[11] );
    if ( m1 >= MCBinCenterMass[12]  && m1 < MCBinCenterMass[13] ) mybkg = MCBinContentm1[12] + MCBinErrm1[12] + ( m1 - MCBinCenterMass[12] )*( MCBinContentm1[13] + MCBinErrm1[13] - MCBinContentm1[12] - MCBinErrm1[12] )/( MCBinCenterMass[13] - MCBinCenterMass[12] );
    if ( m1 >= MCBinCenterMass[13]  && m1 <= 60.000             ) mybkg = MCBinContentm1[13] + MCBinErrm1[13];

    return mybkg;
  }

  double My_BKGShapem1SigmaDn(double m1) {
    double mybkg = 0.0;

    if ( m1 >= 11.000              && m1 < MCBinCenterMass[0] )   mybkg = MCBinContentm1[0] - MCBinErrm1[0];
    if ( m1 >= MCBinCenterMass[0]  && m1 < MCBinCenterMass[1] )   mybkg = MCBinContentm1[0] - MCBinErrm1[0] + ( m1 - MCBinCenterMass[0] )*( MCBinContentm1[1] - MCBinErrm1[1] - MCBinContentm1[0] + MCBinErrm1[0] )/( MCBinCenterMass[1] - MCBinCenterMass[0] );
    if ( m1 >= MCBinCenterMass[1]  && m1 < MCBinCenterMass[2] )   mybkg = MCBinContentm1[1] - MCBinErrm1[1] + ( m1 - MCBinCenterMass[1] )*( MCBinContentm1[2] - MCBinErrm1[2] - MCBinContentm1[1] + MCBinErrm1[1] )/( MCBinCenterMass[2] - MCBinCenterMass[1] );
    if ( m1 >= MCBinCenterMass[2]  && m1 < MCBinCenterMass[3] )   mybkg = MCBinContentm1[2] - MCBinErrm1[2] + ( m1 - MCBinCenterMass[2] )*( MCBinContentm1[3] - MCBinErrm1[3] - MCBinContentm1[2] + MCBinErrm1[2] )/( MCBinCenterMass[3] - MCBinCenterMass[2] );
    if ( m1 >= MCBinCenterMass[3]  && m1 < MCBinCenterMass[4] )   mybkg = MCBinContentm1[3] - MCBinErrm1[3] + ( m1 - MCBinCenterMass[3] )*( MCBinContentm1[4] - MCBinErrm1[4] - MCBinContentm1[3] + MCBinErrm1[3] )/( MCBinCenterMass[4] - MCBinCenterMass[3] );
    if ( m1 >= MCBinCenterMass[4]  && m1 < MCBinCenterMass[5] )   mybkg = MCBinContentm1[4] - MCBinErrm1[4] + ( m1 - MCBinCenterMass[4] )*( MCBinContentm1[5] - MCBinErrm1[5] - MCBinContentm1[4] + MCBinErrm1[4] )/( MCBinCenterMass[5] - MCBinCenterMass[4] );
    if ( m1 >= MCBinCenterMass[5]  && m1 < MCBinCenterMass[6] )   mybkg = MCBinContentm1[5] - MCBinErrm1[5] + ( m1 - MCBinCenterMass[5] )*( MCBinContentm1[6] - MCBinErrm1[6] - MCBinContentm1[5] + MCBinErrm1[5] )/( MCBinCenterMass[6] - MCBinCenterMass[5] );
    if ( m1 >= MCBinCenterMass[6]  && m1 < MCBinCenterMass[7] )   mybkg = MCBinContentm1[6] - MCBinErrm1[6] + ( m1 - MCBinCenterMass[6] )*( MCBinContentm1[7] - MCBinErrm1[7] - MCBinContentm1[6] + MCBinErrm1[6] )/( MCBinCenterMass[7] - MCBinCenterMass[6] );
    if ( m1 >= MCBinCenterMass[7]  && m1 < MCBinCenterMass[8] )   mybkg = MCBinContentm1[7] - MCBinErrm1[7] + ( m1 - MCBinCenterMass[7] )*( MCBinContentm1[8] - MCBinErrm1[8] - MCBinContentm1[7] + MCBinErrm1[7] )/( MCBinCenterMass[8] - MCBinCenterMass[7] );
    if ( m1 >= MCBinCenterMass[8]  && m1 < MCBinCenterMass[9] )   mybkg = MCBinContentm1[8] - MCBinErrm1[8] + ( m1 - MCBinCenterMass[8] )*( MCBinContentm1[9] - MCBinErrm1[9] - MCBinContentm1[8] + MCBinErrm1[8] )/( MCBinCenterMass[9] - MCBinCenterMass[8] );
    if ( m1 >= MCBinCenterMass[9]  && m1 < MCBinCenterMass[10]  ) mybkg = MCBinContentm1[9] - MCBinErrm1[9] + ( m1 - MCBinCenterMass[9] )*( MCBinContentm1[10] - MCBinErrm1[10] - MCBinContentm1[9] + MCBinErrm1[9] )/( MCBinCenterMass[10] - MCBinCenterMass[9] );
    if ( m1 >= MCBinCenterMass[10]  && m1 < MCBinCenterMass[11] ) mybkg = MCBinContentm1[10] - MCBinErrm1[10] + ( m1 - MCBinCenterMass[10] )*( MCBinContentm1[11] - MCBinErrm1[11] - MCBinContentm1[10] + MCBinErrm1[10] )/( MCBinCenterMass[11] - MCBinCenterMass[10] );
    if ( m1 >= MCBinCenterMass[11]  && m1 < MCBinCenterMass[12] ) mybkg = MCBinContentm1[11] - MCBinErrm1[11] + ( m1 - MCBinCenterMass[11] )*( MCBinContentm1[12] - MCBinErrm1[12] - MCBinContentm1[11] + MCBinErrm1[11] )/( MCBinCenterMass[12] - MCBinCenterMass[11] );
    if ( m1 >= MCBinCenterMass[12]  && m1 < MCBinCenterMass[13] ) mybkg = MCBinContentm1[12] - MCBinErrm1[12] + ( m1 - MCBinCenterMass[12] )*( MCBinContentm1[13] - MCBinErrm1[13] - MCBinContentm1[12] + MCBinErrm1[12] )/( MCBinCenterMass[13] - MCBinCenterMass[12] );
    if ( m1 >= MCBinCenterMass[13]  && m1 <= 60.000             ) mybkg = MCBinContentm1[13] - MCBinErrm1[13];

    return mybkg;
  }

  //BraidA starts from +1sigma for the first bin then the -1 sigma for the next, etc
  double My_BKGShapem1SigmaBraidA(double m1) {
    double mybkg = 0.0;

    if ( m1 >= 11.000              && m1 < MCBinCenterMass[0] )   mybkg = MCBinContentm1[0] + MCBinErrm1[0];
    if ( m1 >= MCBinCenterMass[0]  && m1 < MCBinCenterMass[1] )   mybkg = MCBinContentm1[0] + MCBinErrm1[0] + ( m1 - MCBinCenterMass[0] )*( MCBinContentm1[1] - MCBinErrm1[1] - MCBinContentm1[0] - MCBinErrm1[0] )/( MCBinCenterMass[1] - MCBinCenterMass[0] );
    if ( m1 >= MCBinCenterMass[1]  && m1 < MCBinCenterMass[2] )   mybkg = MCBinContentm1[1] - MCBinErrm1[1] + ( m1 - MCBinCenterMass[1] )*( MCBinContentm1[2] + MCBinErrm1[2] - MCBinContentm1[1] + MCBinErrm1[1] )/( MCBinCenterMass[2] - MCBinCenterMass[1] );
    if ( m1 >= MCBinCenterMass[2]  && m1 < MCBinCenterMass[3] )   mybkg = MCBinContentm1[2] + MCBinErrm1[2] + ( m1 - MCBinCenterMass[2] )*( MCBinContentm1[3] - MCBinErrm1[3] - MCBinContentm1[2] - MCBinErrm1[2] )/( MCBinCenterMass[3] - MCBinCenterMass[2] );
    if ( m1 >= MCBinCenterMass[3]  && m1 < MCBinCenterMass[4] )   mybkg = MCBinContentm1[3] - MCBinErrm1[3] + ( m1 - MCBinCenterMass[3] )*( MCBinContentm1[4] + MCBinErrm1[4] - MCBinContentm1[3] + MCBinErrm1[3] )/( MCBinCenterMass[4] - MCBinCenterMass[3] );
    if ( m1 >= MCBinCenterMass[4]  && m1 < MCBinCenterMass[5] )   mybkg = MCBinContentm1[4] + MCBinErrm1[4] + ( m1 - MCBinCenterMass[4] )*( MCBinContentm1[5] - MCBinErrm1[5] - MCBinContentm1[4] - MCBinErrm1[4] )/( MCBinCenterMass[5] - MCBinCenterMass[4] );
    if ( m1 >= MCBinCenterMass[5]  && m1 < MCBinCenterMass[6] )   mybkg = MCBinContentm1[5] - MCBinErrm1[5] + ( m1 - MCBinCenterMass[5] )*( MCBinContentm1[6] + MCBinErrm1[6] - MCBinContentm1[5] + MCBinErrm1[5] )/( MCBinCenterMass[6] - MCBinCenterMass[5] );
    if ( m1 >= MCBinCenterMass[6]  && m1 < MCBinCenterMass[7] )   mybkg = MCBinContentm1[6] + MCBinErrm1[6] + ( m1 - MCBinCenterMass[6] )*( MCBinContentm1[7] - MCBinErrm1[7] - MCBinContentm1[6] - MCBinErrm1[6] )/( MCBinCenterMass[7] - MCBinCenterMass[6] );
    if ( m1 >= MCBinCenterMass[7]  && m1 < MCBinCenterMass[8] )   mybkg = MCBinContentm1[7] - MCBinErrm1[7] + ( m1 - MCBinCenterMass[7] )*( MCBinContentm1[8] + MCBinErrm1[8] - MCBinContentm1[7] + MCBinErrm1[7] )/( MCBinCenterMass[8] - MCBinCenterMass[7] );
    if ( m1 >= MCBinCenterMass[8]  && m1 < MCBinCenterMass[9] )   mybkg = MCBinContentm1[8] + MCBinErrm1[8] + ( m1 - MCBinCenterMass[8] )*( MCBinContentm1[9] - MCBinErrm1[9] - MCBinContentm1[8] - MCBinErrm1[8] )/( MCBinCenterMass[9] - MCBinCenterMass[8] );
    if ( m1 >= MCBinCenterMass[9]  && m1 < MCBinCenterMass[10]  ) mybkg = MCBinContentm1[9] - MCBinErrm1[9] + ( m1 - MCBinCenterMass[9] )*( MCBinContentm1[10] + MCBinErrm1[10] - MCBinContentm1[9] + MCBinErrm1[9] )/( MCBinCenterMass[10] - MCBinCenterMass[9] );
    if ( m1 >= MCBinCenterMass[10]  && m1 < MCBinCenterMass[11] ) mybkg = MCBinContentm1[10] + MCBinErrm1[10] + ( m1 - MCBinCenterMass[10] )*( MCBinContentm1[11] - MCBinErrm1[11] - MCBinContentm1[10] - MCBinErrm1[10] )/( MCBinCenterMass[11] - MCBinCenterMass[10] );
    if ( m1 >= MCBinCenterMass[11]  && m1 < MCBinCenterMass[12] ) mybkg = MCBinContentm1[11] - MCBinErrm1[11] + ( m1 - MCBinCenterMass[11] )*( MCBinContentm1[12] + MCBinErrm1[12] - MCBinContentm1[11] + MCBinErrm1[11] )/( MCBinCenterMass[12] - MCBinCenterMass[11] );
    if ( m1 >= MCBinCenterMass[12]  && m1 < MCBinCenterMass[13] ) mybkg = MCBinContentm1[12] + MCBinErrm1[12] + ( m1 - MCBinCenterMass[12] )*( MCBinContentm1[13] - MCBinErrm1[13] - MCBinContentm1[12] - MCBinErrm1[12] )/( MCBinCenterMass[13] - MCBinCenterMass[12] );
    if ( m1 >= MCBinCenterMass[13]  && m1 <= 60.000             ) mybkg = MCBinContentm1[13] - MCBinErrm1[13];

    return mybkg;
  }

  //BraidB starts from -1sigma for the first bin then the +1 sigma for the next, etc
  double My_BKGShapem1SigmaBraidB(double m1) {
    double mybkg = 0.0;

    if ( m1 >= 11.000              && m1 < MCBinCenterMass[0] )   mybkg = MCBinContentm1[0] - MCBinErrm1[0];
    if ( m1 >= MCBinCenterMass[0]  && m1 < MCBinCenterMass[1] )   mybkg = MCBinContentm1[0] - MCBinErrm1[0] + ( m1 - MCBinCenterMass[0] )*( MCBinContentm1[1] + MCBinErrm1[1] - MCBinContentm1[0] + MCBinErrm1[0] )/( MCBinCenterMass[1] - MCBinCenterMass[0] );
    if ( m1 >= MCBinCenterMass[1]  && m1 < MCBinCenterMass[2] )   mybkg = MCBinContentm1[1] + MCBinErrm1[1] + ( m1 - MCBinCenterMass[1] )*( MCBinContentm1[2] - MCBinErrm1[2] - MCBinContentm1[1] - MCBinErrm1[1] )/( MCBinCenterMass[2] - MCBinCenterMass[1] );
    if ( m1 >= MCBinCenterMass[2]  && m1 < MCBinCenterMass[3] )   mybkg = MCBinContentm1[2] - MCBinErrm1[2] + ( m1 - MCBinCenterMass[2] )*( MCBinContentm1[3] + MCBinErrm1[3] - MCBinContentm1[2] + MCBinErrm1[2] )/( MCBinCenterMass[3] - MCBinCenterMass[2] );
    if ( m1 >= MCBinCenterMass[3]  && m1 < MCBinCenterMass[4] )   mybkg = MCBinContentm1[3] + MCBinErrm1[3] + ( m1 - MCBinCenterMass[3] )*( MCBinContentm1[4] - MCBinErrm1[4] - MCBinContentm1[3] - MCBinErrm1[3] )/( MCBinCenterMass[4] - MCBinCenterMass[3] );
    if ( m1 >= MCBinCenterMass[4]  && m1 < MCBinCenterMass[5] )   mybkg = MCBinContentm1[4] - MCBinErrm1[4] + ( m1 - MCBinCenterMass[4] )*( MCBinContentm1[5] + MCBinErrm1[5] - MCBinContentm1[4] + MCBinErrm1[4] )/( MCBinCenterMass[5] - MCBinCenterMass[4] );
    if ( m1 >= MCBinCenterMass[5]  && m1 < MCBinCenterMass[6] )   mybkg = MCBinContentm1[5] + MCBinErrm1[5] + ( m1 - MCBinCenterMass[5] )*( MCBinContentm1[6] - MCBinErrm1[6] - MCBinContentm1[5] - MCBinErrm1[5] )/( MCBinCenterMass[6] - MCBinCenterMass[5] );
    if ( m1 >= MCBinCenterMass[6]  && m1 < MCBinCenterMass[7] )   mybkg = MCBinContentm1[6] - MCBinErrm1[6] + ( m1 - MCBinCenterMass[6] )*( MCBinContentm1[7] + MCBinErrm1[7] - MCBinContentm1[6] + MCBinErrm1[6] )/( MCBinCenterMass[7] - MCBinCenterMass[6] );
    if ( m1 >= MCBinCenterMass[7]  && m1 < MCBinCenterMass[8] )   mybkg = MCBinContentm1[7] + MCBinErrm1[7] + ( m1 - MCBinCenterMass[7] )*( MCBinContentm1[8] - MCBinErrm1[8] - MCBinContentm1[7] - MCBinErrm1[7] )/( MCBinCenterMass[8] - MCBinCenterMass[7] );
    if ( m1 >= MCBinCenterMass[8]  && m1 < MCBinCenterMass[9] )   mybkg = MCBinContentm1[8] - MCBinErrm1[8] + ( m1 - MCBinCenterMass[8] )*( MCBinContentm1[9] + MCBinErrm1[9] - MCBinContentm1[8] + MCBinErrm1[8] )/( MCBinCenterMass[9] - MCBinCenterMass[8] );
    if ( m1 >= MCBinCenterMass[9]  && m1 < MCBinCenterMass[10]  ) mybkg = MCBinContentm1[9] + MCBinErrm1[9] + ( m1 - MCBinCenterMass[9] )*( MCBinContentm1[10] - MCBinErrm1[10] - MCBinContentm1[9] - MCBinErrm1[9] )/( MCBinCenterMass[10] - MCBinCenterMass[9] );
    if ( m1 >= MCBinCenterMass[10]  && m1 < MCBinCenterMass[11] ) mybkg = MCBinContentm1[10] - MCBinErrm1[10] + ( m1 - MCBinCenterMass[10] )*( MCBinContentm1[11] + MCBinErrm1[11] - MCBinContentm1[10] + MCBinErrm1[10] )/( MCBinCenterMass[11] - MCBinCenterMass[10] );
    if ( m1 >= MCBinCenterMass[11]  && m1 < MCBinCenterMass[12] ) mybkg = MCBinContentm1[11] + MCBinErrm1[11] + ( m1 - MCBinCenterMass[11] )*( MCBinContentm1[12] - MCBinErrm1[12] - MCBinContentm1[11] - MCBinErrm1[11] )/( MCBinCenterMass[12] - MCBinCenterMass[11] );
    if ( m1 >= MCBinCenterMass[12]  && m1 < MCBinCenterMass[13] ) mybkg = MCBinContentm1[12] - MCBinErrm1[12] + ( m1 - MCBinCenterMass[12] )*( MCBinContentm1[13] + MCBinErrm1[13] - MCBinContentm1[12] + MCBinErrm1[12] )/( MCBinCenterMass[13] - MCBinCenterMass[12] );
    if ( m1 >= MCBinCenterMass[13]  && m1 <= 60.000             ) mybkg = MCBinContentm1[13] + MCBinErrm1[13];

    return mybkg;
  }

  double My_BKGShapem2(double m2) {
    //return this mass window size given m1
    double mybkg = 0.0;

    //Interpolation by drawing staight line, we use (m1+m2)/2 here
    //mass window size = y1 + (x-x1)*(y2-y1)/(x2-x1), x = (m1+m2)/2
    //Start and end with 11 and 60GeV to match bkg analysis
    if ( m2 >= 11.000              && m2 < MCBinCenterMass[0] )   mybkg = MCBinContentm2[0];
    if ( m2 >= MCBinCenterMass[0]  && m2 < MCBinCenterMass[1] )   mybkg = MCBinContentm2[0]  + ( m2 - MCBinCenterMass[0] )*( MCBinContentm2[1] - MCBinContentm2[0] )/( MCBinCenterMass[1] - MCBinCenterMass[0] );
    if ( m2 >= MCBinCenterMass[1]  && m2 < MCBinCenterMass[2] )   mybkg = MCBinContentm2[1]  + ( m2 - MCBinCenterMass[1] )*( MCBinContentm2[2] - MCBinContentm2[1] )/( MCBinCenterMass[2] - MCBinCenterMass[1] );
    if ( m2 >= MCBinCenterMass[2]  && m2 < MCBinCenterMass[3] )   mybkg = MCBinContentm2[2]  + ( m2 - MCBinCenterMass[2] )*( MCBinContentm2[3] - MCBinContentm2[2] )/( MCBinCenterMass[3] - MCBinCenterMass[2] );
    if ( m2 >= MCBinCenterMass[3]  && m2 < MCBinCenterMass[4] )   mybkg = MCBinContentm2[3]  + ( m2 - MCBinCenterMass[3] )*( MCBinContentm2[4] - MCBinContentm2[3] )/( MCBinCenterMass[4] - MCBinCenterMass[3] );
    if ( m2 >= MCBinCenterMass[4]  && m2 < MCBinCenterMass[5] )   mybkg = MCBinContentm2[4]  + ( m2 - MCBinCenterMass[4] )*( MCBinContentm2[5] - MCBinContentm2[4] )/( MCBinCenterMass[5] - MCBinCenterMass[4] );
    if ( m2 >= MCBinCenterMass[5]  && m2 < MCBinCenterMass[6] )   mybkg = MCBinContentm2[5]  + ( m2 - MCBinCenterMass[5] )*( MCBinContentm2[6] - MCBinContentm2[5] )/( MCBinCenterMass[6] - MCBinCenterMass[5] );
    if ( m2 >= MCBinCenterMass[6]  && m2 < MCBinCenterMass[7] )   mybkg = MCBinContentm2[6]  + ( m2 - MCBinCenterMass[6] )*( MCBinContentm2[7] - MCBinContentm2[6] )/( MCBinCenterMass[7] - MCBinCenterMass[6] );
    if ( m2 >= MCBinCenterMass[7]  && m2 < MCBinCenterMass[8] )   mybkg = MCBinContentm2[7]  + ( m2 - MCBinCenterMass[7] )*( MCBinContentm2[8] - MCBinContentm2[7] )/( MCBinCenterMass[8] - MCBinCenterMass[7] );
    if ( m2 >= MCBinCenterMass[8]  && m2 < MCBinCenterMass[9] )   mybkg = MCBinContentm2[8]  + ( m2 - MCBinCenterMass[8] )*( MCBinContentm2[9] - MCBinContentm2[8] )/( MCBinCenterMass[9] - MCBinCenterMass[8] );
    if ( m2 >= MCBinCenterMass[9]  && m2 < MCBinCenterMass[10]  ) mybkg = MCBinContentm2[9]  + ( m2 - MCBinCenterMass[9] )*( MCBinContentm2[10] - MCBinContentm2[9] )/( MCBinCenterMass[10] - MCBinCenterMass[9] );
    if ( m2 >= MCBinCenterMass[10]  && m2 < MCBinCenterMass[11] ) mybkg = MCBinContentm2[10] + ( m2 - MCBinCenterMass[10] )*( MCBinContentm2[11] - MCBinContentm2[10] )/( MCBinCenterMass[11] - MCBinCenterMass[10] );
    if ( m2 >= MCBinCenterMass[11]  && m2 < MCBinCenterMass[12] ) mybkg = MCBinContentm2[11] + ( m2 - MCBinCenterMass[11] )*( MCBinContentm2[12] - MCBinContentm2[11] )/( MCBinCenterMass[12] - MCBinCenterMass[11] );
    if ( m2 >= MCBinCenterMass[12]  && m2 < MCBinCenterMass[13] ) mybkg = MCBinContentm2[12] + ( m2 - MCBinCenterMass[12] )*( MCBinContentm2[13] - MCBinContentm2[12] )/( MCBinCenterMass[13] - MCBinCenterMass[12] );
    if ( m2 >= MCBinCenterMass[13]  && m2 <= 60.000             ) mybkg = MCBinContentm2[13];

    return mybkg;
  }

  double My_BKGShapem2SigmaUp(double m2) {
    double mybkg = 0.0;

    if ( m2 >= 11.000              && m2 < MCBinCenterMass[0] )   mybkg = MCBinContentm2[0] + MCBinErrm2[0];
    if ( m2 >= MCBinCenterMass[0]  && m2 < MCBinCenterMass[1] )   mybkg = MCBinContentm2[0] + MCBinErrm2[0] + ( m2 - MCBinCenterMass[0] )*( MCBinContentm2[1] + MCBinErrm2[1] - MCBinContentm2[0] - MCBinErrm2[0] )/( MCBinCenterMass[1] - MCBinCenterMass[0] );
    if ( m2 >= MCBinCenterMass[1]  && m2 < MCBinCenterMass[2] )   mybkg = MCBinContentm2[1] + MCBinErrm2[1] + ( m2 - MCBinCenterMass[1] )*( MCBinContentm2[2] + MCBinErrm2[2] - MCBinContentm2[1] - MCBinErrm2[1] )/( MCBinCenterMass[2] - MCBinCenterMass[1] );
    if ( m2 >= MCBinCenterMass[2]  && m2 < MCBinCenterMass[3] )   mybkg = MCBinContentm2[2] + MCBinErrm2[2] + ( m2 - MCBinCenterMass[2] )*( MCBinContentm2[3] + MCBinErrm2[3] - MCBinContentm2[2] - MCBinErrm2[2] )/( MCBinCenterMass[3] - MCBinCenterMass[2] );
    if ( m2 >= MCBinCenterMass[3]  && m2 < MCBinCenterMass[4] )   mybkg = MCBinContentm2[3] + MCBinErrm2[3] + ( m2 - MCBinCenterMass[3] )*( MCBinContentm2[4] + MCBinErrm2[4] - MCBinContentm2[3] - MCBinErrm2[3] )/( MCBinCenterMass[4] - MCBinCenterMass[3] );
    if ( m2 >= MCBinCenterMass[4]  && m2 < MCBinCenterMass[5] )   mybkg = MCBinContentm2[4] + MCBinErrm2[4] + ( m2 - MCBinCenterMass[4] )*( MCBinContentm2[5] + MCBinErrm2[5] - MCBinContentm2[4] - MCBinErrm2[4] )/( MCBinCenterMass[5] - MCBinCenterMass[4] );
    if ( m2 >= MCBinCenterMass[5]  && m2 < MCBinCenterMass[6] )   mybkg = MCBinContentm2[5] + MCBinErrm2[5] + ( m2 - MCBinCenterMass[5] )*( MCBinContentm2[6] + MCBinErrm2[6] - MCBinContentm2[5] - MCBinErrm2[5] )/( MCBinCenterMass[6] - MCBinCenterMass[5] );
    if ( m2 >= MCBinCenterMass[6]  && m2 < MCBinCenterMass[7] )   mybkg = MCBinContentm2[6] + MCBinErrm2[6] + ( m2 - MCBinCenterMass[6] )*( MCBinContentm2[7] + MCBinErrm2[7] - MCBinContentm2[6] - MCBinErrm2[6] )/( MCBinCenterMass[7] - MCBinCenterMass[6] );
    if ( m2 >= MCBinCenterMass[7]  && m2 < MCBinCenterMass[8] )   mybkg = MCBinContentm2[7] + MCBinErrm2[7] + ( m2 - MCBinCenterMass[7] )*( MCBinContentm2[8] + MCBinErrm2[8] - MCBinContentm2[7] - MCBinErrm2[7] )/( MCBinCenterMass[8] - MCBinCenterMass[7] );
    if ( m2 >= MCBinCenterMass[8]  && m2 < MCBinCenterMass[9] )   mybkg = MCBinContentm2[8] + MCBinErrm2[8] + ( m2 - MCBinCenterMass[8] )*( MCBinContentm2[9] + MCBinErrm2[9] - MCBinContentm2[8] - MCBinErrm2[8] )/( MCBinCenterMass[9] - MCBinCenterMass[8] );
    if ( m2 >= MCBinCenterMass[9]  && m2 < MCBinCenterMass[10]  ) mybkg = MCBinContentm2[9] + MCBinErrm2[9] + ( m2 - MCBinCenterMass[9] )*( MCBinContentm2[10] + MCBinErrm2[10] - MCBinContentm2[9] - MCBinErrm2[9] )/( MCBinCenterMass[10] - MCBinCenterMass[9] );
    if ( m2 >= MCBinCenterMass[10]  && m2 < MCBinCenterMass[11] ) mybkg = MCBinContentm2[10] + MCBinErrm2[10] + ( m2 - MCBinCenterMass[10] )*( MCBinContentm2[11] + MCBinErrm2[11] - MCBinContentm2[10] - MCBinErrm2[10] )/( MCBinCenterMass[11] - MCBinCenterMass[10] );
    if ( m2 >= MCBinCenterMass[11]  && m2 < MCBinCenterMass[12] ) mybkg = MCBinContentm2[11] + MCBinErrm2[11] + ( m2 - MCBinCenterMass[11] )*( MCBinContentm2[12] + MCBinErrm2[12] - MCBinContentm2[11] - MCBinErrm2[11] )/( MCBinCenterMass[12] - MCBinCenterMass[11] );
    if ( m2 >= MCBinCenterMass[12]  && m2 < MCBinCenterMass[13] ) mybkg = MCBinContentm2[12] + MCBinErrm2[12] + ( m2 - MCBinCenterMass[12] )*( MCBinContentm2[13] + MCBinErrm2[13] - MCBinContentm2[12] - MCBinErrm2[12] )/( MCBinCenterMass[13] - MCBinCenterMass[12] );
    if ( m2 >= MCBinCenterMass[13]  && m2 <= 60.000             ) mybkg = MCBinContentm2[13] + MCBinErrm2[13];

    return mybkg;
  }

  double My_BKGShapem2SigmaDn(double m2) {
    double mybkg = 0.0;

    if ( m2 >= 11.000              && m2 < MCBinCenterMass[0] )   mybkg = MCBinContentm2[0] - MCBinErrm2[0];
    if ( m2 >= MCBinCenterMass[0]  && m2 < MCBinCenterMass[1] )   mybkg = MCBinContentm2[0] - MCBinErrm2[0] + ( m2 - MCBinCenterMass[0] )*( MCBinContentm2[1] - MCBinErrm2[1] - MCBinContentm2[0] + MCBinErrm2[0] )/( MCBinCenterMass[1] - MCBinCenterMass[0] );
    if ( m2 >= MCBinCenterMass[1]  && m2 < MCBinCenterMass[2] )   mybkg = MCBinContentm2[1] - MCBinErrm2[1] + ( m2 - MCBinCenterMass[1] )*( MCBinContentm2[2] - MCBinErrm2[2] - MCBinContentm2[1] + MCBinErrm2[1] )/( MCBinCenterMass[2] - MCBinCenterMass[1] );
    if ( m2 >= MCBinCenterMass[2]  && m2 < MCBinCenterMass[3] )   mybkg = MCBinContentm2[2] - MCBinErrm2[2] + ( m2 - MCBinCenterMass[2] )*( MCBinContentm2[3] - MCBinErrm2[3] - MCBinContentm2[2] + MCBinErrm2[2] )/( MCBinCenterMass[3] - MCBinCenterMass[2] );
    if ( m2 >= MCBinCenterMass[3]  && m2 < MCBinCenterMass[4] )   mybkg = MCBinContentm2[3] - MCBinErrm2[3] + ( m2 - MCBinCenterMass[3] )*( MCBinContentm2[4] - MCBinErrm2[4] - MCBinContentm2[3] + MCBinErrm2[3] )/( MCBinCenterMass[4] - MCBinCenterMass[3] );
    if ( m2 >= MCBinCenterMass[4]  && m2 < MCBinCenterMass[5] )   mybkg = MCBinContentm2[4] - MCBinErrm2[4] + ( m2 - MCBinCenterMass[4] )*( MCBinContentm2[5] - MCBinErrm2[5] - MCBinContentm2[4] + MCBinErrm2[4] )/( MCBinCenterMass[5] - MCBinCenterMass[4] );
    if ( m2 >= MCBinCenterMass[5]  && m2 < MCBinCenterMass[6] )   mybkg = MCBinContentm2[5] - MCBinErrm2[5] + ( m2 - MCBinCenterMass[5] )*( MCBinContentm2[6] - MCBinErrm2[6] - MCBinContentm2[5] + MCBinErrm2[5] )/( MCBinCenterMass[6] - MCBinCenterMass[5] );
    if ( m2 >= MCBinCenterMass[6]  && m2 < MCBinCenterMass[7] )   mybkg = MCBinContentm2[6] - MCBinErrm2[6] + ( m2 - MCBinCenterMass[6] )*( MCBinContentm2[7] - MCBinErrm2[7] - MCBinContentm2[6] + MCBinErrm2[6] )/( MCBinCenterMass[7] - MCBinCenterMass[6] );
    if ( m2 >= MCBinCenterMass[7]  && m2 < MCBinCenterMass[8] )   mybkg = MCBinContentm2[7] - MCBinErrm2[7] + ( m2 - MCBinCenterMass[7] )*( MCBinContentm2[8] - MCBinErrm2[8] - MCBinContentm2[7] + MCBinErrm2[7] )/( MCBinCenterMass[8] - MCBinCenterMass[7] );
    if ( m2 >= MCBinCenterMass[8]  && m2 < MCBinCenterMass[9] )   mybkg = MCBinContentm2[8] - MCBinErrm2[8] + ( m2 - MCBinCenterMass[8] )*( MCBinContentm2[9] - MCBinErrm2[9] - MCBinContentm2[8] + MCBinErrm2[8] )/( MCBinCenterMass[9] - MCBinCenterMass[8] );
    if ( m2 >= MCBinCenterMass[9]  && m2 < MCBinCenterMass[10]  ) mybkg = MCBinContentm2[9] - MCBinErrm2[9] + ( m2 - MCBinCenterMass[9] )*( MCBinContentm2[10] - MCBinErrm2[10] - MCBinContentm2[9] + MCBinErrm2[9] )/( MCBinCenterMass[10] - MCBinCenterMass[9] );
    if ( m2 >= MCBinCenterMass[10]  && m2 < MCBinCenterMass[11] ) mybkg = MCBinContentm2[10] - MCBinErrm2[10] + ( m2 - MCBinCenterMass[10] )*( MCBinContentm2[11] - MCBinErrm2[11] - MCBinContentm2[10] + MCBinErrm2[10] )/( MCBinCenterMass[11] - MCBinCenterMass[10] );
    if ( m2 >= MCBinCenterMass[11]  && m2 < MCBinCenterMass[12] ) mybkg = MCBinContentm2[11] - MCBinErrm2[11] + ( m2 - MCBinCenterMass[11] )*( MCBinContentm2[12] - MCBinErrm2[12] - MCBinContentm2[11] + MCBinErrm2[11] )/( MCBinCenterMass[12] - MCBinCenterMass[11] );
    if ( m2 >= MCBinCenterMass[12]  && m2 < MCBinCenterMass[13] ) mybkg = MCBinContentm2[12] - MCBinErrm2[12] + ( m2 - MCBinCenterMass[12] )*( MCBinContentm2[13] - MCBinErrm2[13] - MCBinContentm2[12] + MCBinErrm2[12] )/( MCBinCenterMass[13] - MCBinCenterMass[12] );
    if ( m2 >= MCBinCenterMass[13]  && m2 <= 60.000             ) mybkg = MCBinContentm2[13] - MCBinErrm2[13];

    return mybkg;
  }

  //BraidA starts from +1sigma for the first bin then the -1 sigma for the next, etc
  double My_BKGShapem2SigmaBraidA(double m2) {
    double mybkg = 0.0;

    if ( m2 >= 11.000              && m2 < MCBinCenterMass[0] )   mybkg = MCBinContentm2[0] + MCBinErrm2[0];
    if ( m2 >= MCBinCenterMass[0]  && m2 < MCBinCenterMass[1] )   mybkg = MCBinContentm2[0] + MCBinErrm2[0] + ( m2 - MCBinCenterMass[0] )*( MCBinContentm2[1] - MCBinErrm2[1] - MCBinContentm2[0] - MCBinErrm2[0] )/( MCBinCenterMass[1] - MCBinCenterMass[0] );
    if ( m2 >= MCBinCenterMass[1]  && m2 < MCBinCenterMass[2] )   mybkg = MCBinContentm2[1] - MCBinErrm2[1] + ( m2 - MCBinCenterMass[1] )*( MCBinContentm2[2] + MCBinErrm2[2] - MCBinContentm2[1] + MCBinErrm2[1] )/( MCBinCenterMass[2] - MCBinCenterMass[1] );
    if ( m2 >= MCBinCenterMass[2]  && m2 < MCBinCenterMass[3] )   mybkg = MCBinContentm2[2] + MCBinErrm2[2] + ( m2 - MCBinCenterMass[2] )*( MCBinContentm2[3] - MCBinErrm2[3] - MCBinContentm2[2] - MCBinErrm2[2] )/( MCBinCenterMass[3] - MCBinCenterMass[2] );
    if ( m2 >= MCBinCenterMass[3]  && m2 < MCBinCenterMass[4] )   mybkg = MCBinContentm2[3] - MCBinErrm2[3] + ( m2 - MCBinCenterMass[3] )*( MCBinContentm2[4] + MCBinErrm2[4] - MCBinContentm2[3] + MCBinErrm2[3] )/( MCBinCenterMass[4] - MCBinCenterMass[3] );
    if ( m2 >= MCBinCenterMass[4]  && m2 < MCBinCenterMass[5] )   mybkg = MCBinContentm2[4] + MCBinErrm2[4] + ( m2 - MCBinCenterMass[4] )*( MCBinContentm2[5] - MCBinErrm2[5] - MCBinContentm2[4] - MCBinErrm2[4] )/( MCBinCenterMass[5] - MCBinCenterMass[4] );
    if ( m2 >= MCBinCenterMass[5]  && m2 < MCBinCenterMass[6] )   mybkg = MCBinContentm2[5] - MCBinErrm2[5] + ( m2 - MCBinCenterMass[5] )*( MCBinContentm2[6] + MCBinErrm2[6] - MCBinContentm2[5] + MCBinErrm2[5] )/( MCBinCenterMass[6] - MCBinCenterMass[5] );
    if ( m2 >= MCBinCenterMass[6]  && m2 < MCBinCenterMass[7] )   mybkg = MCBinContentm2[6] + MCBinErrm2[6] + ( m2 - MCBinCenterMass[6] )*( MCBinContentm2[7] - MCBinErrm2[7] - MCBinContentm2[6] - MCBinErrm2[6] )/( MCBinCenterMass[7] - MCBinCenterMass[6] );
    if ( m2 >= MCBinCenterMass[7]  && m2 < MCBinCenterMass[8] )   mybkg = MCBinContentm2[7] - MCBinErrm2[7] + ( m2 - MCBinCenterMass[7] )*( MCBinContentm2[8] + MCBinErrm2[8] - MCBinContentm2[7] + MCBinErrm2[7] )/( MCBinCenterMass[8] - MCBinCenterMass[7] );
    if ( m2 >= MCBinCenterMass[8]  && m2 < MCBinCenterMass[9] )   mybkg = MCBinContentm2[8] + MCBinErrm2[8] + ( m2 - MCBinCenterMass[8] )*( MCBinContentm2[9] - MCBinErrm2[9] - MCBinContentm2[8] - MCBinErrm2[8] )/( MCBinCenterMass[9] - MCBinCenterMass[8] );
    if ( m2 >= MCBinCenterMass[9]  && m2 < MCBinCenterMass[10]  ) mybkg = MCBinContentm2[9] - MCBinErrm2[9] + ( m2 - MCBinCenterMass[9] )*( MCBinContentm2[10] + MCBinErrm2[10] - MCBinContentm2[9] + MCBinErrm2[9] )/( MCBinCenterMass[10] - MCBinCenterMass[9] );
    if ( m2 >= MCBinCenterMass[10]  && m2 < MCBinCenterMass[11] ) mybkg = MCBinContentm2[10] + MCBinErrm2[10] + ( m2 - MCBinCenterMass[10] )*( MCBinContentm2[11] - MCBinErrm2[11] - MCBinContentm2[10] - MCBinErrm2[10] )/( MCBinCenterMass[11] - MCBinCenterMass[10] );
    if ( m2 >= MCBinCenterMass[11]  && m2 < MCBinCenterMass[12] ) mybkg = MCBinContentm2[11] - MCBinErrm2[11] + ( m2 - MCBinCenterMass[11] )*( MCBinContentm2[12] + MCBinErrm2[12] - MCBinContentm2[11] + MCBinErrm2[11] )/( MCBinCenterMass[12] - MCBinCenterMass[11] );
    if ( m2 >= MCBinCenterMass[12]  && m2 < MCBinCenterMass[13] ) mybkg = MCBinContentm2[12] + MCBinErrm2[12] + ( m2 - MCBinCenterMass[12] )*( MCBinContentm2[13] - MCBinErrm2[13] - MCBinContentm2[12] - MCBinErrm2[12] )/( MCBinCenterMass[13] - MCBinCenterMass[12] );
    if ( m2 >= MCBinCenterMass[13]  && m2 <= 60.000             ) mybkg = MCBinContentm2[13] - MCBinErrm2[13];

    return mybkg;
  }

  //BraidB starts from -1sigma for the first bin then the +1 sigma for the next, etc
  double My_BKGShapem2SigmaBraidB(double m2) {
    double mybkg = 0.0;

    if ( m2 >= 11.000              && m2 < MCBinCenterMass[0] )   mybkg = MCBinContentm2[0] - MCBinErrm2[0];
    if ( m2 >= MCBinCenterMass[0]  && m2 < MCBinCenterMass[1] )   mybkg = MCBinContentm2[0] - MCBinErrm2[0] + ( m2 - MCBinCenterMass[0] )*( MCBinContentm2[1] + MCBinErrm2[1] - MCBinContentm2[0] + MCBinErrm2[0] )/( MCBinCenterMass[1] - MCBinCenterMass[0] );
    if ( m2 >= MCBinCenterMass[1]  && m2 < MCBinCenterMass[2] )   mybkg = MCBinContentm2[1] + MCBinErrm2[1] + ( m2 - MCBinCenterMass[1] )*( MCBinContentm2[2] - MCBinErrm2[2] - MCBinContentm2[1] - MCBinErrm2[1] )/( MCBinCenterMass[2] - MCBinCenterMass[1] );
    if ( m2 >= MCBinCenterMass[2]  && m2 < MCBinCenterMass[3] )   mybkg = MCBinContentm2[2] - MCBinErrm2[2] + ( m2 - MCBinCenterMass[2] )*( MCBinContentm2[3] + MCBinErrm2[3] - MCBinContentm2[2] + MCBinErrm2[2] )/( MCBinCenterMass[3] - MCBinCenterMass[2] );
    if ( m2 >= MCBinCenterMass[3]  && m2 < MCBinCenterMass[4] )   mybkg = MCBinContentm2[3] + MCBinErrm2[3] + ( m2 - MCBinCenterMass[3] )*( MCBinContentm2[4] - MCBinErrm2[4] - MCBinContentm2[3] - MCBinErrm2[3] )/( MCBinCenterMass[4] - MCBinCenterMass[3] );
    if ( m2 >= MCBinCenterMass[4]  && m2 < MCBinCenterMass[5] )   mybkg = MCBinContentm2[4] - MCBinErrm2[4] + ( m2 - MCBinCenterMass[4] )*( MCBinContentm2[5] + MCBinErrm2[5] - MCBinContentm2[4] + MCBinErrm2[4] )/( MCBinCenterMass[5] - MCBinCenterMass[4] );
    if ( m2 >= MCBinCenterMass[5]  && m2 < MCBinCenterMass[6] )   mybkg = MCBinContentm2[5] + MCBinErrm2[5] + ( m2 - MCBinCenterMass[5] )*( MCBinContentm2[6] - MCBinErrm2[6] - MCBinContentm2[5] - MCBinErrm2[5] )/( MCBinCenterMass[6] - MCBinCenterMass[5] );
    if ( m2 >= MCBinCenterMass[6]  && m2 < MCBinCenterMass[7] )   mybkg = MCBinContentm2[6] - MCBinErrm2[6] + ( m2 - MCBinCenterMass[6] )*( MCBinContentm2[7] + MCBinErrm2[7] - MCBinContentm2[6] + MCBinErrm2[6] )/( MCBinCenterMass[7] - MCBinCenterMass[6] );
    if ( m2 >= MCBinCenterMass[7]  && m2 < MCBinCenterMass[8] )   mybkg = MCBinContentm2[7] + MCBinErrm2[7] + ( m2 - MCBinCenterMass[7] )*( MCBinContentm2[8] - MCBinErrm2[8] - MCBinContentm2[7] - MCBinErrm2[7] )/( MCBinCenterMass[8] - MCBinCenterMass[7] );
    if ( m2 >= MCBinCenterMass[8]  && m2 < MCBinCenterMass[9] )   mybkg = MCBinContentm2[8] - MCBinErrm2[8] + ( m2 - MCBinCenterMass[8] )*( MCBinContentm2[9] + MCBinErrm2[9] - MCBinContentm2[8] + MCBinErrm2[8] )/( MCBinCenterMass[9] - MCBinCenterMass[8] );
    if ( m2 >= MCBinCenterMass[9]  && m2 < MCBinCenterMass[10]  ) mybkg = MCBinContentm2[9] + MCBinErrm2[9] + ( m2 - MCBinCenterMass[9] )*( MCBinContentm2[10] - MCBinErrm2[10] - MCBinContentm2[9] - MCBinErrm2[9] )/( MCBinCenterMass[10] - MCBinCenterMass[9] );
    if ( m2 >= MCBinCenterMass[10]  && m2 < MCBinCenterMass[11] ) mybkg = MCBinContentm2[10] - MCBinErrm2[10] + ( m2 - MCBinCenterMass[10] )*( MCBinContentm2[11] + MCBinErrm2[11] - MCBinContentm2[10] + MCBinErrm2[10] )/( MCBinCenterMass[11] - MCBinCenterMass[10] );
    if ( m2 >= MCBinCenterMass[11]  && m2 < MCBinCenterMass[12] ) mybkg = MCBinContentm2[11] + MCBinErrm2[11] + ( m2 - MCBinCenterMass[11] )*( MCBinContentm2[12] - MCBinErrm2[12] - MCBinContentm2[11] - MCBinErrm2[11] )/( MCBinCenterMass[12] - MCBinCenterMass[11] );
    if ( m2 >= MCBinCenterMass[12]  && m2 < MCBinCenterMass[13] ) mybkg = MCBinContentm2[12] - MCBinErrm2[12] + ( m2 - MCBinCenterMass[12] )*( MCBinContentm2[13] + MCBinErrm2[13] - MCBinContentm2[12] + MCBinErrm2[12] )/( MCBinCenterMass[13] - MCBinCenterMass[12] );
    if ( m2 >= MCBinCenterMass[13]  && m2 <= 60.000             ) mybkg = MCBinContentm2[13] + MCBinErrm2[13];

    return mybkg;
  }

} // End namespace
