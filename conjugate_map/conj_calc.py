"""Functions for computing geomagnetic conjugate points."""

# Importing packages
import datetime as dt
import logging
import os
import importlib.util

import aacgmv2
from geopack import geopack as gp
import gpxpy
import gpxpy.gpx
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(filename='conjcalc.log', level=logging.INFO)

try:
    import apexpy
except ImportError:
    logger.warning("apexpy is not installed. Quasidipole coordinates not available.")

###############################################################################
def findconj(lat, lon, ut=dt.datetime.now(tz=dt.timezone.utc),
             method='aacgm', alt=0, limit=60):

    """Calculate the geographic latitudes and longitudes of conjugate point for
        given set of coordinates.

    Parameters
    ----------
    lat         : float
            Geographic latitude of station.
    lon         : float
            Geographic longitude of station.
    ut          : datetime
            Datetime used in conversion.T
    method      : string
            Defines method used in conversion. Options are 'auto', 
            'geopack', which uses IGRF + T89 to run field line traces,
            'aacgm', which uses AACGM v2,
            'qdip' for quasi-dipole coordinates via apexpy.
    alt         : float
            Altitude of point in m. 0 by default.
    limit       : float
            Latitude limit, in degrees, used to switch between
            methods in auto mode. Default: 60.
            AACGM will converge above 35 degrees, but may be
            erroneous. See www.doi.org/10.1002/2014JA020264

    Returns
    -------
    lat, lon    : float
        Latitude, longitude of conjugate points

    """

    method = method.lower()  # Cast method as lowercase

    if np.isnan(lat) or np.isnan(lon):
        logger.info("Received NaN for a coordinate; can't compute.")
        return 0, 0

    if method == 'qdip':
        if importlib.util.find_spec("apexpy") is None:
            logger.warning("The apexpy package is not installed. \
                            To use quasidipole coordinates, run 'pip install apexpy'.\
                            Setting method to 'auto' instead.")
            method = "auto"

    if method == 'auto':
        if abs(lat) > limit:
            method = 'aacgm'
        else:
            method = 'geopack'
        logger.info("Setting method according to latitude limits: %s", method)

    if method == 'geopack':
        ut = ut.timestamp()
        ps = gp.recalc(ut)  # pylint: disable=unused-variable # noqa: F841
        # Lint doesn't like it, but geopack needs this command.
        logger.info('.....Calculating conjugate for %s, %s at %s via geopack:'
                    , str(lat), str(lon), str(ut))

        r, theta, phi = [1, 90-lat, lon]
        # r is Earth radii; theta is colatitude (i.e., in degrees from 0 (North
        # Pole) to 360 (South Pole)); phi is longitude in degrees.

        theta, phi = np.deg2rad([theta, phi])
        logger.info('r, theta, phi: ')
        logger.info([r, theta, phi])
        xgeo, ygeo, zgeo = gp.sphcar(r, theta, phi, 1)
        logger.info('Cartesian output: ')
        logger.info([xgeo, ygeo, zgeo])
        logger.info('Sum of squares (should be 1):')
        logger.info(xgeo**2 + ygeo**2 + zgeo**2)
        logger.info('GSM coordinates: ')
        xgsm, ygsm, zgsm = gp.geogsm(xgeo, ygeo, zgeo, 1)
        logger.info([xgsm, ygsm, zgsm])
        logger.info('Sum of squares (should be 1):')
        logger.info(xgsm**2 + ygsm**2 + zgsm**2)

        # Now let's try running the field line trace: help(gp.trace) for doc.
        rlim, r0 = [1000, .9]

        fieldline = gp.trace(xgsm, ygsm, zgsm, dir=-1, rlim=rlim, r0=r0,
                             parmod=2, exname='t89', inname='igrf')

        x1gsm, y1gsm, z1gsm = fieldline[0:3]
        logger.info('Traced GSM Coordinates, Cartesian: ')
        logger.info([x1gsm, y1gsm, z1gsm])
        logger.info('%f points in traced vector.', len(fieldline[4]))
        logger.info('Sum of squares (should be 1):')
        logger.info(x1gsm**2 + y1gsm**2 + z1gsm**2)

        # geogsm
        x1geo, y1geo, z1geo = gp.geogsm(x1gsm, y1gsm, z1gsm, -1)
        logger.info('Geographic coordinates, Cartesian: ')
        logger.info([x1geo, y1geo, z1geo])
        logger.info('Sum of squares (should be 1):')
        logger.info(x1geo**2 + y1geo**2 + z1geo**2)

        # convert back to spherical
        logger.info('Geographic coordinates, spherical: ')
        [x1_r, x1_theta, x1_phi] = gp.sphcar(x1geo, y1geo, z1geo, -1)
        logger.info([x1_r, x1_theta, x1_phi])

        # back to lat/long:
        x1_theta, x1_phi = np.rad2deg([x1_theta, x1_phi])
        logger.info('Lat/lon of conjugate point: ')
        lat = 90-x1_theta
        lon = x1_phi
        logger.info([lat, lon])
        return lat, lon

    if method == "aacgm":
        logger.info('...Calculating conjugate for %s, %s at %s via AACGMv2:',
                    str(lat), str(lon), str(ut))
        mlat, mlon, _ = aacgmv2.convert_latlon(lat, lon, 0, ut, 'G2A')
        logger.info('Magnetic lat/lon: %s', str([mlat, mlon]))
        glat_con, glon_con, _ = aacgmv2.convert_latlon(
            -1.*mlat, mlon, 0, ut, 'A2G')
        logger.info('Conjugate geographic lat/lon: %f, %f', glat_con, glon_con)
        return glat_con, glon_con

    if method == "qdip":
        logger.info("...Calculating conjugate for %s, %s at %s via quasi-dipole coordinates:",
                    f"{lat:.2f}", f"{lon:.2f}", f"{ut:.2f}")
        apex_field = apexpy.Apex(ut)
        mlat, mlon = apex_field.geo2qd(lat, lon, alt)
        logger.info('Quasidipole coordinates for lat/lon: %s', str([mlat, mlon]))
        glat_con, glon_con, _ = apex_field.qd2geo(-mlat, mlon, height = alt)
        logger.info('Conjugate geographic lat/lon: %f, %f', glat_con, glon_con)
        return glat_con, glon_con
    logger.info('Method is not listed.')
    return 0, 0


