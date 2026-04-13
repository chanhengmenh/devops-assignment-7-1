from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid

app = FastAPI(title="FoodExpress API")

# In-memory storage (for demo only)
orders = []

# Data model
class Order(BaseModel):
    item: str
    quantity: int
    price: float

class OrderResponse(Order):
    id: str


# 1) Root endpoint
@app.get("/")
def root():
    return {"message": "FoodExpress API is running"}


# 2) Health check
@app.get("/health")
def health():
    return {"status": "ok"}


# 3) Create new order
@app.post("/orders", response_model=OrderResponse)
def create_order(order: Order):
    order_id = str(uuid.uuid4())
    new_order = {
        "id": order_id,
        "item": order.item,
        "quantity": order.quantity,
        "price": order.price
    }
    orders.append(new_order)
    return new_order

@app.post("/orders/bulk", response_model=List[OrderResponse])
def create_orders_bulk(orders_list: List[Order]):
    new_orders = []
    for order in orders_list:
        order_id = str(uuid.uuid4())
        # Use .model_dump() (Pydantic v2) to simplify dictionary creation
        new_entry = {"id": order_id, **order.model_dump()}
        orders.append(new_entry)
        new_orders.append(new_entry)
    return new_orders

# 4) Get all orders
@app.get("/orders", response_model=List[OrderResponse])
def get_orders():
    return orders


# 5) Get order by ID
@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str):
    for order in orders:
        if order["id"] == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")

@app.put("/orders/{order_id}", response_model=OrderResponse)
def update_order(order_id: str, updated_order: Order):
    for index, order in enumerate(orders):
        if order["id"] == order_id:
            # Create the updated dictionary maintaining the original ID
            new_data = {"id": order_id, **updated_order.model_dump()}
            orders[index] = new_data
            return new_data
    
    raise HTTPException(status_code=404, detail="Order not found")

@app.delete("/orders/{order_id}")
def delete_order(order_id: str):
    for index, order in enumerate(orders):
        if order["id"] == order_id:
            orders.pop(index)
            return {"message": f"Order {order_id} deleted successfully"}
            
    raise HTTPException(status_code=404, detail="Order not found")