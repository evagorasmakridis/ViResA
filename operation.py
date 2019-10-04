#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 17:07:45 2015

@author: Dr. Kyriakos M. Deliparaschos
"""

import numpy as np
import os
import math

Qd = 2*[0]
# Function definitions

# This function changes the demand throughout the operation of the system
def demand(control, t, time, D, demand_scheme, q, random_gen, Q):
    if demand_scheme == 1:
        if control == '1' or control == '3' or control == '5':
            # change the workload at specific time instants
            if t == 30:
                D = 100
            elif t == 50:
                D = 30

            if random_gen == 1:
                D = D + (np.sqrt(Q) * np.random.standard_normal(1) + q)
            elif random_gen == 2:
                D = D + (np.sqrt(Q) * (1 - 2 * np.random.uniform(0, 1)) + q)
            else:
                print("Choose a valid noise distribution (1,2)!")
                return

        elif control == '2' or control == '4' or control == '6':
            print("Not implemented yet!")
            return

        else:
            print("Choose a valid control option (1-8)!")
            return

    elif demand_scheme == 2:
        if control == '1' or control == '3' or control == '5':
            # change the workload at specific time instants
            if 20 <= t < 50:
                D = 0.6 - 0.01 * (t - 20)
            elif t >= 50 or t < 80:
                D = 0.3 + 0.01 * (t - 50)
            elif 80 <= t <= time:
                D = 0.6

            if random_gen == 1:
                D = D + (np.sqrt(Q) * np.random.standard_normal(1) + q)
            elif random_gen == 2:
                D = D + (np.sqrt(Q) * (1 - 2 * np.random.uniform(0, 1)) + q)
            else:
                print("Choose a valid noise distribution (1,2)!")
                return

        elif control == '2' or control == '4' or control == '6':
            print("Not implemented yet!")
            return

        else:
            print("Choose a valid control option (1-8)!")
            return

    elif demand_scheme == 3:
        if control == '1' or control == '3' or control == '5':
            if random_gen == 1:
                D = D + (np.sqrt(Q) * np.random.standard_normal(1) + q)
            elif random_gen == 2:
                D = D + (np.sqrt(Q) * (1 - 2 * np.random.uniform(0, 1)) + q)
            else:
                print("Choose a valid noise distribution (1,2)!")
                return

        elif control == '2' or control == '4' or control == '6':
            print("Not implemented yet!")
            return

        else:
            print("Choose a valid control option (1-8)!")
            return

    elif demand_scheme == 4:
        if control == '1' or control == '3' or control == '5':
            # change the workload at specific time instants
            if 1 <= t < 15:
                D = 0.6 - 0.02 * (t - 1)
            elif t >= 15 or t < 25:
                D = 0.3
            elif 25 <= t <= 40:
                D = 0.6 - 0.02 * (t - 25)
            elif 25 <= t <= 40:
                D = 0.3
            elif 50 <= t <= 65:
                D = 0.6 - 0.02 * (t - 50)
            elif 65 <= t <= 75:
                D = 0.3
            elif 75 <= t <= 90:
                D = 0.6 - 0.02 * (t - 75)
            elif 90 <= t <= time:
                D = 0.3

            if random_gen == 1:
                D = D + (np.sqrt(Q) * np.random.standard_normal(1) + q)
            elif random_gen == 2:
                D = D + (np.sqrt(Q) * (1 - 2 * np.random.uniform(0, 1)) + q)
            else:
                print("Choose a valid noise distribution (1,2)!")
                return

        elif control == '2' or control == '4' or control == '6':
            # change the workload at specific time instants
            if 1 <= t < 15:
                D = 0.6 - 0.02 * (t - 1)
            elif t >= 15 or t < 25:
                D = 0.3
            elif 25 <= t <= 40:
                D = 0.6 - 0.02 * (t - 25)
            elif 25 <= t <= 40:
                D = 0.3
            elif 50 <= t <= 65:
                D = 0.6 - 0.02 * (t - 50)
            elif 65 <= t <= 75:
                D = 0.3
            elif 75 <= t <= 90:
                D = 0.6 - 0.02 * (t - 75)
            elif 90 <= t <= time:
                D = 0.3

            if random_gen == 1:
                D = D + (np.sqrt(Q[0,0]) * np.random.standard_normal(1) + q)
            elif random_gen == 2:
                D = D + (np.sqrt(Q[0,0]) * (1 - 2 * np.random.uniform(0, 1)) + q)
            else:
                print("Choose a valid noise distribution (1,2)!")
                return


    elif demand_scheme == 5:
        if control == '1' or control == '3' or control == '5':
            # change the workload at specific time instants
            if 10 <= t < 30:
                D = 0.6 + 0.02 * (t - 10)
            elif t >= 30 or t < 50:
                D = 1.05
            elif 50 <= t <= 60:
                D = 0.6
            elif 60 <= t <= 80:
                D = 0.6 + 0.02 * (t - 60)
            elif 80 <= t <= 100:
                D = 1.05
            elif 100 <= t <= time:
                D = 0.6

            if random_gen == 1:
                D = D + (np.sqrt(Q) * np.random.standard_normal(1) + q)
            elif random_gen == 2:
                D = D + (np.sqrt(Q) * (1 - 2 * np.random.uniform(0, 1)) + q)
            else:
                print("Choose a valid noise distribution (1-2)!")
                return

        elif control == '2' or control == '4' or control == '6':
            # change the workload at specific time instants
            if 10 <= t < 30:
                D = 0.6 + 0.02 * (t - 10)
            elif t >= 30 or t < 50:
                D = 1.05
            elif 50 <= t <= 60:
                D = 0.6
            elif 60 <= t <= 80:
                D = 0.6 + 0.02 * (t - 60)
            elif 80 <= t <= 100:
                D = 1.05
            elif 100 <= t <= time:
                D = 0.6

            if random_gen == 1:
                D = D + (np.sqrt(Q[0,0]) * np.random.standard_normal(1) + q)
            elif random_gen == 2:
                D = D + (np.sqrt(Q[0,0]) * (1 - 2 * np.random.uniform(0, 1)) + q)
            else:
                print "Choose a valid noise distribution (1-2)!"
            return

        else:
            print "Choose a valid control option (1-8)!"
            return

    elif demand_scheme == 6:
        if control == '1' or control == '3' or control == '5':
            # change the workload at specific time instants
            if 10 <= t < 30:
                D = 60 + 2 * (t - 10)
            elif 30 <= t < 40:
                D = 105
            elif 40 <= t < 50:
                D = 60
            elif 50 <= t < 80:
                D = 60 - 2 * (t - 60)
            elif 80 <= t <= 90:
                D = 60
            elif 90 <= t <= time:
                D = 30

            if random_gen == 1:
                D = D + (np.sqrt(Q) * np.random.standard_normal(1) + q)
            elif random_gen == 2:
                D = D + (np.sqrt(Q) * (1 - 2 * np.random.uniform(0, 1)) + q)
            else:
                print("Choose a valid noise distribution (1-2)!")
                return

        elif control == '2' or control == '4' or control == '6':
            # change the workload at specific time instants
            if 10 <= t < 30:
                D = 60 + 2 * (t - 10)
            elif 30 <= t < 40:
                D[0] = 80
                D[1] = 62
            elif 40 <= t < 50:
                D[0] = 60
                D[1] = 43
            elif 50 <= t < 80:
                D[0] = 60 - 2 * (t - 60)
                D[1] = 43 - 2 * (t - 60)
            elif 80 <= t <= 90:
                D[0] = 54
                D[1] = 36
            elif 90 <= t <= time:
                D[0] = 30
                D[1] = 24

            if random_gen == 1:
                D = D + (np.sqrt(Q[0,0]) * np.random.standard_normal(1) + q)
            elif random_gen == 2:
                D = D + (np.sqrt(Q[0,0]) * (1 - 2 * np.random.uniform(0, 1)) + q)

            else:
                print("Choose a valid noise distribution (1-2)!")
                return

        else:
            print("Choose a valid control option (1-8)!")
            return

    elif demand_scheme == 7:
        if control == '1' or control == '3' or control == '5':
            # change the workload at specific time instants
            Ddefault = D
            if 0 <= t < 30:
                D = 50
            elif 30 <= t < 40:
                D = D + 3
            elif 40 <= t < 80:
                D = 80
            elif 80 <= t < 90:
                D = D - 3
            elif 90 <= t <= time:
                D = 50

            if random_gen == 1:
                D = D + (np.sqrt(Q) * np.random.standard_normal(1) + q)
            elif random_gen == 2:
                D = D + (np.sqrt(Q) * (1 - 2 * np.random.uniform(0, 1)) + q)
            else:
                print("Choose a valid noise distribution (1-2)!")
                return

        elif control == '2' or control == '4' or control == '6':
            # change the workload at specific time instants
            Ddefault0 = D[0]
            Ddefault1 = D[1]
            if 0 <= t < 30:
                D[0] = 50
                D[1] = 30
            elif 30 <= t < 40:
                D[0] = D[0] + 3
                D[1] = D[1] + 1
            elif 40 <= t < 80:
                D[0] = 80
                D[1] = 40
            elif 80 <= t < 90:
                D[0] = D[0] - 3
                D[1] = D[1] - 1
            elif 90 <= t <= time:
                D[0] = 50
                D[1] = 30

            if random_gen == 1:
                D[0] = D[0] + (np.sqrt(Q[0,0]) * (1 - 2 * np.random.standard_normal(1)) + q[0])
                D[1] = D[1] + (np.sqrt(Q[1,1]) * (1 - 2 * np.random.standard_normal(1)) + q[1])
            elif random_gen == 2:
                D[0] = D[0] + (np.sqrt(Q[0,0]) * (1 - 2 * np.random.uniform(0, 1)) + q[0])
                D[1] = D[1] + (np.sqrt(Q[1,1]) * (1 - 2 * np.random.uniform(0, 1)) + q[1])

            else:
                print("Choose a valid noise distribution (1-2)!")
                return

        else:
            print("Choose a valid control option (1-8)!")
            return

    else:
        print("Choose a valid demand scheme (1-7)!")
        return

    return D


# This function computes the current CPU usage
def current_cpu_usage(control, D, a, u):
    if control == '1' or control == '3' or control == '5':
        value = a - D

        # if demand is more than the allocation:
        if value < 0:
            # we can't have a usage larger than the allocation.
            u = a

            # just to make sure u is within the limits: 0 \leq u\leq a
            if u > a:
                u = a
            elif u < 0:
                u = 0

        # if the demand is less than the allocation
        else:
            u = D
            if u > a:
                u = a
            elif u < 0:
                u = 0

    elif control == '2' or control =='4' or control == '6':
        value = a - D

        # if demand is more than the allocation:
        if value.all() < 0:
            # we can't have a usage larger than the allocation.
            u = a

            # just to make sure u is within the limits: 0 \leq u\leq a
            if u.all() > a.all():
                u = a
            elif u.all() < 0:
                u = 0

        # if the demand is less than the allocation
        else:
            u = D
            if u.all() > a.all():
                u = a
            elif u.all() < 0:
                u = 0

    else:
        print("Choose a valid control option (1, 2, 3, 4, 5, 6)!")
        return

    q = D - u
    return u, q


def add_clients():
    os.system("ssh root@10.190.12.56 screen -d -m /root/add_clients.sh ")

# Test
# u = current_cpu_usage(1, 2, 3, 1)
# D = demand(1, 20, 100, 60, 5, 0, 1, 4)
