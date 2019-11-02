#!/usr/bin/env python3
'''Demonstrate the use of the argparse module: how to retrieve the command line argument.'''
import argparse

parser = argparse.ArgumentParser(description="Usage Report based on the last command",epilog="Copyright 2018 - Raymond Chan")
parser.add_argument("-l", "--list", type=str, choices=['user','host'], help="generate user name or remote host IP from the given files")
parser.add_argument("-r", "--rhost", help="usage report for the given remote host IP")
parser.add_argument("-t","--type", type=str, choices=['daily','weekly'], help="type of report: daily or weekly")
parser.add_argument("-u", "--user", help="usage report for the given user name")
parser.add_argument("-v","--verbose", action="store_true",help="turn on output verbosity")
parser.add_argument("files",metavar='F', type=str, nargs='+',help="list of files to be processed")
args=parser.parse_args()
if args.verbose:
    print('Files to be processed:',args.files)
    print('Type of args for files',type(args.files))
    if args.user:
        print('usage report for user:',args.user)
    if args.rhost:
        print('usage report for remote host:',args.rhost)
    if args.type:
        print('usage report type:',args.type)

