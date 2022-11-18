"""
Use this script to change between different openPMD formats.

Everything in the input_file at that iteration will be copied into the
new file in the specified format.
"""

from checkpoint import openpmdcopy

iteration = 0

#input_file =  "/bigdata/hplsim/scratch/spreng88/runs/read_%T.h5"
input_file =  "/bigdata/hplsim/scratch/spreng88/runs/g10_ef.bp"
output_file = "/bigdata/hplsim/scratch/spreng88/runs/write_%T.h5"


files = openpmdcopy(input_file, output_file, iteration)

files.copy_series_data()
files.copy()

