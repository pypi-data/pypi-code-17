#!/usr/bin/env python
# Time-stamp: <2017-04-25 00:19:00 Hongbo Liu>

"""Description: SMART main executable

Copyright (c) 2017 Hongbo Liu <hongbo919@gmail.com>

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD License (see the file COPYING included
with the distribution).

@status: release candidate
@version: 2.1.5
@author:  Hongbo Liu
@contact: hongbo919@gmail.com
"""
# ------------------------------------
# python modules
# dos2unix SMART
# ------------------------------------
import time
import os
import sys
import argparse
from DeNovoDMR_Calling import DeNovoDMR_Calling

def restricted_float_M(x):
    x = float(x)
    if x < 0.01 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.01, 1.0]"%(x,))
    return x

def restricted_float_G(x):
    x = float(x)
    if x < 0.5 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.5, 1.0]"%(x,))
    return x

def restricted_float_MSThreshold(x):
    x = float(x)
    if x < 0.2 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.2, 1.0]"%(x,))
    return x

def restricted_float_EDThreshold(x):
    x = float(x)
    if x < 0.2 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.01, 0.5]"%(x,))
    return x

def restricted_float_SMThreshold(x):
    x = float(x)
    if x < 0.2 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.01, 1.0]"%(x,))
    return x

def restricted_int_CDThreshold(x):
    x = int(x)
    if x < 1 or x > 2000:
        raise argparse.ArgumentTypeError("%r not in range [1, 2000]"%(x,))
    return x

def restricted_int_DLThreshold(x):
    x = int(x)
    if x < 1:
        raise argparse.ArgumentTypeError("%r should be larger than 1 bp"%(x,))
    return x

def restricted_int_pThreshold(x):
    x = float(x)
    if x < 1.0e-100 or x > 0.05:
        raise argparse.ArgumentTypeError("%r should be larger than 1 bp"%(x,))
    return x

