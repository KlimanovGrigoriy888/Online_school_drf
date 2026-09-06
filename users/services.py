import stripe
from stripe import StripeClient

from config.settings import STRIPE_API_KEY

client = StripeClient(STRIPE_API_KEY)


def create_stripe_product(id_product, name, description):
    """Создает продукт на API ресурсе stripe и возвращает его ID."""

    product = client.v1.products.create(
        params={
            "name": name,
            "description": description,
            # Передаем внутренний ID продукта из модели в метаданные
            "metadata": {
                "course_id": str(id_product)
            }
        }
    )

    # Возвращаем уникальный строковый ID продукта, который сгенерировал Stripe
    return product.id

def create_stripe_price(product_id, amount, product_name):
    """Создает цену продукта на API ресурсе stripe"""
    price = client.v1.prices.create(
        params={
            "product": product_id,  # Связываем цену с созданным продуктом в функции create_stripe_product()
            "currency": "rub",      # Валюта платежа
            "unit_amount": int(amount * 100),  # Переводим рубли в копейки требует stripe привести к наименьшему платежу
        }
    )
    # Возвращаем ID созданной цены
    # Этот ID нам необходим для создания сессии оплаты
    print(price.id)
    return price.id


def create_stripe_session(price_id):
    """Создает сессию оплаты на API ресурсе stripe и возвращает ссылку на оплату и ID сессии."""
    session = client.v1.checkout.sessions.create(
        params={
            # Передаем ID цены, которую мы создали функции create_stripe_price()
            "line_items": [
                {
                    "price": price_id,
                    "quantity": 1
                }
            ],
            # Режим — одиночный платеж (не подписка)
            "mode": "payment",
            # Страницы, куда Stripe перенаправит пользователя после оплаты или отмены
            "success_url": "http://127.0.0.1:8000/",
            "cancel_url": "http://127.0.0.1:8000/",
        }
    )

    # Возвращаем два значения:
    # session.id — уникальный ID сессии в Stripe (нужен для проверки статуса оплаты)
    # session.url — это ссылка для реализации платежа на странице Stripe

    return session.id, session.url