#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 13:31:22 2018

@author: Kazantsev Andrey
"""

import os
import sys

from copy import copy
from itertools import product

import numpy as np
import matplotlib.pyplot as plt

from astropy.coordinates import SkyCoord
from astropy import units as u
from tqdm import tqdm

sys.path.append('.')  # Добавляем локальный путь запуска файла для config

from config import *


os.system(f'rm res_iter_p_coords_{name_pulsar}.txt')
os.system(f'rm out_res_iter_p_coords_{name_pulsar}.log')

add_period_list = list(range(period_step, period_range, period_step))

with open(f'{name_pulsar}_start.par', 'r') as file:
    lines = file.readlines()

coords = c = SkyCoord(
        lines[1][11:-1].lstrip()
        + ' '
        + lines[2][11:-1].lstrip(),
        unit=(u.deg, u.deg))

ra_start = copy(coords.ra) - ra_range*u.arcmin
dec_start = copy(coords.dec) - dec_range*u.arcmin
start_period = copy(lines[3][:-1])

ra_list = [ra_start + i*u.arcsec for i in range(
    ra_step_bf,
    ra_bruteforce,
    ra_step_bf
)]

dec_list = [dec_start + i*u.arcsec for i in range(
    dec_step_bf,
    dec_bruteforce,
    dec_step_bf
)]

elem_list = list(product(add_period_list, ra_list, dec_list))

for elements in tqdm(elem_list):
    lines[1] = f'RAJ       {elements[1].to_string(sep=":")}\n'

    lines[2] = f'DECJ       {elements[2].to_string(sep=":")}\n'

    lines[3] = f'start_period{str(elements[0])}    1\n'

    lines[4] = f'F1       0.0     1\n'

    with open(f'{name_pulsar}.par', 'w') as file:
        for line in lines:
            file.write(line)

    os.system(
        f'tempo -f {name_pulsar}.par {work_dir}{name_pulsar}.tim > outtempo.log')
    os.system(f'print_resid -mre > resid_{name_pulsar}.ascii')

    data = np.genfromtxt(f'resid_{name_pulsar}.ascii').T

    with open(f'res_iter_p_coords_{name_pulsar}.txt', 'a') as file:
        file.write(start_period[11:] + str(elements[0]) + ' ')
        file.write(elements[1].to_string(sep=':') + ' ')
        file.write(elements[2].to_string(sep=':') + ' ')
        file.write(str(np.std(data[1])))
        file.write('\n')


data = np.genfromtxt(f'res_iter_p_coords_{name_pulsar}.txt').T
plt.close()
plt.plot(data[3])
plt.savefig(f'res_iter_p_coords_{name_pulsar}.png', format='png', dpi=150)
