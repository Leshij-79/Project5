import stripe

from config.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def create_stripe_products(course):

    product = stripe.Product.create(name=course.title, description=course.description)

    return product.id, product.name


def create_stripe_price(price, product_id):

    price = stripe.Price.create(
        currency="rub",
        unit_amount=int(price * 100),
        product=product_id,
    )

    return price.id


def create_stripe_session(price):

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price, "quantity": 1}],
        mode="payment",
    )

    return session.id, session.url
