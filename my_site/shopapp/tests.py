from string import ascii_letters
from random import choices

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from shopapp.models import Product, Order
from shopapp.utils import add_two_numbers

class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)

class ProductCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="bob_test", password="qwerty")
        permission = Permission.objects.get(codename='add_product')
        cls.user.user_permissions.add(permission)
        cls.user.save()
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()
    def test_created_product(self):
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": self.product_name,
                "price": "123.45",
                "description": "A good table",
                "discount": "10",
            }
        )
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )
class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="bob_test", password="qwerty")
        permission = Permission.objects.get(codename='add_product')
        cls.user.user_permissions.add(permission)
        cls.user.save()
        cls.product = Product.objects.create(name="Best Product", created_by=cls.user)
    # def setUp(self) -> None:
    #     self.product = Product.objects.create(name="Best Product")

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()
        cls.user.delete()
    def setUp(self) -> None:
        self.client.force_login(self.user)
    def test_get_product(self):
        self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": self.product,
                "price": "123.45",
                "description": "A good table",
                "discount": "10",

            }
        )
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)

class ProductsListViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="bob_test", password="qwerty")
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
    def setUp(self) -> None:
        self.client.force_login(self.user)

    fixtures = [
        'products-fixture.json',
    ]
    def test_products(self):
        response = self.client.get(reverse("shopapp:products_list"))

        # # for product in Product.objects.filter(archived=False).all():
        # #     self.assertContains(response, product.name)

        # products = Product.objects.filter(archived=False).all()
        # products_ = response.context["products"]
        # for p, p_ in zip(products, products_):
        #     self.assertEqual(p.pk, p_.pk)

        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, "shopapp/products-list.html")

class ProductExportViewTestCese(TestCase):
    @classmethod
    def setUpClass(cls):
        # cls.credentials = dict(username="bob_test", password="qwerty")
        cls.user = User.objects.create_user(username="bob_test", password="qwerty")
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
    def setUp(self) -> None:
        self.client.force_login(self.user)

    fixtures = [
        "products-fixture.json"
    ]
    def test_get_products_view(self):
        response = self.client.get(
            reverse("shopapp:products-export"),
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data["products"],
            expected_data,
        )

""" 
Order section 
"""

class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # cls.credentials = dict(username="bob_test", password="qwerty")
        cls.user = User.objects.create_user(username="bob_test", password="qwerty")
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
    def setUp(self) -> None:
        self.client.force_login(self.user)
    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, "Orders")

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"))
        # self.assertRedirects(response, str(settings.LOGIN_URL))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)

class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="bob_test", password="qwerty")
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order = Order.objects.create(delivery_address='Pupkin street', user_id=self.user.id)

    def tearDown(self) -> None:
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(
            reverse('shopapp:orders_list')
        )
        # self.assertTrue(Order.objects.filter(delivery_address='Pupkin strasse').exists())
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.pomocode)
        order = Order.objects.filter(user_id=self.user.pk).all()
        order_ = response.context["order_list"]
        for p, p_ in zip(order, order_):
            self.assertEqual(p.pk, p_.pk)

class OrdersExportTestCase(TestCase):
        # Тест проходит, но словари пустые.
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="bob_test", password="qwerty", is_staff='True')
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    fixtures = [
        "orders-fixture.json"
    ]

    @user_passes_test(lambda u: u.is_staff)
    def test_get_orders_view(self):
        response = self.client.get(
            reverse("shopapp:orders-export"),
        )
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by("pk").all()
        expected_data = [
            {
                "id": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.pomocode,
                "user_id": order.user,
                "product_id": order.products
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(
            orders_data["orders"],
            expected_data,
        )