# Discount Code Fix Documentation

## Issue
The discount code validation was failing due to **case-sensitivity** issues. Users entering discount codes with incorrect capitalization (e.g., "welcome10" instead of "WELCOME10") would receive an "Invalid discount code" error, even though the code existed in the database.

## Root Causes

### 1. Case-Sensitivity Issue
The original code used case-sensitive lookups:
```python
DiscountCode.objects.get(code=value)
```

This meant that:
- Database code: `WELCOME10`
- User input: `welcome10` or `Welcome10`
- Result: ❌ "Invalid discount code" error

### 2. Decimal/Float Type Mismatch
When calculating discounts, the code mixed `Decimal` and `float` types:
```python
discount = total * (obj.discount_percent / 100)  # Division creates float!
```

Error: `TypeError: unsupported operand type(s) for *: 'decimal.Decimal' and 'float'`

## Changes Made

### 1. Cart API Serializer (`carts/api/serializers.py`)

**Before:**
```python
def validate_code(self, value):
    try:
        discount_code = DiscountCode.objects.get(code=value)
        return discount_code
    except DiscountCode.DoesNotExist:
        raise serializers.ValidationError("Invalid discount code")
```

**After:**
```python
def validate_code(self, value):
    # Strip whitespace and convert to uppercase for consistency
    value = value.strip().upper()

    if not value:
        raise serializers.ValidationError("Discount code cannot be empty")

    try:
        discount_code = DiscountCode.objects.get(code__iexact=value)
        return discount_code
    except DiscountCode.DoesNotExist:
        raise serializers.ValidationError(
            f"Invalid discount code: '{value}'. Please check the code and try again."
        )
```

**Improvements:**
- ✅ Case-insensitive lookup using `code__iexact`
- ✅ Automatic whitespace trimming
- ✅ Empty string validation
- ✅ Better error messages with the actual code entered
- ✅ Normalizes input to uppercase for consistency

### 2. Cart Model (`carts/models.py`)

**Before:**
```python
if data.get('discount_code'):
    try:
        cart.discount_code = DiscountCode.objects.get(code=data['discount_code'])
    except DiscountCode.DoesNotExist:
        pass
```

**After:**
```python
if data.get("discount_code"):
    try:
        discount_code_value = data["discount_code"].strip()
        if discount_code_value:
            cart.discount_code = DiscountCode.objects.get(
                code__iexact=discount_code_value
            )
            cart.discount_percent = cart.discount_code.discount_percent
    except DiscountCode.DoesNotExist:
        pass
```

**Improvements:**
- ✅ Case-insensitive lookup for session/cookie-based carts
- ✅ Whitespace handling
- ✅ Sets discount_percent from the discount_code object
- ✅ Code formatting improvements

#### 3. **`carts/api/serializers.py`** - Fixed Decimal Type Handling
**Before:**
```python
def get_final_price(self, obj):
    total = self.get_total_price(obj)
    if obj.discount_percent:
        discount = total * (obj.discount_percent / 100)  # ❌ Creates float
        return total - discount
    return total
```

**After:**
```python
def get_final_price(self, obj):
    total = self.get_total_price(obj)
    if obj.discount_percent:
        discount = total * (Decimal(str(obj.discount_percent)) / Decimal("100"))
        return total - discount
    return total
```

**Fix:** Ensures all arithmetic uses `Decimal` type to avoid type mismatch errors.

#### 4. **`carts/models.py`** - Fixed Cart Total Calculation
```python
# Before
discount_amount = (total * self.discount_code.discount_percent) / 100

# After
discount_amount = (
    total * Decimal(str(self.discount_code.discount_percent))
) / Decimal("100")
```

#### 5. **`orders/models.py`** - Fixed Order Total Calculation
```python
# Before
discount_amount = (total * self.discount_code.discount_percent) / 100

# After
discount_amount = (
    total * Decimal(str(self.discount_code.discount_percent))
) / Decimal("100")
```

## Testing

### Available Discount Codes
Run the following command to create sample discount codes:
```bash
python manage.py create_discount_codes
```

Or with Docker:
```bash
docker-compose exec web python manage.py create_discount_codes
```

### Sample Codes
- `WELCOME10` - 10% off
- `SAVE20` - 20% off
- `SUMMER25` - 25% off
- `MEGA50` - 50% off
- `VIP15` - 15% off
- `NEWYEAR30` - 30% off
- `FLASH40` - 40% off
- `STUDENT5` - 5% off

### Test Cases
Now all of these should work:
- ✅ `WELCOME10` (exact match)
- ✅ `welcome10` (lowercase)
- ✅ `Welcome10` (mixed case)
- ✅ `  WELCOME10  ` (with whitespace)
- ✅ `wElCoMe10` (random case)

### API Testing

**Endpoint:** `POST /api/cart/apply-discount/`

**Request:**
```json
{
    "code": "welcome10"
}
```

**Success Response (200):**
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

**Error Response (400):**
```json
{
    "code": ["Invalid discount code: 'INVALID123'. Please check the code and try again."]
}
```

## Benefits

1. **Better User Experience**: Users don't need to worry about exact capitalization
2. **Error Prevention**: Handles common input mistakes (extra spaces, wrong case)
3. **Clear Error Messages**: Users know exactly what went wrong
4. **Data Consistency**: Codes are normalized before lookup
5. **Session Support**: Works for both authenticated and anonymous users
6. **Type Safety**: Fixed Decimal/float type mismatches preventing 500 errors
7. **Accurate Calculations**: Discount calculations now work correctly without type errors

## Backward Compatibility

✅ **Fully backward compatible** - existing discount codes and functionality remain unchanged. Only the lookup mechanism is improved.

## Fixed Errors

### Before Fix
- ❌ Case mismatch: "Invalid discount code" 
- ❌ 500 Internal Server Error: `TypeError: unsupported operand type(s) for *: 'decimal.Decimal' and 'float'`

### After Fix
- ✅ Case-insensitive discount code validation
- ✅ Proper Decimal arithmetic throughout the codebase
- ✅ No more type mismatch errors
- ✅ Successful discount application with correct calculations

## Additional Notes

- Discount codes are stored in the database with their original case (typically uppercase)
- The lookup is case-insensitive, but the stored value maintains its original format
- Empty strings and whitespace-only inputs are properly rejected
- The fix applies to both database-backed carts (authenticated users) and cookie-backed carts (anonymous users)
- All financial calculations now use `Decimal` type consistently to prevent precision loss and type errors
- The `discount_percent` field in Cart is a DecimalField, while in DiscountCode it's an IntegerField - conversion handled properly