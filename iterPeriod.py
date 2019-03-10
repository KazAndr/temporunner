#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 15:55:42 2018

@author: andr
"""
import os

import numpy as np

add_period_list = list(range(1000))
pdot_list = [i/100 for i in range(-400, 400)]
for add in add_period_list:
    for pdot in pdot_list:
        with open('0943_fk_start.par', 'r') as file:
            lines = file.readlines()

        start_period = lines[5][:-1]
        lines[5] = start_period + str(add) + '    1' + '\n'

        lines[8] = 'F1       ' + str(pdot) + 'D-15     1' + '\n'

        with open('0943_fk.par', 'w') as file:
            for line in lines:
                file.write(line)

        os.system("tempo 0943_fk.tim")
        os.system("~/work/tempo/util/print_resid/./print_resid -mre > resid.ascii")

        data = np.genfromtxt("resid.ascii").T

        with open('res_p_pdot.txt', 'a') as file:
            file.write(start_period[11:] + str(add) + ' ')
            file.write(str(pdot) + 'D-15' + ' ')
            file.write(str(np.std(data[1])))
            file.write('\n')
