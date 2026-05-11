class Backend:
    def __init__(self):
        self.deviceRegistry = {}
        self.userCredentials = {}

    def registerDevice(self, serialNumber:str):
        self.deviceRegistry[serialNumber] = "unclaimed"

    def verifyDevice(self, serialNumber: str) -> bool:
        status = self.deviceRegistry.get(serialNumber)
        if status:
            if status == "unclaimed":
                print(f"Device exist in registry. Device is currently {status} by user.")
                return True
            elif status == "claimed":
                print (f"Device exist in registry. Device is currently {status} by user.")
                return False
        else:
            print("Device doesnt't exist")
            return False
    
    def updateDeviceStatus(self, serialNumber: str):
        self.deviceRegistry[serialNumber] = "claimed"

    def storeUserCredential(self, serialNumber: str, layeredKey: bytes):
        self.userCredentials[serialNumber] = layeredKey

    def verifyUserCredential(self, serialNumber: str, inputKey: bytes) -> bool:
        userCred = self.userCredentials.get(serialNumber)
        
        if userCred is None:
            print("Credential not found for this device.")
            return False
        
        if userCred == inputKey:
            print("Credentials match")
            return True
        else:
            print("Credentials didn't match")
            return False


# if __name__ == "__main__":
#     from HSM import HSM
#     from IoTDevice import IoTDevice
#     import hmac
#     import hashlib

#     hsm = HSM()
#     hsm.generateMasterKey()
#     serialNumber = "SN0001"
#     derivedKey = hsm.generateDerivedKey(serialNumber)

#     device = IoTDevice(serialNumber)
#     device.storeDerivedKey(derivedKey)


#     backend = Backend()

#     print("Test 0: Verify device nonexisitent")
#     backend.verifyDevice("SN0002")

#     print("Test 1: Verify Device unclaimed")
#     backend.registerDevice(serialNumber)
#     result = backend.verifyDevice(serialNumber)
#     print()
    
#     print("Test 2: Verify Device claimed")
#     backend.registerDevice(serialNumber)
#     print(f"Status before: {backend.deviceRegistry.get(serialNumber)}")
#     backend.updateDeviceStatus(serialNumber)
#     print(f"Status after: {backend.deviceRegistry.get(serialNumber)}")

#     print()

#     print("Test 3: store the user credential")
#     userPassword = "password"
#     layeredKey = hmac.new(derivedKey, userPassword.encode(), hashlib.sha256).digest()
#     print(f"Layered Key: {layeredKey.hex()}")
#     backend.storeUserCredential(serialNumber, layeredKey)
#     print(f"it stored: {backend.userCredentials[serialNumber].hex()}")
#     print()

#     print("Test 4: verify user credential (credential match)")
#     print(f"serial number: {serialNumber}")
#     input = input("Enter password: ")
#     lk = hmac.new(derivedKey, input.encode(), hashlib.sha256).digest()
#     backend.verifyUserCredential(serialNumber, lk)
#     print()
    
#     print("Test 5: verify user credential (credential didn't match)")
#     wrongPassword = "incorrect"
#     wrongLK = hmac.new(derivedKey, wrongPassword.encode(), hashlib.sha256).digest()
#     print(f"Layered Key: {wrongLK.hex()}")
#     backend.verifyUserCredential(serialNumber, wrongLK)
#     print()
    

    



    

    

