# 🏁 Integration: E-commerce Backend
<!-- ⏱️ 30 min | 🔴 Advanced -->

**What You'll Learn:** Build a complete e-commerce data model with customers, products, orders, inventory, and reporting.

## Models

```python
class Customer(Base):
    __tablename__ = "customers"
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    orders: Mapped[list["Order"]] = relationship(back_populates="customer")

class Product(Base):
    __tablename__ = "products"
    name: Mapped[str]
    price: Mapped[float]
    stock: Mapped[int]

class Order(Base):
    __tablename__ = "orders"
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    status: Mapped[str] = mapped_column(default="pending")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order")
```

## Business Logic

```python
def checkout(customer_id):
    cart = session.query(CartItem).filter(CartItem.customer_id == customer_id).all()
    order = Order(customer_id=customer_id)
    session.add(order)
    session.flush()

    for item in cart:
        if item.product.stock < item.quantity:
            raise ValueError(f"Insufficient stock for {item.product.name}")
        item.product.stock -= item.quantity
        session.add(OrderItem(order_id=order.id, product_id=item.product.id,
                               quantity=item.quantity, price=item.product.price))
        session.delete(item)
    session.commit()
```

## Reports

```python
# Top customers
query = session.query(Customer.name, func.sum(OrderItem.price * OrderItem.quantity))
query = query.join(Order).join(OrderItem).group_by(Customer.id)
query = query.order_by(func.sum(OrderItem.price * OrderItem.quantity).desc()).limit(5)
```

## Key Features Covered

- **Full CRUD** across 6 models
- **Transactions** with rollback on error
- **Stock management** with atomic updates
- **Reporting** with aggregations
- **Relationships** across multiple tables

## Running the Demo

```bash
python code/20-integration-ecommerce.py
```
