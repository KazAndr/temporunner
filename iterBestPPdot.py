#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 15:43:14 2018

@author: andr
"""

import os

import numpy as np
import matplotlib.pyplot as plt

name_pulsar = input('Enter name pulsar: ')

os.system('rm res_iter_p_pdot_prec_' + name_pulsar + '.txt')

data = np.genfromtxt('bestPPdot_' + name_pulsar + '.txt', dtype=str).T

with open(name_pulsar + '_start.par', 'r') as file:
    lines = file.readlines()

for period, pdot in zip(data[0], data[1]):
    for i in range(1, 100):
        add_p = str(i)
        for j in range(1, 100):
            add_pdot = str(j)

            lines[3] = 'F0        ' + period + add_p + '    1' + '\n'

            lines[4] = 'F1        ' + pdot[:-4] + add_pdot + pdot[-4:] + '    1' + '\n'

            with open(name_pulsar + '.par', 'w') as file:
                for line in lines:
                    file.write(line)

            os.system('tempo ' + name_pulsar + '.tim > outtempo.log')
            os.system(
                    '~/work/tempo/util/print_resid/./print_resid -mre > ' +
                    'resid_' + name_pulsar + '.ascii')

            data = np.genfromtxt('resid_' + name_pulsar + '.ascii').T

            with open('res_iter_p_pdot_prec_' + name_pulsar + '.txt', 'a') as file:
                file.write(period + str(add_p) + ' ')
                file.write(pdot[:-4] + str(add_pdot) + pdot[-4:] + ' ')
                file.write(str(np.std(data[1])))
                file.write('\n')

            print(
                    period + str(add_p),
                    pdot[:-4] + str(add_pdot) + pdot[-4:],
                    np.std(data[1]))

data = np.genfromtxt('res_iter_p_pdot_prec_' + name_pulsar + '.txt').T
plt.close()
plt.plot(data[2])
plt.savefig(
        'res_iter_p_pdot_prec_'
        + name_pulsar
        + '.png', format='png', dpi=150)
