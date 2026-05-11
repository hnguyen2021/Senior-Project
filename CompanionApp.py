import hmac
import hashlib
from Backend import Backend
from IoTDevice import IoTDevice

class CompanionApp:
    def __init__(self, backend:Backend, iotDevice:IoTDevice):
        self.backend = backend
        self.iotDevice = iotDevice
        self.deviceSerialNumber = None

    def confirmSerialNumber(self, serialNumber: str) -> bool:
        self.deviceSerialNumber = serialNumber

        if self.backend.verifyDevice(serialNumber):
            print(f"Device with serial number {serialNumber} found.")
            return True
        else:
            print(f"Device with serial number {serialNumber} is not found or alredy claimed")
            return False

    def forceCredentialSetup(self) -> str:
        print("Great! Now, you need to enter a password to claim the device and make it more secure. Please make sure it contains letters and numbers and at least 6 characters long.")
        
        while True:
            userInput = input("Enter here: ")
        
            has_letter = any(char.isalpha() for char in userInput)
            has_number = any(char.isdigit() for char in userInput)

            if has_letter and has_number:
                if len(userInput) >= 6:
                    print("Input valid. Thank you!")
                    return userInput
                else:
                    print("Not 6 characters long. Make sure your input is 6 characters long")
            else:
                print("Invalid input. Please make sure your input contains letters AND numbers.")
    
    def generateLayeredKey(self, derivedKey: bytes, userInput: str) -> bytes:
        layeredKey = hmac.new(derivedKey, userInput.encode(), hashlib.sha256).digest()
        return layeredKey

    def sendLayeredKeyToDevice(self, layeredKey: bytes):
        self.iotDevice.setLayeredKey(layeredKey)

# if __name__ == "__main__":
#     from HSM import HSM
#     from Backend import Backend
#     from IoTDevice import IoTDevice

#     hsm = HSM()
#     hsm.generateMasterKey()
#     serialNumber = "SN001"
#     derivedKey = hsm.generateDerivedKey(serialNumber)


#     device = IoTDevice(serialNumber)
#     device.storeDerivedKey(derivedKey)
#     backend = Backend()


#     app = CompanionApp(backend, device)

#     print("Test 1: Confirm device that doesn't exist")
#     sn = "SN0005"
#     app.confirmSerialNumber(sn)
#     print()

#     print("Other test")
#     backend.registerDevice(sn)
#     app.confirmSerialNumber(sn)
#     print()

#     print("Test 2: Confirm device that does exist")
#     backend.registerDevice(serialNumber)
#     app.confirmSerialNumber(serialNumber)
#     print()

#     print("Test 3: force user to add credential")
#     userInput = app.forceCredentialSetup()
#     print()

#     print("Test 4: Generate layered key")
#     layeredKey = app.generateLayeredKey(derivedKey, userInput)
#     print(f"Layerd Key: {layeredKey.hex()}")
#     print()

#     print("Test 5: send layered key to iot device")
#     app.sendLayeredKeyToDevice(layeredKey)
#     print()

    
    


