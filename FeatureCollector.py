# -*- coding: utf-8 -*-
__author__ = 'Kevin Koo'

"""
The class for feature collection
"""

import commonLib
from enum import Enum
import os
import sys
from time import sleep
from progressBar import *

DEBUG = False

'''
# of subroutines: 
	.text:[0-9A-F]{8}(\s+)sub_
	S U B R O U T I N E
# of blocks
	.text:[0-9A-F]{8}(\s+)loc_
# of function calls
	.text:[A-F0-9]{8}.+call(\s+)sub_
 .idata:[A-F0-9]{8}.+extrn
Call types
	.text:[A-F0-9]{8}.+__cdecl sub_
	.text:[A-F0-9]{8}.+__stdcall sub_
	.text:[A-F0-9]{8}.+__fastcall sub_ (?)
Others
    AsmByteCount.py
    AsmLength.py
    entropyGraph.py
    more..
'''

Feature = Enum('Feature', 'antidebugging alteration backdoor com encoding encryption filesystem \
                            hashdump infogathering injection kernelmsg keystroke mutex nativeAPI \
                            networking newprocess readmemory registry resource screencapture service shell')

antidebugging = ['CheckRemoteDebuggerPresent', 'FindWindow', 'IsDebuggerPresent', \
                'OutputDebugString', 'QueryPerformanceCounter', 'GetTickCount', 'NtQueryInformationProcess', 'rdtsc']
alteration = ['NetScheduleJobAdd', 'SetFileTime', 'SfcTerminateWatcherThread']
backdoor = ['ConnectNamedPipe']
com = ['CoCreateInstance', 'DllCanUnloadNow', 'DllGetClassObject', 'DllInstall', \
        'DllRegisterServer', 'DllUnregisterServer', 'OleInitialize', 'CoInitialize']
encoding = ['xor', 'rol', 'ror', 'rot']
encryption = ['CertOpenSystemStore', 'Cert', 'Crypt', 'CryptAcquireContext']
filesystem = ['CreateFile', 'ReadFile', 'WriteFile', 'CreateFileMapping', 'MapViewOfFile']
hashdump = ['SamIConnect', 'SamIGetPrivateData', 'SamQueryInformationUse']
infogathering = ['FindFirstFile', 'FindNextFile', 'GetAdaptersInfo', 'GetModuleFilename', \
                'GetModuleHandle', 'GetStartupInfo', 'GetSystemDefaultLangId', 'GetTempPath', \
                'GetThreadContext', 'GetVersion', 'GetWindowsDirectory', \
                'IsNTAdmin', 'IsWoW64Process']
injection = ['AdjustTokenPrivileges', 'CreateRemoteThread', 'CreateToolhelp32Snapshot',\
             'EnumProcessModules', 'GetProcAddress', 'LdrLoadDll', 'LoadLibrary', 'Module32First',\
             'Module32Next', 'OpenProcess', 'Process32First', 'Process32Next', 'QueueUserAPC', \
             'ResumeThread', 'ZwUnmapViewOfSection', 'SetThreadContext', 'SuspendThread', 'EnumProcesses' \
             'Thread32First', 'Thread32Next', 'VirtualAlloc', 'VirtualProtect', 'WriteProcessMemory']
kernelmsg = ['DeviceIoControl']
keystroke = ['AttachThreadInput', 'CallNextHook', 'GetAsyncKeyState', 'GetForegroundWindow', \
            'GetKeyState', 'MapVirtualKey', 'SetWindowsHook']
mutex = ['CreateMutex', 'ReleaseMutex', 'OpenMutex']
nativeAPI = ['NtQueryInformationThread', 'NtQueryInformationFile', 'NtQueryInformationKey', \
             'NtSetInformationProcess', '^Zw']
networking = ['accept', 'bind', 'listen', 'socket', 'connect', 'FtpPutFile', 'gethostbyname', \
              'gethostname', 'inet_addr', 'InternetOpen', 'InternetOpenUrl', 'InternetReadFile', \
              'InternetWriteFile', 'NetShareEnum', 'recv', 'send', 'URLDownloadToFile', 'gethostbyaddr',\
              'WSAConnect', 'WSAStartup']
