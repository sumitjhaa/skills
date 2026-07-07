# 📝 Phase 02 Practice — Advanced SQLAlchemy

## Exercise 1: Migration Simulation

Extend the migration schema (lesson 11): create a `V2` state with new columns (`phone`, `is_admin`), then write the corresponding upgrade/downgrade functions. Test rolling forward and backward.

## Exercise 2: Window Functions

Using `Order` (id, customer_id, amount, created_at), write a query that numbers each customer's orders by date using `row_number()`, then returns only the most recent order per customer.

## Exercise 3: Inheritance

Model a `Payment` system using inheritance:
- `Payment` (amount, date, status)
- `CreditCardPayment` + (last_four, cardholder)
- `PayPalPayment` + (email, transaction_id)

Insert 2 of each type, then query all pending payments across types.

## Exercise 4: Event Audit

Add event listeners to track all changes to `Product` (lesson 14): log old/new values when price or stock changes. Print a report after the demo.

## Exercise 5: N+1 Detection

With `Category` → `Product` → `Review` (each category has products, each product has reviews):
1. Query all categories and access `category.products[0].reviews` in a loop
2. Count the queries (use echo=True)
3. Fix with eager loading

## Exercise 6: E-commerce Extension

Extend the e-commerce demo (lesson 20) to support:
- Coupon codes (discount % per order)
- Shipping address per order
- Order status transitions (pending → shipped → delivered)

**Stretch:** Add a `ProductReview` model and calculate average rating per product.
