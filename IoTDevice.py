class IoTDevice:
    def __init__(self, serialNumber:str):
        self.serialNumber = serialNumber
        self.derivedKey = None
        self.layeredKey = None
        self.status = "unclaimed"

    def storeDerivedKey(self, derivedKey: bytes):
        self.derivedKey = derivedKey

    def setLayeredKey(self, layeredKey: bytes):
        self.layeredKey = layeredKey
        self.status = "claimed"

    def verifyAccess(self, userDerivedKey: bytes, userLayeredKey: bytes):
        if self.status == "unclaimed":
            if self.derivedKey == userDerivedKey:
                print("Access verified: Manufacturer gains access")
                return True
            else:
                print("Access denied")
                return False
        elif self.status == "claimed":
            if self.derivedKey == userDerivedKey and self.layeredKey == userLayeredKey:
                print("Access verified: User gains access")
                return True
            else:
                print("Access denied")
                return False
        else:
            print("Device status is unknown or does not exist.")
            return False
        
    def getStatus(self) -> str:
        return self.status


# if __name__ == "__main__":
#     from HSM import HSM
#     import hmac
#     import hashlib

#     hsm = HSM()
#     serialNumber = "SN001"
#     hsm.generateMasterKey()
#     derivedKey = hsm.generateDerivedKey(serialNumber)
    
#     device = IoTDevice(serialNumber)


#     print(f"Derived Key: {derivedKey.hex()}")
#     print()

#     print("Test 1: Storing dervied key to device")
#     device.storeDerivedKey(derivedKey)
#     print(f"Derived key stored: {device.derivedKey.hex()}")
#     print()

#     print("Test 2: get status")
#     print(f"Status: {device.getStatus()}")
#     print()

#     print("Test 3: verify access when unclaimed")
#     device.verifyAccess(derivedKey, None)
#     print()

#     print("Test 4: Set the layered key")
#     userPassword = "hubertx223"
#     layerdKey = hmac.new(derivedKey, userPassword.encode(),hashlib.sha256).digest()
#     device.setLayeredKey(layerdKey)
#     print(f"Layered key stored: {device.layeredKey.hex()}")
#     print()

#     print("Test 5: status change to claimed")
#     print(f"Status: {device.getStatus()}")
#     print()

#     print("Test 6: verify access with both keys")
#     device.verifyAccess(derivedKey, layerdKey)
#     print()

#     print("Test 7: wrong password")
#     wrongPassword = "jjjjj"
#     wrongLK = hmac.new(derivedKey, wrongPassword.encode(),hashlib.sha256).digest()
#     device.verifyAccess(derivedKey, wrongLK)
#     print()

#     print("Test 8: wrong derveid key")
#     wrongDK = hsm.generateDerivedKey("SN-002")
#     device.verifyAccess(wrongDK, layerdKey)
    



    



