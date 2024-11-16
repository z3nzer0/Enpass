import os, re, json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import HMAC, SHA256
import base64

class core:

    masterPass = None
    data = {'accounts': [], 'index': 0}
    
    def masterPassRegex(self, masterPass):
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{12,}$'
        return re.match(pattern, masterPass)

    def setMasterPass(self, masterPass):
        self.masterPass = masterPass

    def pad(self, data):
        # PKCS7 padding
        pad_len = 16 - (len(data) % 16)
        return data + (chr(pad_len) * pad_len)

    def unpad(self, data):
        # Remove PKCS7 padding
        pad_len = ord(data[-1])
        return data[:-pad_len]

    def derive_key(self, password):
        salt = get_random_bytes(16)
        key = PBKDF2(password, salt, dkLen=32, count=1000000, hmac_hash_module=SHA256)
        return key, salt

    def encrypt_data(self, key, data):
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = self.pad(data).encode('utf-8')
        encrypted_data = cipher.encrypt(padded_data)
        
        # HMAC for integrity
        hmac = HMAC.new(key, iv + encrypted_data, digestmod=SHA256).digest()
        
        # Concatenate iv, encrypted data, and HMAC for storage
        return iv + encrypted_data + hmac

    def decrypt_data(self, key, enc_data):
        iv = enc_data[:16]
        hmac_received = enc_data[-32:]
        encrypted_data = enc_data[16:-32]
        
        # Verify HMAC integrity
        hmac_calculated = HMAC.new(key, iv + encrypted_data, digestmod=SHA256).digest()
        if hmac_calculated != hmac_received:
            raise ValueError("Data integrity check failed: HMAC mismatch.")
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(encrypted_data)
        return self.unpad(decrypted_data.decode('utf-8'))

    def checkFile(self):
        return os.path.isfile('npss.ea') and os.path.getsize('npss.ea') > 0

    def readData(self):
        with open('npss.ea', 'rb') as file:
            salt = file.read(16)
            token = file.read()
        return salt, token

    def checkMasterPass(self, masterPass):
        try:
            salt, token = self.readData()
            key = PBKDF2(masterPass, salt, dkLen=32, count=1000000, hmac_hash_module=SHA256)
            decrypted_json_data = self.decrypt_data(key, token)
            self.data = json.loads(decrypted_json_data)
            self.masterPass = masterPass
            return True
        except (ValueError, json.JSONDecodeError):
            return False

    def saveToFile(self, salt, token):
        with open('npss.ea', 'wb') as file:
            file.write(salt + token)

    def addNewAccount(self, username, password, info):
        self.data['accounts'].append({
            'username': username, 'password': password, 'info': info,
            'id': int(self.data['index']) + 1
        })
        self.data['index'] += 1
        
        # Generate key and salt
        key, salt = self.derive_key(self.masterPass)
        
        json_data = json.dumps(self.data)
        encrypted_json_data = self.encrypt_data(key, json_data)
        self.saveToFile(salt, encrypted_json_data)

    def getDecodedData(self):
        return self.data

    def updateAccount(self, newUsername, newPassword, newInfo, id):
        for account in self.data['accounts']:
            if account['id'] == id:
                account['username'] = newUsername
                account['password'] = newPassword
                account['info'] = newInfo

        key, salt = self.derive_key(self.masterPass)
        json_data = json.dumps(self.data)
        encrypted_json_data = self.encrypt_data(key, json_data)
        self.saveToFile(salt, encrypted_json_data)

    def removeAccount(self, id):
        self.data['accounts'] = [acc for acc in self.data['accounts'] if acc['id'] != id]
        key, salt = self.derive_key(self.masterPass)
        json_data = json.dumps(self.data)
        encrypted_json_data = self.encrypt_data(key, json_data)
        self.saveToFile(salt, encrypted_json_data)
