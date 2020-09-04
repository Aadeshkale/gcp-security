"""
This script perform some checks on GCP compute engine VM's
"""
import os
import json
import argparse
import sys
import csv







if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--service_account",
                        help="Pass service account file path with appropriate permissions", type=str)
    args = parser.parse_args()
    try:
        path = args.service_account
    except Exception as e:
        print("Exception:", e)
        sys.exit()



