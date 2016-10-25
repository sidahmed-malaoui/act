#!/usr/bin/python3

import psutil
import os
import argparse
from time import sleep


# This function will execute until the end of the copy
def copy(time, verbose):
    while True:
        iowait = psutil.cpu_times_percent(interval=time).iowait
        if verbose:
            print("Usage of the iowait : {}%".format(iowait))
        if iowait < 2:
            return


# This function will execute until the end of the cpu usage.
def cpu(time, verbose):
    while True:
        cpu_usage = psutil.cpu_times_percent(time).nice
        if verbose:
            print("Usage of the cpu : {}%".format(cpu_usage))
        if cpu_usage < 2:
            return


# This function will execute until the end of the download.
def download(time, verbose):
    while True:
        bytes_recv = psutil.net_io_counters().bytes_recv / 1000
        sleep(time)
        speed = (psutil.net_io_counters().bytes_recv/1000 - bytes_recv)/time
        if verbose:
            print("Download speed : {:.1f} KB/sec".format(speed))
        if speed < 3:
            return


# This function will execute until the end of the upload.
def upload(time, verbose):
    while True:
        bytes_sent = psutil.net_io_counters().bytes_sent / 1000
        sleep(time)
        speed = (psutil.net_io_counters().bytes_sent/1000 - bytes_sent)/time
        if verbose:
            print("Download speed : {:.1f} KB/sec".format(speed))
        if speed < 3:
            return


def main():

    args_parser = argparse.ArgumentParser()

    # Adding the available arguments with the ArgumentParser() object.
    args_parser.add_argument('-o', '--operation', type=str, required=True, choices=['cpu', 'copy', 'download', 'upload'],
                            help="Type of operation to wait for")
    args_parser.add_argument('-a', '--action', type=str, required=False, choices=['poweroff', 'reboot', 'hibernate', 
                            'nothing'], default="poweroff", help="The action to performe after the end of the operation\
                            (default : poweroff)")
    args_parser.add_argument('-t', '--time', type=int, default=10, 
                            help='Interval to test if the operation is still running')
    args_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose')

    args = args_parser.parse_args()
    
    # Need to be root to execute this script.
    if os.getuid() != 0 and args.action in ['poweroff', 'reboot', 'hibernate']:
        print("need to be root to {}".format(args.action))
        exit(-1)
    
    # Waiting for the asked operation.
    if args.operation == 'copy':
        copy(args.time, args.verbose)
    elif args.operation =='cpu':
        cpu(args.time, args.verbose)
    elif args.operation == 'download':
        download(args.time, args.verbose)
    elif args.operation == 'upload':
        upload(args.time, args.verbose)

    # Executing the asked action.
    if args.action == 'poweroff':
        os.system('poweroff')
    elif args.action == 'reboot':
        os.system('reboot')
    elif args.action == 'hibernate':
        os.system('pm-hibernate')
    elif args.action == 'nothing':
        pass


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
