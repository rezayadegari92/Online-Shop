# Quick Testing Guide for Discount Codes

## 🚀 Quick Start

### 1. Create Sample Discount Codes
```bash
# Local
python manage.py create_discount_codes

# Docker
docker-compose exec web python manage.py create_discount_codes
```

### 2. Verify Codes in Database
```bash
# Local
python manage.py shell -c "from orders.models import DiscountCode; [print(f'{c.code} -> {c.discount_percent}%') for c in DiscountCode.objects.all()]"

# Docker
docker-compose exec web python manage.py shell -c "from orders.models import DiscountCode; [print(f'{c.code} -> {c.discount_percent}%') for c in DiscountCode.objects.all()]"
```

## 🧪 Testing Scenarios

### Scenario 1: Exact Match (Should Work ✅)
```bash
curl -X POST http://localhost:8000/api/cart/apply-discount/ \
  -H "Content-Type: application/json" \
  -d '{"code": "WELCOME10"}'
```

### Scenario 2: Lowercase (Should Work ✅)
```bash
curl -X POST http://localhost:8000/api/cart/apply-discount/ \
  -H "Content-Type: application/json" \
  -d '{"code": "welcome10"}'
```

### Scenario 3: Mixed Case (Should Work ✅)
```bash
curl -X POST http://localhost:8000/api/cart/apply-discount/ \
  -H "Content-Type: application/json" \
  -d '{"code": "WeLcOmE10"}'
```

### Scenario 4: With Whitespace (Should Work ✅)
```bash
curl -X POST http://localhost:8000/api/cart/apply-discount/ \
  -H "Content-Type: application/json" \
  -d '{"code": "  WELCOME10  "}'
```

### Scenario 5: Invalid Code (Should Fail ❌)
```bash
curl -X POST http://localhost:8000/api/cart/apply-discount/ \
  -H "Content-Type: application/json" \
  -d '{"code": "INVALID999"}'
```

Expected Response:
```json
{
  "code": ["Invalid discount code: 'INVALID999'. Please check the code and try again."]
}
```

### Scenario 6: Empty Code (Should Fail ❌)
```bash
curl -X POST http://localhost:8000/api/cart/apply-discount/ \
  -H "Content-Type: application/json" \
  -d '{"code": ""}'
```

Expected Response:
```json
{
  "code": ["Discount code cannot be empty"]
}
```

## 📋 Available Test Codes

| Code | Discount | Use Case |
|------|----------|----------|
| `WELCOME10` | 10% | New customer welcome |
| `SAVE20` | 20% | General savings |
| `SUMMER25` | 25% | Seasonal promotion |
| `MEGA50` | 50% | Major sale |
| `VIP15` | 15% | VIP members |
| `NEWYEAR30` | 30% | New year special |
| `FLASH40` | 40% | Flash sale |
| `STUDENT5` | 5% | Student discount |

## 🔍 Frontend Testing (if applicable)

### JavaScript/Fetch Example
```javascript
fetch('http://localhost:8000/api/cart/apply-discount/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_JWT_TOKEN' // if authenticated
  },
  body: JSON.stringify({ code: 'welcome10' })
})
  .then(response => response.json())
  .then(data => console.log('Success:', data))
  .catch(error => console.error('Error:', error));
```

### Expected Success Response
```json
{
  "detail": "Discount code 'WELCOME10' applied successfully. 10% off!",
  "cart": {
    "id": 1,
    "items": [
      {
        "id": 1,
        "product": {
          "id": 1,
          "name": "Product Name",
          "price": "100.00",
          "discounted_price": "90.00"
        },
        "quantity": 2,
        "total_price": "180.00"
      }
    ],
    "total_price": "180.00",
    "discount_percent": "10.00",
    "final_price": "162.00"
  }
}
```

## 🐛 Troubleshooting

### Issue: "Invalid discount code"
**Possible Causes:**
1. ✅ Code doesn't exist in database → Run `create_discount_codes`
2. ✅ Typo in the code → Check available codes
3. ✅ Code expired (if expiry logic added) → Check expiration date

### Issue: "Discount code cannot be empty"
**Cause:** Empty string or whitespace-only input
**Solution:** Provide a valid code

### Issue: Discount not applied to cart
**Possible Causes:**
1. User not authenticated and cookies not enabled
2. Cart is empty
3. Discount code was not saved to cart object

**Check Cart State:**
```bash
# Docker
docker-compose exec web python manage.py shell

# Then in shell:
from carts.models import Cart
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.first()
cart = Cart.objects.get(user=user)
print(f"Discount Code: {cart.discount_code}")
print(f"Discount Percent: {cart.discount_percent}")
print(f"Total: {cart.calculate_total_price()}")
```

## ✅ Test Checklist

- [ ] Discount codes created in database
- [ ] Exact case match works
- [ ] Lowercase input works
- [ ] Uppercase input works
- [ ] Mixed case input works
- [ ] Leading/trailing whitespace handled
- [ ] Invalid code returns proper error
- [ ] Empty code returns proper error
- [ ] Discount applied to authenticated user cart
- [ ] Discount applied to anonymous user cart (via cookies)
- [ ] Final price calculation correct
- [ ] Checkout preserves discount code

## 🎯 What Was Fixed

### Before (Broken ❌)
- Only exact case match worked: `WELCOME10` ✅
- Lowercase failed: `welcome10` ❌
- Mixed case failed: `Welcome10` ❌
- Whitespace caused failure: `  WELCOME10  ` ❌

### After (Fixed ✅)
- Exact case match: `WELCOME10` ✅
- Lowercase works: `welcome10` ✅
- Mixed case works: `Welcome10` ✅
- Whitespace handled: `  WELCOME10  ` ✅
- Better error messages ✅
- Input normalization ✅

## 📝 Notes

- All input is automatically converted to uppercase and trimmed
- Database lookups are case-insensitive
- Discount codes maintain their original case in the database
- Works for both authenticated and anonymous users
- Changes are backward compatible