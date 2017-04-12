import argparse
import sys
from libaws.common import utils


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, dest="file_path",help='file path to caculate md5',required=True)
    parser.add_argument("-p", "--part", type=int, dest="part_number",help='divide part number of file')
    parser.add_argument("-z", "--size", type=int, dest="part_size",help='divide part size of file')
    args = parser.parse_args()
    if 1 == len(sys.argv):
        parser.print_help()
        sys.exit(0)
    file_path = args.file_path
    part_number = args.part_number

    if args.part_number is not None:
        print utils.get_file_hash_by_part(file_path,part_number)
    elif args.part_size is not None:
        print utils.get_file_hash_by_size(file_path,args.part_size)
    else:
        print utils.get_file_hash(file_path)

if __name__ == "__main__":
    main()
    

