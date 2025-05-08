can you add this in your git

def home_page():
    while True:
        print("\n--- HOME PAGE ---")
        print("1. Begin Scanning Items")
        print("2. Apply Discounts")
        print("3. Cancel (Stay on Home Page)")
        choice = input("Choose: ")

        if choice == "1":
            return scanning_items()
        elif choice == "2":
            return applying_discounts()
        elif choice == "3":
            continue
        else:
            print("Invalid choice.")

def scanning_items():
    while True:
        print("\n--- SCANNING ITEMS ---")
        print("1. Scan Item")
        print("2. Proceed to Payment")
        print("3. Cancel and Return to Home Page")
        choice = input("Choose: ")

        if choice == "1":
            print("Item scanned.")
        elif choice == "2":
            return payment_selection()
        elif choice == "3":
            return home_page()
        else:
            print("Invalid choice.")

def applying_discounts():
    while True:
        print("\n--- APPLYING DISCOUNTS ---")
        print("1. Apply Discount")
        print("2. Proceed to Payment")
        print("3. Cancel and Return to Home Page")
        choice = input("Choose: ")

        if choice == "1":
            print("Discount applied.")
        elif choice == "2":
            return payment_selection()
        elif choice == "3":
            return home_page()
        else:
            print("Invalid choice.")

def payment_selection():
    while True:
        print("\n--- PAYMENT SELECTION ---")
        print("1. Pay with E-Wallet")
        print("2. Pay with Card")
        print("3. Cancel and Return to Home Page")
        choice = input("Choose: ")

        if choice == "1":
            return scan_qr()
        elif choice == "2":
            return reading_card()
        elif choice == "3":
            return home_page()
        else:
            print("Invalid choice.")

def scan_qr():
    print("\n--- SCANNING QR ---")
    outcome = input("Was the QR scan successful? (yes/no): ")
    if outcome.lower() == "yes":
        return transaction_complete()
    else:
        print("QR Scan Failed. Returning to Payment Selection.")
        return payment_selection()

def reading_card():
    print("\n--- READING CARD ---")
    outcome = input("Was the card read successful? (yes/no): ")
    if outcome.lower() == "yes":
        return transaction_complete()
    else:
        print("Card Read Failed. Returning to Payment Selection.")
        return payment_selection()

def transaction_complete():
    print("\n--- TRANSACTION COMPLETE ---")
    input("Press Enter to print receipt...")
    return receipt()

def receipt():
    print("\n🧾 Receipt printed. Thank you for shopping!")
    exit()

# Entry point
home_page()
