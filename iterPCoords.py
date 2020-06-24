#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 13:31:22 2018

@author: Kazantsev Andrey
"""

import os
import sys
import subprocess

from copy import copy
from itertools import product
from subprocess import Popen

import numpy as np
import matplotlib.pyplot as plt

from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.coordinates import Angle
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



# Подгрузка диапазона итерации
ra_range = Angle(ra_range)
dec_range = Angle(dec_range)

ra_start = copy(coords.ra) - ra_range
dec_start = copy(coords.dec) - dec_range
ra_stop = copy(coords.ra) + ra_range
dec_stop = copy(coords.dec) + dec_range

# Подгрузка  шага итерации
step_ra = Angle(step_ra)
step_dec = Angle(step_dec)

# Вычисление количества необходимых итераций
numbers_ra = int(round(((ra_stop-ra_start)/step_ra).value))
numbers_dec = int(round(((dec_stop-dec_start)/step_dec).value))

ra_brutforce = np.linspace(ra_start, ra_stop, numbers_ra)
dec_brutforce = np.linspace(dec_start, dec_stop, numbers_dec)
freq_brutforce = [f'{start_period[0]}{i}' for i in range(period_range)]


elem_list = list(product(freq_brutforce, ra_brutforce, dec_brutforce))

for elements in tqdm(elem_list):
    lines[1] = f'RAJ        {elements[1].to_string(sep=":")}    {fit_coords}\n'

    lines[2] = f'DECJ       {elements[2].to_string(sep=":")}   {fit_coords}\n'

    lines[3] = f'F0         {elements[0]}    {fit_period}\n'

    lines[4] = f'F1         0.0     1\n'  # Производная подгонятеся всегда

    with open(f'{name_pulsar}.par', 'w') as file:
        for line in lines:
            file.write(line)

    cmd_tempo = (f'tempo -f {name_pulsar}.par {work_dir}{name_pulsar}.tim')
    run_tempo = Popen(cmd_tempo.split(), stdout=subprocess.PIPE)
    run_tempo.wait()

    with open(f'resid_{name_pulsar}.ascii', 'w') as file:
        cmd_save_resid = f'print_resid -mre'
        run_save = Popen(cmd_save_resid.split(), stdout=file)
        run_save.wait()

    data = np.genfromtxt(f'resid_{name_pulsar}.ascii').T

    with open(f'res_iter_p_coords_{name_pulsar}.txt', 'a') as file:
        file.write(elements[0] + ' ')
        file.write(elements[1].to_string(sep=':') + ' ')
        file.write(elements[2].to_string(sep=':') + ' ')
        file.write(str(np.std(data[1])))
        file.write('\n')


data = np.genfromtxt(f'res_iter_p_coords_{name_pulsar}.txt').T
plt.close()
plt.plot(data[3])
plt.savefig(f'res_iter_p_coords_{name_pulsar}.png', format='png', dpi=150)
