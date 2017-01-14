#!/usr/bin/python3

import os
try:
    import psutil
except ImportError:
    import pip
    print("Installing missing packages (this will be done the first time only) :")
    if os.getuid() == 0:
        pip.main(["install", "psutil"])
    else:
        pip.main(["install", "psutil", "--user"])
    print("Done.\nRerun the command now.")
    exit(0)
import argparse
from time import sleep, localtime


# This function will execute until the end of the copy
def copy(time, verbose):
    while True:
        bytes_read = psutil.disk_io_counters().read_bytes / (1024*1024)
        bytes_wrote = psutil.disk_io_counters().write_bytes / (1024*1024)
        sleep(time)
        bytes_read = (psutil.disk_io_counters().read_bytes / (1024*1024) - bytes_read) / time
        bytes_wrote = (psutil.disk_io_counters().write_bytes / (1024*1024) - bytes_wrote) / time

        if verbose:
            t = localtime()
            print("[{:02}:{:02}:{:02}] R : {:.2f} Mb / W : {:.2f} Mb".format(
                t.tm_hour, t.tm_min, t.tm_sec, bytes_read, bytes_wrote))
        if bytes_read < 0.1 and bytes_wrote < 0.1:
            return


# This function will execute until the end of the cpu usage.
def cpu(time, verbose):
    while True:
        cpu_usage = psutil.cpu_times_percent(time).nice
        if verbose:
            t = localtime()
            print("[{:02}:{:02}:{:02}] cpu usage : {}%".format(t.tm_hour, t.tm_min, t.tm_sec, cpu_usage))
        if cpu_usage < 2:
            return


# This function will execute until the end of the download.
def download(time, verbose):
    while True:
        bytes_recv = psutil.net_io_counters().bytes_recv / 1000
        sleep(time)
        speed = (psutil.net_io_counters().bytes_recv/1000 - bytes_recv)/time
        if verbose:
            t = localtime()
            print("[{:02}:{:02}:{:02}] Download speed : {:.1f} KB/sec".format(
                t.tm_hour, t.tm_min, t.tm_sec, speed))
        if speed < 3:
            return


# This function will execute until the end of the upload.
def upload(time, verbose):
    while True:
        bytes_sent = psutil.net_io_counters().bytes_sent / 1000
        sleep(time)
        speed = (psutil.net_io_counters().bytes_sent/1000 - bytes_sent)/time
        if verbose:
            t = localtime()
            print("[{:02}:{:02}:{:02}] Upload speed : {:.1f} KB/sec".format(t.tm_hour, t.tm_min, t.tm_sec, speed))
        if speed < 3:
            return


def main():

    args_parser = argparse.ArgumentParser(description="This program is used to perform an operation after an action.")

    # Adding the available arguments with the ArgumentParser() object.
    args_parser.add_argument('-o', '--operation', type=str, required=True, choices=['cpu', 'copy', 'download', 'upload'],
                            help="Type of operation to wait for")
    args_parser.add_argument('-a', '--action', type=str, required=False, choices=['poweroff', 'reboot', 'hibernate', 
                            'nothing'], default="poweroff", help="The action to performe after the end of the operation\
                            (default : poweroff)")
    args_parser.add_argument('-t', '--time', type=int, default=10, 
                            help='Interval to test if the operation is still running')
    args_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose')
    args_parser.add_argument('--version', action='version', version='%(prog)s 0.2')

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
