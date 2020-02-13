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

# Удаление результатов от предыдущей обработки
os.system(f'rm res_iter_p_coords_{name_pulsar}.txt')
os.system(f'rm out_res_iter_p_coords_{name_pulsar}.log')
os.system(f'rm res_iter_p_coords_{name_pulsar}.png')


with open(f'{name_pulsar}_start.par', 'r') as file:
    lines = file.readlines()

ra_label, *ra_coord = lines[1].split()
dec_label, *dec_coord = lines[2].split()
period_label, *start_period = lines[3].split()

coords = SkyCoord(
        ra_coord[0]
        + ' '
        + dec_coord[0],
        unit=(u.deg, u.deg))

if dimension == 'arcsec':
    dim = u.arcsec
    ra_bruteforce = int(ra_range*2*60 + ra_step_bf)  # arcsec
    dec_bruteforce = int(dec_range*2*60 + dec_step_bf)  # arcsec
elif dimension == 'marcsec':
    dim = u.milliarcsecond
    ra_bruteforce = int(ra_range*2*60*100 + ra_step_bf)  # arcsec
    dec_bruteforce = int(dec_range*2*60*100 + dec_step_bf)  # arcsec
else:
    print('Unknown dimension!')

ra_start = copy(coords.ra) - ra_range*u.arcmin
dec_start = copy(coords.dec) - dec_range*u.arcmin

ra_list = [ra_start + i*dim for i in range(
    ra_step_bf,
    ra_bruteforce,
    ra_step_bf
)]

dec_list = [dec_start + i*dim for i in range(
    dec_step_bf,
    dec_bruteforce,
    dec_step_bf
)]

add_period_list = range(period_step, period_range, period_step)

elem_list = list(product(add_period_list, ra_list, dec_list))

for elements in tqdm(elem_list):
    lines[1] = f'RAJ        {elements[1].to_string(sep=":")}    {fit_coords}\n'

    lines[2] = f'DECJ       {elements[2].to_string(sep=":")}   {fit_coords}\n'

    lines[3] = f'F0         {start_period[0]}{elements[0]}    {fit_period}\n'

    lines[4] = f'F1         0.0     1\n'  # Производная подгонятеся всегда

    with open(f'{name_pulsar}.par', 'w') as file:
        for line in lines:
            file.write(line)

    os.system(
        f'tempo -f {name_pulsar}.par {work_dir}{name_pulsar}.tim > outtempo.log')
    os.system(f'print_resid -mre > resid_{name_pulsar}.ascii')

    data = np.genfromtxt(f'resid_{name_pulsar}.ascii').T

    with open(f'res_iter_p_coords_{name_pulsar}.txt', 'a') as file:
        file.write(f'{start_period[0]}{elements[0]}' + ' ')
        file.write(elements[1].to_string(sep=':') + ' ')
        file.write(elements[2].to_string(sep=':') + ' ')
        file.write(str(np.std(data[1])))
        file.write('\n')


data = np.genfromtxt(f'res_iter_p_coords_{name_pulsar}.txt').T
plt.close()
plt.plot(data[3])
plt.savefig(f'res_iter_p_coords_{name_pulsar}.png', format='png', dpi=150)
