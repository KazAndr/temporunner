import copy

import numpy as np

from itertools import compress


def get_interval_toas(toas, start, stop):
    mask_toas = []
    copy_toas = copy.copy(toas)
    toas_table = toas.table
    for val in toas_table['mjd_float']:
        if start < val < stop:
            mask_toas.append(True)
        else:
            mask_toas.append(False)
    copy_toas.select(mask_toas)
    return copy_toas


def get_intervals_toas(toas, intervals):
    total_maks = []
    for start, stop in intervals:
        mask_toas = []
        copy_toas = copy.copy(toas)
        toas_table = copy_toas.table
        for val in toas_table['mjd_float']:
            if start < val < stop:
                mask_toas.append(False)
            else:
                mask_toas.append(True)
        total_maks.append(mask_toas)

    primary_mask = np.full(copy_toas.ntoas, False)
    for item in total_maks:
        primary_mask = primary_mask ^ np.array(item)
    
    copy_toas.select(primary_mask)
    return copy_toas


def get_toas_by_residuals(toas, residuals, value_up, value_down, dimension):
    result = []
    for i, val in enumerate(residuals.to(dimension)):
        if val.value < value_down:
            result.append(toas.get_mjds()[i].value)
        elif val.value > value_up:
            result.append(toas.get_mjds()[i].value)
        else:
            continue
            
    return result


def exclude_toas(toas, list_mjd):
    mask_toas = []
    copy_toas = copy.copy(toas)
    toas_table = toas.table
    for val in toas_table['mjd_float']:
        if val in list_mjd:
            mask_toas.append(False)
        else:
            mask_toas.append(True)
    copy_toas.select(mask_toas)
    return copy_toas


def exclude_intervals_toas(toas, intervals):
    total_maks = []
    for start, stop in intervals:
        mask_toas = []
        copy_toas = copy.copy(toas)
        toas_table = copy_toas.table
        for val in toas_table['mjd_float']:
            if start < val < stop:
                mask_toas.append(False)
            else:
                mask_toas.append(True)
        total_maks.append(mask_toas)

    primary_mask = np.full(copy_toas.ntoas, True)
    for item in total_maks:
        primary_mask = primary_mask ^ np.array(item)
    
    copy_toas.select(primary_mask)
    return copy_toas
