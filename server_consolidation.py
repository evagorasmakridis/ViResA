#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 16:56:08 2015
Edited on Fri May 25 01:01:50 2018
@author: Dr. Kyriakos M. Deliparaschos
@author: Evagoras Makridis
"""

import mimo_model
import metrics
import os
from time import sleep

# Global experiment parameters: 
total_exps = 20
duration = 251 # seconds
qos = 0.5  # QoS in seconds
control_interval = 5
samples = (duration-1)/control_interval
N = 25
ans = True

while ans:
    menulist = '''\nChoose a controller from the menu ('q' to quit).
      1  - Kalman MIMO
      2  - Hinf MIMO
      3  - MCC-KF MIMO
      q  - Quit'''
    print menulist
    ans = raw_input('\033[93m' + '#? ' + '\033[0m')

    # initialize variables
    if ans == '1' or ans == '2' or ans == '3':
      if not (os.path.isdir('./experiments')):
        os.makedirs('./experiments')

      print "\nGenerating workload..."
      os.system("screen -d -m /root/start_workload.sh ")
      sleep(20)
      print "\nWorkload has been generated!"

      mimo_model.mimo(ans, total_exps, duration, qos, control_interval, N)
      ans = False

    elif ans == 'q':
      print('\nGood bye!')
      ans = None

    else:
      print('\033[91m' + '\nInvalid option. Try another one!\n' + '\033[0m')
      ans = True