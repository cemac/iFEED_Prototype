#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 12:40:46 2020

Data Collator

Combines data for iFEED runs into single country-level files.

@author: chmcsy
"""

import iris
import os
import rcp_collator as rcpcol
import errlib

countries={
        "malawi":0,
        "safrica":1,
        "tanzania":2,
        "zambia":3
        }
crops={
      "maize":0,
      "potato":1,
      "soybean":2
      }
models={
       "bcc-csm1-1":0,
       "bcc-csm1-1-m":1,
       "BNU-ESM":2,
       "CanESM2":3,
       "CNRM-CM5":4,
       "CSIRO-Mk3-6-0":5,
       "GFDL-CM3":6,
       "GFDL-ESM2G":7,
       "GFDL-ESM2M":8,
       "IPSL-CM5A-LR":9,
       "IPSL-CM5A-MR":10,
       "MIROC5":11,
       "MIROC-ESM":12,
       "MIROC-ESM-CHEM":13,
       "MPI-ESM-LR":14,
       "MPI-ESM-MR":15,
       "MRI-CGCM3":16,
       "NorESM1-M":17
       }
rcps={
     "rcp26":0,
     "rcp85":2
     }

innerproc = 8

outpth='/nfs/a101/chmcsy/ncouts'

datadir='/nfs/a101/earsj/glamOuts/africap/DIMlookup/rawouts'

def dirverify(iopath, inout):
    
    if not os.path.exists(iopath):
        if inout == "output":
            print('Directory for netCDF output does not exist\n')
            try:
                os.makedirs(iopath)
            except:
                raise errlib.FileError("Unable to create output folder")
            else:
                print ("Folder {} was created".format(iopath))
        else:
            raise errlib.FileError('Directory for netCDF output does not exist\n')
            

    if iopath and not os.path.isdir(iopath):
        	raise errlib.ArgumentsError('NetCDF '+inout+' location is not a directory\n')
       
def filesincountry(country):
    
    countrylst = []
    for crop in crops.keys():
        for model in models.keys():
            for rcp in rcps.keys():
                countrylst.append(os.path.join(datadir,country,crop,model,rcp))
                
    for path in countrylst:
        if not os.path.exists(path):
            countrylst.remove(path)
            print (path)
            continue
        if len(os.listdir(os.path.join(path,'2025'))) == 0:
            countrylst.remove(path)
            print (path)

    return countrylst

def rcp (ascdir):
    
    if ascdir[-1]=="/":
        simval=ascdir.split('/')[-5:-1]
    else:    
        simval=ascdir.split('/')[-4:]
        ascdir=ascdir+"/"
    
    yrs=rcpcol.getyrs(ascdir)
    
    dimvals=[]
    
    if simval[0] in countries:
        dimvals.append(countries[simval[0]])
    else:
        raise errlib.ArgumentsError("Unrecognised country in file path : %s\n" % simval[0])        
    
    if simval[1] in crops:
        dimvals.append(crops[simval[1]])
    else:
        raise errlib.ArgumentsError("Unrecognised crop in file path : %s\n" % simval[1])
        
    if simval[2] in models:
        dimvals.append(models[simval[2]])
    else:
        raise errlib.ArgumentsError("Unrecognised model in file path : %s\n" % simval[2])
        
    if simval[3] in rcps:
        dimvals.append(rcps[simval[3]])
    else:
        raise errlib.ArgumentsError("Unrecognised rcp in file path : %s\n" % simval[3])
    
    indata=[yrs,ascdir,simval,innerproc,dimvals]
    
    yrs=rcpcol.getyrs(ascdir)
    
    if len(yrs) == 0:
        raise errlib.FatalError("No yearly folders found in {}\n".format(ascdir))

    if innerproc > 1:
        
        rcp_cube=rcpcol.multiprocess_rcp(indata)
            
    else:
        
        rcp_cube=rcpcol.singleprocess_rcp(indata)
    
    outrcpcube(rcp_cube, simval)
        
    #return rcp_cube

def outrcpcube(cube, simval):
    
    outfol = os.path.join(outpth,"ind_rcp",simval[0])
    
    try:
        os.makedirs(outfol)
    except FileExistsError:
        # directory already exists
        pass
    
    fname = os.path.join(outfol,"_".join(simval[1:])+".nc")
    
    iris.fileformats.netcdf.save(cube, fname, zlib=True)
    
def combinercp(country):
    
    filnms = os.path.join(outpth,"ind_rcp",country,"*.nc")
    
    return iris.load(filnms)

def singlecountry (dirlst,country):
    
    print ("Collecting and merging data for {}".format(country))
    
    bigcubelist=iris.cube.CubeList([])
    
    for direc in dirlst:
        rcp(direc)
        
    bigcubelist = combinercp(country)
    
    outcubelst=bigcubelist.concatenate()
    
    return outcubelst

def main():
    
    dirverify(datadir,"input")
    
    os.chdir(datadir)
    
    dirverify(outpth, "output")
       
    for country in countries.keys():
        
        dirlst=filesincountry(country)
        
        cubelst=iris.cube.CubeList([])
        
        cubelst=singlecountry(dirlst,country)
            
        print ("Cube output for %s\n" % country)
        print (cubelst[0])
        
        outfil = os.path.join(outpth,country+'.nc')

        try:
            iris.fileformats.netcdf.save(cubelst, outfil, zlib=True)
        except:
            raise errlib.NonFatal("Could not output the cube for %s" % country)      
        
if __name__=="__main__":
    main()    

    
        
        
        
    