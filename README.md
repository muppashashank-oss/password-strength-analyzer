# 🔐 Password Strength Analyzer & Security Toolkit

A Python-based **Password Security Toolkit** designed to help users understand password security, evaluate password strength, generate secure passwords, and perform multiple password-related security checks.

This project was created as a hands-on cybersecurity project to improve my understanding of **password security, hashing, encryption, entropy, password policies, and breach awareness**.

---

## 🚀 Features

### 🔍 1. Password Strength Checker
Analyzes an existing password and evaluates its overall security based on factors such as:

- Password length
- Uppercase characters
- Lowercase characters
- Numbers
- Special characters
- Common password patterns

### 🔑 2. Secure Password Generator
Generates strong random passwords using a combination of:

- Uppercase letters
- Lowercase letters
- Numbers
- Special characters

### #️⃣ 3. Hash & Verify Password
Supports password hashing and verification using secure hashing techniques.

### 🔒 4. Encrypt a Password
Encrypts sensitive password data so it is not stored or displayed in plain text.

### 🔓 5. Decrypt an Encrypted Password
Allows previously encrypted data to be decrypted when the correct key is available.

### 📊 6. Password Security Report
Provides a detailed security assessment of a password.

### 📋 7. Password Policy Checker
Checks whether a password satisfies common security requirements such as:

- Minimum length
- Uppercase letters
- Lowercase letters
- Numbers
- Special characters

### ⚡ 8. Entropy & Crack-Time Estimation
Calculates password entropy and provides an estimated cracking-time assessment based on the estimated search space.

> Crack-time results are estimates and should not be treated as guarantees.

### 🌐 9. Password Breach Check
Checks whether a password has appeared in known breach data using a privacy-conscious breach-checking approach.

> Never share passwords publicly or use this tool with passwords belonging to another person.

---

## 🛠️ Technologies Used

- **Python 3**
- `hashlib`
- `secrets`
- `string`
- `math`
- `re`
- `urllib`
- `base64`

No external Python packages are required for the core toolkit.

---

## 📥 Installation

Clone the repository:

```bash
git clone https://github.com/muppashashank-oss/password-strength-analyzer.git
