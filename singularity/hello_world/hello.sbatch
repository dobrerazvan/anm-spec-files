#!/bin/bash

#SBATCH --nodes=1                      # Number of nodes requested
#SBATCH --ntasks-per-node=16           # Tasks per node
#SBATCH --time=01:00:00                # walltime

module load libraries/openmpi-1.8.8-gcc-4.8.5
mpirun singularity exec custom_image.sif hello
