#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 23:52:18 2015
Edited on Tue Jan 25 14:40:24 2018

@author: Dr. Kyriakos M. Deliparaschos
@author: Mr. Evagoras Makridis
"""

from __future__ import division
import numpy as np
from itertools import imap
import math
import matplotlib.ticker as mtick
import decimal
import os
import subprocess
import csv
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Function definitions

# This function plots the real mRT
def real_mrt_plot(controller,total_duration,date,avg_cpu,qos,control_interval):
  QoS = qos * 1000
  avg_mrt = 0
  CR = 0 # number of completed requests
  NR = 0.0 # ratio of mrt <= 1
  file_directory = '/root/viresa/response.txt'
  sampling = str(control_interval) + 's'

  # read the last timestamp from file
  with open (file_directory,"r") as response_file:
    lines = response_file.readlines()
    CR =  len(lines)
  response_file.close()

  data = pd.read_csv(file_directory, sep=",", header=None)
  data.columns = ["timestamps", "rts"]
  data['timestamps'] = pd.to_datetime(data['timestamps'], unit='ms')
  data = data.set_index(['timestamps'])
  rts = data.rts.resample(sampling).mean()
  mrts = rts.values.tolist()

  #mrts[:] = [x / 1000 for x in mrts] # divides each list element (mrt) by 1000 
  NR = sum(1 for i in mrts if i < QoS) / len(mrts) # ratio of mRTs < QoS target
  avg_mrt = sum(mrts)/(total_duration/control_interval)

  if controller == '1' or controller == '2' or controller == '3':
    with open("stats_mimo.txt", "a") as stats_file:
      stats_file.write("%s,%s,%s,%.3f,%d,%.2f\n" %(date, avg_cpu[0], avg_cpu[1], avg_mrt, CR, NR))
    stats_file.close()
    
  return mrts