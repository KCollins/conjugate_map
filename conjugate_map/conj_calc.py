"""Functions for computing geomagnetic conjugate points."""

# Importing packages
import datetime as dt
import os

import aacgmv2
from geopack import geopack as gp
import gpxpy
import gpxpy.gpx
import numpy as np
import pandas as pd


###############################################################################
def findconj(lat, lon, ut=dt.datetime.now(tz=dt.timezone.utc),
             is_verbose=False, method='aacgm', limit=60):

    """
    Calculate the geographic latitudes and longitudes of conjugate point for a
    given set of coordinates.

    Arguments:
        lat         : geographic latitude of station
        lon         : geographic longitude of station
        ut          : datetime used in conversion
        is_verbose  : if set to True, prints debugging text
        method      : method used in conversion. Options are 'auto', 'geopack',
                        which uses IGRF + T89 to run field line traces,
                        or 'aacgm', which uses AACGM v2.
        limit       : latitude limit, in degrees, used to switch between
                        methods in auto mode. Default: 60.
                        AACGM will converge above 35 degrees, but may be
                        erroneous. See www.doi.org/10.1002/2014JA020264


    Returns:
        lat, lon    : latitude, longitude of conjugate points
    """
    method = method.lower()  # Cast method as lowercase

    if method == 'auto':
        if abs(lat) > limit:
            method = 'aacgm'
        else:
            method = 'geopack'
        if is_verbose:
            print("Setting method according to latitude limits: " + method)

    if method == 'geopack':
        ut = ut.timestamp()
        ps = gp.recalc(ut)  # pylint: disable=unused-variable # noqa: F841
        # Lint doesn't like it, but geopack needs this command.
        if is_verbose:
            print('............................................'
                  'Calculating conjugate point for ' + str(lat) + ', '
                  + str(lon) + ' at ' + str(ut) + ' with geopack: ')

        r, theta, phi = [1, 90-lat, lon]
        # r is Earth radii; theta is colatitude (i.e., in degrees from 0 (North
        # Pole) to 360 (South Pole)); phi is longitude in degrees.

        theta, phi = np.deg2rad([theta, phi])
        if is_verbose:
            print('r, theta, phi: ')
            print(r, theta, phi)
        xgeo, ygeo, zgeo = gp.sphcar(r, theta, phi, 1)
        if is_verbose:
            print('Cartesian output: ')
            print(xgeo, ygeo, zgeo)
            print('Sum of squares (should be 1):')
            print(xgeo**2 + ygeo**2 + zgeo**2)
            print('GSM coordinates: ')
        xgsm, ygsm, zgsm = gp.geogsm(xgeo, ygeo, zgeo, 1)
        if is_verbose:
            print(xgsm, ygsm, zgsm)
            print('Sum of squares (should be 1):')
            print(xgsm**2 + ygsm**2 + zgsm**2)

        # Now let's try running the field line trace: help(gp.trace) for doc.
        rlim, r0 = [1000, .9]

        fieldline = gp.trace(xgsm, ygsm, zgsm, dir=-1, rlim=rlim, r0=r0,
                             parmod=2, exname='t89', inname='igrf')

        x1gsm, y1gsm, z1gsm = fieldline[0:3]
        if is_verbose:
            print('Traced GSM Coordinates, Cartesian: ')
            print(x1gsm, y1gsm, z1gsm)
            print(str(len(fieldline[4])) + ' points in traced vector.')
            print('Sum of squares (should be 1):')
            print(x1gsm**2 + y1gsm**2 + z1gsm**2)

        # geogsm
        x1geo, y1geo, z1geo = gp.geogsm(x1gsm, y1gsm, z1gsm, -1)
        if is_verbose:
            print('Geographic coordinates, Cartesian: ')
            print(x1geo, y1geo, z1geo)
            print('Sum of squares (should be 1):')
            print(x1geo**2 + y1geo**2 + z1geo**2)

        # convert back to spherical
        if is_verbose:
            print('Geographic coordinates, spherical: ')
        [x1_r, x1_theta, x1_phi] = gp.sphcar(x1geo, y1geo, z1geo, -1)
        if is_verbose:
            print(x1_r, x1_theta, x1_phi)

        # back to lat/long:
        x1_theta, x1_phi = np.rad2deg([x1_theta, x1_phi])
        if is_verbose:
            print('Lat/lon of conjugate point: ')
        lat = 90-x1_theta
        lon = x1_phi
        if is_verbose:
            print(lat, lon)
        return lat, lon

    if method == "aacgm":
        if is_verbose:
            print('............................................'
                  'Calculating conjugate point for ' + str(lat) + ', '
                  + str(lon) + ' at ' + str(ut) + ' with AACGMV2: ')
        mlat, mlon, _ = aacgmv2.convert_latlon(lat, lon, 0, ut, 'G2A')
        if is_verbose:
            print('Magnetic lat/lon: ' + str([mlat, mlon]))
        glat_con, glon_con, _ = aacgmv2.convert_latlon(
            -1.*mlat, mlon, 0, ut, 'A2G')
        if is_verbose:
            print('Conjugate geographic lat/lon: ' + str([glat_con, glon_con]))
        return glat_con, glon_con

    print('Method is not listed.')
    return 0, 0


