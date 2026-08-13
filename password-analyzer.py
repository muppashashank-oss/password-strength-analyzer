import hashlib
import math
import secrets
import string
import re
import urllib.request
import urllib.error
import base64

# ============================================================
# PASSWORD SECURITY TOOLKIT
# ============================================================

COMMON_PASSWORDS = {
    "password", "password1", "password123", "123456", "12345678",
    "123456789", "1234567890", "qwerty", "qwerty123", "admin",
    "admin123", "letmein", "welcome", "welcome123", "iloveyou",
    "monkey", "dragon", "football", "baseball", "abc123",
    "111111", "000000", "654321", "pass123", "root",
    "toor", "login", "master", "secret", "changeme"
}

WORDS = [
    "apple", "river", "tiger", "cloud", "forest", "rocket",
    "ocean", "falcon", "shadow", "silver", "winter", "coffee",
    "thunder", "orange", "planet", "dragon", "mountain",
    "sunset", "matrix", "cyber", "phoenix", "storm", "wolf",
    "eagle", "neon", "quantum", "castle", "pixel", "cosmic"
]


# ============================================================
# BANNER
# ============================================================

def banner():
    print("\n" + "=" * 65)
    print("              PASSWORD SECURITY TOOLKIT")
    print("=" * 65)
    print(" Password strength • Breach detection • Entropy")
    print(" Secure generation • Hashing • Policy checking")
    print("=" * 65)


# ============================================================
# STRENGTH ANALYSIS
# ============================================================

def analyze_password(password, username="", email=""):
    score = 0
    warnings = []
    positives = []

    length = len(password)

    # Length
    if length >= 16:
        score += 30
        positives.append("Excellent password length")
    elif length >= 12:
        score += 25
        positives.append("Good password length")
    elif length >= 8:
        score += 15
        warnings.append("Password could be longer")
    else:
        warnings.append("Password is too short")

    # Character classes
    if re.search(r"[A-Z]", password):
        score += 10
    else:
        warnings.append("Missing uppercase letters")

    if re.search(r"[a-z]", password):
        score += 10
    else:
        warnings.append("Missing lowercase letters")

    if re.search(r"\d", password):
        score += 10
    else:
        warnings.append("Missing numbers")

    if re.search(r"[^A-Za-z0-9]", password):
        score += 15
    else:
        warnings.append("Missing special characters")

    # Unique characters
    unique_ratio = len(set(password)) / max(len(password), 1)

    if unique_ratio >= 0.8:
        score += 15
    elif unique_ratio < 0.5:
        warnings.append("Many repeated characters")

    # Common password
    if password.lower() in COMMON_PASSWORDS:
        score = min(score, 10)
        warnings.append("This is a commonly used password")

    # Sequential characters
    if has_sequence(password):
        score -= 10
        warnings.append("Contains sequential characters")

    # Repeated characters
    if has_repeated_pattern(password):
        score -= 10
        warnings.append("Contains repeated character patterns")

    # Keyboard patterns
    if has_keyboard_pattern(password):
        score -= 10
        warnings.append("Contains a common keyboard pattern")

    # Personal information
    personal_terms = []

    if username:
        personal_terms.append(username.lower())

    if email:
        personal_terms.append(email.split("@")[0].lower())

    lower_password = password.lower()

    for term in personal_terms:
        if term and len(term) >= 3 and term in lower_password:
            score -= 20
            warnings.append("Password contains personal information")
            break

    score = max(0, min(score, 100))

    if score >= 80:
        rating = "VERY STRONG"
    elif score >= 65:
        rating = "STRONG"
    elif score >= 45:
        rating = "MODERATE"
    elif score >= 25:
        rating = "WEAK"
    else:
        rating = "VERY WEAK"

    return score, rating, warnings, positives


# ============================================================
# PATTERN DETECTION
# ============================================================

def has_sequence(password):
    p = password.lower()

    sequences = [
        "abcdefghijklmnopqrstuvwxyz",
        "0123456789",
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm"
    ]

    for seq in sequences:
        for i in range(len(seq) - 2):
            if seq[i:i + 3] in p:
                return True

    return False