newprocess = ['ShellExecute', 'system', 'WinExec', 'CreateProcess', 'CreateThread']
readmemory = ['ReadProcessMemory', 'Toolhelp32ReadProcessMemory']
registry = ['RegisterHotKey', 'RegOpenKey', 'RegSetValue', 'RegGetValue']
resource = ['FindResource', 'LoadResource']
screencapture = ['BitBlt', 'GetDC']
service = ['ControlService', 'CreateService', 'StartService', 'OpenSCManager', 'StartServiceCtrlDispatcher']
shell = ['PeekNamedPipe']

# 22 Features to describe malware techinques in use
techniques = [antidebugging, alteration, backdoor, com, encoding, encryption, filesystem, \
              hashdump, infogathering, injection, kernelmsg, keystroke, mutex, nativeAPI, \
              networking, newprocess, readmemory, registry, resource, screencapture, service, shell]
    
# Long Instructions  
#   [Ex] :004011DB 81 3D 84 79 40 00
pLongIns = '.+:[0-9A-F]{8}[\s]([0-9A-F][0-9A-F][\s\t]){10,16}'
# Short unidentified data
#   [Ex] (db    0) or (db 03dh)
unidentifiedData = '[\s\t]db\s[0-9A-F\s][0-9A-F\s][0-9A-F\s][\dh$]'

# Some useful identifiers
imports = 'Imports from.+dll'
subroutines1 = 'S U B R O U T I N E'
subroutines2 = '[0-9A-F]{8}(\s+)sub_.+endp'
blocks = '[0-9A-F]{8}(\s+)loc_'
userFunctionCalls = '[A-F0-9]{8}.+call(\s+)sub_'
importFunctionCalls ='[A-F0-9]{8}.+extrn'
dll = '(dllMain|DllEntryPoint)'

# This is one of WIN_Virus_Ramnit patterns
# '83(\s)EC(\s)04(\s).+\r\n.+[A-F0-9]{8}(\s)6?.+pusha'
ramnit1 = '83(\s)EC(\s)04(\s)'
ramnit2 = '.+[A-F0-9]{8}(\s)6?.+pusha'

def existYN(data):
    value = 'F'
    if data == True:
        value = 'T'
    else:
        return value
    return value

