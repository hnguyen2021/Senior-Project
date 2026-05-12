import hmac
import hashlib
import secrets

class HSM:
    def __init__(self):
        self.masterKey = None
        self.iterations = 600000

    def generateMasterKey(self) -> bytes:
        self.masterKey = secrets.token_bytes(32)
        return self.masterKey
    
    def generateDerivedKey(self, serialNumber: str) -> bytes:
        SN = serialNumber.encode()
        derivedKey = hmac.new(self.masterKey, SN, hashlib.sha256).digest()
        for _ in range(self.iterations):
            derivedKey = hmac.new(self.masterKey, derivedKey, hashlib.sha256).digest()

        return derivedKey
    
    def recomputeKey(self, serialNumber: str, ogDerivedKey: bytes) -> bytes:
        print("Manufacturer needs to makes some last minute changes")
        reenterSN = input("Please reenter the serial number: ")
        recomputed = self.generateDerivedKey(reenterSN)

        while ogDerivedKey != recomputed:
            reenterSN = input("Incorrect serial number. Please enter again: ")
            recomputed = self.generateDerivedKey(reenterSN)
        
        print("Access granted.")
        print("Manufacturer makes last minute fixes...")
        return self.generateDerivedKey(serialNumber)
    
if __name__ == "__main__":
    hsm = HSM()

    masterKey = hsm.generateMasterKey()

    print(f"Master key: {masterKey.hex()}")
    print(f"Master key: {len(masterKey)}")
    

    serialNumber = "SN001"

    print(serialNumber)
    derivedKey = hsm.generateDerivedKey(serialNumber)

    print(f"Derived Key: {derivedKey.hex()}")
    print(f"Master key: {len(derivedKey)} bytes")

    user = input("Enter serial number: ")

    recomputed = hsm.recomputeKey(user, derivedKey)
    print(f"Derived Key: {recomputed.hex()}")
    print(f"Master key: {len(recomputed)} bytes")

    if derivedKey == recomputed:
        print("yes")
    else:
        print("no")



