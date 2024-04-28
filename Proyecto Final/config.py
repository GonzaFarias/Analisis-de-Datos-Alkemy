class Config:
    BASE_PATH = 'Proyecto Final/data/'

    @staticmethod
    def get_dataset_path(filename):
        return Config.BASE_PATH + filename

    @classmethod
    def customers_path(cls) -> str:
        return cls.get_dataset_path('ecommerce_customers_dataset.csv')

    @classmethod
    def items_path(cls) -> str:
        return cls.get_dataset_path('ecommerce_order_items_dataset.csv')

    @classmethod
    def payments_path(cls) -> str:
        return cls.get_dataset_path('ecommerce_order_payments_dataset.csv')

    @classmethod
    def orders_path(cls) -> str:
        return cls.get_dataset_path('ecommerce_orders_dataset.csv')

    @classmethod
    def products_path(cls) -> str:
        return cls.get_dataset_path('ecommerce_products_dataset.csv')

