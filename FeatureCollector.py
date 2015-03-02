# -*- coding: utf-8 -*-
__author__ = 'Kevin Koo'

"""
The class for feature collection
"""

import commonLib
from enum import Enum

DEBUG=False

Feature = Enum('Feature', 'antidebugging alteration backdoor com encoding encryption filesystem \
                            hashdump infogathering injection kernelmsg keystroke mutex nativeAPI \
                            networking newprocess readmemory registry resource screencapture service shell')

antidebugging = ['CheckRemoteDebuggerPresent', 'FindWindow', 'IsDebuggerPresent', \
                'OutputDebugString', 'QueryPerformanceCounter', 'GetTickCount', 'NtQueryInformationProcess']
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
    
# Long Instructions  
#   Ex: :004011DB 81 3D 84 79 40 00
pLongIns = ':[0-9A-F]{8}[\s]([0-9A-F][0-9A-F][\s\t]){10,16}'

# Short unidentified data
#   Ex:
pShortIns = '[\s\t]db\s[0-9A-F\s][0-9A-F\s][0-9A-F\s][\dh$]'
subroutine = 'S U B R O U T I N E'

if __name__ == '__main__':
    target = 'E:\\MS_Malware_Classification_Challenge\\train\\5\\8wm2jYBqV30okUMfuDCd.asm'
    resultFile = open('E:\\MS_Malware_Classification_Challenge\\feature\\features.txt','w')
    
    
    fc = commonLib.FeatureCollector(target)
    fc.readAsm()
    #fc.readLine(1, 200)
    
    fileName = target.split('\\')[-1]

    # [F001] # of subroutines identified by IDA Pro
    f001 = fc.checkFeature(subroutine, ['.text'])
    if DEBUG == True:
        print "\t# of subroutines identified by IDA Pro: " + str(f001)
    print "\tsubroutines: %d" % (f001)
    
    # [F002-F004] Packing
    isPacking = False
    f002 = len(fc.getSections())
    f003 = fc.checkFeature(pLongIns, ['.text'])
    f004 = fc.checkFeature(pShortIns, ['.rdata', '.data'])
    if f002 > 10 or f003 > 100 or f004 > 500:
        isPacking = True
    if DEBUG == True:
        print "\tPacking: "+ str(packing)
        print "\t\t# of sections: %d %s" % (f002, str(fc.getSections()))
        print "\t\t# of long instructions (>=16B): " + str(f003)
        print "\t\t# of short instructions (<=2B): " + str(f004)
    print "\tpacking: %s (sections:%d, longIns:%d, shortIns:%d)" % (isPacking, f002, f003, f004)
    
    if f002 > 7:
        print "\t\t" + str(fc.getSections())
    
    #print "%s|%s|%d" % ("packing", str(fc.getSections()), len(fc.getSections()))
    #print "%s|%s|%d" % ("packing", "LongInstructions", fc.checkFeature(pLongIns))
    #print "%s|%s|%d" % ("packing", "ShortInstructions", fc.checkFeature(pShortIns))
    
    #resultFile.write(fileName + "|" + "packing" + "|" + str(fc.getSections()) + "|" + str(len(fc.getSections())) + '\n')
    #resultFile.write(fileName + "|" + "packing" + "|" + "LongInstructions" + "|" + str(fc.checkFeature(pLongIns)) + '\n')
    #resultFile.write(fileName + "|" + "packing" + "|" + "LongInstructions" + "|" + str(fc.checkFeature(pShortIns)) + '\n')
    
    # [F005-F131]
    techniques = [antidebugging, alteration, backdoor, com, encoding, encryption, filesystem, \
                hashdump, infogathering, injection, kernelmsg, keystroke, mutex, nativeAPI, \
                networking, newprocess, readmemory, registry, resource, screencapture, service, shell]
    tIndex = 0
    for technique in techniques:
        total = 0
        isFeature = False
        for s in technique:
            cnt = fc.checkFeature(s, ['.text', '.idata'])
            #print "%s|%s|%d" % (Feature.__members__.keys()[tIndex], s, cnt)
            #resultFile.write(fileName + "|" + Feature.__members__.keys()[tIndex] + "|" + s + "|" + str(cnt) + '\n')
            if DEBUG == True:
                print "\t\t %s %s: %d" % (Feature.__members__.keys()[tIndex], s, cnt)
            total += cnt
            if total > 0:
                isFeature = True
        print "\t%s: %s (%d)" % (Feature.__members__.keys()[tIndex], isFeature, total)
        tIndex += 1
        
    resultFile.close()
    