"""
Self-Checkout Kiosk System
Implementation with while loops for scanning and discount processes
"""

import datetime
import time
import random


class SelfCheckoutKiosk:
    def __init__(self):
        # Initialize the kiosk
        self.current_screen = 'home'
        self.cart = []
        self.subtotal = 0
        self.discounts_applied = []
        self.total_discount = 0
        self.payment_method = None
        self.payment_status = None
        self.receipt_printed = False
        
        # Product database for lookups
        self.product_database = {
            '123456789': {'name': 'Bread', 'price': 2.99},
            '987654321': {'name': 'Milk', 'price': 3.49},
            '456789123': {'name': 'Eggs', 'price': 4.99},
            '789123456': {'name': 'Bananas', 'price': 1.99},
            '321654987': {'name': 'Coffee', 'price': 5.99},
            '654987321': {'name': 'Cereal', 'price': 4.49},
        }
        
        # Discount database
        self.discount_database = {
            'SAVE10': {'code': 'SAVE10', 'amount': 1.00, 'description': '$1.00 off your purchase'},
            'SPRING25': {'code': 'SPRING25', 'amount': 2.50, 'description': '$2.50 off your purchase'},
            '5PERCENTOFF': {'code': '5PERCENTOFF', 'description': '5% off your total'}
        }

    """
    Navigate to a different screen in the kiosk interface
    """
    def navigate_to(self, screen):
        valid_screens = ['home', 'scanning', 'discounts', 'payment', 'scanQR', 'cardReader', 'complete', 'receipt']
        
        if screen not in valid_screens:
            print(f"Error: Invalid screen: {screen}")
            return False
        
        self.current_screen = screen
        print(f"Screen changed to: {screen}")
        return True

    """
    Look up an item in the database by barcode
    """
    def lookup_item(self, barcode):
        if barcode in self.product_database:
            return self.product_database[barcode].copy()
        return None

    """
    Add an item to the cart
    """
    def add_item_to_cart(self, item):
        self.cart.append(item)
        self.subtotal += item['price']
        print(f"Added: {item['name']} - ${item['price']:.2f}")
        return True

    """
    Remove an item from the cart
    """
    def remove_item(self, index):
        if index < 0 or index >= len(self.cart):
            print(f"Error: Invalid item index {index}")
            return False
            
        item = self.cart.pop(index)
        self.subtotal -= item['price']
        print(f"Removed: {item['name']} - ${item['price']:.2f}")
        return True

    """
    Begin shopping process with a while loop for scanning
    """
    def begin_shopping(self):
        self.navigate_to('scanning')
        print('Shopping session started')
        
        # Main scanning loop
        scanning = True
        while scanning:
            print("\nScanning Mode - Options:")
            print("1. Scan item (simulated)")
            print("2. Enter barcode manually")
            print("3. View cart")
            print("4. Remove item")
            print("5. Proceed to discounts")
            print("6. Proceed to payment")
            print("7. Cancel shopping")
            
            choice = input("Enter choice (1-7): ")
            
            if choice == '1':
                # Simulate scanning a random item
                barcode = random.choice(list(self.product_database.keys()))
                item = self.lookup_item(barcode)
                if item:
                    self.add_item_to_cart(item)
                    print(f"Successfully scanned: {item['name']}")
                    time.sleep(1)  # Brief pause to simulate scanning
                
            elif choice == '2':
                # Manual barcode entry
                barcode = input("Enter barcode: ")
                item = self.lookup_item(barcode)
                if item:
                    self.add_item_to_cart(item)
                else:
                    print(f"Barcode {barcode} not found in database")
            
            elif choice == '3':
                # View cart contents
                self.show_cart_summary()
            
            elif choice == '4':
                # Remove an item
                self.show_cart_summary()
                if self.cart:
                    try:
                        index = int(input("Enter item number to remove (1-based): ")) - 1
                        self.remove_item(index)
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                else:
                    print("Cart is empty. Nothing to remove.")
            
            elif choice == '5':
                # End scanning and go to discounts
                scanning = False
                self.process_discounts()
            
            elif choice == '6':
                # Skip discounts and go to payment
                scanning = False
                self.proceed_to_payment()
            
            elif choice == '7':
                # Cancel entire shopping session
                scanning = False
                self.cancel()
            
            else:
                print("Invalid choice. Please try again.")

    """
    Process discounts using a while loop
    """
    def process_discounts(self):
        self.navigate_to('discounts')
        print('Discount section opened')
        
        # Main discount processing loop
        applying_discounts = True
        while applying_discounts:
            print("\nDiscount Mode - Options:")
            print("1. Apply discount code")
            print("2. Apply percentage discount")
            print("3. View applied discounts")
            print("4. View cart")
            print("5. Return to scanning")
            print("6. Proceed to payment")
            print("7. Cancel shopping")
            
            choice = input("Enter choice (1-7): ")
            
            if choice == '1':
                # Apply discount code
                code = input("Enter discount code: ").upper()
                if code in self.discount_database:
                    discount = self.discount_database[code].copy()
                    
                    # Handle percentage discounts
                    if 'PERCENT' in code:
                        # Extract percentage from description
                        percent = int(discount['description'].split('%')[0])
                        discount['amount'] = round(self.subtotal * (percent / 100), 2)
                        print(f"Applied {percent}% discount: ${discount['amount']:.2f}")
                    
                    self.discounts_applied.append(discount)
                    self.total_discount += discount['amount']
                    print(f"Applied discount: {discount['code']} - ${discount['amount']:.2f}")
                else:
                    print(f"Invalid discount code: {code}")
            
            elif choice == '2':
                # Apply custom percentage discount
                try:
                    percent = float(input("Enter discount percentage: "))
                    if 0 <= percent <= 100:
                        amount = round(self.subtotal * (percent / 100), 2)
                        discount = {
                            'code': f'CUSTOM{percent}%',
                            'amount': amount,
                            'description': f'{percent}% off your total'
                        }
                        self.discounts_applied.append(discount)
                        self.total_discount += amount
                        print(f"Applied {percent}% discount: ${amount:.2f}")
                    else:
                        print("Percentage must be between 0 and 100")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            
            elif choice == '3':
                # View applied discounts
                if self.discounts_applied:
                    print("\n--- Applied Discounts ---")
                    for d in self.discounts_applied:
                        print(f"{d['code']} - ${d['amount']:.2f}")
                    print(f"Total discount: ${self.total_discount:.2f}")
                    print("-----------------------")
                else:
                    print("No discounts applied")
            
            elif choice == '4':
                # View cart contents
                self.show_cart_summary()
            
            elif choice == '5':
                # Return to scanning
                applying_discounts = False
                self.navigate_to('scanning')
                self.begin_shopping()  # Resume scanning loop
            
            elif choice == '6':
                # End discounts and go to payment
                applying_discounts = False
                self.proceed_to_payment()
            
            elif choice == '7':
                # Cancel entire shopping session
                applying_discounts = False
                self.cancel()
            
            else:
                print("Invalid choice. Please try again.")

    """
    Cancel the current action and return to home
    """
    def cancel(self):
        self.navigate_to('home')
        print('Action cancelled, returned to home screen')
        
        # Reset kiosk state
        self.cart = []
        self.subtotal = 0
        self.discounts_applied = []
        self.total_discount = 0
        self.payment_method = None
        self.payment_status = None
        self.receipt_printed = False

    """
    Show a summary of the current cart
    """
    def show_cart_summary(self):
        if not self.cart:
            print("Your cart is empty")
            return
            
        print("\n--- Cart Summary ---")
        for i, item in enumerate(self.cart):
            print(f"{i+1}. {item['name']} - ${item['price']:.2f}")
        print(f"Subtotal: ${self.subtotal:.2f}")
        if self.discounts_applied:
            print(f"Discounts: -${self.total_discount:.2f}")
        print(f"Total: ${self.get_total_due():.2f}")
        print("-------------------\n")

    """
    Proceed to payment from either scanning or discounts
    """
    def proceed_to_payment(self):
        self.navigate_to('payment')
        print('Ready for payment selection')
        
        # Payment selection loop
        selecting_payment = True
        while selecting_payment:
            print("\nPayment Mode - Options:")
            print("1. Pay by Card")
            print("2. Pay by E-wallet")
            print("3. Pay by Cash")
            print("4. View cart and total")
            print("5. Cancel payment")
            
            choice = input("Enter choice (1-5): ")
            
            if choice == '1':
                self.select_payment('card')
                self.process_payment(True)  # Simulate successful payment
                selecting_payment = False
            
            elif choice == '2':
                self.select_payment('e-wallet')
                self.process_payment(True)  # Simulate successful payment
                selecting_payment = False
            
            elif choice == '3':
                self.select_payment('cash')
                selecting_payment = False
            
            elif choice == '4':
                self.show_cart_summary()
                print(f"Total to pay: ${self.get_total_due():.2f}")
            
            elif choice == '5':
                selecting_payment = False
                print("Payment cancelled")
                # Ask if they want to return to scanning or cancel
                if input("Return to scanning? (y/n): ").lower() == 'y':
                    self.navigate_to('scanning')
                    self.begin_shopping()
                else:
                    self.cancel()
            
            else:
                print("Invalid choice. Please try again.")

    """
    Select a payment method
    """
    def select_payment(self, method):
        valid_methods = ['e-wallet', 'card', 'cash']
        if method not in valid_methods:
            print(f"Error: Invalid payment method: {method}")
            return False
        
        self.payment_method = method
        
        if method == 'e-wallet':
            self.navigate_to('scanQR')
            print('Please scan QR code for e-wallet payment')
        elif method == 'card':
            self.navigate_to('cardReader')
            print('Please insert or tap your card')
        elif method == 'cash':
            print(f"Please insert ${self.get_total_due():.2f} in cash")
            # In a real implementation, this would interface with a cash acceptor
            time.sleep(2)  # Simulate cash insertion
            print("Cash accepted")
            self.navigate_to('complete')
            self.payment_status = 'successful'
            print('Cash payment processed successfully. Transaction complete.')
            self.complete_transaction()
            return True
        
        return True

    """
    Process the payment attempt
    """
    def process_payment(self, success=True):
        if self.current_screen != 'scanQR' and self.current_screen != 'cardReader':
            print('Error: Cannot process payment from current screen')
            return False
        
        # Simulate payment processing
        print("Processing payment...")
        time.sleep(2)
        
        if success:
            self.payment_status = 'successful'
            self.navigate_to('complete')
            print('Payment successful! Transaction complete.')
            self.complete_transaction()
        else:
            self.payment_status = 'failed'
            self.navigate_to('payment')
            print('Payment failed. Please select a payment method again.')
        
        return success

    """
    Complete the transaction and handle receipt
    """
    def complete_transaction(self):
        # Ask about receipt
        if input("Would you like a receipt? (y/n): ").lower() == 'y':
            self.print_receipt()
        else:
            print("Receipt skipped.")
            self.navigate_to('receipt')  # Still mark transaction as complete
            
        # Ask about starting a new transaction
        if input("Start a new transaction? (y/n): ").lower() == 'y':
            self.start_new_transaction()

    """
    Print receipt after successful transaction
    """
    def print_receipt(self):
        if self.current_screen != 'complete':
            print('Error: Cannot print receipt before completing transaction')
            return False
        
        self.receipt_printed = True
        self.navigate_to('receipt')
        
        # Generate receipt content
        receipt_content = {
            'items': self.cart,
            'subtotal': self.subtotal,
            'discounts': self.discounts_applied,
            'total_discount': self.total_discount,
            'total': self.subtotal - self.total_discount,
            'payment_method': self.payment_method,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        # Print formatted receipt
        print('\n' + '=' * 40)
        print('           RECEIPT')
        print('=' * 40)
        print(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print('-' * 40)
        print('Items:')
        for item in self.cart:
            print(f"  {item['name']:20} ${item['price']:.2f}")
        print('-' * 40)
        print(f"{'Subtotal':20} ${self.subtotal:.2f}")
        if self.discounts_applied:
            for discount in self.discounts_applied:
                print(f"Discount ({discount['code']}): -${discount['amount']:.2f}")
        print(f"{'Total Discount':20} -${self.total_discount:.2f}")
        print(f"{'Total':20} ${self.get_total_due():.2f}")
        print('-' * 40)
        print(f"Payment Method: {self.payment_method}")
        print(f"Status: {self.payment_status}")
        print('\nThank you for shopping with us!')
        print('=' * 40 + '\n')
        
        return receipt_content

    """
    Start a new transaction after completing one
    """
    def start_new_transaction(self):
        # Reset the kiosk state
        self.cart = []
        self.subtotal = 0
        self.discounts_applied = []
        self.total_discount = 0
        self.payment_method = None
        self.payment_status = None
        self.receipt_printed = False
        
        # Return to home screen
        self.navigate_to('home')
        print('Ready for new transaction')
        
        # Start shopping again
        self.begin_shopping()

    """
    Check if the transaction is complete
    """
    def is_transaction_complete(self):
        return self.current_screen == 'receipt'

    """
    Get the total amount due
    """
    def get_total_due(self):
        return self.subtotal - self.total_discount

    """
    Get the current state of the kiosk
    """
    def get_kiosk_state(self):
        return {
            'current_screen': self.current_screen,
            'cart_items': len(self.cart),
            'cart_contents': [f"{item['name']} (${item['price']:.2f})" for item in self.cart],
            'subtotal': round(self.subtotal, 2),
            'discounts_applied': len(self.discounts_applied),
            'discount_details': [f"{d['code']} (${d['amount']:.2f})" for d in self.discounts_applied],
            'total_discount': round(self.total_discount, 2),
            'total_due': round(self.get_total_due(), 2),
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'receipt_printed': self.receipt_printed
        }


# Main function to run the kiosk
def main():
    print("=" * 50)
    print("     SELF-CHECKOUT KIOSK SYSTEM")
    print("=" * 50)
    print("Welcome to the interactive self-checkout system!")
    
    kiosk = SelfCheckoutKiosk()
    
    # Start the shopping process with the main while loop
    kiosk.begin_shopping()


if __name__ == "__main__":
    main()
