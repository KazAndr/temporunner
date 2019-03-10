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

os.system('rm res_iter_p_pdot_' + name_pulsar + '_' + degree + '.txt')

add_period_list = [i for i in range(0, 10000, 3)]
pdot_list = [i/100 for i in range(-1000, 100, 3)]

for add in add_period_list:
    for pdot in pdot_list:
        with open(name_pulsar + '_start.par', 'r') as file:
            lines = file.readlines()

        start_period = lines[3][:-1]
        lines[3] = start_period + str(add) + '    1' + '\n'

        lines[4] = 'F1       ' + str(pdot) + degree + '     1' + '\n'

        with open(name_pulsar + '.par', 'w') as file:
            for line in lines:
                file.write(line)

        os.system('tempo ' + name_pulsar + '.tim > outtempo.log')
        os.system(
                '~/work/tempo/util/print_resid/./print_resid -mre > ' +
                'resid_' + name_pulsar + '.ascii')

        data = np.genfromtxt('resid_' + name_pulsar + '.ascii').T

        with open(
                'res_iter_p_pdot_'
                + name_pulsar
                + '_'
                + degree
                + '.txt', 'a') as file:
            file.write(start_period[11:] + str(add) + ' ')
            file.write(str(pdot) + degree + ' ')
            file.write(str(np.std(data[1])))
            file.write('\n')

        print(
                start_period[11:].lstrip() + str(add),
                str(pdot) + degree,
                np.std(data[1]))

data = np.genfromtxt(
        'res_iter_p_pdot_'
        + name_pulsar
        + '_'
        + degree
        + '.txt').T

plt.close()
plt.plot(data[2])
plt.savefig(
        'res_iter_p_pdot_'
        + name_pulsar
        + '_'
        + degree
        + '.png', format='png', dpi=150)
