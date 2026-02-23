from fastapi import FastAPI
from models import Product
app = FastAPI()

@app.get("/")
def greet():
    return "Welcome to shad trac"


# products = [
#     Product(1, "phone", "budget phone", 89, 10),
#     Product(2, "laptop", "budget phone", 189, 5),
#     Product(3, "phone", "budget phone", 89, 10),
#     Product(4, "phone", "budget phone", 89, 10),  
#     Product(5, "phone", "budget phone", 89, 10),
# ]

products = [
    Product(id=1, name="phone", description="budget phone", price=89, quantity=10),
    Product(id=2, name="laptop", description="budget phone", price=189, quantity=5),
    Product(id=3, name="phone", description="budget phone", price=89, quantity=10),
    Product(id=4, name="phone", description="budget phone", price=89, quantity=10),  
    Product(id=5, name="phone", description="budget phone", price=89, quantity=10),
]

@app.get('/products')
def get_all_products():
    return products
 

@app.get('/product/{id}')
def get_product_by_id(id: int):
    # return products [id -1]
    for product in products:
        if product.id == id:
            return product
    return "product not found"


@app.post("/product")
def add_product(product: Product):
    products.append(product)
    return product
 

@app.put("/product")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "product Added successfully"

    return "No Product found"

@app.delete("/product")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i] == id:
            del products[i]
            return "Product Deleted"
    return "Product not found"

