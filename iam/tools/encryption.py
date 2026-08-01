# -*- coding: utf-8 -*-
"""
IAM Encryption - Cifrar y descifrar archivos
AES, RSA, hashing, generacion de claves
"""

import os
import hashlib
import base64
from typing import Tuple, List


class Encryption:
    """
    Herramientas de cifrado y seguridad
    """
    
    # === HASHING ===
    
    def hash_file(self, file_path: str, algorithm: str = "sha256") -> Tuple[bool, str]:
        """Calcular hash de un archivo"""
        try:
            h = hashlib.new(algorithm)
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    h.update(chunk)
            return True, h.hexdigest()
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    def hash_text(self, text: str, algorithm: str = "sha256") -> str:
        """Calcular hash de texto"""
        h = hashlib.new(algorithm)
        h.update(text.encode('utf-8'))
        return h.hexdigest()
    
    def hash_file_quick(self, file_path: str) -> Tuple[bool, str]:
        """Hash rapido MD5"""
        return self.hash_file(file_path, "md5")
    
    def verify_hash(self, file_path: str, expected_hash: str, algorithm: str = "sha256") -> Tuple[bool, bool]:
        """Verificar hash de archivo"""
        success, actual_hash = self.hash_file(file_path, algorithm)
        if success:
            return True, actual_hash.lower() == expected_hash.lower()
        return False, False
    
    # === CIFRADO SIMPLE (XOR) ===
    
    def xor_encrypt(self, data, key) -> bytes:
        """Cifrado XOR - acepta str o bytes"""
        if isinstance(data, str):
            data = data.encode()
        if isinstance(key, str):
            key = key.encode()
        return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
    
    def xor_decrypt(self, data, key) -> bytes:
        """Descifrado XOR (mismo proceso) - acepta str o bytes"""
        return self.xor_encrypt(data, key)
    
    def encrypt_file_xor(self, input_path: str, output_path: str, key: str) -> Tuple[bool, str]:
        """Cifrar archivo con XOR"""
        try:
            with open(input_path, 'rb') as f:
                data = f.read()
            
            encrypted = self.xor_encrypt(data, key.encode())
            
            with open(output_path, 'wb') as f:
                f.write(encrypted)
            
            return True, f"[OK] Archivo cifrado: {output_path}"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    def decrypt_file_xor(self, input_path: str, output_path: str, key: str) -> Tuple[bool, str]:
        """Descifrar archivo con XOR"""
        try:
            with open(input_path, 'rb') as f:
                data = f.read()
            
            decrypted = self.xor_decrypt(data, key.encode())
            
            with open(output_path, 'wb') as f:
                f.write(decrypted)
            
            return True, f"[OK] Archivo descifrado: {output_path}"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    # === BASE64 ===
    
    def base64_encode(self, text: str) -> str:
        """Codificar a Base64"""
        return base64.b64encode(text.encode()).decode()
    
    def base64_decode(self, encoded: str) -> str:
        """Decodificar de Base64"""
        return base64.b64decode(encoded).decode()
    
    def encode_file_base64(self, input_path: str, output_path: str) -> Tuple[bool, str]:
        """Codificar archivo a Base64"""
        try:
            with open(input_path, 'rb') as f:
                data = f.read()
            
            encoded = base64.b64encode(data).decode()
            
            with open(output_path, 'w') as f:
                f.write(encoded)
            
            return True, f"[OK] Archivo codificado: {output_path}"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    def decode_file_base64(self, input_path: str, output_path: str) -> Tuple[bool, str]:
        """Decodificar archivo de Base64"""
        try:
            with open(input_path, 'r') as f:
                encoded = f.read()
            
            decoded = base64.b64decode(encoded)
            
            with open(output_path, 'wb') as f:
                f.write(decoded)
            
            return True, f"[OK] Archivo decodificado: {output_path}"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    # === CIFRADO AES (requiere pycryptodome) ===
    
    def aes_encrypt(self, data: bytes, key: bytes) -> Tuple[bool, bytes]:
        """Cifrar con AES"""
        try:
            from Crypto.Cipher import AES
            from Crypto.Random import get_random_bytes
            
            # Padding
            padding_length = 16 - (len(data) % 16)
            data += bytes([padding_length]) * padding_length
            
            iv = get_random_bytes(16)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            encrypted = cipher.encrypt(data)
            
            return True, iv + encrypted
        except ImportError:
            return False, b"[ERROR] Instala pycryptodome: pip install pycryptodome"
        except Exception as e:
            return False, str(e).encode()
    
    def aes_decrypt(self, data: bytes, key: bytes) -> Tuple[bool, bytes]:
        """Descifrar con AES"""
        try:
            from Crypto.Cipher import AES
            
            iv = data[:16]
            encrypted = data[16:]
            
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(encrypted)
            
            # Remover padding
            padding_length = decrypted[-1]
            decrypted = decrypted[:-padding_length]
            
            return True, decrypted
        except ImportError:
            return False, b"[ERROR] Instala pycryptodome: pip install pycryptodome"
        except Exception as e:
            return False, str(e).encode()
    
    def encrypt_file_aes(self, input_path: str, output_path: str, key: str) -> Tuple[bool, str]:
        """Cifrar archivo con AES"""
        try:
            # Generar clave de 32 bytes
            key_bytes = hashlib.sha256(key.encode()).digest()
            
            with open(input_path, 'rb') as f:
                data = f.read()
            
            success, encrypted = self.aes_encrypt(data, key_bytes)
            if not success:
                return False, encrypted.decode()
            
            with open(output_path, 'wb') as f:
                f.write(encrypted)
            
            return True, f"[OK] Archivo cifrado con AES: {output_path}"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    def decrypt_file_aes(self, input_path: str, output_path: str, key: str) -> Tuple[bool, str]:
        """Descifrar archivo con AES"""
        try:
            key_bytes = hashlib.sha256(key.encode()).digest()
            
            with open(input_path, 'rb') as f:
                data = f.read()
            
            success, decrypted = self.aes_decrypt(data, key_bytes)
            if not success:
                return False, decrypted.decode()
            
            with open(output_path, 'wb') as f:
                f.write(decrypted)
            
            return True, f"[OK] Archivo descifrado con AES: {output_path}"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    # === GENERACION DE CLAVES ===
    
    def generate_key(self, length: int = 32) -> str:
        """Generar clave aleatoria"""
        import secrets
        return secrets.token_hex(length)
    
    def generate_password(self, length: int = 16) -> str:
        """Generar contrasena segura"""
        import secrets
        import string
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(chars) for _ in range(length))
    
    # === CONTRASENAS ===
    
    def hash_password(self, password: str) -> Tuple[bool, str]:
        """Hash de contrasena con salt"""
        try:
            import bcrypt
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            return True, hashed.decode()
        except ImportError:
            # Fallback a hashlib
            salt = os.urandom(16)
            h = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
            return True, f"{salt.hex()}:{h.hex()}"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    def verify_password(self, password: str, hashed: str) -> Tuple[bool, bool]:
        """Verificar contrasena"""
        try:
            import bcrypt
            return True, bcrypt.checkpw(password.encode(), hashed.encode())
        except ImportError:
            salt_hex, hash_hex = hashed.split(':')
            salt = bytes.fromhex(salt_hex)
            h = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
            return True, h.hex() == hash_hex
        except Exception as e:
            return False, False


# Instancia global
encryption = Encryption()
