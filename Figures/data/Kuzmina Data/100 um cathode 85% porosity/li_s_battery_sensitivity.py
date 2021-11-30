# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 14:41:28 2021

@author: korff
"""

import numpy as np
import pandas as pd
import cantera as ct
from matplotlib import pyplot as plt

"Import model data"
model_data_01C = pd.read_csv(r'dch0.1C_100um_Kuzmina.csv')
model_data_05C = pd.read_csv(r'dch0.5C_100um_Kuzmina.csv') 
model_data_1C = pd.read_csv(r'dch1.0C_100um_Kuzmina.csv') 

"Import experimental data"
exp_data_01C = pd.read_csv(r'0.1C Data.csv', header=None)  
exp_data_05C = pd.read_csv(r'0.5C Data.csv', header=None)
exp_data_1C = pd.read_csv(r'1C Data.csv', header=None)

Cap_01C_exp = exp_data_01C.iloc[:, 0]
V_cell_01C_exp = exp_data_01C.iloc[:, 1]

Cap_05C_exp = exp_data_05C.iloc[:, 0]
V_cell_05C_exp = exp_data_05C.iloc[:, 1]

Cap_1C_exp = exp_data_1C.iloc[:, 0]
V_cell_1C_exp = exp_data_1C.iloc[:, 1]

"Split out cell voltage of each species sensitivity run"
V_cell_01C = model_data_01C['Phi_ed1']
V_cell_05C = model_data_05C['Phi_ed1']
V_cell_1C = model_data_1C['Phi_ed1']

"Split out capacity of each species sensitivity run"
Cap_01C = model_data_01C['Time']
Cap_05C = model_data_05C['Time']
Cap_1C = model_data_1C['Time']

"Interpolate between data points of model to match experimental data"
V_cell_01C_int = np.interp(Cap_01C_exp, Cap_01C, V_cell_01C)
V_cell_05C_int = np.interp(Cap_05C_exp, Cap_05C, V_cell_05C)
V_cell_1C_int = np.interp(Cap_1C_exp, Cap_1C, V_cell_1C)

dCap_min = 10
C_prev = 0
V_cell_01C_RSS = np.array([])
V_cell_01C_exp_RSS = np.array([])
Cap_01C_RSS = np.array([])
for i in np.arange(0, len(V_cell_01C_int)):
    if Cap_01C_exp[i] - C_prev > dCap_min:
        V_cell_01C_RSS = np.append(V_cell_01C_RSS, V_cell_01C_int[i])
        V_cell_01C_exp_RSS = np.append(V_cell_01C_exp_RSS, V_cell_01C_exp[i])
        Cap_01C_RSS = np.append(Cap_01C_RSS, Cap_01C_exp[i])
        C_prev = Cap_01C_exp[i]
        
C_prev = 0
V_cell_05C_RSS = np.array([])
V_cell_05C_exp_RSS = np.array([])
Cap_05C_RSS = np.array([])
for i in np.arange(0, len(V_cell_05C_int)):
    if Cap_05C_exp[i] - C_prev > dCap_min:
        V_cell_05C_RSS = np.append(V_cell_05C_RSS, V_cell_05C_int[i])
        V_cell_05C_exp_RSS = np.append(V_cell_05C_exp_RSS, V_cell_05C_exp[i])
        Cap_05C_RSS = np.append(Cap_05C_RSS, Cap_05C_exp[i])
        C_prev = Cap_05C_exp[i]
        
C_prev = 0
V_cell_1C_RSS = np.array([])
V_cell_1C_exp_RSS = np.array([])
Cap_1C_RSS = np.array([])
for i in np.arange(0, len(V_cell_1C_int)):
    if Cap_1C_exp[i] - C_prev > dCap_min:
        V_cell_1C_RSS = np.append(V_cell_1C_RSS, V_cell_1C_int[i])
        V_cell_1C_exp_RSS = np.append(V_cell_1C_exp_RSS, V_cell_1C_exp[i])
        Cap_1C_RSS = np.append(Cap_1C_RSS, Cap_1C_exp[i])
        C_prev = Cap_1C_exp[i]
        

"""Calculate relative change in RSS between baseline and 1% shift in species
    thermo"""
RSS_01C = np.sum((V_cell_01C_RSS - V_cell_01C_exp_RSS)**2)
RSS_05C = np.sum((V_cell_05C_RSS - V_cell_05C_exp_RSS)**2)
RSS_1C = np.sum((V_cell_1C_RSS - V_cell_1C_exp_RSS)**2)

RSS_tot = RSS_01C + RSS_05C + RSS_1C

V_cell_concat = np.concatenate((V_cell_01C_int, V_cell_05C_int, V_cell_1C_int))
V_cell_exp_concat = np.concatenate((V_cell_01C_exp, V_cell_05C_exp, V_cell_1C_exp))
RSS_tot_2 = np.sum((V_cell_concat - V_cell_exp_concat)**2)
print('Kuzmina', RSS_tot, RSS_tot_2)