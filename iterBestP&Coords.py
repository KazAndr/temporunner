#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 18:23:39 2018

@author: andr
"""

import os

from copy import copy
from datetime import datetime, timedelta

import numpy as np
import matplotlib.pyplot as plt

name_pulsar = input('Enter name pulsar: ')

os.system('rm res_iter_p_coords_' + name_pulsar + '.txt')

periods = np.genfromtxt('bestP_' + name_pulsar + '.txt').T[0]

with open(name_pulsar + '_start.par', 'r') as file:
    lines = file.readlines()

ra = datetime.strptime(lines[1][11:-1], '%H:%M:%S')
dec = datetime.strptime(lines[2][11:-1], '%H:%M:%S')
ra_start = copy(ra)
dec_start = copy(dec)


for idx, period in enumerate(periods):
    ra = ra_start

    for i in range(60):
        ra += timedelta(seconds=1)
        dec = dec_start

        for j in range(60):
            dec += timedelta(seconds=1)

            lines[1] = 'RAJ       ' + ra.strftime('%H:%M:%S') + '\n'

            lines[2] = 'DECJ       ' + dec.strftime('%H:%M:%S') + '\n'

            lines[3] = 'F0        ' + str(period) + '    1' + '\n'

            with open(name_pulsar + '.par', 'w') as file:
                for line in lines:
                    file.write(line)

            os.system('tempo ' + name_pulsar + '.tim > outtempo.log')
            os.system(
                    '~/work/tempo/util/print_resid/./print_resid -mre > ' +
                    'resid_' + name_pulsar + '.ascii')

            data = np.genfromtxt('resid_' + name_pulsar + '.ascii').T

            with open('res_iter_p_coords_' + name_pulsar + '.txt', 'a') as file:
                file.write(str(period) + ' ')
                file.write(ra.strftime('%H:%M:%S') + ' ')
                file.write(dec.strftime('%H:%M:%S') + ' ')
                file.write(str(np.std(data[1])))
                file.write('\n')

            print(
                    str(idx) + '/' + len(periods),
                    period,
                    ra.strftime('%H:%M:%S'),
                    dec.strftime('%H:%M:%S'),
                    np.std(data[1]))

data = np.genfromtxt('res_iter_p_coords_' + name_pulsar + '.txt').T
plt.close()
plt.plot(data[3])
plt.savefig('res_iter_p_coords_' + name_pulsar + '.png', format='png', dpi=150)
