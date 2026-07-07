from woocommerce_local.client import WooCommerceClient


class WooCommerceService:

    @staticmethod
    def get_products(params=None):

        wcapi = WooCommerceClient.client()

        response = wcapi.get("products", params=params)

        if response.status_code != 200:

            raise Exception(response.text)

        return response

    @staticmethod
    def get_orders(params=None):

        wcapi = WooCommerceClient.client()

        response = wcapi.get("orders", params=params)

        if response.status_code != 200:

            raise Exception(response.text)

        return response

    @staticmethod
    def get_coupons():

        wcapi = WooCommerceClient.client()

        response = wcapi.get("coupons")

        if response.status_code != 200:

            raise Exception(response.text)

        return response

    @staticmethod
    def get_product(product_id):

        wcapi = WooCommerceClient.client()

        response = wcapi.get(
            f"products/{product_id}"
        )

        if response.status_code != 200:

            raise Exception(response.text)

        return response

    @staticmethod
    def get_order(order_id):

        wcapi = WooCommerceClient.client()

        response = wcapi.get(
            f"orders/{order_id}"
        )

        if response.status_code != 200:

            raise Exception(response.text)

        return response

    @staticmethod
    def post(endpoint, data):
        wcapi = WooCommerceClient.client()
        response = wcapi.post(endpoint, data)
        return response

    @staticmethod
    def put(endpoint, data):
        wcapi = WooCommerceClient.client()
        response = wcapi.put(endpoint, data)
        return response