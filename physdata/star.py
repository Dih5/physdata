# -*- coding: UTF-8 -*-

"""star.py: A module to interface the
`ESTAR <http://physics.nist.gov/PhysRefData/Star/Text/ESTAR.html>`_,
`PSTAR <http://physics.nist.gov/PhysRefData/Star/Text/PSTAR.html>`_, and
`ASTAR <http://physics.nist.gov/PhysRefData/Star/Text/ASTAR.html>`_ data.

"""

import requests
import re


def fetch_estar(el_id):
    return _fetch_star(el_id, particle="e")


def fetch_pstar(el_id):
    return _fetch_star(el_id, particle="p")


def fetch_astar(el_id):
    return _fetch_star(el_id, particle="a")


def _fetch_star(el_id, particle="e"):
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


print(fetch_astar("13"))