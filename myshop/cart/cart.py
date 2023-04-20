from _decimal import Decimal

from django.conf import settings

from shop.models import Product


class Cart:
    """
    Класс Корзина, который позволит управлять корзиной покупок
    """

    def __init__(self, request):
        """Инициализировать корзину"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product: Product,
            quantity: int = 1, override_quantity: bool = False) -> None:
        """
        Добавить товар в корзиу либо обновить его количество
        :param product: товар
        :param quantity: количество товара
        :param override_quantity: перезаписать количество
        :return: None
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': product.price
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Пометить сеанс как измененный, чтобы
        обеспечить его сохранение"""
        self.session.modified = True

    def remove(self, product: Product):
        """Удалить товар из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        В методе __iter__() извлекаются присутствующие в корзине экземпляры
        класса Product, чтобы включить их в товарные позиции корзины. Текущая
        корзина копируется в переменную cart, и в нее добавляются экземпляры
        класса Product. Наконец, товары корзины прокручиваются в цикле, конвер-
        тируя цену каждого товара обратно в десятичное число фиксированной точ-
        ности и добавляя в каждый товар атрибут total_price. Метод __iter__() по-
        зволит легко прокручивать товарные позиции корзины в представлениях
        и шаблонах.
        """
        product_ids = self.cart.keys()
        # получить объекты product и добавить их в корзину
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Подсчитать все товарные позиции в корзине"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Метод расчета общей стоимости товаров в корзине"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Удалить корзину из сеанса"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
