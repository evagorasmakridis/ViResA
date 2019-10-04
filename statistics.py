#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  10 10:36:14 2017

@author: Evagoras Makridis
"""

import numpy as np
import math

def variance(N, data, y_new, y_old, sw): # sw: sliding window
  QN = 0.0
  z = y_new - y_old
  if data > N:
    sw = sw[1:] + [z]
    QN = np.var(sw)
  else:
    sw.append(z)
    QN = np.var(sw)
  return QN, sw

def covariance(N, data, y_new, y_old, sw_web, sw_db): # sw: sliding window
  QN = 0.0
  z = np.subtract(y_new,y_old)
  if data > N:
    sw_web = sw_web[1:] + [z[0]]
    sw_db = sw_db[1:] + [z[1]]
    QN = np.cov(sw_web, sw_db, ddof=1)
  else:
    sw_web.append(z[0])
    sw_db.append(z[1])
    QN = np.cov(sw_web, sw_db, bias=1)
  return QN, sw_web, sw_db




