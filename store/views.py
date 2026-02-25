from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Store, Product, Order, OrderItem, Review


def store_list(request):
    """Display a list of all stores."""
    stores = Store.objects.all()
    return render(request, "store/store_list.html", {"stores": stores})


def product_list(request, store_id):
    """Display all products belonging to a specific store."""
    store = get_object_or_404(Store, id=store_id)
    products = Product.objects.filter(store=store)
    return render(
        request,
        "store/product_list.html",
        {"store": store, "products": products},
    )


@login_required
def product_detail(request, product_id):
    """Display full details of a single product including reviews."""
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    return render(
        request,
        "store/product_detail.html",
        {"product": product, "reviews": reviews},
    )


@login_required
def add_to_cart(request, product_id):
    """Add a product to the session cart with a specified quantity."""
    product = get_object_or_404(Product, id=product_id)

    if not product.is_in_stock():
        messages.error(request, "This product is out of stock")
        return redirect("product_list", store_id=product.store.id)

    quantity = int(request.POST.get("quantity", 1))

    if quantity > product.stock:
        messages.error(
            request,
            f"Only {product.stock} units available.",
        )
        return redirect("product_detail", product_id=product_id)

    cart = request.session.get("cart", {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str]["quantity"] += quantity
    else:
        cart[product_id_str] = {
            "name": product.name,
            "price": str(product.price),
            "quantity": quantity,
        }

    request.session["cart"] = cart
    request.session.modified = True

    messages.success(request, f"{product.name} added to cart")
    return redirect("product_list", store_id=product.store.id)


@login_required
def view_cart(request):
    """Display the current session cart with subtotals and total."""
    cart = request.session.get("cart", {})
    cart_items = []
    total = 0

    for product_id, item in cart.items():
        subtotal = float(item["price"]) * item["quantity"]
        total += subtotal
        cart_items.append(
            {
                "product_id": product_id,
                "name": item["name"],
                "price": item["price"],
                "quantity": item["quantity"],
                "subtotal": round(subtotal, 2),
            }
        )

    return render(
        request,
        "store/cart.html",
        {"cart_items": cart_items, "total": round(total, 2)},
    )


@login_required
def remove_from_cart(request, product_id):
    """Remove a product from the session cart."""
    cart = request.session.get("cart", {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]
        request.session["cart"] = cart
        request.session.modified = True
        messages.success(request, "Product removed from cart")

    return redirect("view_cart")


@login_required
def checkout(request):
    """
    Handle the checkout process.

    Creates an Order and OrderItems from the session cart,
    updates product stock, clears the cart, and sends an
    invoice email to the buyer.
    """
    cart = request.session.get("cart", {})

    if not cart:
        messages.error(request, "Your cart is empty")
        return redirect("view_cart")

    order = Order.objects.create(
        buyer=request.user,
        total_price=0,
    )

    for product_id_str, item in cart.items():
        product = get_object_or_404(Product, id=int(product_id_str))

        if not product.is_in_stock():
            messages.error(
                request,
                f"{product.name} is out of stock and was removed",
            )
            del cart[product_id_str]
            request.session["cart"] = cart
            request.session.modified = True
            continue

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item["quantity"],
            price_at_purchase=product.price,
        )

        product.stock -= item["quantity"]
        product.save()

    order.calculate_total()

    del request.session["cart"]
    request.session.modified = True

    try:
        send_invoice_email(request.user, order)
    except Exception:
        messages.warning(
            request,
            "Order placed successfully, but invoice email could not be sent",
        )

    messages.success(request, "Order placed successfully")
    return redirect("store_list")


def send_invoice_email(user, order):
    """Build and send an invoice email to the buyer after checkout."""
    try:
        items = OrderItem.objects.filter(order=order)
        body = f"Thank you for your order #{order.id}\n\n"
        body += "Items:\n"

        for item in items:
            body += (
                f"- {item.product.name} x {item.quantity}"
                f" @ R{item.price_at_purchase}\n"
            )

        body += f"\nTotal: R{order.total_price}"

        email = EmailMessage(
            subject=f"Invoice for Order #{order.id}",
            body=body,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email],
        )
        email.send()
    except Exception:
        pass


@login_required
def leave_review(request, product_id):
    """Allow a buyer to leave a review on a product."""
    product = get_object_or_404(Product, id=product_id)

    has_purchased = OrderItem.objects.filter(
        order__buyer=request.user,
        product=product,
    ).exists()

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        review = Review.objects.create(
            product=product,
            reviewer=request.user,
            rating=rating,
            comment=comment,
            is_verified=has_purchased,
        )
        review.set_verified_status(has_purchased)

        messages.success(request, "Review submitted successfully")
        return redirect("product_list", store_id=product.store.id)

    return render(
        request,
        "store/leave_review.html",
        {"product": product, "has_purchased": has_purchased},
    )


@login_required
def vendor_dashboard(request):
    """Display the vendor dashboard showing all their stores."""
    if not request.user.groups.filter(name="vendor").exists():
        messages.error(request, "You are not a vendor")
        return redirect("store_list")

    stores = Store.objects.filter(owner=request.user)
    return render(
        request,
        "store/vendor_dashboard.html",
        {"stores": stores},
    )


@login_required
def vendor_store_detail(request, store_id):
    """Display a single store with its products for the vendor."""
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    products = Product.objects.filter(store=store)
    return render(
        request,
        "store/vendor_store_detail.html",
        {"store": store, "products": products},
    )


@login_required
def create_store(request):
    """Allow a vendor to create a new store."""
    if not request.user.groups.filter(name="vendor").exists():
        messages.error(request, "You are not a vendor")
        return redirect("store_list")

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        Store.objects.create(
            owner=request.user,
            name=name,
            description=description,
        )

        messages.success(request, "Store created successfully")
        return redirect("vendor_dashboard")

    return render(request, "store/create_store.html")


@login_required
def edit_store(request, store_id):
    """Allow a vendor to edit one of their stores."""
    store = get_object_or_404(Store, id=store_id, owner=request.user)

    if request.method == "POST":
        store.name = request.POST.get("name")
        store.description = request.POST.get("description")
        store.save()

        messages.success(request, "Store updated successfully")
        return redirect("vendor_dashboard")

    return render(request, "store/edit_store.html", {"store": store})


@login_required
def delete_store(request, store_id):
    """Allow a vendor to delete one of their stores."""
    store = get_object_or_404(Store, id=store_id, owner=request.user)

    if request.method == "POST":
        store.delete()
        messages.success(request, "Store deleted successfully")

    return redirect("vendor_dashboard")


@login_required
def add_product(request, store_id):
    """Allow a vendor to add a product to one of their stores."""
    store = get_object_or_404(Store, id=store_id, owner=request.user)

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        stock = request.POST.get("stock")

        Product.objects.create(
            store=store,
            name=name,
            description=description,
            price=price,
            stock=stock,
        )

        messages.success(request, "Product added successfully")
        return redirect("vendor_dashboard")

    return render(request, "store/add_product.html", {"store": store})


@login_required
def edit_product(request, product_id):
    """Allow a vendor to edit one of their products."""
    product = get_object_or_404(
        Product,
        id=product_id,
        store__owner=request.user,
    )

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")
        product.save()

        messages.success(request, "Product updated successfully")
        return redirect("vendor_dashboard")

    return render(request, "store/edit_product.html", {"product": product})


@login_required
def delete_product(request, product_id):
    """Allow a vendor to delete one of their products."""
    product = get_object_or_404(
        Product,
        id=product_id,
        store__owner=request.user,
    )

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully")

    return redirect("vendor_dashboard")
