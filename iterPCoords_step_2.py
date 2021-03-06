#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 13:31:22 2018

@author: andr
"""

import os

from copy import copy

import numpy as np
import matplotlib.pyplot as plt

from astropy.coordinates import SkyCoord
from astropy import units as u
from tqdm import tqdm

name_pulsar = input('Enter name pulsar: ')

os.system('rm res_iter_p_coords_' + name_pulsar + '.txt')
os.system('rm out_res_iter_p_coords_' + name_pulsar + '.log')

add_period_list = list(range(0, 1000, 2))
#add_period_list = [i for i in add_period_list if str(i)[-1] != '0']

with open(name_pulsar + '_start.par', 'r') as file:
    lines = file.readlines()

coords = c = SkyCoord(
        lines[1][11:-1].lstrip()
        + ' '
        + lines[2][11:-1].lstrip(),
        unit=(u.deg, u.deg))

ra_start = copy(coords.ra) - 12.5*u.arcmin
dec_start = copy(coords.dec) - 12.5*u.arcmin
start_period = copy(lines[3][:-1])

for add in tqdm(add_period_list):
    ra = copy(ra_start)

    for i in tqdm(range(150), leave='False'):
        ra += 10*u.arcsec
        dec = copy(dec_start)

        for j in tqdm(range(150), leave='False'):
            dec += 10*u.arcsec

            lines[1] = 'RAJ       ' + ra.to_string(sep=':') + '\n'

            lines[2] = 'DECJ       ' + dec.to_string(sep=':') + '\n'

            lines[3] = start_period + str(add) + '    1' + '\n'

            lines[4] = 'F1       ' + '0.0' + '     1' + '\n'

            with open(name_pulsar + '.par', 'w') as file:
                for line in lines:
                    file.write(line)

            os.system('tempo ' + name_pulsar + '.tim > outtempo.log')
            os.system(
                    '~/work/tempo/util/print_resid/./print_resid -mre > ' +
                    'resid_' + name_pulsar + '.ascii')

            data = np.genfromtxt('resid_' + name_pulsar + '.ascii').T

            with open('res_iter_p_coords_' + name_pulsar + '.txt', 'a') as file:
                file.write(start_period[11:] + str(add) + ' ')
                file.write(ra.to_string(sep=':') + ' ')
                file.write(dec.to_string(sep=':') + ' ')
                file.write(str(np.std(data[1])))
                file.write('\n')


data = np.genfromtxt('res_iter_p_coords_' + name_pulsar + '.txt').T
plt.close()
plt.plot(data[3])
plt.savefig('res_iter_p_coords_' + name_pulsar + '.png', format='png', dpi=150)
