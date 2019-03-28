from astropy.coordinates import SkyCoord
from astropy import units as u

coord = SkyCoord('11:15:38 +50:13:12', unit=(u.deg, u.deg))

coord_range = [coord.ra + i*u.arcsec for i in range(5, 150, 5)]

print(len(coord_range))
print(coord_range[0], coord_range[1], coord_range[2])

print('Done!')
