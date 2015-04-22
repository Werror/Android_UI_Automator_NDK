#!/usr/bin/python

import subprocess
import os.path

class bcolors:
    OK = '\033[95m'
    XBLUE = '\033[94m'
    YGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def init():
    fileName = raw_input("Enter the file name: ") + ".autc"
    if os.path.isfile(fileName):
        print "File already exist, please pick another one"
        exit()
    print 'Automated UI test case will be saved as: {0}'.format(fileName)
    return fileName

def adbinfo():
    adbDeviceSerialProc = subprocess.Popen('adb shell getprop ro.boot.serialno', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    serialno = adbDeviceSerialProc.stdout.read()
    adbBrandProc = subprocess.Popen('adb shell getprop ro.product.brand', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    brand =  adbBrandProc.stdout.read()
    androidOSVerProc = subprocess.Popen('adb shell getprop ro.build.version.release', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    OSVer = androidOSVerProc.stdout.read()
    print "Brand: ", brand, "Serial: ", serialno, "ANDROID OS: ", OSVer
    return OSVer

def geteventid(OSVer):
    if "4.1.1" in OSVer:
        eventID = 6
    elif "4.4.4" in OSVer:
        eventID = 2
    elif "5.1" in OSVer:
        eventID = 1
    return eventID


def record(fileName, OSVer):
    fo = open(fileName, 'w')
    privPressedTime = 0.0
    durationBetweenPress = 0.0
    eventID = geteventid(OSVer)
    command = 'adb shell getevent -lt /dev/input/event{0}'.format(eventID)
    tapPositionProc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        line = tapPositionProc.stdout.readline()
        if line != '':
            #the real code does filtering here
            if "ABS_MT_TRACKING_ID" in line:
                if "ffffffff" in line:
                    print "Release"
                    fo.write("tap\n")
                else:
                    currentPressedTime = float(line.split()[1][:-1])
                    if privPressedTime != 0.0:
                        durationBetweenPress = currentPressedTime - privPressedTime
                    privPressedTime = currentPressedTime
                    print "Waited for " + str(durationBetweenPress) + " to press"
                    fo.write("wait " + str(durationBetweenPress) + "\n")
                print bcolors.BOLD, line.rstrip(), bcolors.ENDC
            elif "ABS_MT_POSITION_X" in line:
                print bcolors.XBLUE, line.rstrip(), bcolors.ENDC
                xposHex = line.split()[-1]
                xposDec = int("0x"+xposHex, 0);
                print xposDec
                fo.write("xpos " + str(xposDec) + "\n")
            elif "ABS_MT_POSITION_Y" in line:
                print bcolors.YGREEN, line.rstrip(), bcolors.ENDC
                yposHex = line.split()[-1]
                yposDec = int("0x"+yposHex, 0)
                print yposDec
                fo.write("ypos " + str(yposDec) + "\n")
        else:
            break
    fo.close()

# start
fileName = init()
OSVer = adbinfo()
record(fileName, OSVer)
