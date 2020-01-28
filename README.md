# dlmonte_python_setup
 Setup scripts and object for DL_monte 
 
Useful files included:

Controlwriter - A simple class-based script for writing DL_Monte control files
windowscan.py - A script for doing umbrella sampling with DL_Monte and transition matrix files
tmatrix_combine.py - a simple script for taking multiple tmatrix files in and summing them

Less useful scripts:
Supercell.py - a way of turning music .mol files into CONFIG files for DL_Monte that need ot be manually edited before they're handy. But it'll make a 1x1x1 or 2x2x2 cell, so there's that.
Configlength.py - a script for chopping molecules off a configuration file to make artificial starting configs. Only workks ofr simulations of N2 only
Controlwriter - debug.py - a testbed for more general classes to be used in Controlwriter.py
