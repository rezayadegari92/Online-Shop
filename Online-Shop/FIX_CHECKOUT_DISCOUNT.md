# Checkout Discount Display Fix

## Issue
Discount codes were being applied successfully in the cart page but were **not showing on the checkout page**. Users would see the discount applied in the cart (e.g., 50% off, $180 discount) but when navigating to checkout, the discount would disappear and show the full price ($359.99 instead of $180).

## Root Cause

### Frontend State Management Problem
The discount information was stored in **local component state** in the CartDrawer component, not in the global cart store. When users navigated from the cart page to the checkout page, this local state was lost.

**CartDrawer.vue** had:
```typescript
const discountApplied = ref(false)
const discountPercent = ref(0)
```

These were local reactive variables that didn't persist across page navigation.

### Missing Data in Cart Store
The cart store (`cart.store.ts`) was only storing:
- Cart items
- Item details (name, price, quantity)

But NOT storing:
- Discount code
- Discount percentage
- Total price (before discount)
- Final price (after discount)

### Checkout Page Not Using Discount Data
The CheckoutView was calculating subtotal manually from cart items without considering any applied discounts:
```typescript
const subtotal = computed(() => {
  return cart.items.reduce((sum, item) => sum + (item.price || 0) * item.quantity, 0)
})
```

And displaying this as the final total without any discount deduction.

## Solution

### 1. Enhanced Cart Store (`cart.store.ts`)

**Added discount-related state:**
```typescript
state: () => ({
  items: [] as CartItem[],
  isOpen: false,
  discountCode: null as string | null,      // NEW
  discountPercent: 0,                        // NEW
  totalPrice: 0,                             // NEW
  finalPrice: 0,                             // NEW
})
```

**Updated load() action to capture discount data from API:**
```typescript
async load() {
  const { data } = await api.get("/api/cart/");
  
  if (data.items && Array.isArray(data.items)) {
    this.items = data.items.map(...);
    
    // Store discount information from API response
    this.discountPercent = data.discount_percent || 0;
    this.totalPrice = data.total_price || 0;
    this.finalPrice = data.final_price || 0;
  }
}
```

### 2. Updated CartDrawer Component

**Changed from local state to computed properties:**
```typescript
// BEFORE (Local State)
const discountApplied = ref(false)
const discountPercent = ref(0)

// AFTER (Computed from Store)
const discountApplied = computed(() => cart.discountPercent > 0)
const discountPercent = computed(() => cart.discountPercent)
```

**Reload cart after applying discount:**
```typescript
async function applyDiscount() {
  try {
    const { data } = await api.post('/api/cart/apply-discount/', {
      code: discountCode.value.toUpperCase()
    })
    
    // Reload cart to get updated discount information
    await cart.load()  // ✅ This ensures store has latest data
    discountError.value = ''
  } catch (error: any) {
    discountError.value = error.response?.data?.code?.[0] || 'Invalid discount code'
  }
}
```

### 3. Updated CheckoutView Component

**Added discount display in Order Total section:**
```vue
<div class="space-y-3 mb-6">
  <!-- Subtotal (before discount) -->
  <div class="flex justify-between text-gray-600">
    <span>Subtotal:</span>
    <span>{{ formatPrice(subtotal) }}</span>
  </div>
  
  <!-- Discount (NEW) -->
  <div v-if="cart.discountPercent > 0" class="flex justify-between text-green-600">
    <span>Discount ({{ cart.discountPercent }}%):</span>
    <span>-{{ formatPrice(discountAmount) }}</span>
  </div>
  
  <!-- Shipping -->
  <div class="flex justify-between text-gray-600">
    <span>Shipping:</span>
    <span>Free</span>
  </div>
  
  <!-- Final Total (NEW - now includes discount) -->
  <div class="border-t pt-3 flex justify-between text-xl font-bold">
    <span>Total:</span>
    <span>{{ formatPrice(finalTotal) }}</span>
  </div>
</div>
```

**Added discount calculation logic:**
```typescript
const subtotal = computed(() => {
  return cart.items.reduce((sum, item) => sum + (item.price || 0) * item.quantity, 0)
})

const discountAmount = computed(() => {
  if (!cart.discountPercent) return 0
  return (subtotal.value * cart.discountPercent) / 100
})

const finalTotal = computed(() => {
  return subtotal.value - discountAmount.value
})
```

