# rf-explorer-detailed-scan

RFExplorer Detailed Scan

The RF Explorer is limited to 112 steps in a frequency sweep. When coordinating a larger frequency range, the resolution bandwidth (RBW) becomes larger and imprecise.

This script helps create scan datafiles with a lower RBW by breaking the sweep into smaller chunks and "stitching" them together for a final dataset. It connects to the RF Explorer over its USB interface and produces output files on the host computer.

Presently, only header-free CSV files are supported output -- suitable for import into Shure Wireless Workbench.

## Requirements

- A command line environemnt, such as:
  - Linux terminal
  - macOS X terminal
  - Windows command prompt
  - Windows running Git Bash
- Python (3.11 or greater)
  - virtualenv support preferred
- An RF Explorer (spectrum analyzer) with USB interface supported by the [RF Explorer for Python](https://github.com/RFExplorer/RFExplorer-for-Python) library

## Installation

If you simply want to install and use the latest published version of this script, run the following command (preferably within a Python virtual environment):

    pip install rfexplorer-detailed-scan

[Here is a video](https://www.youtube.com/watch?v=4yypnxZqxKc) demonstrating the installation and usage of this script with Shure Wireless Workbench.

## Usage

    Usage: rfexplorerDetailedScan [OPTIONS] OUTPUT_FILE

    Options:
      -p, --serialport TEXT           Serial port (None to autodetect)
      -b, --baudrate INTEGER          Serial port baud (default 500000)
      -s, --start-freq INTEGER        Scan start frequency (MHz)
      -e, --end-freq INTEGER          Scan end frequency (MHz)
      -r, --step-resolution INTEGER   Subdivide full spectrum into this many MHz
                                      (112 steps per)

      -i, --iterations INTEGER        Ensure at least this many sweeps run of the
                                      spectrum

      -a, --aggregation [average|max]
                                      Calculation to aggregate sweep passes
      -f, --format [csv]              Output format
      -v, --verbose

Leave `serialport` empty to auto-detect the connect RF Explorer.

`start-freq` and `end-freq` define the full range of the resulting scan data.

`step-resolution` is the size (in MHz) of each smaller scan. For instance, a step-resolution of 2 MHz (the default) results in an effective RBW of 2MHz/112 = 17.9 KHz, which is slightly better than the 25 KHz RBW of many Shure networked microphone receivers. The smaller the step-resolution, the longer the complete scan will take to complete.

In its spectrum analyzer mode, RF Explorer works by repeatedly scanning the configured sweep range. This script will let sweeps run at least `iterations` (default 10) times before incrementing the sweep frequencies by the step-resolution. The larger the number of iterations, the longer the scan will take to complete. However, with sufficiently small step-resolutions, there are often 5 or more sweeps complete by the time the script can even check!

With all of the sweep iteration data, the script currently has two `aggregation` calculations it can perform on each frequency's amplitude: `average` (default) or `max`. _Average_ speaks for itself, and _max_ uses the highest value found at each frequency across all iterations -- kind of like a peak hold.

## Examples

    rfexplorerDetailedScan -s 450 -e 650 scan-$(date +%Y%m%d-%H%M%S).csv

This will perform a scan from 450MHz to 650MHz with other defaults: Auto-detected RF Explorer using a baud rate of 500 Kbps, step resolution of 2 MHz (18 KHz RBW), at least 10 sweep iterations per step-resolution, averaging the amplitude at each frequency's sweep. Provided this is a bash-like environment with the `date` command available, this will save the results to a CSV file with the current date and time in the name.

## Credits

This script is made possible by [RF Explorer for Python](https://github.com/RFExplorer/RFExplorer-for-Python), and much of it is based on the included example scripts.
