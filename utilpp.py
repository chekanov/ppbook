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

  if (X[0]>X[1]): print("X min larger than X max"); return
  if (Y[0]>Y[1]): print("X min larger than X mas"); return
  if (YB[0]>YB[1]): print ("X min larger than X mas"); return

  inp="plot"
  if (len(sys.argv) ==2):
     inp = sys.argv[1]
  print "Mode=",inp

  c1=TCanvas("cv","",600,500)
  c1.Divide()
  c1.SetTickx()
  c1.SetTicky()
  gROOT.SetStyle("Plain")
  gStyle.SetOptStat(0)

  cv1= TPad("cv_a", "",0.0,0.20,1.0,1.0)
  cv1.SetTickx()
  cv1.SetTicky()
  cv1.SetTopMargin(0.05)
  cv1.SetBottomMargin(0.001)
  cv1.SetLeftMargin(0.12)
  cv1.SetRightMargin(0.05)
  cv1.Draw()
  cv2 = TPad("cv_b", "",0.0,0.0,1.0,0.275)
  cv2.SetTopMargin(0.0)
  cv2.SetTickx()
  cv2.SetTicky()
  cv2.SetLeftMargin(0.12)
  cv2.SetRightMargin(0.05)
  cv2.SetBottomMargin(0.35)
  cv2.Draw()

  if (Y[3]==1): cv1.cd().SetLogy()
  if (X[3]==1): cv1.cd().SetLogx()
  if (YB[3]==1): cv2.cd().SetLogy()

  h1=gPad.DrawFrame(X[0],Y[0],X[1],Y[1])
  h1.Draw()
  ay=h1.GetYaxis(); ay.SetTitleOffset(1.1)
  ay.SetTitle( Y[2] )

  data.Draw("same pe")
  theory.Draw("histo same")

  #########################################
  #cv2.cd().SetGridy()
  cv2.cd().SetGridx()
  h2=gPad.DrawFrame(X[0],YB[0],X[1],YB[1])
  h2.Draw()
  ax=h2.GetXaxis(); ax.SetTitleOffset(0.8)
  ax.SetTitle( X[2] )
  ax.SetLabelSize(0.12)
  ax.SetTitleSize(0.14)
  ay=h2.GetYaxis() 
  #ay.SetTitle("OOOO" )
  ay.SetNdivisions(505)
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
       ratio.SetFillColor(2)
       ratio.SetLineWidth(1)
       ratio.SetLineColor(1)
       ratio.Draw("same histo ][")
  else:
       ratio.Draw("P same")

  l1=TLatex()
  l1.SetTextAngle(90)
  l1.SetTextSize(0.12)
  l1.SetNDC()
  l1.SetTextColor(1)
  l1.DrawLatex(0.06,0.5,YB[2])

  # draw line
  x1=c1.XtoPad(X[0])
  x2=c1.XtoPad(X[1])
  ar5=TLine(x1,0,x2,0)
  ar5.SetLineWidth(2)
  ar5.SetLineStyle(2)
  ar5.Draw("same")

  c1.Print(figure)

  if (inp != "-b"):
   if (raw_input("Press any key to exit") != "-9999"):
     c1.Close(); sys.exit(1)



def GetZVal(p, excess) :
  '''The function normal_quantile converts a p-value into a significance,
     i.e. the number of standard deviations corresponding to the right-tail of 
     Gaussian
  ''' 
  if excess:
    zval = Math.normal_quantile(1-p,1)
  else :
    zval = Math.normal_quantile(p,1)
  return zval



'''
  p-value for Poisson distribution when there is uncertainty on the
  parameter
  -----------------------------------------------------------------
  Diego Casadei <casadei@cern.ch>  6 Nov 2011
  Last update: 3 Mar 2012 (logarithms used only for big numbers)
  -----------------------------------------------------------------
  Consider Poi(k|nExp) and compute the p-value which corresponds to
  the observation of nObs counts, in the case of uncertain nExp whose
  variance is provided.

  The prior for nExp is a Gamma density which matches the expectation
  and variance provided as input.  The marginal model is provided by
  the Poisson-Gamma mixture, which is used to compute the p-value.

  Gamma density: the parameters are
   * a = shape param  [dimensionless]
   * b = rate param   [dimension: inverse of x]

    nExp ~ Ga(x|a,b) = [b^a/Gamma(a)] x^{a-1} exp(-bx)

  One has E[x] = a/b and V[x] = a/b^2 hence
   * b = E/V
   * a = E*b

  The integral of Poi(n|x) Ga(x|a,b) over x gives the (marginal)
  probability of observing n counts as

                b^a [Gamma(n+a) / Gamma(a)]
    P(n|a,b) = -----------------------------
                       n! (1+b)^{n+a}

  When nObs > nExp there is an excess of observed events and

    p-value = P(n>=nObs) = \sum_{n=nObs}^{\infty} P(n)
            = 1 - \sum_{n=0}^{nObs-1} P(n)

  Otherwise (nObs <= nExp) there is a deficit and

    p-value = P(n<=nObs) = \sum_{n=0}^{nObs} P(n)

  To compute the sum, we use the following recurrent relation:

    P(n=0) = [b/(1+b)]^a
    P(n=1) = [b/(1+b)]^a a/(1+b) = P(n=0) a/(1+b)
    P(n=2) = [b/(1+b)]^a a/(1+b) (a+1)/[2(1+b)] = P(n=1) (a+1)/[2(1+b)]
    ...        ...
    P(n=k) = P(n=k-1) (a+k-1) / [k(1+b)]

  and to avoid rounding errors, we work with logarithms.
'''

# nObs,observed counts
# E expected counts
# V variance of expectation
def pValuePoissonError(nObs,E,V):

  if (E<=0 or V<=0): 
    print("ERROR in pValuePoissonError(): expectation and variance must be positive. ")
    print("Returning 0.5")
    return 0.5

  B = E/V
  A = E*B
  nObs=int(nObs)

  if (A>100):  #  need to use logarithms
    stop=nObs 
    if (nObs>E): --stop
    #NB: must work in log-scale otherwise troubles!
    logProb = A*math.log(B/(1+B))
    sum=math.exp(logProb)#  P(n=0)
    for u in range(1,stop+1):
      logProb += math.log((A+u-1)/(u*(1+B)))
      sum += math.exp(logProb)
    if (nObs>E): #  excess
      return 1-sum
    else:  #  deficit
      return sum

  else:
    # Recursive formula: P(nA,B) = P(n-1A,B) (A+n-1)/(n*(1+B))
    p0 = math.pow(B/(1+B),A) # P(0A,B)
    nExp = A/B
    if (nObs>nExp): #  excess
      pLast = p0
      sum = p0
      for k in range(1,nObs):
        p = pLast * (A+k-1) / (k*(1+B))
        # cout << Form("Excess: P(%d%8.5g) = %8.5g and sum = %8.5g",k-1,nExp,pLast,sum) << " -> "
        sum += p
        pLast = p
        #cout << Form("P(%d%8.5g) = %8.5g and sum = %8.5g",k,nExp,pLast,sum) << endl
      return 1-sum
    else: #  deficit
      pLast = p0
      sum = p0
      for k in range(1,nObs+1):
        #cout << Form("Deficit: P(%d%8.5g) = %8.5g and sum = %8.5g",k-1,nExp,pLast,sum) << " -> "
        p = pLast * (A+k-1) / (k*(1+B))
        sum += p
        pLast = p
        #cout << Form("P(%d%8.5g) = %8.5g and sum = %8.5g",k,nExp,pLast,sum) << endl
    return sum
 