def has_repeated_pattern(password):
    if len(password) < 4:
        return False

    # aaa, 111, !!!
    if re.search(r"(.)\1{2,}", password):
        return True

    # abcabc / 1212
    for size in range(1, len(password) // 2 + 1):
        pattern = password[:size]
        repetitions = len(password) // size

        if repetitions >= 2 and pattern * repetitions == password:
            return True

    return False


def has_keyboard_pattern(password):
    patterns = [
        "qwerty",
        "asdfgh",
        "zxcvbn",
        "qwertyui",
        "asdfghjk",
        "123456",
        "654321"
    ]

    p = password.lower()

    return any(pattern in p for pattern in patterns)


# ============================================================
# ENTROPY
# ============================================================

def calculate_entropy(password):
    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26

    if re.search(r"[A-Z]", password):
        charset += 26

    if re.search(r"\d", password):
        charset += 10

    if re.search(r"[^A-Za-z0-9]", password):
        charset += 32

    if charset == 0:
        return 0

    return len(password) * math.log2(charset)


# ============================================================
# CRACK TIME
# ============================================================

def crack_time(entropy):
    guesses = 2 ** entropy

    scenarios = {
        "Online attack": 10,
        "Offline attack": 1_000_000_000,
        "Fast GPU attack": 100_000_000_000
    }

    print("\nEstimated crack time:")
    print("-" * 50)

    for name, guesses_per_second in scenarios.items():
        seconds = guesses / guesses_per_second
        print(f"{name:22}: {format_time(seconds)}")


def format_time(seconds):
    if seconds < 1:
        return "Less than 1 second"

    if seconds < 60:
        return f"{seconds:.1f} seconds"

    if seconds < 3600:
        return f"{seconds / 60:.1f} minutes"

    if seconds < 86400:
        return f"{seconds / 3600:.1f} hours"

    if seconds < 31536000:
        return f"{seconds / 86400:.1f} days"

    if seconds < 3153600000:
        return f"{seconds / 31536000:.1f} years"

    if seconds < 315360000000:
        return f"{seconds / 3153600000:.1f} decades"

    return "Extremely long / practically infeasible"


# ============================================================
# PASSWORD GENERATOR
# ============================================================

def generate_password(length=20):
    alphabet = string.ascii_letters + string.digits + string.punctuation

    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(length))

        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in string.punctuation for c in password)
        ):
            return password


def generate_passphrase(words_count=5):
    selected = [secrets.choice(WORDS) for _ in range(words_count)]

    separator = secrets.choice(["-", "_", ".", "!"])

    number = secrets.randbelow(1000)

    return separator.join(selected) + separator + str(number)


# ============================================================
# PASSWORD POLICY
# ============================================================

def check_policy(password):
    print("\nPassword Policy Check")
    print("-" * 50)

    min_length = int(input("Minimum length [12]: ") or "12")

    require_upper = input("Require uppercase? (y/n) [y]: ").lower() != "n"
    require_lower = input("Require lowercase? (y/n) [y]: ").lower() != "n"
    require_number = input("Require number? (y/n) [y]: ").lower() != "n"
    require_special = input("Require special character? (y/n) [y]: ").lower() != "n"

    checks = {
        f"Minimum {min_length} characters":
            len(password) >= min_length,

        "Uppercase":
            not require_upper or bool(re.search(r"[A-Z]", password)),

        "Lowercase":
            not require_lower or bool(re.search(r"[a-z]", password)),

        "Number":
            not require_number or bool(re.search(r"\d", password)),

        "Special character":
            not require_special or bool(re.search(r"[^A-Za-z0-9]", password))
    }

    print()

    for name, result in checks.items():
        print(f"[{'PASS' if result else 'FAIL'}] {name}")

    return all(checks.values())


# ============================================================
# BREACH CHECK - HAVE I BEEN PWNED
# Uses K-Anonymity.
# The complete password is NEVER sent.
# ============================================================

