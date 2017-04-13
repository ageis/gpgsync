# -*- coding: utf-8 -*-

from ctypes import *
from ctypes.util import find_library

from .cparser import define, parse

# Cryptic message codes
def err_sub(x):
    return (((x)&0xfff)<<14)

def err_system(x):
    return (((x)&0x3f)<<26)

def sys_iokit():
    return err_system(0x38)

def sub_iokit_common():
    return err_sub(0)

def iokit_common_msg(message):
    return (sys_iokit()|sub_iokit_common()|message)

# System message codes
kIOMessageSystemWillSleep = iokit_common_msg(0x280)
kIOMessageSystemWillPowerOn = iokit_common_msg(0x320)
kIOMessageSystemHasPoweredOn = iokit_common_msg(0x300)
kIOMessageCanSystemSleep = iokit_common_msg(0x270)
kIOMessageSystemWillNotSleep = iokit_common_msg(0x290)

# various types to match headers
mach_port_t = define('mach_port_t',  'void*')
io_object_t = define('io_object_t',  'void*')
io_iterator_t = define('io_iterator_t','void*')
io_service_t = define('io_service_t', 'void*')
io_connect_t = define('io_connect_t', io_object_t)
io_registry_entry_t = define('io_registry_entry_t', io_object_t)

define('__CFRunLoop', 'void*')
CFRunLoopRef = define('CFRunLoopRef', '__CFRunLoop*')
define('__CFRunLoopSource', 'void*')
CFRunLoopSourceRef = CFRunLoopSourceRef = define('CFRunLoopSourceRef', '__CFRunLoopSource*')
define('__CFString', 'void*')
CFStringRef = define('CFStringRef', '__CFString*')
CFTimeInterval = define('CFTimeInterval', 'double')

Boolean = define('Boolean',c_ubyte)
uint32_t = define('uint32_t',c_uint32)
SInt32 = define('SInt32',c_int32)

IONotificationPortRef = define('IONotificationPortRef', 'void*')

IOServiceInterestCallback = parse('void (*IOServiceInterestCallback)'
                                  '(void *refcon, io_service_t service, '
                                  'uint32_t messageType, void *messageArgument)').ctype
define('IOServiceInterestCallback',IOServiceInterestCallback)

# load the CoreFoundation Library
cfLibraryLocation = find_library('CoreFoundation')
cf = CDLL(cfLibraryLocation)

# CoreFoundation functions
CFRunLoopAddSource = parse('void CFRunLoopAddSource(CFRunLoopRef rl, '
                           'CFRunLoopSourceRef source, CFStringRef mode)').from_lib(cf)
CFRunLoopGetCurrent = parse('CFRunLoopRef CFRunLoopGetCurrent()').from_lib(cf)
CFRunLoopRunInMode = parse('SInt32 CFRunLoopRunInMode(CFStringRef mode, '
                           'CFTimeInterval seconds, Boolean returnAfterSourceHandled)').from_lib(cf)

kCFRunLoopCommonModes = CFStringRef.in_dll(cf, 'kCFRunLoopCommonModes')
kCFRunLoopDefaultMode = CFStringRef.in_dll(cf, 'kCFRunLoopDefaultMode')

# Load IOKit
iokitLibraryLocation = find_library('IOKit')
iokit = CDLL(iokitLibraryLocation)

# IOKit functions we need
IORegisterForSystemPower = parse('io_connect_t IORegisterForSystemPower('
                               'void *refcon, IONotificationPortRef *thePortRef,'
                               ' IOServiceInterestCallback callback, io_object_t'
                               ' *notifier)').from_lib(iokit)
IONotificationPortGetRunLoopSource = parse('CFRunLoopSourceRef IONotificationPortGetRunLoopSource(IONotificationPortRef notify)').from_lib(iokit)

# The callback that will be triggered
def callback(refCon, service, messageType, messageArgument):
    msg = {
        kIOMessageSystemWillSleep: 'kIOMessageSystemWillSleep',
        kIOMessageSystemWillPowerOn: 'kIOMessageSystemWillPowerOn',
        kIOMessageSystemHasPoweredOn: 'kIOMessageSystemHasPoweredOn',
        kIOMessageCanSystemSleep: 'kIOMessageCanSystemSleep',
        kIOMessageSystemWillNotSleep: 'kIOMessageSystemWillNotSleep'
    }
    print(msg[messageType])

def listener():
    notifyPortRef = IONotificationPortRef()
    notifierObject = io_object_t()
    refCon = c_void_p()
    sleepCallback = IOServiceInterestCallback(callback)

    root_port = IORegisterForSystemPower(refCon, notifyPortRef, sleepCallback, notifierObject)
    if root_port == 0:
        return

    CFRunLoopAddSource(CFRunLoopGetCurrent(), IONotificationPortGetRunLoopSource(notifyPortRef), kCFRunLoopDefaultMode)

    while True:
        CFRunLoopRunInMode(kCFRunLoopDefaultMode, 0.1, True)