###############################################################################

def conjcalc(gdf, latname="GLAT", lonname="GLON",
             dtime=dt.datetime.now(tz=dt.timezone.utc),
             method='aacgm', mode='S2N',
             is_saved=False, directory='output/', name='stations'):

    """Calculate the geographic latitudes and longitudes of conjugate points
    for all points in a dataframe. Calls findconj().

    Parameters
    ----------
    gdf         : dataframe of points whose conjugate points we're finding
    lat         : float
            Geographic latitude of station.
    lon         : float
            Geographic longitude of station.
    ut          : datetime
            Datetime used in conversion.
    method      : string
            Defines method used in conversion. Options are 'auto', 'geopack',
            which uses IGRF + T89 to run field line traces,
            or 'aacgm', which uses AACGM v2.
    limit       : float
            Latitude limit, in degrees, used to switch between
            methods in auto mode. Default: 60.
            AACGM will converge above 35 degrees, but may be
            erroneous. See www.doi.org/10.1002/2014JA020264
    latname     : string
            Name of column containing latitude coordinates.
    lonname     : string
            Name of column containing longitude coordinates.
    dtime       : datetime
            Datetime used in conversion.
    method      : string
            Method used in conversion, passed to findconj().
            Options are 'geopack', which uses IGRF + T89 to run
            field line traces, or 'aacgm'.
    mode        : string
                    'S2N'     :
                                Return station coordinates for
                                northern hemisphere, conjugate
                                for southern. Map appears over
                                the Arctic. Default.
                    'N2S'     :
                                Return station coordinates for
                                southern hemisphere, conjugate
                                for northern. Map appears over
                                the Antarctic.
                    'flip'    :
                                Return conjugate coordinates for
                                points regardless of hemisphere.

    is_saved    : boolean
        Boolean dictating whether the final .csv is saved to
        the output directory.
    directory   : string
        Name of local directory to which .csv is saved;
        'output/' by default.
    name        : string
        First part of saved filename. 'stations' by default.

    Returns
    -------
    gdf         : pandas.DataFrame
        Dataframe with PLAT, PLON columns added indicating which
        points to plot

    See Also
    --------
    conjugate_map.findconj

    Note
    ----
    Calls findconj for each entry in the dataframe.

    """

    gdf['Hemisphere'] = np.nan
    gdf['PLAT'] = np.nan  # latitude and longitude to plot
    gdf['PLON'] = np.nan  # latitude and longitude to plot

    # Iterate over the DataFrame
    for index, row in gdf.iterrows():
        lat = row[latname]
        lon = row[lonname]
        logger.info('Checking hemisphere.')
        if isinstance(lon, str):
            logger.info('Longitude encoded as string. Fixing...')
            try:
                lon = lon.replace('−', '-')
                lon = float(lon)
            except ValueError as e:
                logger.warning(e)
                continue
        if isinstance(lat, str):
            logger.info('Latitude encoded as string. Fixing...')
            lat = lat.replace('−', '-')
            lat = float(lat)
            logger.info('Now floats: %f, %f', lat, lon)

        if lon > 180:
            lon = lon-360

        [clat, clon] = findconj(lat, lon, dtime, method=method)
        logger.info('Conjugate latitude and longitude: ')
        logger.info([clat, clon])
        gdf.loc[index, 'PLAT'], gdf.loc[index, 'PLON'] = [clat, clon]

        # Figure out what coordinates we ultimately want to plot:
        if lat > 0:
            logger.info('Setting Northern hemisphere for GLAT of %f on station %s', lat, index)  # noqa: E501
            gdf.loc[index, 'Hemisphere'] = "N"
            if mode in ('N2S', 'flip'):
                gdf.loc[index, 'PLAT'] = clat
                gdf.loc[index, 'PLON'] = clon
            else:
                gdf.loc[index, 'PLAT'] = lat
                gdf.loc[index, 'PLON'] = lon

        else:
            logger.info('Setting Southern hemisphere for GLAT of %f on station %s', lat, index)  # noqa: E501
            gdf.loc[index, 'Hemisphere'] = "S"
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
                    is_saved=False):

    """Calculate the geographic latitudes and longitudes of a circle of points
    for a list of magnetic latitudes.

    Parameters
    ----------
    mlats       : np.array
            List of magnetic latitudes
    ut          : dt.datetime
            Datetime used in AACGMv2 conversion;
            by default, ut=dt.datetime.now(tz=dt.timezone.utc)
    is_saved    : boolean
            If is_saved == True, saves .gpx versions.
                        to local output directory

    Returns
    -------
    mlats_dct: dict
        Dictionary with geographic latitude and longitude
        points for each of the specified magnetic latitudes.

    Example Use
    ------------
    Saves .gpx magnetic graticules for 1 January 2020 every 5
    degrees latitude::

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
            logger.info('Saving magnetic graticule for %f degrees magnetic latitude.', mlat)  # noqa: E501
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

        logger.info(gpx.to_xml())

        with open('output/graticules/'+filename+'.gpx', 'w',
                  encoding="utf-8") as f:
            f.write(gpx.to_xml())
            logger.info("Writing %s to gpx. ", filename)
    return mlats_dct