def check_breach(password):
    print("\nChecking breach database...")
    print("Using privacy-preserving k-anonymity method.")

    sha1_hash = hashlib.sha1(
        password.encode("utf-8")
    ).hexdigest().upper()

    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    try:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Password-Security-Toolkit"
            }
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            data = response.read().decode("utf-8")

        for line in data.splitlines():
            parts = line.split(":")

            if len(parts) == 2:
                returned_suffix = parts[0]
                count = int(parts[1])

                if returned_suffix == suffix:
                    print("\n[!] BREACHED PASSWORD")
                    print(f"Found approximately {count:,} times in breach data.")
                    return True

        print("\n[+] Password was not found in the queried breach data.")
        return False

    except urllib.error.URLError:
        print("\n[!] Unable to connect to breach database.")
        print("Check your internet connection.")
        return None

    except Exception as e:
        print(f"\n[!] Breach check failed: {e}")
        return None


# ============================================================
# SECURE PASSWORD HASHING
# ============================================================

def hash_password(password):
    """
    Uses Python's built-in scrypt password hashing.
    A random salt is generated for every password.
    """

    salt = secrets.token_bytes(16)

    key = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=2**14,
        r=8,
        p=1,
        dklen=32
    )

    encoded = (
        "scrypt$"
        + base64.b64encode(salt).decode()
        + "$"
        + base64.b64encode(key).decode()
    )

    return encoded


def verify_password(password, stored_hash):
    try:
        parts = stored_hash.split("$")

        if len(parts) != 3:
            return False

        algorithm, salt_b64, hash_b64 = parts

        if algorithm != "scrypt":
            return False

        salt = base64.b64decode(salt_b64)
        expected_hash = base64.b64decode(hash_b64)

        actual_hash = hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=2**14,
            r=8,
            p=1,
            dklen=32
        )

        return secrets.compare_digest(actual_hash, expected_hash)

    except Exception:
        return False


# ============================================================
# OPTIONAL ENCRYPTION
# ============================================================

def encrypt_password():
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        print("\n[!] Encryption requires:")
        print("    pip install cryptography")
        return

    password = input("Enter password to encrypt: ")

    key = Fernet.generate_key()
    cipher = Fernet(key)

    encrypted = cipher.encrypt(password.encode())

    print("\nEncrypted password:")
    print(encrypted.decode())

    print("\nEncryption key:")
    print(key.decode())

    print("\nIMPORTANT:")
    print("Keep the key safe. Without it, the encrypted data cannot be decrypted.")


def decrypt_password():
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        print("\n[!] Encryption requires:")
        print("    pip install cryptography")
        return

    encrypted = input("Enter encrypted password: ").strip()
    key = input("Enter encryption key: ").strip()

    try:
        cipher = Fernet(key.encode())
        decrypted = cipher.decrypt(encrypted.encode())

        print("\nDecrypted password:")
        print(decrypted.decode())

    except Exception:
        print("\n[!] Invalid key or corrupted encrypted data.")


# ============================================================
# FULL PASSWORD SECURITY REPORT
# ============================================================

def security_report():
    print("\n" + "=" * 65)
    print("                 PASSWORD SECURITY REPORT")
    print("=" * 65)

    password = input("Enter password to analyze: ")

    username = input("Username (optional): ").strip()
    email = input("Email (optional): ").strip()

    score, rating, warnings, positives = analyze_password(
        password,
        username,
        email
    )

    entropy = calculate_entropy(password)

    print("\n--- SECURITY SCORE ---")
    print(f"Score   : {score}/100")
    print(f"Rating  : {rating}")
    print(f"Length  : {len(password)} characters")
    print(f"Entropy : {entropy:.2f} bits")

    print("\n--- POSITIVE FINDINGS ---")

    if positives:
        for item in positives:
            print(f"[+] {item}")
    else:
        print("No major positive findings.")

    print("\n--- WARNINGS ---")

    if warnings:
        for warning in warnings:
            print(f"[!] {warning}")
    else:
        print("[+] No obvious weaknesses detected.")

    crack_time(entropy)

    print("\n--- BREACH CHECK ---")

    check_breach(password)

    print("\n" + "=" * 65)


