# Fix for 500 Internal Server Error - Discount Code Application

## Error Description
When applying a discount code, users encountered a **500 Internal Server Error** with the following traceback:

```
TypeError: unsupported operand type(s) for *: 'decimal.Decimal' and 'float'
```

**Location:** `/app/carts/api/serializers.py`, line 108, in `get_final_price`

## Root Cause

### The Problem
Python's division operator (`/`) converts integers to floats. When we did:
```python
obj.discount_percent / 100
```

This created a **float**, which cannot be directly multiplied with a **Decimal** type in Python.

### Why This Happened
- `obj.discount_percent` is a `DecimalField` in the Cart model
- `total` (the cart total price) is a `Decimal`
- Division by `100` converted the discount_percent to a `float`
- Attempting to multiply `Decimal * float` raised a `TypeError`

## The Fix

### Files Modified
1. `carts/api/serializers.py` - Fixed `get_final_price` method
2. `carts/models.py` - Fixed `calculate_total_price` method
3. `orders/models.py` - Fixed `calculate_total_price` method

### Changes Applied

#### Before (Broken ❌)
```python
def get_final_price(self, obj):
    total = self.get_total_price(obj)
    if obj.discount_percent:
        discount = total * (obj.discount_percent / 100)  # TypeError!
        return total - discount
    return total
```

#### After (Fixed ✅)
```python
def get_final_price(self, obj):
    total = self.get_total_price(obj)
    if obj.discount_percent:
        discount = total * (Decimal(str(obj.discount_percent)) / Decimal("100"))
        return total - discount
    return total
```

### Key Changes
- Explicitly convert `discount_percent` to `Decimal` using `Decimal(str(...))`
- Use `Decimal("100")` instead of integer `100` for division
- Ensures all arithmetic operations use `Decimal` type consistently

## Why This Solution Works

### Type Consistency
All financial calculations now use the `Decimal` type from Python's `decimal` module, which:
- ✅ Prevents floating-point precision errors
- ✅ Maintains type safety
- ✅ Is the standard for financial calculations in Django

### Best Practice
Django's `DecimalField` returns `Decimal` objects. When doing calculations with Decimals:
- Always use `Decimal("100")` instead of `100`
- Convert other values to Decimal: `Decimal(str(value))`
- Never mix `Decimal` with `float` directly

## Testing

### Before Fix
```bash
curl -X POST http://localhost:3000/api/cart/apply-discount/ \
  -H "Content-Type: application/json" \
  -d '{"code": "WELCOME10"}'
```

**Result:** 500 Internal Server Error

### After Fix
```bash
curl -X POST http://localhost:3000/api/cart/apply-discount/ \
  -H "Content-Type: application/json" \
  -d '{"code": "WELCOME10"}'
```

**Result:** 200 OK with proper response:
```json
{
  "detail": "Discount code 'WELCOME10' applied successfully. 10% off!",
  "cart": {
    "id": 1,
    "items": [...],
    "total_price": "100.00",
    "discount_percent": "10.00",
    "final_price": "90.00"
  }
}
```

## Impact Areas

### Fixed Calculations In:
1. **Cart Serializer** - API response generation
2. **Cart Model** - Total price calculation
3. **Order Model** - Order total calculation with discount

### Related Features Working Now:
- ✅ Applying discount codes to cart
- ✅ Viewing cart with applied discount
- ✅ Calculating final price with discount
- ✅ Creating orders with discounts
- ✅ Checkout process with discount codes

## Prevention

To prevent similar issues in the future:

### 1. Always Use Decimal for Money
```python
# Good ✅
from decimal import Decimal
price = Decimal("10.99")
discount = Decimal("0.10")
final = price - (price * discount)

# Bad ❌
price = 10.99  # float
discount = 0.10  # float
final = price - (price * discount)  # imprecise
```

### 2. Division with Decimals
```python
# Good ✅
result = Decimal("100") / Decimal("3")

# Bad ❌
result = 100 / 3  # Creates float
```

### 3. Type Checking
```python
# Add assertions in development
assert isinstance(total, Decimal), "Total must be Decimal"
assert isinstance(discount_percent, Decimal), "Discount must be Decimal"
```

## Summary

**Problem:** Mixing `Decimal` and `float` types in discount calculations  
**Solution:** Ensure all financial arithmetic uses `Decimal` type consistently  
**Result:** Discount codes now work correctly without 500 errors  

**Status:** ✅ FIXED AND TESTED

---

**Date Fixed:** December 20, 2025  
**Related Files:** 
- `carts/api/serializers.py`
- `carts/models.py`
- `orders/models.py`
- `DISCOUNT_CODE_FIX.md` (comprehensive fix documentation)