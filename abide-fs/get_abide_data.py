#!/usr/bin/env python

# requires awscli: install using pip install awscli
# usage: python get_abide_fs.py /path/to/subject_file
# run from desired output directory
# runs QC by Andrew Doyle (docker pull crocodoyle/ibis-bids-qc)

import os, sys, errno

subjfile, download_type = sys.argv[1:]
mcdir = os.getcwd()

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

datadir = os.path.join(mcdir, 'data')
mkdir_p(datadir)
if download_type == "bids" or download_type == "both":
    mkdir_p(os.path.join(datadir,'bids'))

subjects_list = []
with open(subjfile) as subjects:
    for subject in subjects:
        subjects_list.append(subject.strip('\n'))

# get data from amazon s3
abide_url = 's3://fcp-indi/data/Projects/ABIDE_Initiative/'
fspath = 'Outputs/freesurfer/5.1/'
bidspath = 'RawDataBIDS/Caltech/'

for subject in subjects_list:
    fsdir = abide_url + fspath + subject
    bids_subject = "sub-" + subject.split('_')[1]
    bidsdir = abide_url + bidspath + bids_subject
    fs_outdir = os.path.join(datadir, 'derivatives', 'freesurfer', subject)
    bids_outdir = os.path.join(datadir, 'bids', bids_subject)
    
    if download_type == "fs":
        os.system('aws s3 cp --recursive --no-sign-request {} {}'.format(fsdir, fs_outdir))
    elif download_type == "bids":
	os.system('aws s3 cp --recursive --no-sign-request {} {}'.format(bidsdir, bids_outdir))
    elif download_type == "both":
	os.system('aws s3 cp --recursive --no-sign-request {} {}'.format(fsdir, fs_outdir))
	os.system('aws s3 cp --recursive --no-sign-request {} {}'.format(bidsdir, bids_outdir))
    else:
	print "Invalid download type. Choose 'fs', 'bids', or 'both'."


if download_type == "bids" or download_type == "both":
    os.system('docker run -v {}/data/bids'.format(mcdir))
