"""
This library exposes clients for:
* interacting with external libraries (such as Google Docs)
* interacting with a combination of internal and/or external libraries (such as SeisoParser and Spetekmyo)

If your client only deals with an internal library you should not define it here.

Clients may have dependencies, which should be included externally in this project.
Client files within this library contain dependency hints so you may want to check them out.
"""

__author__ = "Raphael Nguyen"
__copyright__ = "© 2025 Raphael Nguyen"
__license__ = "MIT"
__version__ = "1.0.0"

from . import *
