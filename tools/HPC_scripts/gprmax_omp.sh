#!/bin/sh

#####################################################################################
### Change to current working directory:
### Use consistent indentation and add comments
#####################################################################################

# Change to the directory where this script is located
cd "$(dirname "$0")"

### Specify runtime (hh:mm:ss):
### Use consistent indentation and add comments
#####################################################################################

# Request 1 hour of runtime
#$ -l h_rt=01:00:00

### Email options:
### Use consistent indentation and add comments
#####################################################################################

# Send an email when the job starts, ends, or aborts
#$ -m ea -M joe.bloggs@email.com

### Parallel environment ($NSLOTS):
### Use consistent indentation and add comments
#####################################################################################

# Request 16 shared memory slots
#$ -pe sharedmem 16

### Job script name:
### Use a more descriptive job name
#####################################################################################

# Give the job a descriptive name
#$ -N simulate_gprmax_model.sh

#####################################################################################
### Initialise environment module
### Load and activate Anaconda environment for gprMax, i.e. Python 3 and required packages
### Set number of OpenMP threads for each gprMax model
#####################################################################################

# Load the Anaconda module
module load anaconda

# Activate the gprMax environment
conda activate gprMax

# Set the number of OpenMP threads
export OMP_NUM_THREADS=16

### Run gprMax with input file
### Use full paths instead of relative paths
#####################################################################################

# Run gprMax with the input file and 10 iterations
python -m /full/path/to/gprMax/mymodel.in -n 10
