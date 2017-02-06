setwd("G:\\Projects\\UCLA\\WebInfo\\cleaned-version\\data")
not.installed <- function(pkg) !is.element(pkg, installed.packages()[,1])

if (not.installed("AppliedPredictiveModeling")) { 
    install.packages("AppliedPredictiveModeling", repos="http://cran.us.r-project.org")  
    library(AppliedPredictiveModeling)
    for (chapter in c(2,3,4,6,7,8,10, 11,12,13,14,16,17,19))  getPackages(chapter, repos="http://cran.us.r-project.org")
}

library(AppliedPredictiveModeling)
library(caret)
library(kernlab)
library(e1071)
library(ggplot2)
library(mice)
library(RANN)
library(missForest)