#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 15:14:02 2018

@author: Kazantsev Andrey
03.02.2019
Changes"
        Rewriting file for work with best params from file
"""

import os

import numpy as np
import matplotlib.pyplot as plt

name_pulsar = input('Enter name pulsar: ')

par_data = np.genfromtxt('best_par_' + name_pulsar + '.txt', dtype=str).T

with open(name_pulsar + '_start.par', 'r') as file:
    lines = file.readlines()

iteration = 0
for i in range(len(par_data[0])):
    lines[1] = 'RAJ      ' + par_data[1][i] + '\n'
    lines[2] = 'DECJ     ' + par_data[2][i] + '\n'
    lines[3] = 'F0       ' + par_data[0][i] + '    1' + '\n'

    with open(name_pulsar + '.par', 'w') as file:
        for line in lines:
            file.write(line)

    os.system('tempo ' + name_pulsar + '.tim > outtempo.log')
    os.system(
            '~/work/tempo/util/print_resid/./print_resid -mre > ' +
            'resid_' + name_pulsar + '.ascii')
    data = np.genfromtxt('resid_' + name_pulsar + '.ascii').T

    plt.close()
    plt.title(
            str(iteration)
            + '/' + par_data[0][i]
            + '/' + par_data[1][i]
            + '/' + par_data[2][i]
            + '/' + par_data[3][i])
    plt.xlabel('MJD')
    plt.ylabel('Residuals, us')
    plt.plot(data[0], data[1], '+')

    # создание директории в том случае, если она не существует
    if os.path.isdir('./plot_res_' + name_pulsar + '/'):
        pass
    else:
        os.system('mkdir ' + './plot_res_' + name_pulsar + '/')

    plt.savefig(
            './plot_res_' + name_pulsar + '/'
            + str(iteration)
            + '_'
            + name_pulsar
            + '.png',
            format='png')
    iteration += 1
