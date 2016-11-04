# -*- coding: UTF-8 -*-

"""star.py: A module to interface the
`Stopping-Power & Range Tables for Electrons, Protons, and Helium Ions
<https://www.nist.gov/pml/stopping-power-range-tables-electrons-protons-and-helium-ions>`_.

"""

import requests
import re


def fetch_estar(el_id):
    """
    Fetch from the website the data for electrons in a medium.

    Check the `STAR appendix <http://physics.nist.gov/PhysRefData/Star/Text/appendix.html>`_ for further details.

    Args:
        el_id (int): The positive integer identifying the medium.

    Returns:
        (list): a list of lists, a list with the data for each tabulated energy value, each a list with:

            * (float): Kinetic energy in MeV.
            * (float): Collision stopping power in MeV cm^2/g.
            * (float): Radiative stopping power in MeV cm^2/g.
            * (float): Total stopping power in MeV cm^2/g.
            * (float): CSDA range in g/cm^2.
            * (float): Radiation yield (fraction of kinetic energy converted into bremsstrahlung).
            * (float): Density effect parameter

    """
    return _fetch_star(el_id, particle="e")


def fetch_pstar(el_id):
    """
        Fetch from the website the data for protons in a medium.

        Check the `STAR appendix <http://physics.nist.gov/PhysRefData/Star/Text/appendix.html>`_ for further details.

        Args:
            el_id (int): The positive integer identifying the medium.

        Returns:
            (list): a list of lists, a list with the data for each tabulated energy value, each a list with:

                * (float): Kinetic energy in MeV.
                * (float): Electronic stopping power in MeV cm^2/g.
                * (float): Nuclear stopping power in MeV cm^2/g.
                * (float): Total stopping power in MeV cm^2/g.
                * (float): CSDA range in g/cm^2.
                * (float): Projected CSDA range in g/cm^2.
                * (float): Detour factor (prjected CSDA / CSDA).

        """
    return _fetch_star(el_id, particle="p")


def fetch_astar(el_id):
    """
        Fetch from the website the data for alpha particles in a medium.

        Check the `STAR appendix <http://physics.nist.gov/PhysRefData/Star/Text/appendix.html>`_ for further details.

        Args:
            el_id (int): The positive integer identifying the medium.

        Returns:
            (list): a list of lists, a list with the data for each tabulated energy value, each a list with:

                * (float): Kinetic energy in MeV.
                * (float): Electronic stopping power in MeV cm^2/g.
                * (float): Nuclear stopping power in MeV cm^2/g.
                * (float): Total stopping power in MeV cm^2/g.
                * (float): CSDA range in g/cm^2.
                * (float): Projected CSDA range in g/cm^2.
                * (float): Detour factor (prjected CSDA / CSDA).

        """
    return _fetch_star(el_id, particle="a")


def _fetch_star(el_id, particle="e"):
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
        r = requests.post('http://physics.nist.gov/cgi-bin/Star/ap_table-t.pl', data={"matno": z, "ShowDefault": "on", "prog": "PSTAR"})
    elif particle == "a":
        r = requests.post('http://physics.nist.gov/cgi-bin/Star/ap_table-t.pl', data={"matno": z, "ShowDefault": "on", "prog": "ASTAR"})
    else:
        raise TypeError("particle must be a string containing either 'e', 'p' or 'a'.")
    # TODO: Catch unexisting material
    html = r.text
    number_pattern = '-?[0-9]+\.?[0-9]*E[-+][0-9]+'
    # Find lines with seven numbers ending in <br>
    # In e, all in scientific notation, in a and p the last one is a proper ratio (in (0, 1)).
    if particle == "e":
        lines = re.findall("("+(number_pattern + "  ")*6+number_pattern+")"+"<br>", html)
    else:  # p or a
        lines = re.findall("(" + (number_pattern + "  ") * 6 + "0.[0-9]+" + ")" + "<br>", html)
    output = []
    for l in lines:
        output.append(list(map(float,l.split())))
    return output
