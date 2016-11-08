# -*- coding: UTF-8 -*-

"""star.py: A module to interface the
`Stopping-Power & Range Tables for Electrons, Protons, and Helium Ions
<https://www.nist.gov/pml/stopping-power-range-tables-electrons-protons-and-helium-ions>`_.

"""

import requests
import re


def fetch_estar(el_id, density=None):
    """
    Fetch from the website the data for electrons in a medium.

    Check the `STAR appendix <http://physics.nist.gov/PhysRefData/Star/Text/appendix.html>`_ for further details.

    Args:
        el_id (int): The positive integer identifying the medium.
        density (float or bool, optional): If given, the density scaling is removed. If it is the boolean True, the
            density will be taken from the website.

    Returns:
        (list): a list of lists, a list with the data for each tabulated energy value, each a list with:

            * (float): Kinetic energy in MeV.
            * (float): Collision stopping power in MeV cm^2/g or in MeV/cm if a density was given.
            * (float): Radiative stopping power in MeV cm^2/g or in MeV/cm if a density was given.
            * (float): Total stopping power in MeV cm^2/g or in MeV/cm if a density was given.
            * (float): CSDA range in g/cm^2 or in cm if a density was given.
            * (float): Radiation yield (fraction of kinetic energy converted into bremsstrahlung).
            * (float): Density effect parameter

    """
    return _fetch_star(el_id, particle="e", density=density)


def fetch_pstar(el_id, density=None):
    """
        Fetch from the website the data for protons in a medium.

        Check the `STAR appendix <http://physics.nist.gov/PhysRefData/Star/Text/appendix.html>`_ for further details.

        Args:
            el_id (int): The positive integer identifying the medium.
            density (float or bool, optional): If given, the density scaling is removed. If it is the boolean True, the
            density will be taken from the website.

        Returns:
            (list): a list of lists, a list with the data for each tabulated energy value, each a list with:

                * (float): Kinetic energy in MeV.
                * (float): Electronic stopping power in MeV cm^2/g or in MeV/cm if a density was given.
                * (float): Nuclear stopping power in MeV cm^2/g or in MeV/cm if a density was given.
                * (float): Total stopping power in MeV cm^2/g or in MeV/cm if a density was given.
                * (float): CSDA range in g/cm^2 or in cm if a density was given.
                * (float): Projected CSDA range in g/cm^2 or in cm if a density was given.
                * (float): Detour factor (projected CSDA / CSDA).

        """
    return _fetch_star(el_id, particle="p", density=density)


def fetch_astar(el_id, density=None):
    """
        Fetch from the website the data for alpha particles in a medium.

        Check the `STAR appendix <http://physics.nist.gov/PhysRefData/Star/Text/appendix.html>`_ for further details.

        Args:
            el_id (int): The positive integer identifying the medium.
            density (float or bool, optional): If given, the density scaling is removed. If it is the boolean True, the
            density will be taken from the website.

        Returns:
            (list): a list of lists, a list with the data for each tabulated energy value, each a list with:

                * (float): Kinetic energy in MeV.
                * (float): Electronic stopping power in MeV cm^2/g or in MeV/cm if a density was given.
                * (float): Nuclear stopping power in MeV cm^2/g or in MeV/cm if a density was given.
                * (float): Total stopping power in MeV cm^2/g or in MeV/cm if a density was given.
                * (float): CSDA range in g/cm^2 or in cm if a density was given.
                * (float): Projected CSDA range in g/cm^2 or in cm if a density was given.
                * (float): Detour factor (projected CSDA / CSDA).

        """
    return _fetch_star(el_id, particle="a", density=density)


def _fetch_star(el_id, particle="e", density=None):
    # Note: 3 public functions are offered instead of this one  because the return of estar and pstar/astar is
    # different.

    # el_id is a 3 character string in the website, so it has to converted.
    # Despite only int support is documented for el_id, also check for strings.
    if type(el_id) == int:
        z = str(el_id)
    elif (type(el_id) is not str) or not el_id.isdigit():
        raise TypeError("el_id must be either a positive integer or a string with a positive integer.")
    else:
        z = el_id
    z = z.zfill(3)  # Ensure 3 digits
    if particle == "e":
        r = requests.post('http://physics.nist.gov/cgi-bin/Star/e_table-t.pl', data={"matno": z, "ShowDefault": "on"})
    elif particle == "p":
        r = requests.post('http://physics.nist.gov/cgi-bin/Star/ap_table-t.pl',
                          data={"matno": z, "ShowDefault": "on", "prog": "PSTAR"})
    elif particle == "a":
        r = requests.post('http://physics.nist.gov/cgi-bin/Star/ap_table-t.pl',
                          data={"matno": z, "ShowDefault": "on", "prog": "ASTAR"})
    else:
        raise TypeError("particle must be a string containing either 'e', 'p' or 'a'.")
    # TODO: Catch unexisting material
    html = r.text
    number_pattern = '-?[0-9]+\.?[0-9]*E[-+][0-9]+'

    if density is None:
        density = 1.0
    elif type(density) is bool:
        if density:  # If density is True, read from html
            if particle == "e":
                # The first scientific number is the density
                density = float(re.search(number_pattern, html).group(0))
            else:
                # Density is stored in a different page
                html2 = requests.get('http://physics.nist.gov/cgi-bin/Star/compos.pl?ap-text' + z).text
                density = float(re.search(number_pattern, html2).group(0))
        else:  # If false, do not scale
            density = 1.0
    elif type(density) is int:
        density = float(density)
    elif type(density) is not float:
        raise ValueError("density must be a float or a bool")
    output = []

    # Find lines with seven numbers ending in <br>
    # In e, all in scientific notation, in a and p the last one is a proper ratio (in (0, 1)).
    if particle == "e":
        lines = re.findall("(" + (number_pattern + "  ") * 6 + number_pattern + ")" + "<br>", html)
        unit_scale = [1.0, density, density, density, density, 1.0, 1.0]
    else:  # p or a
        lines = re.findall("(" + (number_pattern + "  ") * 6 + "0.[0-9]+" + ")" + "<br>", html)
        unit_scale = [1.0, density, density, density, density, density, 1]

    for l in lines:
        l_float = map(float, l.split())
        # Scale with the density the magnitudes that depend on it
        output.append(list(map(lambda a, b: a * b, l_float, unit_scale)))
    return output
