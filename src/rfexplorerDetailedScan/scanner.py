#!/usr/bin/env python
import time
import RFExplorer
import csv
import sys


def eprint(*args, **kwargs):
    """ error print """
    print(*args, file=sys.stderr, **kwargs)
    sys.stderr.flush()


def dprint(*args, **kwargs):
    """ debug print """
    if 'verbose' in kwargs:
        if kwargs['verbose']:
            del kwargs['verbose']
            eprint(*args, **kwargs)


class DetailedScanner:
    def __init__(self, serialport, baudrate, verbose):
        self.verbose = verbose
        self.goodState = False
        self.sweepsComplete = False

        try:
            self.objRFE = RFExplorer.RFECommunicator()
            self.objRFE.AutoConfigure = False
            self.objRFE.GetConnectedPorts()
        except Exception as obEx:
            eprint("Error: " + str(obEx))

        if (self.objRFE.ConnectPort(serialport, baudrate)):

            # Reset the unit to start fresh
            self.objRFE.SendCommand("r")
            # Wait for unit to notify reset completed
            while(self.objRFE.IsResetEvent):
                pass
            # Wait for unit to stabilize
            time.sleep(3)

            # Request RF Explorer configuration
            self.objRFE.SendCommand_RequestConfigData()
            # Wait to receive configuration and model details
            while(self.objRFE.ActiveModel == RFExplorer.RFE_Common.eModel.MODEL_NONE):
                # Process the received configuration
                self.objRFE.ProcessReceivedString(True)

            if(self.objRFE.IsAnalyzer()):
                self.goodState = True
            else:
                eprint(
                    "Error: Device connected is a Signal Generator. \nPlease, connect a Spectrum Analyzer")

            sys.stdout.flush()
        else:
            eprint("Not Connected")

    def __del__(self):
        self.goodState = False
        self.objRFE.Close()
        self.objRFE = None

    def _updateFreqRange(self, startFreq, stopFreq):
        self.objRFE.UpdateDeviceConfig(startFreq, stopFreq)

        self.objRFE.ProcessReceivedString(True)
        dprint("Updating freq range to %s-%s" %
               (startFreq, stopFreq), verbose=self.verbose)
        dprint("   scans in memory: %s" %
               self.objRFE.SweepData.Count, verbose=self.verbose)

        objSweep = None
        while (objSweep is None or objSweep.StartFrequencyMHZ != startFreq):
            self.objRFE.ProcessReceivedString(True)
            if (self.objRFE.SweepData.Count > 0):
                objSweep = self.objRFE.SweepData.GetData(
                    self.objRFE.SweepData.Count - 1)
        dprint("(done. scans in memory now: %s)" %
               self.objRFE.SweepData.Count, verbose=self.verbose)

    def _processSweeps(self, aggregation):
        sweepCount = self.objRFE.SweepData.Count

        for sweepIndex in range(sweepCount):
            singleSweepData = self.objRFE.SweepData.GetData(sweepIndex)

            for i in range(singleSweepData.TotalSteps):
                freq = round(singleSweepData.GetFrequencyMHZ(i), 3)
                ampl = round(singleSweepData.GetAmplitude_DBM(i), 2)
                if freq in self.scanDataCounts:
                    self.scanDataCounts[freq] += 1

                    if aggregation == 'max':
                        if self.scanDataCalc[freq] < ampl:
                            self.scanDataCalc[freq] = ampl
                    elif aggregation == 'average':
                        self.scanDataCalc[freq] = self.scanDataCalc[freq] - self.scanDataCalc[freq] / \
                            self.scanDataCounts[freq] + \
                            ampl / self.scanDataCounts[freq]
                else:
                    self.scanDataCounts[freq] = 1
                    self.scanDataCalc[freq] = ampl

    def sweep(self, start_freq, end_freq, step_resolution, iterations, aggregation):
        if self.goodState:
            self.scanDataCalc = {}
            self.scanDataCounts = {}
            self.sweepsComplete = False

            for startFreq in range(start_freq, end_freq, step_resolution):
                stopFreq = startFreq + step_resolution
                dprint("starting process for %s" %
                       startFreq, verbose=self.verbose)

                self._updateFreqRange(startFreq, stopFreq)

                # Process all received data from device
                while (self.objRFE.SweepData.Count < iterations):
                    self.objRFE.ProcessReceivedString(True)

                self._processSweeps(aggregation)

            if len(self.scanDataCounts) > 0:
                self.sweepsComplete = True
        else:
            eprint("Analyzer not initialized properly. Not proceeding with sweep.")

    def writeData(self, format, output_file):
        if self.sweepsComplete:
            if format == 'csv':
                for freq in self.scanDataCalc.keys():
                    output_file.write("%s,%s\n" %
                                      (freq, self.scanDataCalc[freq]))
            else:
                eprint("Unsupported format, %s" % format)
        else:
            eprint("Sweeps did not complete. Not writing data to file.")
