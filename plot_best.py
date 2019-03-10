#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 15:14:02 2018

@author: andr
"""

import os

import numpy as np
import matplotlib.pyplot as plt

name_pulsar = input('Enter name pulsar: ')

p_pdot_data = np.genfromtxt('bestPPdot_' + name_pulsar + '.txt', dtype=str).T

with open(name_pulsar + '_start.par', 'r') as file:
    lines = file.readlines()

iteration = 0
for period, pdot in zip(p_pdot_data[0], p_pdot_data[1]):
    lines[3] = 'F0       ' + period + '    1' + '\n'
    lines[4] = 'F1       ' + pdot + '   1' + '\n'

    with open(name_pulsar + '.par', 'w') as file:
        for line in lines:
            file.write(line)

    os.system('tempo ' + name_pulsar + '.tim > outtempo.log')
    os.system(
            '~/work/tempo/util/print_resid/./print_resid -mre > ' +
            'resid_' + name_pulsar + '.ascii')
    data = np.genfromtxt('resid_' + name_pulsar + '.ascii').T

    plt.close()
    plt.title(period + ' ' + pdot)
    plt.xlabel('MJD')
    plt.ylabel('Residuals, ms')
    plt.plot(data[0], data[1], '+')
    plt.savefig(
            './plot_res/'
            + str(iteration)
            + '_'
            + name_pulsar
            + '.png',
            format='png')
    print(iteration)
    iteration += 1