###############################################################################

def conjcalc(gdf, latname="GLAT", lonname="GLON",
             dtime=dt.datetime.now(tz=dt.timezone.utc),
             is_verbose=False, method='aacgm', mode='S2N',
             is_saved=False, directory='output/', name='stations'):
    """
    Calculate the geographic latitudes and longitudes of conjugate points for
    all points in a dataframe. Calls findconj().

    Arguments:
        gdf         : dataframe of points whose conjugate points we're finding
        latname     : name of column containing latitude coordinates
        lonname     : name of column containing longitude coordinates
        dtime       : datetime used in conversion
        is_verbose  : if set to True/1, prints debugging text
        method      : method used in conversion, passed to findconj().
                        Options are 'geopack', which uses IGRF + T89 to run
                        field line traces, or 'aacgm'.
        mode        :
                                 'S2N'     : Return station coordinates for
                                              northern hemisphere, conjugate
                                              for southern. Map appears over
                                              the Arctic. Default.
                                 'N2S'     : Return station coordinates for
                                              southern hemisphere, conjugate
                                              for northern. Map appears over
                                              the Antarctic.
                                 'flip'    : Return conjugate coordinates for
                                             points regardless of hemisphere.
        is_saved    : Boolean dictating whether the final .csv is saved to
                        the output directory.
        directory   : Name of local directory to which .csv is saved;
                        'output/' by default.
        name        : First part of saved filename. 'stations' by default.

    Returns:
        gdf         : dataframe with PLAT, PLON columns added indicating which
                        points to plot
    """

    gdf['Hemisphere'] = np.nan
    gdf['PLAT'] = np.nan  # latitude and longitude to plot
    gdf['PLON'] = np.nan  # latitude and longitude to plot

    # Iterate over the DataFrame
    for index, row in gdf.iterrows():
        lat = row[latname]
        lon = row[lonname]
        if is_verbose:
            print('Checking hemisphere.')
        if isinstance(lon, str):
            if is_verbose:
                print('Longitude encoded as string. Fixing...')
            try:
                lon = lon.replace('−', '-')
                lon = float(lon)
            except ValueError as e:
                print(e)
                continue
        if isinstance(lat, str):
            if is_verbose:
                print('Latitude encoded as string. Fixing...')
            lat = lat.replace('−', '-')
            lat = float(lat)
            if is_verbose:
                print('Now floats: ' + str([lat, lon]))

        if lon > 180:
            lon = lon-360

        [clat, clon] = findconj(lat, lon, dtime, is_verbose=is_verbose,
                                method=method)
        if is_verbose:
            print('Conjugate latitude and longitude: ')
            print([clat, clon])
        gdf.loc[index, 'PLAT'], gdf.loc[index, 'PLON'] = [clat, clon]

        # Figure out what coordinates we ultimately want to plot:
        if lat > 0:
            if is_verbose:
                print('Setting Northern hemisphere for GLAT of ' + str(lat)
                      + ' on station ' + index)
            gdf.loc[index, 'Hemisphere'] = 'N'
            if mode in ('N2S', 'flip'):
                gdf.loc[index, 'PLAT'] = clat
                gdf.loc[index, 'PLON'] = clon
            else:
                gdf.loc[index, 'PLAT'] = lat
                gdf.loc[index, 'PLON'] = lon

        else:
            if is_verbose:
                print('Setting Southern hemisphere for GLAT of ' + str(lat)
                      + ' on station ' + index)
            gdf.loc[index, 'Hemisphere'] = 'S'
            if mode in ('S2N', 'flip'):
                gdf.loc[index, 'PLAT'] = clat
                gdf.loc[index, 'PLON'] = clon
            else:
                gdf.loc[index, 'PLAT'] = lat
                gdf.loc[index, 'PLON'] = lon

        if is_saved:
            filename = name + '_' + mode + '-' + method + '-' + str(dtime)
            gdf.to_csv(os.path.join(directory, ''.join([filename, '.csv'])))

    return gdf

