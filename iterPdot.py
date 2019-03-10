#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 15:55:42 2018

@author: andr
"""
import os

import numpy as np
import matplotlib.pyplot as plt

name_pulsar = input('Enter name pulsar: ')
degree = 'D-' + input('Enter degree of pdot')
start_pdot = input('Enter start pdot')

os.system('rm res_iter_pdot_' + name_pulsar + '_' + degree + '.txt')

add_pdot_list = list(range(1000))
for add in add_pdot_list:
    with open(name_pulsar + '_start.par', 'r') as file:
        lines = file.readlines()

    lines[4] = 'F1       ' + start_pdot + str(add) + degree + '     1' + '\n'

    with open(name_pulsar + '.par', 'w') as file:
        for line in lines:
            file.write(line)

    os.system('tempo ' + name_pulsar + '.tim > outtempo.log')
    os.system(
            '~/work/tempo/util/print_resid/./print_resid -mre > ' +
            'resid_' + name_pulsar + '.ascii')

    data = np.genfromtxt('resid_' + name_pulsar + '.ascii').T

    with open('res_iter_pdot_' + name_pulsar + '.txt', 'a') as file:
        file.write(start_pdot + str(add) + degree + ' ')
        file.write(str(np.std(data[1])))
        file.write('\n')

    print(
           start_pdot + str(add) + degree,
           np.std(data[1])
            )

data = np.genfromtxt('res_iter_pdot_' + name_pulsar + '_' + degree + '.txt').T

plt.close()
plt.plot(data[1])
plt.savefig(
        'res_iter_pdot_'
        + name_pulsar
        + '_'
        + degree
        + '.png', format='png', dpi=150)
