import hashlib
import getpass

def hash_password(plain_text_password: str) -> str:
    """
    """

    return hashlib.sha256(plain_text_password.encode()).hexdigest()

def check_password(attempt: str, stored_hash: str) -> bool:
    """
    """

    return hash_password(attempt) == stored_hash


def login_gate(stored_hash: str, max_attempts: int = 3) -> bool:

    """
    """

    for _ in range(max_attempts):
        attempt = getpass.getpass("Enter password to view reports: ")
        if check_password(attempt, stored_hash):
            print("Access granted.")
            return True
        else:
            print("Incorrect password. Try again.")

    print("Access denied - too many failed attempts.") 
    return False



password = getpass.getpass("[sudo] password for root: ")
hash = hash_password(password)
print(hash)
login_gate(hash, 3)
