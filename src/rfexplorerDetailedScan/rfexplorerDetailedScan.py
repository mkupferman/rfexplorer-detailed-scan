#!/usr/bin/env python
import click
from rfexplorerDetailedScan.scanner import DetailedScanner


@click.command()
@click.argument('output-file', type=click.File('w'))
@click.option('--serialport', '-p', default=None, help='Serial port (None to autodetect)')
@click.option('--baudrate', '-b', default=500000, help='Serial port baud (default 500000)')
@click.option('--start-freq', '-s', default=450, help='Scan start frequency (MHz)')
@click.option('--end-freq', '-e', default=550, help='Scan end frequency (MHz)')
@click.option('--step-resolution', '-r', default=2, help='Subdivide full spectrum into this many MHz (112 steps per)')
@click.option('--iterations', '-i', default=10, help='Ensure at least this many sweeps run of the spectrum')
@click.option('--aggregation', '-a', default='average', type=click.Choice(['average', 'max']), help='Calculation to aggregate sweep passes')
@click.option('--format', '-f', default='csv', type=click.Choice(['csv']), help='Output format')
@click.option('--verbose', '-v', is_flag=True, default=False)
def rfexplorerDetailedScan(output_file, serialport, baudrate, start_freq, end_freq, step_resolution, iterations, aggregation, format, verbose):
    scanner = DetailedScanner(serialport, baudrate, verbose)
    scanner.sweep(start_freq, end_freq, step_resolution,
                  iterations, aggregation)
    scanner.writeData(format, output_file)
