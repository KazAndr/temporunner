# Setup name of pulsar and working directory
name_pulsar = '1112'
work_dir = (
    f'/home/andr/Yandex.Disk/1.Работа/'
    f'TIMING/tulbashev/original_data/1112+50/'
)

# Setup range for brute force period/frequency
period_range = 10
period_step = 1

# Setup range for brute force coordinates
ra_range = 1  # arcmin
dec_range = 1  # arcmin

# Setup dimension and step for brute force coordinates
dimension = 'marcsec'  # arcsec or marcsec
ra_step_bf = 500  # arcsec
dec_step_bf = 500  # arcsec

# on/off fitting params
fit_period = '1'
fit_coords = '1'
