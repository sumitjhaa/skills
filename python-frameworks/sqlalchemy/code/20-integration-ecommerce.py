"""Integration: E-Commerce Backend — full schema with all production patterns."""
from sqlalchemy import create_engine, String, Integer, Float, Boolean, ForeignKey, Text, DateTime, func, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker, relationship, selectinload
from datetime import datetime, date
from typing import Optional

engine = create_engine("sqlite:///:memory:", echo=False)

class Base(DeclarativeBase):
    pass

# ======================== Models ========================

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(20), default="customer")
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    orders: Mapped[list["Order"]] = relationship(back_populates="user")
    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="user")

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    products: Mapped[list["Product"]] = relationship(back_populates="category")

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    price: Mapped[float] = mapped_column(Float)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="products")
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="product")

class CartItem(Base):
    __tablename__ = "cart_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    user: Mapped["User"] = relationship(back_populates="cart_items")
    product: Mapped["Product"] = relationship()

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(20), default="pending")
    total: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[float] = mapped_column(Float)
    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="order_items")

# Event: update stock on order placement
@event.listens_for(OrderItem, "after_insert")
def reduce_stock(mapper, connection, target):
    connection.execute(
        Product.__table__.update().where(Product.id == target.product_id)
        .values(stock=Product.stock - target.quantity)
    )

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# ======================== Seed ========================

session.add_all([
    User(username="alice", email="alice@shop.com", role="admin"),
    User(username="bob", email="bob@shop.com", role="customer"),
    User(username="charlie", email="charlie@shop.com", role="customer"),
])
session.add_all([
    Category(name="Electronics"), Category(name="Books"), Category(name="Clothing"),
])
session.commit()

session.add_all([
    Product(name="Laptop", price=999.99, stock=10, category_id=1),
    Product(name="Mouse", price=29.99, stock=50, category_id=1),
    Product(name="Keyboard", price=89.99, stock=30, category_id=1),
    Product(name="Python Book", price=39.99, stock=100, category_id=2),
    Product(name="SQL Guide", price=49.99, stock=75, category_id=2),
    Product(name="T-Shirt", price=19.99, stock=200, category_id=3),
])
session.commit()

# ======================== Operations ========================

print("=" * 60)
print("  E-COMMERCE BACKEND")
print("=" * 60)

def add_to_cart(username, product_name, qty=1):
    user = session.query(User).filter(User.username == username).first()
    product = session.query(Product).filter(Product.name == product_name).first()
    if not user or not product:
        return "User or product not found"
    existing = session.query(CartItem).filter(CartItem.user_id == user.id, CartItem.product_id == product.id).first()
    if existing:
        existing.quantity += qty
    else:
        session.add(CartItem(user_id=user.id, product_id=product.id, quantity=qty))
    session.commit()
    return f"Added {qty}x {product_name} to {username}'s cart"

def view_cart(username):
    user = session.query(User).filter(User.username == username).first()
    if not user:
        return "User not found"
    items = session.query(CartItem).filter(CartItem.user_id == user.id).options(selectinload(CartItem.product)).all()
    return [f"  {i.product.name:15s} x{i.quantity} = ${i.product.price * i.quantity:.2f}" for i in items]

def checkout(username):
    user = session.query(User).filter(User.username == username).first()
    if not user:
        return "User not found"
    cart = session.query(CartItem).filter(CartItem.user_id == user.id).options(selectinload(CartItem.product)).all()
    if not cart:
        return "Cart is empty"
    total = sum(ci.product.price * ci.quantity for ci in cart)
    order = Order(user_id=user.id, total=total)
    session.add(order)
    session.flush()
    for ci in cart:
        session.add(OrderItem(order_id=order.id, product_id=ci.product_id, quantity=ci.quantity, unit_price=ci.product.price))
        session.delete(ci)
    session.commit()
    return f"Order #{order.id} created for {username}: ${total:.2f}"

def list_orders(username):
    user = session.query(User).filter(User.username == username).first()
    if not user:
        return "User not found"
    orders = session.query(Order).filter(Order.user_id == user.id).options(selectinload(Order.items).selectinload(OrderItem.product)).all()
    result = []
    for o in orders:
        items = ", ".join(f"{i.product.name} x{i.quantity}" for i in o.items)
        result.append(f"  [#{o.id}] {o.status:10s} ${o.total:.2f} — {items}")
    return result

def inventory_report():
    cats = session.query(Category).options(selectinload(Category.products)).all()
    report = []
    for c in cats:
        total_stock = sum(p.stock for p in c.products)
        total_value = sum(p.price * p.stock for p in c.products)
        report.append(f"  {c.name:15s} {len(c.products):2d} products, {total_stock:4d} units, ${total_value:.2f} value")
    return report

print("\n1. Shopping:")
print(f"   {add_to_cart('alice', 'Laptop', 1)}")
print(f"   {add_to_cart('alice', 'Mouse', 2)}")
print(f"   {add_to_cart('alice', 'Python Book', 1)}")
print(f"   {add_to_cart('bob', 'Keyboard', 1)}")

print("\n2. Alice's cart:")
for item in view_cart("alice"):
    print(item)

print(f"\n3. Checkout:")
print(f"   {checkout('alice')}")
print(f"   {checkout('bob')}")

print("\n4. Alice's orders:")
for o in list_orders("alice"):
    print(o)

print("\n5. Bob's orders:")
for o in list_orders("bob"):
    print(o)

print("\n6. Inventory report:")
for line in inventory_report():
    print(line)

stats = session.query(
    func.count(Product.id).label("products"),
    func.sum(Product.stock).label("total_stock"),
    func.sum(Order.total).label("revenue"),
    func.count(Order.id).label("orders"),
).first()
print(f"\n7. Store stats: {stats.products} products, {stats.total_stock} units, {stats.orders} orders, ${stats.revenue:.2f} revenue")

session.close()
print("\n✅ E-Commerce Backend complete")
