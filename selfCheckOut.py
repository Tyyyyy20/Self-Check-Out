"""
Self-Checkout Kiosk System
An improved implementation of a self-checkout system with recurring scanning functionality
"""

import datetime
import time
import threading
import random  # For simulating barcode scanning in demo


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
        self.scanner_active = False
        self._scanner_thread = None
        self._scanner_stop_event = threading.Event()
        self.product_database = {
            '123456789': {'name': 'Bread', 'price': 2.99},
            '987654321': {'name': 'Milk', 'price': 3.49},
            '456789123': {'name': 'Eggs', 'price': 4.99},
            '789123456': {'name': 'Bananas', 'price': 1.99},
            '321654987': {'name': 'Coffee', 'price': 5.99},
            '654987321': {'name': 'Cereal', 'price': 4.49},
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
    Start the shopping process
    """
    def begin_shopping(self):
        self.navigate_to('scanning')
        print('Shopping session started')
        # Automatically start scanning when shopping begins
        self.start_continuous_scanning()

    """
    Cancel the current action and return to home
    """
    def cancel(self):
        # Stop scanning if active
        if self.scanner_active:
            self.stop_continuous_scanning()
            
        self.navigate_to('home')
        print('Action cancelled, returned to home screen')

    """
    Look up an item in the database by barcode
    """
    def lookup_item(self, barcode):
        if barcode in self.product_database:
            return self.product_database[barcode].copy()
        return None

    """
    Scan an item and add it to the cart
    """
    def scan_item(self, item):
        if self.current_screen != 'scanning':
            print('Error: Cannot scan items outside scanning screen')
            return False
        
        self.cart.append(item)
        self.subtotal += item['price']
        print(f"Scanned: {item['name']} - ${item['price']:.2f}")
        return True

    """
    Simulated scanner that continuously reads barcodes
    """
    def _scanner_worker(self):
        print("Scanner activated and ready to scan items")
        scan_count = 0
        
        while not self._scanner_stop_event.is_set():
            if self.current_screen != 'scanning':
                # If we leave the scanning screen, pause the scanner
                time.sleep(0.5)
                continue
                
            # Simulate barcode scanning (in a real system, this would be hardware input)
            barcode = random.choice(list(self.product_database.keys()))
            item = self.lookup_item(barcode)
            
            if item:
                self.scan_item(item)
                scan_count += 1
                
                # Simulate time between scans
                time.sleep(random.uniform(1.5, 3.0))
                
                # For demo purposes, stop after scanning 5 items
                if scan_count >= 5:
                    print("Please place scanned items in bagging area")
                    # In a real system, you might pause here for weight verification
                    time.sleep(2)
                    scan_count = 0
            else:
                print("Unrecognized barcode, please try again")
                time.sleep(1)

    """
    Start continuous scanning mode
    """
    def start_continuous_scanning(self):
        if self.current_screen != 'scanning':
            self.navigate_to('scanning')
        
        if self.scanner_active:
            print("Scanner is already active")
            return
            
        self.scanner_active = True
        self._scanner_stop_event.clear()
        self._scanner_thread = threading.Thread(target=self._scanner_worker)
        self._scanner_thread.daemon = True  # Allow program to exit even if thread is running
        self._scanner_thread.start()
        
        print('Continuous scanning activated - ready to scan multiple items')

    """
    Stop the continuous scanning process
    """
    def stop_continuous_scanning(self):
        if not self.scanner_active:
            print("Scanner is not active")
            return
            
        self._scanner_stop_event.set()
        if self._scanner_thread:
            self._scanner_thread.join(timeout=1.0)  # Wait for scanner thread to finish
        
        self.scanner_active = False
        print('Scanning completed')

    """
    Manually add an item by barcode
    """
    def add_item_by_barcode(self, barcode):
        if self.current_screen != 'scanning':
            print('Error: Cannot scan items outside scanning screen')
            return False
            
        item = self.lookup_item(barcode)
        if item:
            return self.scan_item(item)
        else:
            print(f"Error: Barcode {barcode} not found in database")
            return False

    """
    Remove the last scanned item
    """
    def remove_last_item(self):
        if not self.cart:
            print("Cart is empty, nothing to remove")
            return False
            
        item = self.cart.pop()
        self.subtotal -= item['price']
        print(f"Removed: {item['name']} - ${item['price']:.2f}")
        return True

    """
    Remove a specific item from the cart
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
    Open the discounts section
    """
    def open_discounts(self):
        # Stop scanning when moving to discounts
        if self.scanner_active:
            self.stop_continuous_scanning()
            
        self.navigate_to('discounts')
        print('Discount section opened')

    """
    Apply a discount to the transaction
    """
    def apply_discount(self, discount):
        if self.current_screen != 'discounts':
            print('Error: Cannot apply discount outside discounts screen')
            return False
        
        self.discounts_applied.append(discount)
        self.total_discount += discount['amount']
        print(f"Applied discount: {discount['code']} - ${discount['amount']:.2f}")
        return True

    """
    Apply a discount code (simulated lookup)
    """
    def apply_discount_code(self, code):
        discount_codes = {
            'SAVE10': {'code': 'SAVE10', 'amount': 1.00, 'description': '$1.00 off your purchase'},
            'SPRING25': {'code': 'SPRING25', 'amount': 2.50, 'description': '$2.50 off your purchase'},
            '5PERCENTOFF': {'code': '5PERCENTOFF', 'amount': self.subtotal * 0.05, 'description': '5% off your total'}
        }
        
        if code in discount_codes:
            return self.apply_discount(discount_codes[code])
        else:
            print(f"Invalid discount code: {code}")
            return False

    """
    Return to scanning after applying discounts
    """
    def resume_scanning(self):
        if self.current_screen != 'discounts':
            print('Error: Can only resume scanning from discounts screen')
            return False
            
        self.navigate_to('scanning')
        print('Returned to scanning')
        self.start_continuous_scanning()
        return True

    """
    Proceed to payment from either scanning or discounts
    """
    def proceed_to_payment(self):
        if self.current_screen != 'scanning' and self.current_screen != 'discounts':
            print('Error: Cannot proceed to payment from current screen')
            return False
        
        # Stop scanning if active
        if self.scanner_active:
            self.stop_continuous_scanning()
            
        self.navigate_to('payment')
        print('Ready for payment selection')
        return True

    """
    Select a payment method
    """
    def select_payment(self, method):
        if self.current_screen != 'payment':
            print('Error: Cannot select payment method outside payment screen')
            return False
        
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
            self.navigate_to('complete')
            self.payment_status = 'successful'
            print('Cash payment processed successfully. Transaction complete.')
            return True
        
        return True

    """
    Process the payment attempt
    """
    def process_payment(self, success=True):
        if self.current_screen != 'scanQR' and self.current_screen != 'cardReader':
            print('Error: Cannot process payment from current screen')
            return False
        
        if success:
            self.payment_status = 'successful'
            self.navigate_to('complete')
            print('Payment successful! Transaction complete.')
        else:
            self.payment_status = 'failed'
            self.navigate_to('payment')
            print('Payment failed. Please select a payment method again.')
        
        return success

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
            'receipt_printed': self.receipt_printed,
            'scanner_active': self.scanner_active
        }

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


# Example usage with automated continuous scanning simulation
def demonstrate_kiosk():
    kiosk = SelfCheckoutKiosk()
    
    # Start shopping (automatically starts scanning)
    kiosk.begin_shopping()
    
    # Wait for items to be scanned automatically
    print("Waiting for automatic scanning...")
    # In a real application this would be an event loop or GUI
    time.sleep(10)  # Wait for simulated scanning to occur
    
    # Stop scanning and show what's in the cart
    kiosk.stop_continuous_scanning()
    kiosk.show_cart_summary()
    
    # Manually add another item
    kiosk.add_item_by_barcode('654987321')  # Add cereal
    
    # Apply a discount
    kiosk.open_discounts()
    kiosk.apply_discount_code('SAVE10')
    
    # Return to scanning and scan one more item
    kiosk.resume_scanning()
    time.sleep(3)  # Wait for another item to be scanned
    kiosk.stop_continuous_scanning()  
    
    # Proceed to payment
    kiosk.proceed_to_payment()
    
    # Select payment method
    kiosk.select_payment('card')
    
    # Process payment (success)
    kiosk.process_payment(True)
    
    # Print receipt
    kiosk.print_receipt()
    
    # Check final state
    print('Final kiosk state:')
    print(kiosk.get_kiosk_state())
    
    # Start new transaction
    kiosk.start_new_transaction()


# Interactive mode demonstration for manual testing
def interactive_demo():
    kiosk = SelfCheckoutKiosk()
    print("Self-Checkout Kiosk Interactive Demo")
    print("Commands: start, scan, view, discount, pay, receipt, cancel, exit")
    
    running = True
    while running:
        cmd = input("\nEnter command: ").strip().lower()
        
        if cmd == "start":
            kiosk.begin_shopping()
        elif cmd == "scan":
            if kiosk.scanner_active:
                kiosk.stop_continuous_scanning()
                print("Scanning paused. Enter 'scan' again to resume.")
            else:
                kiosk.start_continuous_scanning()
        elif cmd == "view":
            kiosk.show_cart_summary()
            print(f"Current screen: {kiosk.current_screen}")
        elif cmd == "discount":
            kiosk.open_discounts()
            code = input("Enter discount code (SAVE10, SPRING25, 5PERCENTOFF): ")
            kiosk.apply_discount_code(code)
        elif cmd == "pay":
            kiosk.proceed_to_payment()
            method = input("Payment method (card, e-wallet, cash): ")
            kiosk.select_payment(method)
            if method in ["card", "e-wallet"]:
                kiosk.process_payment(True)
        elif cmd == "receipt":
            kiosk.print_receipt()
        elif cmd == "cancel":
            kiosk.cancel()
        elif cmd == "exit":
            running = False
        else:
            print("Unknown command")
    
    print("Demo ended")


# Run the demonstration
if __name__ == "__main__":
    # Choose which demo to run
    demo_type = input("Run [a]utomated or [i]nteractive demo? ").lower()
    if demo_type.startswith('i'):
        interactive_demo()
    else:
        demonstrate_kiosk()
