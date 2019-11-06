from django.db import migrations


def insert(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    db_alias = schema_editor.connection.alias
    Product.objects.using(db_alias).bulk_create([
        Product(**data) for data in product_data
    ])


def delete(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    db_alias = schema_editor.connection.alias
    for data in product_data:
        matched = Product.objects.using(db_alias).filter(**data).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert, delete),
    ]


# photos are provided in the myproject_docker/data/product-photos/ folder
product_data = [
    {"title": "Web Development with Django Cookbook, Second Edition",
     "slug": "web-development-django-cookbook-second-edition"},
    {"title": "jQuery UI 1.8: The User Interface Library for jQuery",
     "slug": "jquery-ui-1-8-user-interface-library",
     "price": 44.99},
    {"title": "Developing Responsive Web Applications with AJAX and jQuery",
     "slug": "developing-responsive-web-apps-ajax-jquery",
     "price": 39.99},
    {"title": "Django JavaScript Integration: AJAX and jQuery",
     "slug": "django-javascript-integration-ajax-jquery",
     "price": 44.99},
    {"title": "Django: Web Development with Python",
     "slug": "django-web-development-with-python"},
    {"title": "Web Development with Django Cookbook, Third Edition",
     "slug": "web-development-django-cookbook-third-edition"},
]
