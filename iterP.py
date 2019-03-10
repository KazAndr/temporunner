#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 15:55:42 2018

@author: andr
"""
import os

import numpy as np
import matplotlib.pyplot as plt

from copy import copy
from tqdm import tqdm

name_pulsar = input('Enter name pulsar: ')
work_path = input('Enter work directory: ')
num_iter = int(input('Enter numbers of iteration: '))
step_iter = int(input('Enter step of iteration: '))

os.system('rm ' + work_path + os.sep + 'res_iter_p_' + name_pulsar + '.txt')

with open(work_path + os.sep + name_pulsar + '_start.par', 'r') as file:
    lines = file.readlines()
start_period = copy(lines[3][:-1])

for add in tqdm(range(1, num_iter, step_iter)):
    lines[3] = start_period + str(add) + '    1' + '\n'

    with open(work_path + os.sep + name_pulsar + '.par', 'w') as file:
        for line in lines:
            file.write(line)

    os.system('tempo -f'
              + work_path + os.sep
              + name_pulsar + '.par '
              + work_path + os.sep
              + name_pulsar + '.tim > '
              + 'outtempo_' + name_pulsar + '.log')
    os.system(
            '~/work/tempo/util/print_resid/./print_resid -mre > '
            + work_path + os.sep + 'resid_' + name_pulsar + '.ascii')

    data = np.genfromtxt(work_path +
                         os.sep + 'resid_' + name_pulsar + '.ascii').T

    with open(work_path + os.sep
              + 'res_iter_p_' + name_pulsar + '.txt', 'a') as file:
        file.write(start_period[11:] + str(add) + ' ')
        file.write(str(np.std(data[1])))
        file.write('\n')


data = np.genfromtxt(work_path + os.sep
                     + 'res_iter_p_' + name_pulsar + '.txt').T

plt.close()
plt.plot(data[1])
plt.savefig(work_path + os.sep
            + 'res_iter_p_' + name_pulsar + '.png', format='png', dpi=150)
