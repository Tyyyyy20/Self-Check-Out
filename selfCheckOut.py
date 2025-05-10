def home_page():
    while True:
        print("\n--- HOME PAGE ---")
        print("1. Begin Scanning Items")
        print("2. Apply Discounts")
        choice = input("Choose: ")

        if choice == "1":
            return scanning_items()
        elif choice == "2":
            return applying_discounts()
        else:
            print("Invalid choice.")

def scanning_items():
    while True:
        print("\n--- SCANNING ITEMS ---")
        print("1. Scan Item")
        print("2. Proceed to Payment")
        choice = input("Choose: ")

        if choice == "1":
            print("Item scanned.")
        elif choice == "2":
            return payment_selection()
        else:
            print("Invalid choice.")

def applying_discounts():
    while True:
        print("\n--- APPLYING DISCOUNTS ---")
        print("1. Apply Discount")
        print("2. Proceed to Payment")
        choice = input("Choose: ")

        if choice == "1":
            print("Discount applied.")
        elif choice == "2":
            return payment_selection()
        else:
            print("Invalid choice.")

def payment_selection():
    while True:
        print("\n--- PAYMENT SELECTION ---")
        print("1. Pay with E-Wallet")
        print("2. Pay with Card")
        print("3. Cancel")
        choice = input("Choose: ")

        if choice == "1":
            return scan_qr()
        elif choice == "2":
            return reading_card()
        elif choice == "2":
            return home_page()
        else:
            print("Invalid choice.")

def scan_qr():
    while True:
        print("\n--- SCANNING QR ---")
            outcome = input("Was the QR scan successful? (yes/no): ")
            if outcome.lower() == "yes":
                return transaction_complete()
            else:
                print("QR Scan Failed. Please Scan Again.")

def reading_card():
    while True:
        print("\n--- READING CARD ---")
        outcome = input("Was the card read successful? (yes/no): ")
        if outcome.lower() == "yes":
            return transaction_complete()
        else:
            print("Card Read Failed. Scan your Card Again.")

def transaction_complete():
    while True:
        print("\n--- TRANSACTION COMPLETE ---")
        print("1. Print Receipt")
        print("2. No Receipt")
        choice = input("Choose: ")

        if choice == "1":
            return receipt()
        elif choice == "2":
            print("Thank you for shopping!")
            exit()
        else:
            print("Invalid choice.")

def receipt():
    print("\n🧾 Receipt printed. Thank you for shopping!")
    exit()

# Entry point
home_page()
