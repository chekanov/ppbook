# pyROOT utility classes used for "Data Analysis Techniques in Particle Physics"
# https://handwiki.org/wiki/Physics:PP/Start
# S.Chekanov (ANL)

import sys,os,math 
from ROOT import gROOT,gStyle,TH1D,TH1F,gPad,TPad,TCanvas,TLine,TPostScript,TLatex 
from ROOT import Math,TFile,TGraphErrors, TGraph, TGraphAsymmErrors

def showme(data,theory,ratio,Xmin=0.01,Xmax=1000,Ymin=0.001,Ymax=5000,BMin=-1.99, BMax=1.99, titX="X",titY="Y",titR="Ratio"):
  """A function to draw and and theory as well as their ratio. S.Chekanov
   @param: data   Histogram with data 
   @param: theory Histogram with theory
   @param: ratio  TGraph with for buttom plot
   @param: Xmin, Xmax - Min and Max values of X-axis
   @param: Ymin, Ymax - Min and Max values of Y-axis
   @param: Bmin, Bmax - Min and Max values of Y-axis of bottom plot
   @param titX, titY, titR - labels
   @author S.Chekanov (ANL)
  """

  inp="plot"
  if (len(sys.argv) ==2):
     inp = sys.argv[1]
  print "Mode=",inp

  # prepare the canvas
  epsfig=__file__.replace(".py",".eps")

  c1=TCanvas("cv","",600,500);
  ps1 = TPostScript( epsfig,113)
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

  cv1.cd().SetLogy();

  h1=gPad.DrawFrame(Xmin,Ymin,Xmax,Ymax);
  h1.Draw()
  ay=h1.GetYaxis(); ay.SetTitleOffset(1.1)
  ay.SetTitle( titY );

  data.Draw("same pe")
  theory.Draw("histo same")

  #########################################
  #cv2.cd().SetGridy();
  cv2.cd().SetGridx();
  h2=gPad.DrawFrame(Xmin,BMin,Xmax,BMax);
  h2.Draw()
  ax=h2.GetXaxis(); ax.SetTitleOffset(0.8)
  ax.SetTitle( titX );
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
  l1.DrawLatex(0.06,0.5,titR);

  # draw line
  x1=c1.XtoPad(Xmin)
  x2=c1.XtoPad(Xmax)
  ar5=TLine(x1,0,x2,0);
  ar5.SetLineWidth(2)
  ar5.SetLineStyle(2)
  ar5.Draw("same")

  print epsfig
  ps1.Close()

  if (inp != "-b"):
   if (raw_input("Press any key to exit") != "-9999"):
     c1.Close(); sys.exit(1);