# ------------------------------------
# Main function
# ------------------------------------
def main(argv):
    """The Main function/pipeline for SMART.
    """
    # Parse options...
    description = "%(prog)s 2.1 -- Specific Methylation Analysis and Report Tool for BS-Sequencing Data"
    epilog = "For any help, type: %(prog)s -h, or write to Hongbo Liu (hongbo919@gmail.com)"
    parser = argparse.ArgumentParser(description = description, epilog = epilog)
    parser.add_argument("MethylMatrix", type = str, default = '',
                        help = "The input methylation file (such as /WGBS/MethylMatrix.txt) including methylation values in all samples to compare (REQUIRED). The methylation data should be arranged as a matrix in which each row represents a CpG site. The columns are tab-separated. The column names should be included in the first line, with the first three columns representing the location of CpG sites: chrom, start, end. The methylation values starts from the fourth column. The names of samples should be given as G1_1,G1_2,G2_1,G2_2,G3_1,G3_2,G3_3, in which Gi represents group i. \nThe Methylation matrix can be build based on bed files (chrom start end betavalue) by bedtools as: bedtools unionbedg -i G1_1.bed G1_2.bed G2_1.bed  G2_2.bed  G3_1.bed   G3_2.bed   G3_3.bed -header -names G1_1 G1_2 G2_1 G2_2 G3_1 G3_2 G3_3 -filler - > MethylMatrix.txt. [Type: file]")
    parser.add_argument("-t", dest='ProjectType',type = str, choices=['DeNovoDMR','DMROI','DMC'], default = 'DeNovoDMR',
                        help = "Type of project including 'DeNovoDMR','DMROI' and 'DMC'. DeNovoDMR means de novo identification of differentially methylated regions (DMRs) based on genome segmentation. DMROI means the comparison of the methylation difference in regions of interest (ROIs) across multiple groups. DMC means identification of differentially methylated CpG sites (DMCs). DEFAULT: \'DeNovoDMR\' [Type: string]")
    parser.add_argument("-g", dest='GenomeRegions',type = str, default = '',
                        help = "Genome of regions of interest in bed format without column names (such as /WGBS/Regions_of_interest.bed) for project type DMROI. If this file is provided, SMART treat each region as a unit and compare its mean methylation across groups by methylation specificity and ANOVA analysis. DEFAULT: \'\' [Type: string]")
    parser.add_argument("-n", dest='ProjectName',type = str, default = "SMART",
                        help = "Project name, which will be used to generate output file names. DEFAULT: \"SMART\" [Type: string]")
    parser.add_argument("-o", dest='OutputFolder',type = str, default = '',
                        help = "The folder in which the result will be output. If specified all output files will be written to that directory. [Type: folder] [DEFAULT: the directory named using project name and current time (such as SMART20140801132559) in the current working directory]")
    parser.add_argument("-MR", dest='MissReplace',type = restricted_float_M, default = 0.5,
                        help = "Replace the missing value with the mediate methylation value of available samples in the corresponding group. The user can control whether to replace missing value by setting this parameter from 0.01 (meaning methylation values are available in at least 1%% of samples) to 1.0 (meaning methylation values are available in 100%% of samples). [Type: float] [Range: 0.01 ~ 1.0] [DEFAULT: 0.5]")
    parser.add_argument("-MS", dest='MSthreshold',type = restricted_float_MSThreshold, default = 0.5,
                        help = "Methylation Specificity Threshold for DMC or DMR calling. This parameter can be used to identify DMC or DMR as the the CpG site or region with methylation specificity which is greater than the threshold. [Type: float] [Range: 0.2 ~ 1.0] [DEFAULT: 0.5]")
    parser.add_argument("-ED", dest='EDthreshold',type = restricted_float_EDThreshold, default = 0.2,
                        help = "Euclidean Distance Threshold for methylation similarity between neighboring CpGs which is used in genome segmentation for de novo identification of DMR. The methylation similarity between neighboring CpGs is high if the Euclidean distance is less than the threshold. [Type: float] [Range: 0.01 ~ 0.5] [DEFAULT: 0.2]")
    parser.add_argument("-SM", dest='SMthreshold',type = restricted_float_SMThreshold, default = 0.6,
                        help = "Similarity Entropy Threshold for methylation similarity between neighboring CpGs which is used in genome segmentation for de novo identification of DMR. The methylation similarity between neighboring CpGs is high if similarity entropy is less than the threshold. [Type: float] [Range: 0.01 ~ 1.0] [DEFAULT: 0.6]")
    parser.add_argument("-CD", dest='CDthreshold',type = restricted_int_CDThreshold, default = 500,
                        help = "CpG Distance Threshold for the maximal distance between neighboring CpGs which is used in genome segmentation for de novo identification of DMR. The neighboring CpGs will be merged if the distance less than this threshold. [Type: int] [Range: 1 ~ 2000] [DEFAULT: 500]")
    parser.add_argument("-SC", dest='SCthreshold',type = restricted_int_DLThreshold, default = 5,
                        help = "Segment CpG Number Threshold for the minimal number of CpGs of merged segment and de novo identified DMR. The segments/DMRs with CpG number larger than this threshold will be output for further analysis. [Type: int] [Range: > 1] [DEFAULT: 5]")
    parser.add_argument("-SL", dest='SLthreshold',type = restricted_int_DLThreshold, default = 20,
                        help = "Segment Length Threshold for the minimal length of merged segment and de novo identified DMR. The segments/DMRs with a length larger than this threshold will be output for further analysis. [Type: int] [Range: > 1] [DEFAULT: 20]")
    parser.add_argument("-pD", dest='p_DMR',type = restricted_int_pThreshold, default = 0.05,
                        help = "p value of one-way analysis of variance (ANOVA) which is carried out for identification of DMRs across multiple groups. The segments with p value less than this threshold are identified as DMR. [Type: float] [Range: 1.0e-100 ~ 0.05] [DEFAULT: 0.05]")
    parser.add_argument("-pM", dest='p_MethylMark',type = restricted_int_pThreshold, default = 0.05,
                        help = "p value of one sample t-test which is carried out for identification of Methylation mark in a specific group based on the identified DMRs. The DMRs with p value less than this threshold is identified as group- specific methylation mark (Hyper methylation mark or Hypo methylation mark). [Type: float] [Range: 1.0e-100 ~ 0.05] [DEFAULT: 0.05]")
    parser.add_argument("-v", "--version",dest='version',action='version', version='SMATR 2.1.5')
        
    UserArgs = parser.parse_args()
    MethyData=UserArgs.MethylMatrix
    ProjectType=UserArgs.ProjectType
    GenomeRegions=UserArgs.GenomeRegions
    ProjectName=UserArgs.ProjectName
    OutFolder=UserArgs.OutputFolder
    MissReplace=UserArgs.MissReplace
    MSthreshold=UserArgs.MSthreshold
    EDthreshold=UserArgs.EDthreshold
    SMthreshold=UserArgs.SMthreshold
    CDthreshold=UserArgs.CDthreshold
    SCthreshold=UserArgs.SCthreshold
    SLthreshold=UserArgs.SLthreshold
    p_DMR=UserArgs.p_DMR
    p_MethylMark=UserArgs.p_MethylMark
    UserArgslist = str(vars(UserArgs))
    
    if (MethyData==''):
        sys.exit( "[Error:] Methylation data is needed. Please re-run it giving the location of the methylation data.")
    if (MethyData):
        if not os.path.exists( MethyData ):
                sys.exit( "[Error:] Methylation data directory (%s) could not be found. Please re-run it giving the correct location of the methylation data." % MethyData )
                
        if (OutFolder==''):
            homedir = os.getcwd()
            Starttime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
            OutFolder=homedir+"/"+ProjectName+Starttime+"/"
            #print OutFolder
        if OutFolder:
            # use a output directory to store SMART output
            if OutFolder[-1]!='/':
                OutFolder=OutFolder+'/'
            
            if not os.path.exists( OutFolder ):
                try:
                    os.makedirs( OutFolder )
                except:
                    sys.exit( "[Error:] Output directory (%s) could not be created. Terminating program." % OutFolder )            
        
                
        if ProjectType == 'DeNovoDMR':
            DeNovoDMR_Callingrun=DeNovoDMR_Calling()
            DeNovoDMR_Callingrun.runDeNovo(UserArgslist,MethyData,ProjectName,MissReplace,MSthreshold,EDthreshold,SMthreshold,CDthreshold,SCthreshold,SLthreshold,p_DMR,p_MethylMark,OutFolder)
        elif ProjectType == 'DMROI':
            if (GenomeRegions==''):
                sys.exit( "[Error:] Genome Regions is needed. Please re-run it giving the location of the bed file for Genome Regions.")
            if (GenomeRegions):
                if not os.path.exists( GenomeRegions ):
                        sys.exit( "[Error:] Genome Regions file (%s) could not be found. Please re-run it giving the correct location of the bed file for Genome Regions." % GenomeRegions )
            DeNovoDMR_Callingrun=DeNovoDMR_Calling()
            DeNovoDMR_Callingrun.runDMROI(UserArgslist,MethyData,ProjectName,MissReplace,GenomeRegions,MSthreshold,EDthreshold,SMthreshold,CDthreshold,SCthreshold,SLthreshold,p_DMR,p_MethylMark,OutFolder)    
            
        elif ProjectType == 'DMC':
            DeNovoDMR_Callingrun=DeNovoDMR_Calling()
            DeNovoDMR_Callingrun.runDMC(UserArgslist,MethyData,ProjectName,MissReplace,MSthreshold,EDthreshold,SMthreshold,CDthreshold,SCthreshold,SLthreshold,p_DMR,p_MethylMark,OutFolder)
        else:
            sys.exit( "[Error:] Project Type (%s) is not supported. Please re-run it giving the correct project type 'DeNovoDMR','DMROI' or 'DMC'. " % ProjectType )
        


if __name__ == '__main__':
    main(sys.argv)
