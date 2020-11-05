#!/bin/bash
#SBATCH --job-name=DLM-N2-bulk
#SBATCH --partition=batch
#SBATCH --nodes=1
#SBATCH --tasks-per-node=16
#SBATCH --time=24:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=jrhm21@bath.ac.uk #Change this to your email!
#SBATCH --account=re-ce1100

function nmols {
  awk '{if($1=="timestamp:")printf("%f\t",$2);else if($1=="orderparam:")printf("%f\t",$2);else if($1=="nmol:")printf("%f\n",$3);}' YAMLDATA.000 > $1_nmols.dat
}

module purge
module load group ce-molsim stack
module load dlmonte/2.06
cd "$1"
pwd

../DLMONTE-SRL.X &>/dev/null
if grep -i "normal exit" "./OUTPUT.000" >/dev/null
then
    echo "Simulation in directory $1 terminated normally"
    nmols $1
    mkdir archive/002/
    cp CONFIG archive/002/
    cp REVCON.000 CONFIG
    cp TMATRX.000 TMATRX
    rename 000 002 *
    mv *.002* archive/002/
    mv *.dat archive/002/
else
    echo "Uh oh! something's borked in simulation $1"
fi
