#!/bin/bash

# directory containing GLAM output files:
DATA_DIR='/nobackup/earsj/out/africap/DIMlookup/rawouts'

# directory from which jobs will be run:
NC_DIR='/nobackup/chmcsy/out/nc_outs'

# directory job std out / std err:
JOB_OUT='/nobackup/chmcsy/job_out_consolidate'

# directory for completed job scripts:
JOB_DONE='/nobackup/chmcsy/consolidate_completed'

# conda install location
CONDA_LOC='/nobackup/chmcsy/miniconda3'

# python script location
PYLOC='~/iFEED_Prototype/DIMCool_data_tool'

RUN_DIR=$PWD

# number of parallel processes for rcp-level consolidation
N_PROC='8'

mkdir -p $JOB_DONE
mkdir -p $JOB_OUT

# going to loop over these in turn, and submit a job for each cobination:
#CROPS="maize soybean potato groundnut"
#REGIONS="malawi zambia tanzania safrica"
#MODELS="bcc-csm1-1 BNU-ESM CSIRO-Mk3-6-0 GFDL-ESM2G IPSL-CM5A-LR MIROC-ESM MPI-ESM-LR MRI-CGCM3 NorESM1-M bcc-csm1-1-m CanESM2 CNRM-CM5 GFDL-CM3 GFDL-ESM2M IPSL-CM5A-MR MIROC5 MIROC-ESM-CHEM MPI-ESM-MR"
#RCPS="rcp26 rcp85"

CROPS="groundnut"
REGIONS="malawi"
MODELS="bcc-csm1-1"
RCPS="rcp26"

# prefix for job script:
JOB_PREFIX='consolidate'

# start looping:
for c in ${CROPS}
do
  for r in ${REGIONS}
  do
    for m in ${MODELS}
    do
      for rcp in ${RCPS}
      do

        # make directories for job outputs and job scripts:
        mkdir -p ${JOB_OUT}/${r}/${c}/${m}
        mkdir -p ${JOB_DONE}/${r}/${c}/${m}

        # job script name:
        JOB_SCRIPT="${RUN_DIR}/${JOB_PREFIX}_${c}_${r}_${m}_${rcp}.sge"
        SGE_STDOUT_PATH="${JOB_OUT}/${r}/${c}/${m}/$(basename ${JOB_SCRIPT}).o"
        SGE_STDERR_PATH="${JOB_OUT}/${r}/${c}/${m}/$(basename ${JOB_SCRIPT}).e"
        RCP_DATA_DIR="${DATA_DIR}/${r}/${c}/${m}/${rcp}"

        # copy template script:
        cat > ${JOB_SCRIPT} <<-EOF
#!/bin/bash
#$ -cwd -V
#$ -l h_rt=12:00:00
#$ -o ${SGE_STDOUT_PATH}
#$ -e ${SGE_STDERR_PATH}
#$ -pe smp ${N_PROC}

. ${CONDA_LOC}/etc/profile.d/conda.sh
conda activate DIMdata

cd ${PYLOC}

python3 year_collator.py -d ${RCP_DATA_DIR} -o ${NC_DIR} -p ${N_PROC}
EOF
        chmod 755 ${JOB_SCRIPT}

        # submit:
        cd ${RUN_DIR}
        # remove existing output files:
        \rm -f ${SGE_STDOUT_PATH} ${SGE_STDERR_PATH}
        qsub ./$(basename ${JOB_SCRIPT})

      done
    done
  done
done
