# Daemon Supervisor
This tool checks that the process is running at all times and starts it in case is down.

### Prerequisites
Python 3.5+
The script doesn't use any external dependencies.
No additional packages required, standard library is enough to run it.

### Usage
supervisor.py [-h] [-w WAIT] [-r RETRIES] [-i INTERVAL] [-v] cmd

### Arguments

positional arguments:
-  cmd                   The process to supervise

optional arguments:
-  -h, --help                          show the help message and exit
-  -w WAIT, --wait WAIT                Seconds to wait between restart attempts (default = 2)
-  -r RETRIES, --retries RETRIES       Number of restart attempts before giving up (default = 5)
-  -i INTERVAL, --interval INTERVAL    Check interval in seconds (default = 2)
-  -v, --verbosity                     Increase logging verbosity (default loglevel INFO)
