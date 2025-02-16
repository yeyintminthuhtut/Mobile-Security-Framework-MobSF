# -*- coding: utf_8 -*-
import os,platform,subprocess,sys
BASE_DIR=os.path.dirname(os.path.realpath(__file__))
TOOLSDIR=os.path.join(BASE_DIR, 'DynamicAnalyzer/tools/')  #TOOLS DIR
ROOTCA=os.path.join(BASE_DIR, 'DynamicAnalyzer/pyWebProxy/ca.crt')

def ExecuteCMD(args,ret =False):
    try:
        print "\n[INFO] Executing Command - " + ' '.join(args)
        if ret:
            return subprocess.check_output(args)
        else:
            subprocess.call(args)
    except Exception as e:
        print ("\n[ERROR] Executing Command - " + str(e))

def getADB(TOOLSDIR):
    print ("\n[INFO] Getting ADB Location")
    try:
        adb='adb'
        if platform.system()=="Darwin":
            adb_dir=os.path.join(TOOLSDIR, 'adb/mac/')
            subprocess.call(["chmod", "777", adb_dir])
            adb=os.path.join(TOOLSDIR , 'adb/mac/adb')
        elif platform.system()=="Linux":
            adb_dir=os.path.join(TOOLSDIR, 'adb/linux/')
            subprocess.call(["chmod", "777", adb_dir])
            adb=os.path.join(TOOLSDIR , 'adb/linux/adb')
        elif platform.system()=="Windows":
            adb=os.path.join(TOOLSDIR , 'adb/windows/adb.exe')
        return adb
    except Exception as e:
        print ("\n[ERROR] Getting ADB Location - "+str(e))
        return "adb"
print "\nMobSFy Script\n\nThis script allows you to configure any rooted android Device or VM to perfrom MobSF dynamic analysis.\n(Supports Android Version 4.03 to 4.4)"
try:
    adbconnect = raw_input("Enter the IP and Port of the Device/VM (Ex: 192.168.1.2:5555) and press enter: ")
    if ":" in adbconnect:
        vm_or_ip = raw_input("Choose\n 1. VM\n 2. Device\nEnter your choice: ")
        adb = getADB(TOOLSDIR)
        ExecuteCMD([adb, "kill-server"])
        ExecuteCMD([adb, "start-server"])
        ExecuteCMD([adb, "connect",adbconnect])
        ExecuteCMD([adb, "wait-for-device"])
        #Install MITM RootCA
        ExecuteCMD([adb, "-s",adbconnect ,"push", ROOTCA, "/data/local/0025aabb.0"])
        ExecuteCMD([adb, "-s",adbconnect ,"shell", "su", "-c", "mount", "-o", "rw,remount,rw", "/system"])
        ExecuteCMD([adb, "-s",adbconnect ,"shell", "su", "-c", "cp", "/data/local/0025aabb.0", "/system/etc/security/cacerts/0025aabb.0"])
        ExecuteCMD([adb, "-s",adbconnect ,"shell", "rm", "/data/local/0025aabb.0"])
        #Install MobSF requirements
        DP = os.path.join(TOOLSDIR,'onDevice/DataPusher.apk')
        SC = os.path.join(TOOLSDIR,'onDevice/ScreenCast.apk')
        #3P
        XP = os.path.join(TOOLSDIR,'onDevice/Xposed.apk')
        #Xposed Modules and Support Files
        HK = os.path.join(TOOLSDIR,'onDevice/hooks.json')
        DM = os.path.join(TOOLSDIR,'onDevice/Droidmon.apk')
        JT = os.path.join(TOOLSDIR,'onDevice/JustTrustMe.apk')
        RC = os.path.join(TOOLSDIR,'onDevice/RootCloak.apk')
        #Anti-VM Bypass
        AP = os.path.join(TOOLSDIR,'onDevice/AndroidBluePill.apk')
        FB = os.path.join(TOOLSDIR,'onDevice/antivm/fake-build.prop')
        FC = os.path.join(TOOLSDIR,'onDevice/antivm/fake-cpuinfo')
        FD = os.path.join(TOOLSDIR,'onDevice/antivm/fake-drivers')

        print "\n[INFO] Installing MobSF DataPusher"
        ExecuteCMD([adb,"-s",adbconnect ,"install", "-r", DP])
        print "\n[INFO] Installing MobSF ScreenCast"
        ExecuteCMD([adb,"-s",adbconnect ,"install", "-r", SC])
        print "\n[INFO] Copying hooks.json"
        ExecuteCMD([adb,"-s",adbconnect ,"push", HK, "/data/local/tmp/"])
        print "\n[INFO] Installing Xposed Framework"
        ExecuteCMD([adb,"install", "-r", XP])
        print "\n[INFO] Installing Droidmon API Analyzer"
        ExecuteCMD([adb,"-s",adbconnect ,"install", "-r", DM])
        print "\n[INFO] Installing JustTrustMe"
        ExecuteCMD([adb,"-s",adbconnect ,"install", "-r", JT])
        print "\n[INFO] Installing RootCloak"
        ExecuteCMD([adb,"-s",adbconnect ,"install", "-r", RC])

        if vm_or_ip == "1":
            print "\n[INFO] Installing Android BluePill"
            ExecuteCMD([adb,"-s",adbconnect ,"install", "-r", AP])
            print "\n[INFO] Copying fake-build.prop"
            ExecuteCMD([adb,"-s",adbconnect ,"push", FB, "/data/local/tmp/"])
            print "\n[INFO] Copying fake-cpuinfo"
            ExecuteCMD([adb,"-s",adbconnect ,"push", FC, "/data/local/tmp/"])
            print "\n[INFO] Copying fake-drivers"
            ExecuteCMD([adb,"-s",adbconnect ,"push", FD, "/data/local/tmp/"])
            
        print "\n[INFO] Launching Xposed Framework."
        print "\n 1 .Install the Framework\n 2. Restart the device\n 3. Enable Droidmon, JustTrustMe and RootCloak."
        ExecuteCMD([adb,"-s",adbconnect ,"shell", "am", "start", "-n", "de.robv.android.xposed.installer/de.robv.android.xposed.installer.WelcomeActivity"])

        print "\n[INFO] MobSFy Script Executed Successfully"
    else:
        print "\n[ERROR] Please enter the IP and Port in the following format (192.168.1.2:5555)"
        sys.exit(0)
except Exception as e:
    print "\n[ERROR] Error occured - "+ str(e)
    sys.exit(0)


