#!/usr/bin/env python3
"""
Apple Store Stock Monitor Setup
Quick setup for monitoring iPhone 17 Pro Deep Blue 512GB or any Apple product
"""

import subprocess
import sys
import os


def install_dependencies():
    """Install required Python packages."""
    packages = ["requests"]

    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package} already installed")
        except ImportError:
            print(f"📦 Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed")


def quick_setup_iphone_17_pro():
    """Quick setup for iPhone 17 Pro Deep Blue 512GB."""
    print("🍎 Quick Setup: iPhone 17 Pro Deep Blue 512GB")
    print("=" * 50)

    # Add the iPhone 17 Pro Deep Blue 512GB
    os.system(
        'python apple_monitor.py add-product MG7Q4LL/A "iPhone 17 Pro 512GB Deep Blue"'
    )

    # Add some common stores
    print("\n🏪 Adding common Apple stores...")
    stores = [
        ("R090", "Washington Square, Tigard"),
        ("R191", "Pioneer Place, Portland"),
        ("R409", "Fifth Avenue, NYC"),
        ("R014", "SoHo, NYC"),
    ]

    for store_code, store_name in stores:
        os.system(f'python apple_monitor.py add-store {store_code} "{store_name}"')

    print("\n✅ Quick setup complete!")
    print("🚀 Start monitoring with: python apple_monitor.py run")


def interactive_setup():
    """Interactive setup for any products."""
    print("🍎 Interactive Apple Store Monitor Setup")
    print("=" * 50)

    # Discover products
    print("\n1. Let's find your products...")
    search_term = input(
        "Enter product search term (e.g., 'iPhone 17 Pro', 'iPad Pro'): "
    ).strip()

    if search_term:
        print(f"\n🔍 Searching for '{search_term}'...")
        os.system(f'python apple_monitor.py discover "{search_term}"')

        print("\nTo add a product, use:")
        print("python apple_monitor.py add-product <CODE> <NAME>")

    # Discover stores
    print("\n2. Let's find stores near you...")
    zipcode = input("Enter your zipcode (default: 10001): ").strip()
    if not zipcode:
        zipcode = "10001"

    print(f"\n🏪 Finding stores near {zipcode}...")
    os.system(f"python apple_monitor.py stores {zipcode}")

    print("\nTo add a store, use:")
    print("python apple_monitor.py add-store <CODE> <NAME>")

    print("\n✅ Setup complete!")
    print("📊 Check status with: python apple_monitor.py status")
    print("🚀 Start monitoring with: python apple_monitor.py run")


def main():
    """Main setup function."""
    print("🍎 Apple Store Stock Monitor Setup")
    print("=" * 40)

    # Install dependencies
    print("📦 Installing dependencies...")
    install_dependencies()

    print("\nChoose setup option:")
    print("1. Quick setup for iPhone 17 Pro Deep Blue 512GB")
    print("2. Interactive setup for any products")
    print("3. Skip setup")

    choice = input("\nEnter choice (1-3): ").strip()

    if choice == "1":
        quick_setup_iphone_17_pro()
    elif choice == "2":
        interactive_setup()
    else:
        print("Setup skipped. Use 'python apple_monitor.py' for manual setup.")

    print(f"\n📚 Available commands:")
    print(f"  python apple_monitor.py discover <term>  - Find products")
    print(f"  python apple_monitor.py stores <zip>     - Find stores")
    print(f"  python apple_monitor.py check            - Check stock")
    print(f"  python apple_monitor.py run              - Start monitoring")
    print(f"  python apple_monitor.py status           - Show config")


if __name__ == "__main__":
    main()
