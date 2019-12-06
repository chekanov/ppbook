# pyROOT utility classes used for "Data Analysis Techniques in Particle Physics"
# https://handwiki.org/wiki/Physics:PP/Start
# This code is protected by CC BY-ND License: https://creativecommons.org/licenses/by-nd/4.0/ 
# S.Chekanov (ANL)

import sys,os,math 
from ROOT import gROOT,gStyle,TH1D,TH1F,gPad,TPad,TCanvas,TLine,TPostScript,TLatex 
from ROOT import Math,TFile,TGraphErrors, TGraph, TGraphAsymmErrors

def showme(figure,data,theory,ratio,X,Y,YB):
  """A function to draw and and theory as well as their ratio. S.Chekanov
   @param  figure Figure file
   @param: data   Histogram with data 
   @param: theory Histogram with theory
   @param: ratio  TGraph or Histogram with for bottom plot
   @param: X      X-axis attributes (Min,Max,Name,IsLog) 
   @param: Y      Y-axis attributes (Min,Max,Name,IsLog)  
   @param: YB     Bottom (lower) panel attributes (Min,Max,Name,IsLog)  
   @author S.Chekanov (ANL)
  """

  if (X[0]>X[1]): print("X min larger than X max"); return;
  if (Y[0]>Y[1]): print("X min larger than X mas"); return;
  if (YB[0]>YB[1]): print ("X min larger than X mas"); return;

  inp="plot"
  if (len(sys.argv) ==2):
     inp = sys.argv[1]
  print "Mode=",inp

  c1=TCanvas("cv","",600,500);
  c1.Divide();
  c1.SetTickx()
  c1.SetTicky()
  gROOT.SetStyle("Plain");
  gStyle.SetOptStat(0);

  cv1= TPad("cv_a", "",0.0,0.20,1.0,1.0);
  cv1.SetTickx()
  cv1.SetTicky()
  cv1.SetTopMargin(0.05);
  cv1.SetBottomMargin(0.001);
  cv1.SetLeftMargin(0.12);
  cv1.SetRightMargin(0.05);
  cv1.Draw();
  cv2 = TPad("cv_b", "",0.0,0.0,1.0,0.275);
  cv2.SetTopMargin(0.0);
  cv2.SetTickx()
  cv2.SetTicky()
  cv2.SetLeftMargin(0.12);
  cv2.SetRightMargin(0.05);
  cv2.SetBottomMargin(0.35);
  cv2.Draw();

  if (Y[3]==1): cv1.cd().SetLogy();
  if (X[3]==1): cv1.cd().SetLogx();
  if (YB[3]==1): cv2.cd().SetLogy();

  h1=gPad.DrawFrame(X[0],Y[0],X[1],Y[1]);
  h1.Draw()
  ay=h1.GetYaxis(); ay.SetTitleOffset(1.1)
  ay.SetTitle( Y[2] );

  data.Draw("same pe")
  theory.Draw("histo same")

  #########################################
  #cv2.cd().SetGridy();
  cv2.cd().SetGridx();
  h2=gPad.DrawFrame(X[0],YB[0],X[1],YB[1]);
  h2.Draw()
  ax=h2.GetXaxis(); ax.SetTitleOffset(0.8)
  ax.SetTitle( X[2] );
  ax.SetLabelSize(0.12)
  ax.SetTitleSize(0.14)
  ay=h2.GetYaxis(); 
  #ay.SetTitle("OOOO" );
  ay.SetNdivisions(505);
  ay.SetLabelSize(0.12)
  ay.SetTitleSize(0.14)
  ax.SetTitleOffset(1.1); ay.SetTitleOffset(0.0)
  ax.Draw("same")
  ay.Draw("same")

  ratio.SetMarkerColor( 1 )
  ratio.SetMarkerStyle( 20 )
  ratio.SetMarkerSize( 1.0 )
  ratio.SetMarkerColor( 2 )

  # plot depending on style
  if (type(ratio)== TGraphErrors or type(ratio) == TGraph or type(ratio) == TGraphAsymmErrors ):
        ratio.Draw("P same")
  elif (type(ratio)== TH1F or type(ratio) == TH1D):
       ratio.SetFillColor(2);
       ratio.SetLineWidth(1);
       ratio.SetLineColor(1);
       ratio.Draw("same histo ][")
  else:
       ratio.Draw("P same")

  l1=TLatex()
  l1.SetTextAngle(90)
  l1.SetTextSize(0.12);
  l1.SetNDC();
  l1.SetTextColor(1);
  l1.DrawLatex(0.06,0.5,YB[2]);

  # draw line
  x1=c1.XtoPad(X[0])
  x2=c1.XtoPad(X[1])
  ar5=TLine(x1,0,x2,0);
  ar5.SetLineWidth(2)
  ar5.SetLineStyle(2)
  ar5.Draw("same")

  c1.Print(figure);

  if (inp != "-b"):
   if (raw_input("Press any key to exit") != "-9999"):
     c1.Close(); sys.exit(1)



def GetZVal(p, excess) :
  '''The function normal_quantile converts a p-value into a significance,
     i.e. the number of standard deviations corresponding to the right-tail of 
     Gaussian
  ''' 
  if excess:
    zval = Math.normal_quantile(1-p,1);
  else :
    zval = Math.normal_quantile(p,1);
  return zval

