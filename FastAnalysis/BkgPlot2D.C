//=====================================================================
//= Run it as: root -l -b -q BkgPlot2D.C                              =
//=====================================================================
#include "TFile.h"
#include "TStopwatch.h"
#include "TCanvas.h"
#include "TTree.h"
#include "TF1.h"
#include "TF2.h"
#include "TH1.h"
#include "TH2.h"
#include "TChain.h"
#include "TRandom3.h"
#include "TStyle.h"
#include "TPaveText.h"
#include "TLatex.h"
#include "TLegend.h"
#include "TROOT.h"
#include "TMatrixDSym.h"
#include "TMath.h"
#include "TColor.h"

#include <sstream>
#include <iostream>
#include <string>

#include "RooAbsPdf.h"
#include "RooProdPdf.h"
#include "RooRealVar.h"
#include "RooDataHist.h"
#include "RooDataSet.h"
#include "RooPlot.h"
#include "RooHist.h"
#include "RooWorkspace.h"
#include "RooRandom.h"
#include "RooFitResult.h"
#include "RooClassFactory.h"
#include "RooHistPdf.h"
#include "RooCustomizer.h"
#include "RooMultiVarGaussian.h"
#include "RooTFnBinding.h"
#include "RooArgusBG.h"
#include "RooBernstein.h"
#include "RooGaussian.h"
#include "RooPolynomial.h"
#include "RooChebychev.h"
#include "RooGenericPdf.h"
#include "RooAddPdf.h"

#include "macros/tdrStyle.C"
#include "Constants.h"
#include "Config.h"

#ifndef __CINT__
#include "RooCFunction1Binding.h"
#endif

using namespace RooFit;