###############################################################################


def calc_mlat_rings(mlats, ut=dt.datetime.now(tz=dt.timezone.utc),
                    is_verbose=False, is_saved=False):
    """
    Calculate the geographic latitudes and longitudes of a circle of points
    for a list of magnetic latitudes.

    Arguments:
        mlats       : list of magnetic latitudes
        ut          : dt.datetime used in AACGMv2 conversion;
                        by default, ut=dt.datetime.now(tz=dt.timezone.utc)
        is_verbose  : if set to True/1, prints debugging text
        is_saved    : if is_saved == True, saves .gpx versions
                        to local output directory

    Returns:
        mlats_dct: dictionary with geographic latitude and longitude
                    points for each of the specified magnetic latitudes

    Example use: Saves .gpx magnetic graticules for 1 January 2020 every 5
                degrees latitude:

                 rings = calc_mlat_rings(list(range(-90, 90, 5)), ut =
                            dt.datetime(2020, 1, 1), is_saved = True)
    """
    mlons = np.arange(0, 360)
    mlats_dct = {}
    for mlat in mlats:
        glats = []
        glons = []
        for mlon in mlons:
            result = aacgmv2.convert_latlon(mlat, mlon, 0, ut, 'A2G')
            glats.append(result[0])
            glons.append(result[1])

        mlats_dct[mlat] = {'glats': glats, 'glons': glons}

        if is_saved is True:
            if is_verbose:
                print('Saving magnetic graticule for ' + str(mlat) +
                      ' degrees magnetic latitude.')
            filename = 'Graticule_ ' + str(mlat) + '_' + str(ut)
            directory = 'output/'
            df = pd.DataFrame({'MLAT': mlats_dct[mlat]['glats'],
                               'MLON': mlats_dct[mlat]['glons']})

            f = os.path.join(directory, filename)
            gpx = gpxpy.gpx.GPX()

            # Create first track in our GPX:
            gpx_track = gpxpy.gpx.GPXTrack()
            gpx.tracks.append(gpx_track)

            # Create first segment in our GPX track:
            gpx_segment = gpxpy.gpx.GPXTrackSegment()
            gpx_track.segments.append(gpx_segment)

            # Create points:
            for idx in df.index:
                gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(
                    df.loc[idx, 'MLAT'], df.loc[idx, 'MLON']))

            # print(gpx.to_xml())

            with open('output/graticules/'+filename+'.gpx', 'w',
                      encoding="utf-8") as f:
                f.write(gpx.to_xml())
            if is_verbose:
                print('Writing ' + filename + " to gpx. ")

    return mlats_dct
