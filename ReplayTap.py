#!/usr/bin/python

import subprocess
import sys
from time import sleep
import multiprocessing

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
    if len(sys.argv) < 2:
        print "not .autc file input"
        exit()
    fileName = sys.argv[1]
    if ".autc" not in fileName:
        print "not a recognized file format .autc"
        exit()
    print 'Automated UI test case will execute from: {0}'.format(fileName)
    return fileName

def recordScreen(fileName):
    print "Started Recording Thread"
    command = 'adb shell screenrecord /sdcard/{0}.mp4'.format(fileName)
    recordScreenProc = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def reinstallsequence():
    ANDROID_PKG = ""
    ACTIVITY = ""
    reinstallCommands = []
    reinstallCommands.append('adb shell am force-stop %s' % (ANDROID_PKG))
    # reinstallCommands.append('adb uninstall %s' % (ANDROID_PKG))
    # reinstallCommands.append('adb install *.apk')
    reinstallCommands.append('adb shell am start -n %s/%s' % (ANDROID_PKG, ACTIVITY))
    for command in reinstallCommands:
        print command
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print proc.stdout.read()

def adbinfo():
    adbDeviceSerialProc = subprocess.Popen('adb shell getprop ro.boot.serialno', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    serialno = adbDeviceSerialProc.stdout.read()
    adbBrandProc = subprocess.Popen('adb shell getprop ro.product.brand', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    brand =  adbBrandProc.stdout.read()
    androidOSVerProc = subprocess.Popen('adb shell getprop ro.build.version.release', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    OSVer = androidOSVerProc.stdout.read()
    print "Brand: ", brand, "Serial: ", serialno, "ANDROID OS: ", OSVer


def execute_tap(fileName):
    fo = open(fileName, 'r')
    privPressedTime = 0.0
    durationBetweenPress = 0.0
    for line in fo.readlines():
        if "wait" in line:
            waitTime = float(line.split()[-1])
            sleep(waitTime)
        elif "xpos" in line:
            xpos = int(line.split()[-1])
        elif "ypos" in line:
            ypos = int(line.split()[-1])
        elif "tap" in line:
            command = 'adb shell input tap {0} {1}'.format(xpos, ypos)
            print command
            subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    fo.close()

# start
fname = init()
adbinfo()
reinstallsequence()
sleep(25)

# print "Started Recording Thread"
# command = 'adb shell screenrecord /sdcard/{0}.mp4'.format(fname)
# recordScreenProc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#
# sleep(2)
execute_tap(fname)


command = 'adb pull /sdcard/{0}.mp4'.format(fname)
proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print proc.stdout.read()