# ============================================================
# OPTION 1
# ============================================================

def check_existing_password():
    password = input("\nEnter password to check: ")

    username = input("Username (optional): ").strip()
    email = input("Email (optional): ").strip()

    score, rating, warnings, positives = analyze_password(
        password,
        username,
        email
    )

    entropy = calculate_entropy(password)

    print("\n" + "=" * 60)
    print("PASSWORD ANALYSIS")
    print("=" * 60)

    print(f"Length       : {len(password)}")
    print(f"Strength     : {rating}")
    print(f"Score        : {score}/100")
    print(f"Entropy      : {entropy:.2f} bits")

    print("\nPositive findings:")

    for item in positives:
        print(f"[+] {item}")

    print("\nWarnings:")

    if warnings:
        for warning in warnings:
            print(f"[!] {warning}")
    else:
        print("[+] No obvious weaknesses detected.")

    crack_time(entropy)

    choice = input("\nCheck breach database? (y/n): ").lower()

    if choice == "y":
        check_breach(password)


# ============================================================
# OPTION 2
# ============================================================

def generate_secure_password():
    print("\n1. Random secure password")
    print("2. Secure passphrase")

    choice = input("\nSelect: ")

    if choice == "1":
        try:
            length = int(input("Password length [20]: ") or "20")

            if length < 12:
                print("Minimum recommended length is 12.")
                length = 12

            password = generate_password(length)

            print("\nGenerated secure password:")
            print(password)

            print(f"\nEntropy: {calculate_entropy(password):.2f} bits")

        except ValueError:
            print("Invalid length.")

    elif choice == "2":
        try:
            count = int(input("Number of words [5]: ") or "5")

            if count < 3:
                count = 3

            password = generate_passphrase(count)

            print("\nGenerated secure passphrase:")
            print(password)

            print(f"\nLength: {len(password)} characters")

        except ValueError:
            print("Invalid number.")


# ============================================================
# OPTION 3 - HASH
# ============================================================

def hash_menu():
    print("\n1. Create password hash")
    print("2. Verify password against hash")

    choice = input("\nSelect: ")

    if choice == "1":
        password = input("Enter password: ")

        result = hash_password(password)

        print("\nPassword hash:")
        print(result)

        print("\nStore the hash, NOT the original password.")

    elif choice == "2":
        password = input("Enter password to verify: ")
        stored_hash = input("Enter stored hash: ")

        if verify_password(password, stored_hash):
            print("\n[+] PASSWORD MATCH")
        else:
            print("\n[-] PASSWORD DOES NOT MATCH")


# ============================================================
# MAIN MENU
# ============================================================

def main():
    while True:

        banner()

        print("\nOptions:")
        print("1. Check an existing password")
        print("2. Generate a strong, secure password")
        print("3. Hash & verify a password")
        print("4. Encrypt a password")
        print("5. Decrypt an encrypted password")
        print("6. Password security report")
        print("7. Check password policy")
        print("8. Calculate entropy & crack time")
        print("9. Check password breach")
        print("10. Exit")

        choice = input("\nSelect an option (1-10): ").strip()

        if choice == "1":
            check_existing_password()

        elif choice == "2":
            generate_secure_password()

        elif choice == "3":
            hash_menu()

        elif choice == "4":
            encrypt_password()

        elif choice == "5":
            decrypt_password()

        elif choice == "6":
            security_report()

        elif choice == "7":
            password = input("\nEnter password: ")
            check_policy(password)

        elif choice == "8":
            password = input("\nEnter password: ")

            entropy = calculate_entropy(password)

            print(f"\nEntropy: {entropy:.2f} bits")

            crack_time(entropy)

        elif choice == "9":
            password = input("\nEnter password to check: ")
            check_breach(password)

        elif choice == "10":
            print("\nExiting Password Security Toolkit...")
            break

        else:
            print("\n[!] Invalid option.")

        input("\nPress ENTER to continue...")


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    main()