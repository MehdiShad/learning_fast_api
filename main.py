import database_models
from models import Product
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from database import session, engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)


database_models.Base.metadata.create_all(bind=engine)

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
    Product(id=8, name="phone", description="budget phone", price=89, quantity=10),
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()

    count = db.query(database_models.Product).count

    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()

init_db()   

@app.get('/products/')
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products
 

@app.get('/product/{id}')
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "Product not found"
 
    # # return products [id -1]
    # for product in products:
    #     if product.id == id:
    #         return product
    # return "product not found"


@app.post("/products/")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))

    db.commit()
    return product

    # products.append(product)
    # return product


@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product= db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not db_product:
        return "No Product found"
    
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    db.commit()
    return product

    # for i in range(len(products)):
    #     if products[i].id == id:
    #         products[i] = product
    #         return "product Added successfully"

    # return "No Product found"

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not db_product:
        return "Product not found"
    db.delete(db_product)
    db.commit()
    return "Product Deleted"

    # for i in range(len(products)):
    #     if products[i] == id:
    #         del products[i]
    #         return "Product Deleted"
    # return "Product not found"

