from app.core.database import SessionLocal
from app.products.models import Product

# Create DB session
db = SessionLocal()

# Sample furniture and common products
sample_products = [
    {
        "name": "Wooden Dining Table",
        "description": "Solid wood dining table",
        "price": 8999.00,
        "stock": 20,
        "category": "Furniture",
        "image_url": "https://Wooden_Dinning_table.jpg"
    },
    {
        "name": "Office Chair",
        "description": "chair with adjustable height and back support.",
        "price": 3299.00,
        "stock": 40,
        "category": "Furniture",
        "image_url": "https://office_chair.jpg"
    },
    {
        "name": "Sofa Set",
        "description": "3-seater  sofa with a modern design.",
        "price": 14999.00,
        "stock": 15,
        "category": "Furniture",
        "image_url": "https://sofa_set.jpg"
    },
    {
        "name": "Electric Kettle",
        "description": " stainless steel electric kettle",
        "price": 799.00,
        "stock": 60,
        "category": "Appliances",
        "image_url": "https://electric_kettle.jpg"
    },
    {
        "name": "Fan",
        "description": "High-speed fan ",
        "price": 1799.00,
        "stock": 35,
        "category": "Appliances",
        "image_url": "https://ceiling_fan.jpg"
    },
]

# Insert into DB
for prod in sample_products:
    product = Product(**prod)
    db.add(product)

db.commit()
db.close()

print("✅ Sample products seeded.")
