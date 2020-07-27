#!/usr/bin/env python3
import argparse
import subprocess
import time
import logging
from shlex import split

logger = logging.getLogger("supervisor")

def parse_commandline_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", help="The process to supervise")
    parser.add_argument("-w", "--wait", help="Seconds to wait between restart attempts", type=int, default=2)
    parser.add_argument("-r", "--retries", help="Number of restart attempts before giving up", type=int, default=5)
    parser.add_argument("-i", "--interval", help="Check interval in seconds", type=int, default=2)
    parser.add_argument("-v", "--verbosity", help="Increase logging verbosity", action="count", default=0)
    return parser.parse_args()

def configure_logger(verbosity):
    console_handler = logging.StreamHandler()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    if verbosity > 0:
        logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    logger.debug('Logger has been configured')

def start_process(command):
    if isinstance(command, str):
        command = split(command)
        logger.debug('String command has been configured to list representation -> %s', command)
    try:
        process = subprocess.Popen(command)
        logger.debug('Attempting to spawn the process with command %s', command)
    except OSError as ex:
        logger.error('Failed to spawn the process: %s', ex)
        exit(1)
    else:
        logger.info('Spawned process with PID %d', process.pid)
        return process

def watch_process(process, args):
    while args.retries > 0:
        if process.poll() != None:
            args.retries = args.retries - 1
            logger.warning('Process exited with code %d, restarting. %d restarts left', process.returncode, args.retries)
            process = start_process(process.args)
            continue
        logger.debug('Process still running, waiting for %d seconds before the next check.', args.interval)
        time.sleep(args.interval)
    while process.poll() == None:
        logger.debug('Process still running, waiting for %d seconds before the next check.', args.interval)
        time.sleep(args.interval)
    logger.warning('Process exited with code %d and will not be restarted anymore', process.returncode)

if __name__ == "__main__":
    args = parse_commandline_arguments()
    configure_logger(args.verbosity)
    logger.debug('Command line arguments parsed: %s', vars(args))    
    process = start_process(args.cmd)
    watch_process(process, args)