void BkgPlot2D() {

  //Configure inputs for year
  BKG_cfg::ConfigureInput(year);
  setTDRStyle();

  //for template
  TLegend *txtHeader = new TLegend(.00001, 0.95, 0.94, 1.);
  txtHeader->SetFillColor(kWhite);
  txtHeader->SetFillStyle(0);
  txtHeader->SetBorderSize(0);
  txtHeader->SetTextFont(42);
  txtHeader->SetTextSize(0.045);
  txtHeader->SetTextAlign(22);
  txtHeader->SetHeader(headertpl2);

  //for validation plot
  TLegend *txtHeadervld = new TLegend(0.14, 0.93, 0.98, 0.98);
  txtHeadervld->SetFillColor(kWhite);
  txtHeadervld->SetFillStyle(0);
  txtHeadervld->SetBorderSize(0);
  txtHeadervld->SetTextFont(42);
  txtHeadervld->SetTextSize(0.045);
  txtHeadervld->SetTextAlign(22);
  txtHeadervld->SetHeader(headervld);

  //gStyle->SetPalette(52); //Grey Scale
  Double_t Red[2]    = {1.00, 0.00};
  Double_t Green[2]  = {1.00, 0.00};
  Double_t Blue[2]   = {1.00, 0.00};
  Double_t Length[2] = {0.00, 1.00};
  Int_t nb=50;

  //====================================================================================
  //          Pre-calculated m1 and m2 values for drawing the corridor curves
  //====================================================================================
  //Straigt line interpolation, just use the signal mass points
  double m2Small[11];
  double m2Large[11];
  for (int i = 0; i < 11; i++) {
    m2Small[i] = mean[i] - window[i];
    m2Large[i] = mean[i] + window[i];
  }
  TGraph* corridorDn = new TGraph(11, mean, m2Small);
  TGraph* corridorUp = new TGraph(11, mean, m2Large);
  corridorDn->SetLineColor(1); corridorDn->SetLineStyle(9); corridorDn->SetLineWidth(2);
  corridorUp->SetLineColor(1); corridorUp->SetLineStyle(9); corridorUp->SetLineWidth(2);

  //==================================================================================
  //            The workspace stores all background pdf and the dataset after cuts
  //==================================================================================

  TFile* file = new TFile(inputFile2);
  RooWorkspace *w = (RooWorkspace*) file->Get("w");
  
TH2D* h2_dimudimu_control_Iso_offDiagonal_2D_all = (TH2D*)w->data("ds_dimudimu_control_Iso_offDiagonal_2D_all")->createHistogram("m1_all,m2_all", m_bins_all, m_bins_all);

  h2_dimudimu_control_Iso_offDiagonal_2D_all->SetMarkerColor(kBlack);
  h2_dimudimu_control_Iso_offDiagonal_2D_all->SetMarkerStyle(20);
  h2_dimudimu_control_Iso_offDiagonal_2D_all->SetMarkerSize(1.5);
  // Don't draw titles inheritted from dataset
  h2_dimudimu_control_Iso_offDiagonal_2D_all->SetXTitle("");
  h2_dimudimu_control_Iso_offDiagonal_2D_all->SetYTitle("");

  TH2D * h2_dimudimu_control_Iso_offDiagonal_2D_all_tmp = new TH2D( *h2_dimudimu_control_Iso_offDiagonal_2D_all);
  h2_dimudimu_control_Iso_offDiagonal_2D_all_tmp->SetMarkerColor(kWhite);
  h2_dimudimu_control_Iso_offDiagonal_2D_all_tmp->SetMarkerStyle(20);
  h2_dimudimu_control_Iso_offDiagonal_2D_all_tmp->SetMarkerSize(1.0);

  TCanvas * c_data_m1_vs_m2_all = new TCanvas("c_data_m1_vs_m2_all", "c_data_m1_vs_m2_all", 0, 1320, 1044, 928);
  c_data_m1_vs_m2_all->SetCanvasSize(1040, 900);
  c_data_m1_vs_m2_all->SetLeftMargin(0.121);
  c_data_m1_vs_m2_all->SetRightMargin(0.17);
  c_data_m1_vs_m2_all->SetTopMargin(0.05);
  c_data_m1_vs_m2_all->cd();

  TPad* pad_all_data = new TPad("pad_all_data", "pad_all_data", 0, 0, 1, 1);
  pad_all_data->Draw();
  pad_all_data->cd();
  pad_all_data->SetLeftMargin(0.121);
  pad_all_data->SetRightMargin(0.17);
  pad_all_data->SetTopMargin(0.05);
  pad_all_data->SetFillColor(0);
  pad_all_data->SetFillStyle(4000);
  pad_all_data->SetBorderMode(0);
  pad_all_data->SetBorderSize(2);
  pad_all_data->SetTickx(1);
  pad_all_data->SetTicky(1);
  pad_all_data->SetFrameFillStyle(0);
  pad_all_data->SetFrameBorderMode(0);
  pad_all_data->SetFrameFillStyle(0);
  pad_all_data->SetFrameBorderMode(0);

  h2_dimudimu_control_Iso_offDiagonal_2D_all->GetXaxis()->SetTitle("m_{#mu#mu_{1}} [GeV]");
  h2_dimudimu_control_Iso_offDiagonal_2D_all->GetXaxis()->SetTitleOffset(0.93);
  h2_dimudimu_control_Iso_offDiagonal_2D_all->GetYaxis()->SetTitle("m_{#mu#mu_{2}} [GeV]");
  h2_dimudimu_control_Iso_offDiagonal_2D_all->GetYaxis()->SetTitleOffset(0.85);
  h2_dimudimu_control_Iso_offDiagonal_2D_all->Draw();
  h2_dimudimu_control_Iso_offDiagonal_2D_all_tmp->Draw("same");

  //========================================================
  //    !!!BEGIN: unblinded data
  //========================================================

  TH2D* h2D_dimudimu_signal_2D_all = (TH2D*)w->data("ds_dimudimu_signal_2D_all")->createHistogram("m1_all,m2_all", m_bins_all, m_bins_all);
  h2D_dimudimu_signal_2D_all->SetMarkerColor(kBlack);
  h2D_dimudimu_signal_2D_all->SetMarkerStyle(22);
  h2D_dimudimu_signal_2D_all->SetMarkerSize(1.5);
  //Don't draw titles inheritted from dataset
  h2D_dimudimu_signal_2D_all->SetXTitle("");
  h2D_dimudimu_signal_2D_all->SetYTitle("");
  h2D_dimudimu_signal_2D_all->Draw("same");

  TH2D * h2D_dimudimu_signal_2D_all_tmp = new TH2D( *h2D_dimudimu_signal_2D_all);
  h2D_dimudimu_signal_2D_all_tmp->SetMarkerColor(kYellow);
  h2D_dimudimu_signal_2D_all_tmp->SetMarkerStyle(22);
  h2D_dimudimu_signal_2D_all_tmp->SetMarkerSize(1.0);
  h2D_dimudimu_signal_2D_all_tmp->Draw("same");

  //==========================================================
  //    !!!END: unblinded data  
  //==========================================================

  corridorDn->Draw("L"); corridorUp->Draw("L"); txtHeader->Draw();
  c_data_m1_vs_m2_all->SaveAs("DATA_all.pdf");
  c_data_m1_vs_m2_all->SaveAs("DATA_all.png");
  c_data_m1_vs_m2_all->SaveAs("DATA_all.root");
}
