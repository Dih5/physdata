# -*- coding: UTF-8 -*-

"""xray.py: A module to interface the
`X-Ray Mass Attenuation Coefficients <https://www.nist.gov/pml/x-ray-mass-attenuation-coefficients>`_ data.

"""
from __future__ import print_function

import requests
import re
import sys


class ElementData:
    """
    An element in the database.

    Attributes:
        z (int): The atomic number.
        symbol (str): Symbol of the element.
        name (str): Name of the element.
        mass_ratio (float): Atomic number-mass ratio Z/A.
        excitation (float): Mean excitation energy in eV.
        density (float): Density in g/cm^3.

    Note:
        Some density values are only nominal, according to the data. Values for Z=85 and 87 where arbitrarily set to 10.

    """

    def __init__(self, row):
        """
        Create an ElementData instance using a row from the NIST tables.

        Args:
            row (List): The elements of the row in the NIST table defining the element.

        """
        self.z = int(row[0])
        self.symbol = str(row[1])
        self.name = str(row[2])
        self.mass_ratio = float(row[3])
        self.excitation = float(row[4])
        self.density = float(row[5])

    def __repr__(self):
        return "ElementData<" + str(self.z) + ">"

    def get_coefficients(self, use_density=False):
        if use_density:
            if self.z in [85, 87]:
                print("Warning: using a density value arbitrarily set to 10 g/cm^3.", file=sys.stderr)
            return fetch_coefficients(self.z, self.density)
        else:
            return fetch_coefficients(self.z)


class CompoundData:
    """
    An composite material in the database.

    Attributes:
        short_name (str): Short name of the material.
        name (str): Name of the material.
        mass_ratio (float): Mean atomic number-mass ratio <Z/A>.
        excitation (float): Mean excitation energy in eV.
        density (float): Density in g/cm^3.

    Note:
        Some density values are only nominal, according to the data.

    """

    def __init__(self, row, short_name):
        """
        Create a CompoundData instance using a row from the NIST tables.

        Args:
            row (List): The elements of the row in the NIST table defining the material.
            short_name (str): The short name of the material.

        """
        self.short_name = short_name
        self.name = str(row[0])
        self.mass_ratio = float(row[1])
        self.excitation = float(row[2])
        self.density = float(row[3])
        # TODO: add composition information from row[4]

    def __repr__(self):
        return "CompoundData<" + str(self.short_name) + ">"

    def get_coefficients(self, use_density=False):
        if use_density:
            return fetch_coefficients(self.short_name, self.density)
        else:
            return fetch_coefficients(self.short_name)


def fetch_coefficients(z, density=None):
    """
    Fetch from the website the data for an element or compound.

    Args:
        z (int or str): The atomic number (element) or a string representing the compound.
        density (float, optional): If given, the density scaling is removed.

    Returns:
        List: a list with the data for each tabulated energy value, each a list with:

            * (float): Energy in MeV.
            * (float): Attenuation coefficient in cm^2/g or in cm^-1 if a density was given.
            * (float): Energy absorption coefficient in cm^2/g or in cm^-1 if a density was given.

    """
    if density is None:
        density = 1

    if type(z) is int or (type(z) is str and z.isdigit()):  # Either an integer or a string with a natural number
        str_z = str(z) if int(z) > 9 else "0" + str(z)  # Two digit string
        url = "http://physics.nist.gov/PhysRefData/XrayMassCoef/ElemTab/z" + str_z + ".html"
    else:
        url = "http://physics.nist.gov/PhysRefData/XrayMassCoef/ComTab/" + z + ".html"

    r = requests.get(url)
    # TODO: Check for errors
    html = r.text
    html = str(html).split("</DIV>")[2]  # Pick the div with the ascii table
    # How numbers are represented in the NIST web.
    number_pattern = '-?[0-9]+\.?[0-9]*E[-+][0-9]+'
    lines = re.findall(number_pattern + "  " + number_pattern + "  " + number_pattern, html)
    data = []
    for l in lines:
        l2 = list(map(float, l.split("  ")))

        data.append([l2[0], l2[1] * density, l2[2] * density])
    return data


def fetch_elements():
    """
    Fetch the element data from the NIST database.

    Returns:
        List[:obj:`ElementData`]: A list with the info of each element available.

    """
    r = requests.get("http://physics.nist.gov/PhysRefData/XrayMassCoef/tab1.html")
    html = r.text
    rows = re.findall(r"<TR.*?>(.*?)</TR>", html, re.DOTALL)[3:]  # Pick the rows, excluding the headers
    output = []
    for row in rows:
        parsed_row = re.findall(r"<TD.*?>(.*?)</TD>", row)
        # Remove some cells with only "&nbsp;" (which are only in H, probably a bad formatting practice)
        parsed_row = list(filter(lambda s: s != "&nbsp;", parsed_row))
        # Remove trailing spaces
        parsed_row = list(map(lambda x: x.strip(), parsed_row))
        # Dictionary entries by atomic number (as string), symbol and name.
        output.append(ElementData(parsed_row))
    return output


def fetch_compounds():
    """
    Fetch the compound data from the NIST database.

    Returns:
        List[:obj:`CompoundData`]: A list with the info of each compound available.

    """
    # First relate short names with names from the links in table 4
    r = requests.get("http://physics.nist.gov/PhysRefData/XrayMassCoef/tab4.html")
    html = r.text
    cells = re.findall(r"<TD.*?>(.*?)</TD>", html, re.DOTALL)[4:]  # Pick the cells, excluding the headers
    cells = list(filter(lambda s: s != "&nbsp;", map(lambda x: x.strip(), cells)))
    # Now cells are of the form:
    # <A href="ComTab/adipose.html">Adipose Tissue</A> (ICRU-44)
    # The part after </A> being optional
    name_dict = {}
    for c in cells:
        data = re.findall(r'<A.*?/(.*?).html">(.*?)</A>(.*)', c)[0]
        # data is a tuple with for example ('adipose', 'Adipose Tissue', ' (ICRU-44)')
        # The last element might be the empty string.
        # We associate short names to names
        name_dict[data[1] + data[2]] = data[0]

    # Now fetch the compound data
    r = requests.get("http://physics.nist.gov/PhysRefData/XrayMassCoef/tab2.html")
    html = r.text
    rows = re.findall(r"<TR.*?>(.*?)</TR>", html, re.DOTALL)[3:]  # Pick the rows, excluding the headers
    output = []
    errored = False
    for row in rows:
        parsed_row = re.findall(r"<TD.*?>(.*?)</TD>", row)
        # Remove trailing spaces
        parsed_row = list(map(lambda x: x.strip(), parsed_row))
        # Remove some cells with only "&nbsp;" (which are only in the first element, probably a bad formatting practice)
        parsed_row = list(filter(lambda s: s != "&nbsp;", parsed_row))
        # Dictionary entries by atomic number (as string), symbol and name.
        try:
            short_name = name_dict[parsed_row[0]]
            output.append(CompoundData(parsed_row, short_name))
        except KeyError:
            # TODO: Manually fix these errors.
            if not errored:
                print("Warning: errors found the following compounds:", file=sys.stderr)
                errored = True
            print("- " + parsed_row[0], file=sys.stderr)
    if errored:
        print("These materials are not available in the list", file=sys.stderr)

    return output
