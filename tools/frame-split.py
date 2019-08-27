#!/usr/bin/python3

import numpy as np
import argparse
from ase import Atoms as atom
from ase.io import read, write
import spglib

def main(fxyz, prefix, stride):

    # read frames
    if (fxyz != 'none'):
        frames = read(fxyz,':')
        nframes = len(frames)
        print("read xyz file:", fxyz,", a total of",nframes,"frames")


    standardized_frames = []

    for s in range(0,nframes,stride):
        lattice, scaled_positions, numbers = spglib.standardize_cell(frames[s],
                                                      to_primitive=True,
                                                      no_idealize=False,
                                                      symprec=1e-2)
        # output
        if np.sum(lattice) > 0:
            pbc = [True, True, True]
        else:
            pbc = [False,False,False]
        standardized_frame = atom(numbers=numbers,cell=lattice,scaled_positions=scaled_positions,pbc=pbc)
        write(prefix+'-'+str(s)+'.xyz',standardized_frame)

##########################################################################################
##########################################################################################

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-fxyz', type=str, required=True, help='Location of xyz file')
    parser.add_argument('--prefix', type=str, default='output', help='Filename prefix')
    parser.add_argument('--stride', type=int, default=1, help='output stride')
    args = parser.parse_args()

    main(args.fxyz, args.prefix,args.stride)
