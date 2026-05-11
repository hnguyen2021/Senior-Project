import time
import hashlib
import hmac
from IoTDevice import IoTDevice
from HSM import HSM
class TestingAttack:
    def __init__ (self, targetDerivedKey:IoTDevice, serialNumber, leakedMasterKey: HSM):
        self.passwordList = ["admin", "password", "admin123", "asdf", "qwer", "1234", "wasd360", "56789", "Hello123", "password123"]
        self.serialNumberList = ["SN0001", "SN0002", "SN0003", "SN0004", "SN0005", "SN0006", "SN0007", "SN0008", "SN0009", "SN0010"]
        self.targetDefault = "admin123"
        self.targetDerivedKey = targetDerivedKey
        self.serialNumber = serialNumber
        self.leakedMasterKey = leakedMasterKey
        

    def attackDefault(self):
        target = self.targetDefault
        start_time = time.perf_counter()
        attempt = 0

        for password in self.passwordList:
            attempt += 1
            if password == target:
                duration = time.perf_counter() - start_time
                print("Device found!")
                print(f"Password found: {password}")
                print(f"It took {duration:.6f} s ")
                print(f"It took {attempt} attempt(s)")
                return
        duration = time.perf_counter() - start_time
        print("Device cannot be found.")    
        print("Password cannot be foud.")
        print(f"Total time: {duration:.6f} s")
        print(f"It took {attempt} attempt(s)")    

    def attackDerivedKeySHA256(self):
        start_time = time.perf_counter()
        attempt = 0
        for serialNumber in self.serialNumberList:
            sn = serialNumber.encode()
            attempt += 1
            guess = hashlib.sha256(sn).digest()
            target = self.targetDerivedKey
            if guess == target:
                duration = time.perf_counter() - start_time
                print("Device found!")
                print(f"serial number: {serialNumber}")
                print(f"It took {duration:.6f} s")
                print(f"It took {attempt} attempt(s)")
                return
        
        duration = time.perf_counter() - start_time    
        print("Device cannot be foud.")
        print(f"Total time: {duration:.6f} s") 
        print(f"It took {attempt} attempt(s)")

    def attackDerivedKeyMK(self, targetDerivedKey: IoTDevice, leakedMasterKey: HSM, serialNumber):
        start_time = time.perf_counter()
        attempt = 0

        for serialNumber in self.serialNumberList:
            sn = serialNumber.encode()
            attempt += 1
            target = targetDerivedKey
            guess = hmac.new(leakedMasterKey, sn, hashlib.sha256).digest()

            for _ in range(600000):
                guess = hmac.new(leakedMasterKey, guess, hashlib.sha256).digest()
            if guess == target:
                duration = time.perf_counter() - start_time
                print("Device found!")
                print(f"It took {duration: .6f} s")
                print(f"It took {attempt} attempt(s)")
                return
        
        duration = time.perf_counter() - start_time    
        print("Device cannot be foud.")
        print(f"Total time: {duration:.6f} s") 
        print(f"It took {attempt} attempt(s)")

            
        
                
        

# if __name__ == "__main__":
#     from HSM import HSM
#     from IoTDevice import IoTDevice

#     hsm = HSM()
#     serialNumber = "SN0008"
#     serialNumber_2 = "SN0001"
#     hsm.generateMasterKey()
#     leakedMasterKey = hsm.masterKey
#     derivedKey = hsm.generateDerivedKey(serialNumber)
#     derivedKey_2 = hsm.generateDerivedKey(serialNumber_2)

#     device = IoTDevice(serialNumber)
#     device.storeDerivedKey(derivedKey)

#     attack = TestingAttack(derivedKey, serialNumber, leakedMasterKey)

#     print("Test 1: Attack default")
#     attack.attackDefault()
#     print()

#     print("Test 2: Attack derived key (know to use hmac)")
#     attack.attackDerivedKeySHA256()
#     print()

#     print("Test 3: Attack knowing master key (very bad)")
#     attack.attackDerivedKeyMK(derivedKey, leakedMasterKey, serialNumber)
#     print(f"{serialNumber}")
#     print()

#     print("Other test: first serial number")
#     attack.attackDerivedKeyMK(derivedKey_2, leakedMasterKey, serialNumber_2)
    

    







        

    

    
                
        

