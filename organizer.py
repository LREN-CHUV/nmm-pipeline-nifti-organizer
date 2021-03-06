#!/usr/bin/env python2

import argparse
import logging
import os
import glob
import shutil


DEFAULT_PROTOCOL = "T1"
DEFAULT_REPETITION = "1"
DEFAULT_ORGANISATION = ['PatientID', 'StudyID', 'SeriesDescription', 'SeriesNumber']


def main():
    logging.basicConfig(level=logging.INFO)

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("input_folder")
    args_parser.add_argument("output_folder")
    args = args_parser.parse_args()

    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    organize_nifti(args.input_folder, args.output_folder)


def organize_nifti(input_folder, output_folder):
    for nii_file in glob.glob(os.path.join(input_folder, "*.nii")):
        logging.info("Processing %s..." % nii_file)

        nii_file_basename = os.path.basename(nii_file)

        metadata = dict()
        metadata['SeriesDescription'] = DEFAULT_PROTOCOL
        metadata['SeriesNumber'] = DEFAULT_REPETITION
        metadata['PatientID'] = nii_file_basename.split('_')[0]
        metadata['StudyID'] = nii_file_basename.split('_')[1][:-4]

        nii_file_output_fullpath = output_folder
        for attribute in DEFAULT_ORGANISATION:
            nii_file_output_fullpath = os.path.join(nii_file_output_fullpath, metadata[attribute])

        if not os.path.exists(nii_file_output_fullpath):
            os.makedirs(nii_file_output_fullpath)
        logging.info("Copying %s to %s..." % (nii_file, nii_file_output_fullpath))
        shutil.copy2(nii_file, nii_file_output_fullpath)
    logging.info("DONE")


if __name__ == '__main__':
    main()
