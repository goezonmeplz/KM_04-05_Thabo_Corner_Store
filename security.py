import hashlib
import getpass

def hash_password(plain_text_password: str) -> str:
    """
    Computes a plain-text password's SHA-256 hash.

    Args:
        plain_text_password: user supplied password.

    Returns:
        the hex-digest string of the SHA-256 hash.
    """

    return hashlib.sha256(plain_text_password.encode()).hexdigest()

def check_password(attempt: str, stored_hash: str) -> bool:
    """
    Checks if a login attempt matches a stored hash.

    Args:
        attempt: the plain-text user supplied password 
        stored_hash: the hash saved earlier with hash_password.

    Returns:
        True if the attempt's hash matches stored_hash, else False.
    """

    return hash_password(attempt) == stored_hash


def login_gate(stored_hash: str, max_attempts: int = 3) -> bool:

    """
    Prompts the user for a passowrd and checks it against a stored hash, allows the user up to max_attempts of retries.

    Returns:
        True if the user authenticated successfully, False otherwise.
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


STORED_PASSWORD_STR = "admin1" # LOL
STORED_PASSWORD_HASH = hash_password(STORED_PASSWORD_STR)