def collectFeatures(fc, target):
    fc.readAsm()
    #fc.readLine(100, 110)
    
    fileName = target.split(os.sep)[-1]
    label = target.split(os.sep)[-2]
    
    # [F001-F004] Basic assembly charateristics
    f001 = len(fc.getSections())
    f002 = fc.checkFeature(pLongIns)
    f003 = fc.checkFeature(unidentifiedData)
    
    # [F005-F008] Some useful identifiers
    f004 = fc.checkFeature(imports)
    f005 = fc.checkFeature(subroutines1)
    f006 = fc.checkFeature(subroutines2)
    f007 = fc.checkFeature(blocks)
    f008 = fc.checkFeature(userFunctionCalls)
    f009 = fc.checkFeature(importFunctionCalls)
    
    isDll = False
    f010 = existYN(isDll)
    if fc.checkFeature(dll) > 0:
        isDll = True
        f010 = existYN(isDll)
    
    isRamnIt = False
    f011 = existYN(isRamnIt)
    f011_1 = fc.checkFeature(ramnit1)
    f011_2 = fc.checkFeature(ramnit2)
    if f010 and f011_1 > 0 and f011_2 > 0:
        isRamnIt = True
        f011 = existYN(isRamnIt)
     
    if DEBUG == True:
        print "\t\t# of sections: %d %s" % (f001, str(fc.getSections()))
        print "\t\t# of long instructions in .text section(>=16B): " + str(f002)
        print "\t\t# of unidentified data in .rdata and .data section(<=2B): " + str(f003)
        print "\t\t# of imports from IAT: " + str(f004)
        print "\t\t# of subroutines (IDA): " + str(f005)
        print "\t\t# of subroutines (sub_): " + str(f006)
        print "\t\t# of blocks (loc_): " + str(f007)
        print "\t\t# of user function calls (call loc_): " + str(f008)
        print "\t\t# of import function calls (extrn): " + str(f009)
        print "\t\tDLL? " + str(f010)
        print "\t\tpusha? " + str(f011)

    result = fileName.split('.asm')[0] + ',' + str(label) + ',' + str(f001) + ',' + \
            str(f002) + ',' + str(f003) + ',' + str(f004) + ',' + str(f005) + ',' + \
            str(f006) + ',' + str(f007) + ',' + str(f008) + ',' + str(f009) + ',' + \
            str(f010) + ',' + str(f011) + ','
            
    resultDetails = result

    tIndex = 0
    for technique in techniques:
        total = 0
        isFeature = False
        for s in technique:
            cnt = fc.checkFeature(s)
            resultDetails += str(cnt) + ','
            #print "%s|%s|%d" % (Feature.__members__.keys()[tIndex], s, cnt)
            #resultFile.write(fileName + "|" + Feature.__members__.keys()[tIndex] + "|" + s + "|" + str(cnt) + '\n')
            if DEBUG == True:
                print "\t\t %s %s: %d" % (Feature.__members__.keys()[tIndex], s, cnt)
            total += cnt
            if total > 0:
                isFeature = True
        #print "\t%s: %s (%d)" % (Feature.__members__.keys()[tIndex], isFeature, total)
        result += existYN(isFeature) + ','
        tIndex += 1
    
    return (result[:-1] + '\n', resultDetails[:-1] + '\n')

    
if __name__ == '__main__':
    
    dataBase = commonLib.getBase(os.name)
    trainDir = dataBase + 'train' + os.sep
    featureResult1 = dataBase + 'feature' + os.sep + 'feature_results.csv'
    featureResult2 = dataBase + 'feature' + os.sep + 'feature_results_details.csv'
    trainLabels = range(1,10)
    
    targets = []
    for trainLabel in trainLabels:
        for tr in os.listdir(trainDir + str(trainLabel)):
            trFile = trainDir + str(trainLabel) + os.sep + tr
            fileSize = os.stat(trFile).st_size
            if tr.endswith('asm') and fileSize < 5000000L: #and fileSize >= 5000000L:
                targets.append(trFile)
    
    #targets = [trainDir + os.sep + '1' + os.sep + '0iS3pwlgJco8XORD4TLq.asm']
    totalTarget = len(targets)
    resultFile1 = open(featureResult1, 'w')
    resultFile2 = open(featureResult2, 'w')
    
    category1 = 'malware, label, sections, longIns, unidentifiedData, imports, subRoutines, sub_, blocks, userfuncalls, importfuncalls, dll, pusha, '
    category2 = 'antidebugging, alteration, backdoor, com, encoding, encryption, filesystem, hashdump, infogathering, injection, kernelmsg, keystroke, mutex, nativeAPI, networking, newprocess, readmemory, registry, resource, screencapture, service, shell\n'
    category3 = ''
    
    tIndex = 0
    for technique in techniques:
        for s in technique:
            tech = Feature.__members__.keys()[tIndex]
            category3 += tech[:3] + '_' + s + ','
        tIndex += 1
    
    category3 = category3[:-1] + '\n'
    
    resultFile1.write(category1 + category2)
    resultFile2.write(category1 + category3)
    print "Total targets: %d" % (totalTarget)
    
    cnt = 0
    progress = progressBar(0, totalTarget, 50)
    for target in targets:
        fc = commonLib.FeatureCollector(target)
        #print "[%04d] Processing... %s" % (cnt, target)
        (results, resultDetails) = collectFeatures(fc, target)
        resultFile1.write(results)
        resultFile2.write(resultDetails)
        cnt += 1
        progress(cnt)
        sleep(0.1)
        
    resultFile1.close()
    resultFile2.close()