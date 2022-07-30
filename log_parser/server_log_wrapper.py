import argparse
import re

from parsers import server_log_parser
from parsers import pm_log_parser

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_path', type=str, required=True, help='The path of raw server logs file. (require list of jsons format with .txt).')
    parser.add_argument('-o', '--save_path', type=str, required=True, help='The path to save parsed csv data.')
    return parser.parse_args()

def main():
    SERVER_IP = '10.19.11.215'
    args = parse_args()
    slp = server_log_parser.ServerLogParser(args.file_path, re.sub(r'/(?=.*?.csv)', '/1_', args.save_path))
    pmlp = pm_log_parser.PMLogParser(args.save_path, re.sub(r'/(?=.*?.csv)', '/2_', args.save_path), SERVER_IP)
    slp.main()
    pmlp.main()

if __name__ == '__main__':
    main()