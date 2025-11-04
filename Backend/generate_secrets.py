"""
Generate secure SECRET_KEY and JWT_SECRET_KEY for Flask application
Run this script to generate random secure keys for your .env file
"""

import secrets
import string

def generate_secret_key(length=64):
    """Generate a random secret key"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def main():
    """Generate and display secret keys"""
    print("=" * 70)
    print("ZeTheta FinArcade - Secret Key Generator")
    print("=" * 70)
    print()
    
    secret_key = generate_secret_key(64)
    jwt_secret_key = generate_secret_key(64)
    
    print("Generated secure keys:")
    print("-" * 70)
    print(f"SECRET_KEY={secret_key}")
    print()
    print(f"JWT_SECRET_KEY={jwt_secret_key}")
    print()
    print("-" * 70)
    print()
    print("Copy these keys and add them to your .env file:")
    print()
    print("   SECRET_KEY=" + secret_key)
    print("   JWT_SECRET_KEY=" + jwt_secret_key)
    print()
    print("=" * 70)
    print()
    print("IMPORTANT:")
    print("   - Never commit these keys to version control")
    print("   - Keep these keys secure and private")
    print("   - Use different keys for development and production")
    print("   - If keys are compromised, regenerate them immediately")
    print()
    print("=" * 70)

if __name__ == '__main__':
    main()

