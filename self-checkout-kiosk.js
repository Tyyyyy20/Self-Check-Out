/**
 * Self-Checkout Kiosk System
 * A basic implementation of a self-checkout system that can be referenced
 * for creating an NFA representation of the shopping flow.
 */

class SelfCheckoutKiosk {
  constructor() {
    // Initialize the kiosk
    this.currentScreen = 'home';
    this.cart = [];
    this.subtotal = 0;
    this.discountsApplied = [];
    this.totalDiscount = 0;
    this.paymentMethod = null;
    this.paymentStatus = null;
    this.receiptPrinted = false;
  }

  /**
   * Navigate to a different screen in the kiosk interface
   */
  navigateTo(screen) {
    const validScreens = ['home', 'scanning', 'discounts', 'payment', 'scanQR', 'cardReader', 'complete', 'receipt'];
    
    if (!validScreens.includes(screen)) {
      console.error(`Invalid screen: ${screen}`);
      return false;
    }
    
    this.currentScreen = screen;
    console.log(`Screen changed to: ${screen}`);
    return true;
  }

  /**
   * Start the shopping process
   */
  beginShopping() {
    this.navigateTo('scanning');
    console.log('Shopping session started');
  }

  /**
   * Cancel the current action and return to home
   */
  cancel() {
    this.navigateTo('home');
    console.log('Action cancelled, returned to home screen');
  }

  /**
   * Scan an item and add it to the cart
   */
  scanItem(item) {
    if (this.currentScreen !== 'scanning') {
      console.error('Cannot scan items outside scanning screen');
      return false;
    }
    
    this.cart.push(item);
    this.subtotal += item.price;
    console.log(`Scanned: ${item.name} - $${item.price}`);
    return true;
  }
  // Add this method to the SelfCheckoutKiosk class
  continuousScanning() {
    if (this.currentScreen !== 'scanning') {
      this.navigateTo('scanning');
    }
    
    // This would connect to your actual scanner hardware
    this.scannerActive = true;
    console.log('Continuous scanning activated - ready to scan multiple items');
    
    // In a real implementation, you would connect this to hardware events
    // For example:
    // this.scannerDevice.addEventListener('scan', (scanData) => {
    //   const item = this.lookupItemFromDatabase(scanData);
    //   this.scanItem(item);
    // });
  }

// Add this method to stop scanning
finishScanning() {
  this.scannerActive = false;
  console.log('Scanning completed');
}

  /**
   * Open the discounts section
   */
  openDiscounts() {
    this.navigateTo('discounts');
    console.log('Discount section opened');
  }

  /**
   * Apply a discount to the transaction
   */
  applyDiscount(discount) {
    if (this.currentScreen !== 'discounts') {
      console.error('Cannot apply discount outside discounts screen');
      return false;
    }
    
    this.discountsApplied.push(discount);
    this.totalDiscount += discount.amount;
    console.log(`Applied discount: ${discount.code} - $${discount.amount}`);
    return true;
  }

  /**
   * Proceed to payment from either scanning or discounts
   */
  proceedToPayment() {
    if (this.currentScreen !== 'scanning' && this.currentScreen !== 'discounts') {
      console.error('Cannot proceed to payment from current screen');
      return false;
    }
    
    this.navigateTo('payment');
    console.log('Ready for payment selection');
    return true;
  }

  /**
   * Select a payment method
   */
  selectPayment(method) {
    if (this.currentScreen !== 'payment') {
      console.error('Cannot select payment method outside payment screen');
      return false;
    }
    
    const validMethods = ['e-wallet', 'card'];
    if (!validMethods.includes(method)) {
      console.error(`Invalid payment method: ${method}`);
      return false;
    }
    
    this.paymentMethod = method;
    
    if (method === 'e-wallet') {
      this.navigateTo('scanQR');
      console.log('Please scan QR code for e-wallet payment');
    } else if (method === 'card') {
      this.navigateTo('cardReader');
      console.log('Please insert or tap your card');
    }
    
    return true;
  }

  /**
   * Process the payment attempt
   */
  processPayment(success = true) {
    if (this.currentScreen !== 'scanQR' && this.currentScreen !== 'cardReader') {
      console.error('Cannot process payment from current screen');
      return false;
    }
    
    if (success) {
      this.paymentStatus = 'successful';
      this.navigateTo('complete');
      console.log('Payment successful! Transaction complete.');
    } else {
      this.paymentStatus = 'failed';
      this.navigateTo('payment');
      console.log('Payment failed. Please select a payment method again.');
    }
    
    return success;
  }

  /**
   * Print receipt after successful transaction
   */
  printReceipt() {
    if (this.currentScreen !== 'complete') {
      console.error('Cannot print receipt before completing transaction');
      return false;
    }
    
    this.receiptPrinted = true;
    this.navigateTo('receipt');
    
    // Generate receipt content
    const receiptContent = {
      items: this.cart,
      subtotal: this.subtotal,
      discounts: this.discountsApplied,
      totalDiscount: this.totalDiscount,
      total: this.subtotal - this.totalDiscount,
      paymentMethod: this.paymentMethod,
      timestamp: new Date().toISOString()
    };
    
    console.log('Receipt printed:');
    console.log(receiptContent);
    
    return receiptContent;
  }

  /**
   * Check if the transaction is complete
   */
  isTransactionComplete() {
    return this.currentScreen === 'receipt';
  }

  /**
   * Get the total amount due
   */
  getTotalDue() {
    return this.subtotal - this.totalDiscount;
  }

  /**
   * Get the current state of the kiosk
   */
  getKioskState() {
    return {
      currentScreen: this.currentScreen,
      cartItems: this.cart.length,
      subtotal: this.subtotal,
      discountsApplied: this.discountsApplied.length,
      totalDiscount: this.totalDiscount,
      totalDue: this.getTotalDue(),
      paymentMethod: this.paymentMethod,
      paymentStatus: this.paymentStatus,
      receiptPrinted: this.receiptPrinted
    };
  }
}

// Example usage
function demonstrateKiosk() {
  const kiosk = new SelfCheckoutKiosk();
  
  // Start shopping
  kiosk.beginShopping();
  
  // Scan some items
  kiosk.scanItem({ name: 'Bread', price: 2.99 });
  kiosk.scanItem({ name: 'Milk', price: 3.49 });
  kiosk.scanItem({ name: 'Eggs', price: 4.99 });
  
  // Apply discounts
  kiosk.openDiscounts();
  kiosk.applyDiscount({ code: 'SAVE10', amount: 1.00 });
  
  // Proceed to payment
  kiosk.proceedToPayment();
  
  // Select payment method
  kiosk.selectPayment('card');
  
  // Process payment (success)
  kiosk.processPayment(true);
  
  // Print receipt
  kiosk.printReceipt();
  
  // Check final state
  console.log('Final kiosk state:', kiosk.getKioskState());
}

// Run the demonstration
// demonstrateKiosk();
