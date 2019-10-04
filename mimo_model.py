#!/usr/bin/python
# -*- coding: utf-8 -*-

import estimators
import metrics
import statistics
import sys
import os
import math
import csv
import numpy as np
from time import sleep
from datetime import datetime
import subprocess
import copy

# Function definitions

def mimo(ans, total_exps, duration, qos, control_interval, N):
    # os.makedirs('./experiments/experiment-%s'%date)
    for exp in range(total_exps):
        a_min = [20, 20]
        a_max = [100, 100]
        sampling_point = 0
        samples = (duration-1)/control_interval
        # components addresses
        webserver = 'root@172.16.56.9'
        database = 'root@172.16.56.10'
        controller = 'root@172.16.56.14'
        vm_web_name = 'Tomcat'
        vm_db_name ='MySQL'
        # controller's variables
        P = np.array([[10, 0], [0, 10]])  # error matrix
        R = np.array([[1, 0], [0, 1]])  # measurement noise matrix
        Q = np.array([[4, 0], [0, 4]])  # process noise matrix
        K = np.array([[1, 1], [1, 1]])  # gain matrix
        C = np.array([[1, 0], [0, 1]])  # ECC'16: 0.95 , ETFA'17: 0.70
        # system model's variables
        a = np.array([100, 100])
        cap = [100, 100]
        y = np.array([0.0, 0.0])
        a_old = np.array([0.0, 0.0])
        a_mean = np.array([0.0, 0.0])
        a_hold_mean = np.array([0.0, 0.0])
        theta = 0.1  
        sigma = 1
        c_parameter = 0.8
        # archives
        archive_K = np.zeros((samples, 2))
        archive_a = np.zeros((duration, 2))
        archive_u = np.zeros((duration, 2))
        archive_alloc = np.zeros((samples, 2))
        archive_usage = np.zeros((samples, 2))
        archive_cap = np.zeros((duration, 2))
        archive_var = np.zeros((samples, 2))
        archive_sd = np.zeros((samples, 2))
        archive_cov = np.zeros(samples)
        archive_a_hold_mean = np.zeros((duration, 2))
        # statistics
        sliding_window_web = []
        sliding_window_db = []
        # average cpu usage
        avg_cpu = np.array([0.0, 0.0])
        
        print "\nStarting experiment no: %s" % (exp+1)               

        try:
          # initialize the allocation at 100% for domains 5 and 10
          os.system("ssh %s xl sched-credit -d %s -c %s" % (webserver, vm_web_name, a[0]))
          os.system("ssh %s xl sched-credit -d %s -c %s" % (database, vm_db_name, a[1]))
          # client connection and exit (install screen on remote machine)
          print "\nConnecting to Client..."
          sleep(30)
          print "\nConnection established!"

          # capture cpu usage every 1 sec for t secs for Tomcat and MySQL domains
          print "\nCPU usage%:"
          vm_web_cmd_record = "ssh " + webserver + " xentop -b -d 1 -i 2100 | awk '/" + vm_web_name + "/ {print $4 fflush(stdout) }' &"
          vm_web_record = subprocess.Popen(vm_web_cmd_record, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
          stdout = []

          vm_db_cmd_record = "ssh " + database + " xentop -b -d 1 -i 2100 | awk '/" + vm_db_name + "/ {print $4 fflush(stdout) }' &"
          vm_db_record = subprocess.Popen(vm_db_cmd_record, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
          stdout = []

          date = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
          open('/root/RUBiS/response.txt', 'w').close() # clear the response file for the new experiment

          with open("./experiments/log_sp_%s.txt" %date, 'w', newline='') as stlog:
              writer = csv.writer(stlog)
              writer.writerow(["k", "expid", "uweb", "udb", "aweb", "adb", "kweb", "kdb", "varweb", "vardb", "sdweb", "sddb", "cov", "mrt"])
              
          # convert string cpu usage into float and start estimator for (duration) seconds
          for t in range(duration):
            a_old = copy.deepcopy(a) # asigns the old value of y to y_old
            
            vm_web_line = vm_web_record.stdout.readline()
            stdout.append(vm_web_line)
            y[0] = float(vm_web_line)
            if vm_web_line == '' and vm_web_record.poll() is not None:
              break

            vm_db_line = vm_db_record.stdout.readline()
            stdout.append(vm_db_line)
            y[1] = float(vm_db_line)
            if vm_db_line == '' and vm_db_record.poll() is not None:
              break

            print "Measured cpu recourse usage: %s" %y

            if t % control_interval != 0:s
              a_mean = np.add(a_mean, a)

            # adapt the predicted allocation
            if t >= 1: # first measurement in Xen is always 0
              
              # calculate variance
              Q, sliding_window_web, sliding_window_db = statistics.covariance(N, t, y, a_old, sliding_window_web, sliding_window_db)

              # predict allocation using the filters
              if ans == '1':
                (a, P, K) = estimators.kalman_mimo(P, Q, R, C, y, a)  # Kalman MIMO
              elif ans == '2':
                (a, P, K) = estimators.hinf_mimo(P, Q, R, C, y, a, theta)  # Hinf MIMO
              elif ans == '3':
                (a, P, K) = estimators.mcc_kf_mimo(P, Q, R, C, y, a, sigma)  # MCC-KF MIMO
              print "Estimated cpu resources: %s" %a
              
              if t % control_interval == 0:
                if sampling_point == 20:
                  os.system("screen -d -m /root/add_workload.sh ")
      
                print "Sample: %s" %(sampling_point)
                a_mean = np.true_divide(np.add(a_mean, a), control_interval)

                # apply bounded allocations
                cap = capAllocation(cap, a_mean, a_min, a_max, c_parameter)
                print "Allocated cpu resources: %s\n" %cap
                os.system("ssh %s xl sched-credit -d %s -c %s" % (webserver, vm_web_name, cap[0]))  # set the predicted allocation (cpu cap)
                os.system("ssh %s xl sched-credit -d %s -c %s" % (database, vm_db_name, cap[1]))  # set the predicted allocation (cpu cap)
                
                archive_usage[sampling_point] = a_mean
                archive_alloc[sampling_point] = cap
                archive_K[sampling_point] = K[0,0], K[1,1]
                archive_var[sampling_point] = Q[0,0], Q[1,1]
                archive_sd[sampling_point] = math.sqrt(Q[0,0]), math.sqrt(Q[1,1])
                archive_cov[sampling_point] = Q[0,1]

                with open("./experiments/log_sp_%s.txt" %date, "a") as stlog:
                  stlog.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" %sampling_point
                      (datetime.now().strftime('%Y-%m-%d-%H:%M:%S'), 
                      archive_usage[sampling_point, 0],
                      archive_usage[sampling_point, 1],
                      archive_alloc[sampling_point, 0],
                      archive_alloc[sampling_point, 1],
                      archive_K[sampling_point, 0],
                      archive_K[sampling_point, 1],
                      archive_var[sampling_point, 0],
                      archive_var[sampling_point, 1],
                      archive_sd[sampling_point, 0],
                      archive_sd[sampling_point, 1],
                      archive_cov[sampling_point]))
                
                sampling_point += 1
                a_hold_mean = a_mean
                a_mean = 0

              # archives
              archive_u[t] = y
              archive_a[t] = a
              archive_cap[t] = cap
              archive_a_hold_mean[t] = a_hold_mean
              with open("./experiments/log_%s.txt" %date, "a") as stlog:
                stlog.write("%s,%s,%s,%s,%s,%s,%s\n" %(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'), 
                                                    archive_u[t, 0],
                                                    archive_u[t, 1],
                                                    archive_a[t, 0],
                                                    archive_a[t, 1],
                                                    archive_a_hold_mean[t, 0],
                                                    archive_a_hold_mean[t, 1]))

          sleep(3)
          sampling_point = 0
          # compute average cpu usage
          avg_cpu = archive_u.mean(axis=0)
          
          # compute mrt
          os.system("scp %s:/root/RUBiS/response.txt /root/viresa/response.txt" %controller)
          sleep(3)
          mrt = metrics.real_mrt_plot(ans,duration,date,avg_cpu,qos,control_interval)
          with open("./experiments/mrt_%s.txt" %date, mode="w") as mrtlog:
            for s in mrt:
              mrtlog.write("%s\n" % s)

        except IOError as e:
          print("\n({})\n".format(e))
          ans = True

def capAllocation(cap, a_mean, a_min, a_max, c_parameter):
    cap[0] = a_mean[0] * (1/c_parameter)
    cap[1] = a_mean[1] * (1/c_parameter)

    if cap[0] > a_max[0]:
      cap[0] = a_max[0]
    if cap[1] > a_max[1]:
      cap[1] = a_max[1]
    if cap[0] < a_mean[0]:
      cap[0] = a_mean[0]
    if cap[1] < a_mean[1]:
      cap[1] = a_mean[1]
    if cap[0] < a_min[0]:
      cap[0] = a_min[0]
    if cap[1] < a_min[1]:
      cap[1] = a_min[1]
  
    return cap