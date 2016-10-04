#!/usr/bin/python3

import psutil
import os
import argparse


def copy(time, verbose):
    while True:
        iowait = psutil.cpu_times_percent(interval=time).iowait
        if verbose:
            print("Usage of the iowait : {}%".format(iowait))
        if iowait < 2:
            os.system("poweroff")


def cpu(time, verbose):
    while True:
        cpu_usage = psutil.cpu_times_percent(time).nice
        if verbose:
            print("Usage of the cpu : {}%".format(cpu_usage))
        if cpu_usage < 2:
            os.system("poweroff")


def main():

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('-o', '--operation', type=str, required=True, choices=['cpu', 'copy', 'download', 'upload'],
                            help="Type of operation to wait for")
    args_parser.add_argument('-t', '--time', type=int, default=10, 
                            help='Time to wait for after the operation has finished')
    args_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose')

    args = args_parser.parse_args()
    
    if os.getuid() != 0:
        print("need to be root")
        exit(-1)
    
    if args.operation == 'copy':
        copy(args.time, args.verbose)
    elif args.operation =='cpu':
        cpu(args.time, args.verbose)



if __name__ == '__main__':
    try:
        main()
    except:
        pass