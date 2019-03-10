#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 16:26:36 2018

@author: andr
"""
import os

from datetime import datetime, timedelta

import numpy as np
import matplotlib.pyplot as plt


os.system("rm res_iter_coords.txt")

with open('0943_fk_start.par', 'r') as file:
            lines = file.readlines()

ra = datetime.strptime(lines[1][11:-1], '%H:%M:%S')
dec = datetime.strptime(lines[2][11:-1], '%H:%M:%S')

for sec_ra in range(60):
    for sec_dec in range(60):
        ra += timedelta(seconds=sec_ra)
        dec += timedelta(seconds=sec_dec)

        lines[1] = 'RAJ       ' + ra.strftime('%H:%M:%S') + '     1' + '\n'

        lines[2] = 'DECJ       ' + dec.strftime('%H:%M:%S') + '     1' + '\n'

        with open('0943_fk.par', 'w') as file:
            for line in lines:
                file.write(line)

        os.system("tempo 0943_fk.tim")
        os.system("~/work/tempo/util/print_resid/./print_resid -mre > resid.ascii")

        data = np.genfromtxt("resid.ascii").T

        with open('res_iter_coords.txt', 'a') as file:
            file.write(ra.strftime('%H:%M:%S') + ' ')
            file.write(dec.strftime('%H:%M:%S') + ' ')
            file.write(str(np.std(data[1])))
            file.write('\n')

data = np.genfromtxt('res_iter_coords.txt').T
plt.close()
plt.plot(data[2])
plt.savefig('res_iter_coords.png', format='png', dpi=150)

