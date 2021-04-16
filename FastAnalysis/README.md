# Instructions 

Once you get (use wget) all files under folder "FastAnalysis", 
 
    wget https://raw.githubusercontent.com/weishi10141993/DarkSector/master/FastAnalysis/Config.h
    
then run:
    
    root -l -b -q BkgPlot2D.C 

# Notes

The names of the datasets (with all analysis cuts applied) are,

    * 0.2113 - 2.72 GeV *
    ds_dimudimu_control_Iso_offDiagonal_2D_below_Jpsi: control region
    ds_dimudimu_signal_2D_below_Jpsi: signal region
    
    * 3.24 - 9 GeV *
    ds_dimudimu_control_Iso_offDiagonal_2D_above_Jpsi: control region
    ds_dimudimu_signal_2D_above_Jpsi: signal region
    
    * 11 - 60 GeV  *
    ds_dimudimu_control_Iso_offDiagonal_2D_above_Upsilon: control region
    ds_dimudimu_signal_2D_above_Upsilon: signal region
    
    * All mass range (a simple addition of dataset above) *
    ds_dimudimu_control_Iso_offDiagonal_2D_all: control region
    ds_dimudimu_signal_2D_all: signal region
    
To examine the dataset:

    // This prints the variables and total entries in the dataset
    w->data("ds_dimudimu_signal_2D_all")->Print()
    
    // This prints values of the first data point in the dataset
    w->data("ds_dimudimu_signal_2D_all")->get(0)->Print("V");
    
    // In the macro, to plot one variable 
    RooPlot* plotm1 = w->var("m1_all")->frame(Title("m1 data"), Bins(300));
    w->data("ds_dimudimu_signal_2D_all")->plotOn(plotm1, DataError(RooAbsData::SumW2), Name("data_m1"));
    TCanvas * c1 = new TCanvas("c1");
    c1->cd(); plotm1->Draw(); 

The original macro is here: https://github.com/weishi10141993/MuJetAnalysis_BKGEstimation/blob/test/LowMassBKGPlot2D18.C

The cuts applied to each dataset is here: https://github.com/weishi10141993/MuJetAnalysis_BKGEstimation/blob/test/LowMassBKGFit1D18.C#L826-L975

The datasets are built from the trees in 2018 ntuples (no cuts applied for ntuples). The 2018 data ntuples are stored at TAMU Terra cluster: /scratch/user/ws13/2018DataNtuples_2SAmu_NoVtxProbCut_4HLT
