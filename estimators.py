#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 17:31:55 2015
@author: Dr. Kyriakos M. Deliparaschos
@author: Evagoras Makridis
"""

import numpy as np

# Attributes
# ----------
# x: State estimate vector
# y: Measurement (or observation)
# P: Covariance matrix
# W: Measurement noise matrix
# V: Process noise matrix
# A: State Transition matrix
# C: Measurement function
# r: Residual of the update step.
# K: Kalman gain of the update step
# S: Systen uncertaintly projected to measurement space

# Function definitions

# This function evaluates the MIMO Kalman filter
def kalman_mimo(P, W, V, C, y, x):
    A = np.array([[1, 0],[0, 1]])  # process equation
    # Measurement Update (Correction)
    # ===============================
    # Compute the Kalman Gain
    S = C.dot(P).dot(C) + V
    K = C.dot(P).dot(np.linalg.pinv(S))
    # Update the state estimate
    r = y - C.dot(x)  # innovation term (measurement residual)
    x = x + K.dot(r)
    # Update the error covariance
    P = np.eye(len(x)) - C.dot(K).dot(P)

    # Time Update (Prediction)
    # ========================
    # Project the state ahead
    x = A.dot(x)
    # Project the error covariance ahead
    P = A.dot(P) + W

    return x, P, K
    

# This function evaluates the MIMO Hinf filter
def hinf_mimo(P, W, V, C, y, x, theta):
    A = np.array([[1, 0],[0, 1]])  # process equation
    V_inv = np.linalg.pinv(V)
    C_tr = np.transpose(C)
    A_tr = np.transpose(A)
    I = np.eye(len(x))

    # Update
    innov = y - C.dot(x)
    L = (I-theta.dot(P)+C_tr.dot(V_inv).dot(C).dot(P))
    L_inv = np.linalg.pinv(L)
    K = P.dot(L_inv).dot(C_tr).dot(V_inv)
    x = x + K.dot(innov)
    P = P.dot(L_inv)

    # Predict
    x = A.dot(x)
    P= A.dot(P).dot(A_tr) + W

    return x, P, K


# This function evaluates the MIMO MCC Kalman filter
def mcc_kf_mimo(P, W, V, C, y, x, sigma):
    A = np.array([[1, 0],[0, 1]])  # process equation
    A_tr = np.transpose(A)
    C_tr = np.transpose(C)
    V_inv = np.linalg.pinv(V)
    n = len(x)
    I = np.eye(n)
    
    P_inv = np.linalg.pinv(P)
    innov = y - C.dot(x)
    innov_tr = np.transpose(innov)
    norm_innov = np.sqrt(innov_tr.dot(V_inv).dot(innov))
    L = np.exp(-(norm_innov ** 2) / (2 * sigma ** 2))
    K = np.linalg.pinv(P_inv + (L*C_tr).dot(V_inv).dot(C)).dot(L*C_tr).dot(V_inv)
    x = x + K.dot(innov)
    K_tr = np.transpose(K)
    P = (I - K.dot(C)).dot(P).dot(np.transpose(I - K.dot(C))) + (K.dot(V).dot(K_tr))

    x = A.dot(x)
    P = A.dot(P).dot(A_tr) + W

    return x, P, K