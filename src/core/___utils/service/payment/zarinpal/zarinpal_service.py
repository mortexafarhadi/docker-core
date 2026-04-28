import requests

from ___utils.functions.json_function import str_to_json
from ___utils.functions.string_function import print_debug, red_text, green_text
from .zarinpal_variable import (
    ZARINPAL_IS_TOMAN,
    ZARINPAL_CALLBACK_URL,
    SITE_FEE_PAYMENT,
)


class Zarinpal:
    #  VALIDATE FROM .ENV FILE
    _PAYMENT_CALCULATE_FEE_URL = (
        "https://payment.zarinpal.com/pg/v4/payment/feeCalculation.json"
    )
    _CALLBACK_URL = ZARINPAL_CALLBACK_URL
    _SITE_FEE_PAYMENT = SITE_FEE_PAYMENT
    _IS_TOMAN = ZARINPAL_IS_TOMAN

    # VALIDATE FROM CHILD CLASS
    _MERCHANT_ID = None
    _PAYMENT_REQUEST_URL = None
    _PAYMENT_VERIFY_URL = None
    _PAYMENT_GATEWAY_URL = None
    free_site_fee = False

    # ###### RESPONSE VARIABLES
    status = False
    errors = None
    msg = None
    total_amount = 0
    fee = 0
    gateway_url = None
    authority = None

    def calculate_gateway_fee(self, amount):
        payload = {"merchant_id": self._MERCHANT_ID, "amount": amount}
        payload["currency"] = "IRT" if self._IS_TOMAN else "IRR"
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            self._PAYMENT_CALCULATE_FEE_URL, headers=headers, json=payload
        )
        result = response.json()

        if errors := result.get("errors"):
            print_debug(errors)
            self.errors = errors
            self.total_amount = amount
            return amount
        else:
            suggested_amount = result.get("data").get("suggested_amount")
            if self._IS_TOMAN:
                suggested_amount = suggested_amount // 10
            self.total_amount = suggested_amount
            return suggested_amount

    def _add_site_fee(self, amount):
        if self.free_site_fee:
            return amount
        return int(amount) + int(self._SITE_FEE_PAYMENT)

    def payment_request(self, amount: int, description="پرداخت سفارش", order_pk=None):
        amount = self._add_site_fee(amount)
        amount = self.calculate_gateway_fee(amount)
        payload = {
            "merchant_id": self._MERCHANT_ID,
            "amount": amount,
            "callback_url": self._CALLBACK_URL + f"?order={order_pk}",
            "description": f"{description} {order_pk}",
        }
        payload["currency"] = "IRT" if self._IS_TOMAN else "IRR"

        headers = {"Content-Type": "application/json"}
        response = requests.post(
            self._PAYMENT_REQUEST_URL, headers=headers, json=payload
        )
        result = response.json()
        """
        {'data': {}, 'errors': {'code': -9, 'message': 'The amount must not be greater than 2000000000.', 'validations': []}}
        {'data': {'authority': 'S000000000000000000000000000000qe6lq', 'code': 100, 'fee': 123000, 'fee_type': 'Merchant', 'message': 'Success'}, 'errors': []}
        """
        if errors := result.get("errors"):
            print(errors)
            self.errors = errors
        else:
            data = result.get("data")
            self.status = True
            self.authority = data.get("authority")
            self.fee = data.get("fee")
        return result

    def generate_payment_gateway(
        self, amount, description="پرداخت سفارش", order_pk=None
    ):
        response = self.payment_request(
            amount, description=description, order_pk=order_pk
        )
        if response:
            data = response.get("data", {})
            _errors = None
            if data.get("authority"):
                _payment_gateway = (
                    f"{self._PAYMENT_GATEWAY_URL}/{data.get('authority')}"
                )
                self.gateway_url = _payment_gateway
                _subject = green_text("Payment Gateway Created:")
                print_debug(
                    f"\n{_subject}\nurl: {_payment_gateway}\nfee (* Rial *):{data.get('fee')}",
                    "ZarinpalPayment -> generate_payment_gateway :",
                )
                return True, _payment_gateway, _errors
            else:
                try:
                    data_json = str_to_json(response.text)
                    _errors = data_json.get("errors")
                    _subject = red_text("Payment Gateway Error:")
                    print_debug(
                        f"\n{_subject}\n{_errors}",
                        "ZarinpalPayment -> generate_payment_gateway :",
                    )
                except Exception as e:
                    _subject = red_text("Payment Gateway Error:")
                    print_debug(
                        f"\n{e}",
                        "ZarinpalPayment -> generate_payment_gateway :",
                    )
                return False, None, _errors
        else:
            return False, None, "Something went wrong"

    def payment_verify(self, request, amount):
        status = request.GET.get("Status") or request.POST.get("Status")
        if status == "OK":
            authority = request.GET.get("Authority") or request.POST.get("Authority")
            payload = {
                "merchant_id": self._MERCHANT_ID,
                "amount": amount,
                "authority": authority,
            }
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                self._PAYMENT_VERIFY_URL, headers=headers, json=payload
            )
            data = response.json().get("data", {})

            if data.get("code") in [100, 101]:
                tracking_code = data.get("ref_id")
                _code = data.get("code")
                _msg = "پرداخت با موفقیت انجام شد"
                self.msg = _msg
                _subject = green_text("Verify Payment Success:")
                print_debug(
                    f"\n{_subject}\n{_msg}", "ZarinpalPayment -> payment_verify :"
                )
                return True, tracking_code, _code, None, _msg
            else:
                x = str_to_json(response.text)
                _errors = x.get("errors")
                _code = data.get("code")
                _msg = f"پرداخت ناموفق بود. کد خطا: {data.get('code')}"
                self.msg = _msg
                _subject = red_text("Verify Payment Error:")
                print_debug(
                    f"\n{_subject}\n{_msg}", "ZarinpalPayment -> payment_verify :"
                )
                return False, None, _code, _errors, _msg
        else:
            _msg = "پرداخت توسط کاربر لغو شد"
            self.msg = _msg
            _subject = red_text("Verify Payment Error:")
            print_debug(f"\n{_subject}\n{_msg}", "ZarinpalPayment -> payment_verify :")
            return False, None, -1, None, _msg

    class Meta:
        abstract = True


class ZarinpalSandboxPayment(Zarinpal):
    _MERCHANT_ID = "Sd35a22a-0015-433b-887c-d5ff344d58a2"
    _PAYMENT_REQUEST_URL = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    _PAYMENT_VERIFY_URL = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    _PAYMENT_GATEWAY_URL = "https://sandbox.zarinpal.com/pg/StartPay"
    _CALLBACK_URL = "http://127.0.0.1:8000/payment/check/"

    def calculate_gateway_fee(self, amount):
        return amount


class ZarinpalPayment(Zarinpal):
    _MERCHANT_ID = "c2461613-dd2b-416b-b4dc-a88b240703ee"
    _PAYMENT_REQUEST_URL = "https://payment.zarinpal.com/pg/v4/payment/request.json"
    _PAYMENT_VERIFY_URL = "https://payment.zarinpal.com/pg/v4/payment/verify.json"
    _PAYMENT_GATEWAY_URL = "https://www.zarinpal.com/pg/StartPay"
    _CALLBACK_URL = "http://127.0.0.1:8000/payment/check/"
