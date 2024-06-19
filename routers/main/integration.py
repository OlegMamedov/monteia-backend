import requests
import hashlib
import json

class P2p:
    def __init__(self, base, merchant_id, secret_key):
        self.base = base
        self.merchant_id = merchant_id
        self.secret_key = secret_key

    def _build_params(self, params):
        return requests.compat.urlencode(params)

    def _sign(self, data):
        encoded_data = json.dumps(data, separators=(',', ':'))
        signature_string = f"{self.secret_key}+{encoded_data}"
        return hashlib.md5(signature_string.encode()).hexdigest()

    def request(self, url, method, data=None):
        if data is None:
            data = {}

        url = f"{self.base}/{url}"
        headers = {}

        if method == 'GET':
            url += '?' + self._build_params(data)
            response = requests.get(url)
        elif method == 'POST':
            data['merchant_id'] = self.merchant_id
            data['signature'] = self._sign(data)
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.post(url, json=data, headers=headers)

        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            error_message = {
                'status_code': response.status_code,
                'error': response.reason,
                'message': response.text
            }
            return error_message

    def get_limits(self, method_type, currency):
        return self.request('merchant-api/limits', 'POST', {'method_type': method_type, 'currency': currency})

    def create_order(self, type_, amount, currency, method_type, customer_id, invoice_id, sell_details=None):
        data = {
            'type': type_,
            'amount': str(amount),
            'currency': currency,
            'method_type': method_type,
            'customer_id': customer_id,
            'invoice_id': invoice_id
        }

        if sell_details is not None:
            data['sell_details'] = sell_details

        return self.request('merchant-api/create-order', 'POST', data)

    def cancel_order(self, order_id):
        return self.request('merchant-api/cancel-order', 'POST', {'order_id': order_id})