from HSM import HSM
from IoTDevice import IoTDevice
from Backend import Backend
from CompanionApp import CompanionApp
from TestingAttack import TestingAttack
import time


def main():
    hsm = HSM()
    backend = Backend()
    print("The following is a simulation of how operations can work.")
    print("Manufacturers will use derived key instead of default credentials for IoT devices.")
    time.sleep(8)
    print()

    print("========== Manufacturing Stage ==========")
    print("First the master key is made with the CSPRNG")
    print("Creating master key...")
    masterKey = hsm.generateMasterKey()
    print("Master key created.")
    print()

    print("For this demo, the master key will be shown. Printing the hexadecimal representation of the master key key.")
    print(masterKey.hex())
    time.sleep(5)
    print()

    serialNumber = input("Now enter a serial number of the device. EX. SN0001: ")
    iotDevice = IoTDevice(serialNumber)
    print("Creating derived key for device...")
    derivedKey = hsm.generateDerivedKey(serialNumber)
    print("Dervied key for device " + serialNumber + " is created")
    time.sleep(2)
    print()
    
    print("For this demo, the derived key will be shown. Printing the hexadecimal representation of the derived key.")
    print(derivedKey.hex())
    time.sleep(3)
    print()

    print("Storing dervied key into IoT Device...")
    time.sleep(3)
    iotDevice.storeDerivedKey(derivedKey)
    print("Derived key has been store in device.")
    print()

    print("Storing device in the backend...")
    backend.registerDevice(serialNumber)
    print()

    hsm.recomputeKey(serialNumber, derivedKey)
    print()

    print("========== Attack Stage!!! ==========")
    attack = TestingAttack(derivedKey, serialNumber, hsm.masterKey)
    print("Hackers are trying to infiltrate IoT Devices! Seems like their using leaked credentials.")
    print()

    time.sleep(5)
    print("It attacks a device that has default credential with password 'admin123'")
    print("Hacker attacks...")
    attack.attackDefault()
    print()

    print("They are attacking our device again. They know it involves serial numbers and SHA256 hash function, but not the HMAC nor master key")
    attack.attackDerivedKeySHA256()
    time.sleep(10)
    print()

    print("The hackers are attacking once again. but they got a list of serial numbers and the master key (worst case scenario)")
    attack.attackDerivedKeyMK(derivedKey, hsm.masterKey, serialNumber)
    time.sleep(20)

    print("========== Onboarding/Force User Credential Stage ==========")
    companionApp = CompanionApp(backend, iotDevice)
    print("For this stage, the device has been shipped to users and required to download a companion app.")
    print()

    print("Hello, user! Before you can use your device there are few things you need to do first.")
    time.sleep(2)
    print()

    userSerialNumInput = input("Scan or enter the device serial number found at the bottom of the device: ")
    while not companionApp.confirmSerialNumber(userSerialNumInput):
        userSerialNumInput = input("Scan or enter the device serial number found at the bottom of the device: ")
        print()
    companionApp.confirmSerialNumber(userSerialNumInput)
    backend.updateDeviceStatus(userSerialNumInput)
    print()

    userCredential = companionApp.forceCredentialSetup()
    print()

    print("Creating layered key using user's credential...")
    time.sleep(3)
    layeredKey = companionApp.generateLayeredKey(derivedKey, userCredential)
    print("Layered key created.")
    print()

    print("Now finishing the onboarding process...")
    print()

    print("Sending layered key to device...")
    companionApp.sendLayeredKeyToDevice(layeredKey)
    time.sleep(3)
    print("layered key sent.")
    print()

    print("Updating the backend...")
    time.sleep(7)
    backend.storeUserCredential(userSerialNumInput, layeredKey)
    print("Updates complete!")
    print()

    print("Everything is ready! Enjoy!")

    print("========== User Login Stage ==========")
    print("User tries to get access to the device")
    print()

    userPassword = input("Enter your password here: ")

    userLayeredKey = companionApp.generateLayeredKey(derivedKey, userPassword)

    if backend.verifyUserCredential(serialNumber, userLayeredKey):
        if iotDevice.verifyAccess(derivedKey, userLayeredKey):
            print("Access granted! Welcome, user!")
        
        else:
            print("Access denied.")
    else:
        print("Backend can't verify credential. Access denied.")

    time.sleep(10)
    print()

    print("========== Database Stage ==========")
    derivedKey_2 = hsm.generateDerivedKey("SN0002")
    iotDevice.storeDerivedKey(derivedKey_2)
    backend.registerDevice("SN0002")
    backend.updateDeviceStatus("SN0002")
    print(f"Master Key: {masterKey.hex()}")
    print(f"Device 2 derived key: {derivedKey_2.hex()}")
    print()

    derivedKey_3 = hsm.generateDerivedKey("SN0003")
    iotDevice.storeDerivedKey(derivedKey_3)
    backend.registerDevice("SN0003")
    print(f"Master Key: {masterKey.hex()}")
    print(f"Device 3 derived key: {derivedKey_3.hex()}")
    print()


    derivedKey_4 = hsm.generateDerivedKey("SN0004")
    iotDevice.storeDerivedKey(derivedKey_4)
    backend.registerDevice("SN0004")
    print(f"Master Key: {masterKey.hex()}")
    print(f"Device 4 derived key: {derivedKey_4.hex()}")
    print()


    derivedKey_5 = hsm.generateDerivedKey("SN0005")
    iotDevice.storeDerivedKey(derivedKey_5)
    backend.registerDevice("SN0005")
    backend.updateDeviceStatus("SN0005")
    print(f"Master Key: {masterKey.hex()}")
    print(f"Device 5 derived key: {derivedKey_5.hex()}")
    print()

    print("You are working with the database and you are just viewing the devices that are in the the system. Let look and see!")
    
    while True:
        snInput = input("Enter a serial number to look up: ")
        backend.verifyDevice(snInput)
        response = input("Want to check on more devices?: y/n: ")
        print()
        if response == "y":
            snInput = input("Enter a serial number to look up: ")
            backend.verifyDevice(snInput)
        else:
            break

main(); 