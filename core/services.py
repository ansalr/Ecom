from .models import Product, SizePrice, Order, OrderItem, Contact
from decimal import Decimal
import uuid
import json

def calculate_item_price(product, size_name):
    price = Decimal(product.base_price)
    price_obj = SizePrice.objects.filter(product=product, size_name=size_name).first()
    if price_obj:
        price = Decimal(price_obj.price)
    
    if product.offer_percent > 0:
        multiplier = (Decimal('100') - Decimal(product.offer_percent)) / Decimal('100')
        price = price * multiplier
    
    return price

def normalize_extras(extras):
    if not extras:
        return []
    if isinstance(extras, str):
        try:
            extras = json.loads(extras)
        except:
            pass 
    
    if isinstance(extras, list):
        return sorted([str(e) for e in extras])
    return extras

def create_order_from_data(contact_id, items_data):
    contact = Contact.objects.get(id=contact_id)
    order_no = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    
    order = Order.objects.create(
        order_no=order_no,
        contact=contact
    )
    
    merged_items = {}
    
    for item in items_data:
        product_id = item['product_id']
        size_name = item['size_name']
        qty = int(item['qty'])
        customization = item.get('customization', '').strip()
        extras = item.get('extras', [])
        
        normalized_extras = normalize_extras(extras)
        extras_key = json.dumps(normalized_extras)
        
        key = (product_id, size_name, extras_key, customization)
        
        if key in merged_items:
            merged_items[key]['qty'] += qty
        else:
            merged_items[key] = {
                'product_id': product_id,
                'size_name': size_name,
                'qty': qty,
                'extras': normalized_extras,
                'customization': customization
            }
            
    for val in merged_items.values():
        product = Product.objects.get(id=val['product_id'])
        unit_price = calculate_item_price(product, val['size_name'])
        
        OrderItem.objects.create(
            order=order,
            product=product,
            size_name=val['size_name'],
            qty=val['qty'],
            unit_price=unit_price,
            extras=val['extras'],
            customization=val['customization']
        )
        
    return order