## Backend Verification

The backend was already working correctly:

### Cart API Response
The CartSerializer already includes all necessary fields:
```python
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "total_price",
            "discount_percent",  # ✅ Already present
            "final_price",       # ✅ Already present
            "is_authenticated",
        ]
```

### Checkout Process
The CheckoutView in backend correctly transfers discount to order:
```python
order = Order.objects.create(
    user=user,
    # ... address fields ...
    discount_code=cart.discount_code,  # ✅ Discount preserved
)

# Calculate order total with discount
order.calculate_total_price()  # ✅ Applies discount
```

## Testing

### Test Scenario 1: Apply Discount and Navigate to Checkout
1. ✅ Add product to cart (Samsung Galaxy A54 - $360)
2. ✅ Apply discount code "MEGA50" (50% off)
3. ✅ Cart shows: Subtotal $360, Discount -$180, Total $180
4. ✅ Navigate to /checkout
5. ✅ Checkout shows: Subtotal $360, Discount (50%) -$180, Total $180
6. ✅ Complete order
7. ✅ Order is created with discount_code and correct total

### Test Scenario 2: Multiple Page Navigation
1. ✅ Apply discount in cart
2. ✅ Go to checkout (discount visible)
3. ✅ Go back to products page
4. ✅ Return to checkout
5. ✅ Discount still visible (persisted in store)

### Test Scenario 3: Update Cart with Discount
1. ✅ Apply discount code
2. ✅ Go to checkout
3. ✅ Change quantity of item
4. ✅ Discount recalculates correctly
5. ✅ Total updates with discount applied

## Files Modified

1. **`frontend/src/stores/cart.store.ts`**
   - Added discount state fields
   - Updated load() to capture discount data from API
   - Reset discount fields when cart is empty

2. **`frontend/src/components/cart/CartDrawer.vue`**
   - Changed from local state to computed properties using cart store
   - Added cart.load() after applying discount
   - Use cart.discountPercent directly

3. **`frontend/src/views/CheckoutView.vue`**
   - Added discount display in Order Total section
   - Added discountAmount computed property
   - Updated finalTotal to subtract discount
   - Show discount percentage from cart store

## Benefits

1. ✅ **Discount Persistence**: Discount information persists across page navigation
2. ✅ **Consistent Display**: Same discount shown in cart and checkout
3. ✅ **Single Source of Truth**: Cart store is the authoritative source for cart data
4. ✅ **Real-time Updates**: Changes to cart automatically update discount calculations
5. ✅ **User Clarity**: Users see exactly what they'll pay before completing order

## API Response Example

**GET /api/cart/** with discount applied:
```json
{
  "id": 1,
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "Samsung Galaxy A54",
        "price": "360.00",
        "discounted_price": "360.00"
      },
      "quantity": 1,
      "total_price": "360.00"
    }
  ],
  "total_price": "360.00",
  "discount_percent": "50.00",
  "final_price": "180.00",
  "is_authenticated": true
}
```

## User Flow (Fixed)

### Before Fix ❌
1. User adds product to cart: $360
2. User applies "MEGA50" discount code
3. Cart shows: $360 - 50% = $180 ✅
4. User clicks "Proceed to Checkout"
5. Checkout shows: $360 (NO DISCOUNT) ❌
6. User confused - discount disappeared!

### After Fix ✅
1. User adds product to cart: $360
2. User applies "MEGA50" discount code
3. Cart shows: $360 - 50% = $180 ✅
4. User clicks "Proceed to Checkout"
5. Checkout shows: $360 - 50% = $180 ✅
6. User completes order with correct price ✅
7. Order saved with discount_code and final price $180 ✅

## Summary

**Problem**: Discount shown in cart but not in checkout  
**Root Cause**: Discount data stored in local component state, not global store  
**Solution**: Store discount data in cart store, load from API, display in both views  
**Result**: Discount persists across navigation and displays correctly everywhere  

**Status**: ✅ FIXED AND TESTED

---

**Date Fixed**: December 20, 2025  
**Related Files**:
- `frontend/src/stores/cart.store.ts`
- `frontend/src/components/cart/CartDrawer.vue`
- `frontend/src/views/CheckoutView.vue`
- `carts/api/serializers.py` (already correct)
- `carts/api/views.py` (already correct)