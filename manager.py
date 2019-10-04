#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 16:56:08 2015

@author: Evagoras Makridis
"""
import math
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import sys
import subprocess
from time import sleep
from datetime import datetime
from cStringIO import StringIO
import operation
import estimators
import metrics
import statistics
from datetime import datetime
from multiprocessing import Process

# os.system('clear')
# Global Parameters: 
time = 251 # 250 seconds
delay = 1  # the first measurement of cpu usage is always 0 because of Xen
qos = 0.5  # Quality of Service in seconds (0.5 = 500ms)
N = 10  # variance and covariance window
timelist = np.zeros(time)  # keep timing logs
w = 0
a_min = 20
a_max = 100

vm_name = sys.argv[1]
a = sys.argv[2]
ans = sys.argv[3]
date = sys.argv[4]

def set_initial_allocation(vm_name, a):
  # initialize the allocation at 100% on domain (eg. -d 1 for domain 1)
  os.system("xl sched-credit -d %s -c %s" %(vm_name,a))
  # connection to Client Server & begin Client Emulator (workload generation)
  print "\nConnecting to Client..."
  # client connection and exit (install screen on remote machine)
  sleep(30)
  os.system("ssh root@10.190.12.56 screen -d -m /root/initialize.sh")

def update_allocation(time, delay, date, qos, N, timelist, w, a_min, a_max, a, ans, vm_name):
  real_data = 0
  # control interval
  ca = 5 # control action interval every 5s
  sp = 0 # sampling point
  # variables for Kalman SISO, Hinf SISO, MCC-KF SISO
  K = 1
  F = 1
  P = 10
  R = 1
  Q = 4
  c = 0.8  # ECC'16: 0.95 , ETFA'17: 0.70
  # set the initial required demand (D) and initialize CPU usage (u)
  D = 50
  u = D
  y_mean = 0
  y_hold = 0
  # set the max allocation
  cap = 100
  # allocation and usage logs
  a_in = np.zeros((time, np.size(a)))
  obs = np.zeros((time, np.size(a)))
  a_out = np.zeros((time, np.size(a)))
  obs_win = []
  # for average cpu usage
  cntr = sum_cpu = avg_cpu = 0
  # define archives
  archive_var = np.zeros((time, np.size(a)))
  archive_a = np.zeros((time, np.size(a)))
  archive_K = np.zeros((time, np.size(a)))
  archive_u = np.zeros((time, np.size(u)))
  archive_D = np.zeros((time, np.size(D)))
  archive_yhold = np.zeros((time, np.size(a)))
  archive_usag = np.zeros((time, np.size(a)))
  archive_alloc = np.zeros((time, np.size(a)))
  archive_vr = np.zeros((time, np.size(a)))
  archive_K = np.zeros((time, np.size(a)))
  # variance error
  qerr = np.zeros(time)
  var1 = 0
  var2 = 0
  cov = 0
  # usage
  usages = np.zeros(time)

  # capture cpu usage every 1 sec for 300 secs for component
  print "\nCPU usage%:"
  cmd1 = "xentop -b -d 1 -i 300 | awk '/%s/ {print $4 fflush(stdout) }' &" %vm_name
  p1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  stdout = []

  # capture current cpu allocation
  cmd2 = "xl sched-credit | awk '/%s/ {print $4} '" %vm_name
  p2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, shell=True)
  a_string = p2.stdout.readline()
  a = int(a_string)

  # convert string cpu usage into float and start estimator for (time) seconds
  for t in range(time):
    line = p1.stdout.readline()
    stdout.append(line)
    y = float(line)

    if line == '' and p.poll() is not None:
      break
    print "Current cpu usage: %d" %y

    a_in[t] = a  # save current allocation
    obs[t] = y  # save current observed utilization
    usages[t] = y

    if t % ca != 0:
      y_mean = y_mean + y

    if t >= delay:
      # calculate variance
      Q, obs_win = statistics.variance(N,t,y,obs_win)
      if t == delay:
        qerr[t] = 0
      else:
        qerr[t] = math.sqrt(Q)

      if t % ca == 0:
        sp = sp + 1
        y_mean = (y_mean+y) / ca

        # allocation prediction using the filters
        if ans == '1':
          (a, P, K) = estimators.kalman_siso(P, Q, R, c, y_mean, a)  # Kalman SISO
        elif ans == '2':
          (a, P, K) = estimators.hinf_siso(P, Q, R, c, y_mean, a)  # Hinf SISO
        elif ans == '3':
          (a, P, K) = estimators.mcc_kf_siso(P, Q, R, c, y_mean, a)  # MCC-KF SISO
  
        print "Predicted cpu allocation: %.2f" %a
        cap = a
        if cap > a_max: # a_max = 100
          cap = a_max
        if cap < y:
          cap = y
        if cap < a_min: # a_min = 20
          cap = a_min
          
        cntr += 1
        sum_cpu = sum_cpu + y
        a_out[t] = a  # save predicted allocation
        
        # adapt the predicted allocation
        os.system("xl sched-credit -d %s -c %s" %(vm_name, cap))  # set the predicted allocation (cpu cap)
    
        archive_usag[sp] = y_mean
        archive_alloc[sp] = cap
        archive_K[sp] = K
        archive_vr[sp] = Q

        with open("/root/viresa/experiments/log_sp_%s.txt" %date, "a") as stlog:
          stlog.write("%s,%.2f,%.2f,%.2f,%.2f\n" %(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'),archive_usag[sp],archive_alloc[sp],archive_K[sp],archive_vr[sp]))
        
        y_hold = y_mean   
        y_mean = 0
      
      # archives
      archive_a[t] = cap
      archive_u[t] = y
      archive_D[t] = y
      archive_var[t] = Q
      timelist[t] = t
      archive_yhold[t] = y_hold
     
      # add workload/clients
      if vm_name == 'Tomcat' and t == 50:
        os.system("ssh root@10.190.12.56 screen -d -m /root/add_clients.sh ")
      if vm_name == 'MySQL' and t == 150:
        os.system("ssh root@10.190.12.56 screen -d -m /root/add_clients.sh ")
      
      with open("/root/viresa/experiments/log_%s.txt" %date, "a") as stlog:
        stlog.write("%s,%.2f,%.2f,%.2f,%.2f\n" %(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'),archive_u[t],archive_a[t],archive_var[t],archive_yhold[t]))
      
  # compute average cpu usage after delay
  avg_cpu = sum_cpu / cntr
  # compute average usage variance
  var1 = np.var(usages)
  # compute mrt
  os.system("scp root@10.190.12.56:/root/RUBiS/response.txt /root/viresa/response.txt")
  sleep(10)
  mrt = metrics.real_mrt_plot(ans,time,date,avg_cpu,var1,var2,cov,qos,ca)
  with open("/root/viresa/experiments/mrt_%s.txt" %date, mode="w") as mrtlog:
    for s in mrt:
      mrtlog.write("%s\n" % s)

set_initial_allocation(vm_name, a)
update_allocation(time, delay, date, qos, N, timelist, w, a_min, a_max, a, ans, vm_name)
