#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 15:00:01 2019

@author: andr
"""

import os

import numpy as np
import matplotlib.pyplot as plt

from copy import copy
from tqdm import tqdm

name_pulsar = input('Enter name pulsar: ')

with open(name_pulsar + '_start.par', 'r') as file:
    lines = file.readlines()
start_period = copy(lines[3][:-1])

first_part = ["%.2d" % i for i in range(1, 100)]

for first in tqdm(first_part):
    os.system('rm ' + 'res_iter_p_' + name_pulsar + '.txt')
    for add in tqdm(range(1, 10000), leave=False):
        lines[3] = start_period + first + str(add) + '    1' + '\n'

        with open(name_pulsar + '.par', 'w') as file:
            for line in lines:
                file.write(line)

        os.system('tempo ' + name_pulsar + '.tim > outtempo.log')
        os.system(
                '~/work/tempo/util/print_resid/./print_resid -mre > ' +
                'resid_' + name_pulsar + '.ascii')

        data = np.genfromtxt('resid_' + name_pulsar + '.ascii').T

        with open('res_iter_p_' + name_pulsar + '.txt', 'a') as file:
            file.write(start_period[11:] + first + str(add) + ' ')
            file.write(str(np.std(data[1])))
            file.write('\n')

    data = np.genfromtxt('res_iter_p_' + name_pulsar + '.txt').T

    if os.path.isdir('./deep_period_plot_' + name_pulsar + '/'):
        pass
    else:
        os.system('mkdir ' + './deep_period_plot_' + name_pulsar + '/')

    plt.close()
    plt.plot(data[1])
    plt.savefig(
            './deep_period_plot_' + name_pulsar + '/'
            + first + '.png', format='png', dpi=150)
