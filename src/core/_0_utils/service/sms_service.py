# from celery import shared_task
#
# from decouple import config
# from _0_utils.functions.date_and_time_function import (
#     datetime_to_jalali_date__month_day__str_month,
#     time_remove_seconds__str,
# )
# from _0_utils.functions.string_function import (
#     three_digit_separator_without_decimal,
#     red_text,
#     blue_text,
#     green_text,
# )
# from django.conf import settings
# from sms_ir import SmsIr
#
# USE_SMS_SERVICE = config("USE_SMS_SERVICE", default=False, cast=bool)
#
#
# def send_sms_code_signup_login(phone, code):
#     """send to user"""
#     if not phone or phone is None:
#         print(f"Error in -> send_sms_code_signup_login : Phone is None")
#         return False, "Phone is None", "Phone is None"
#
#     if not USE_SMS_SERVICE:
#         msg = f"USE_SMS_SERVICE Key in .env Config Not Set. code is : {code}"
#         print(msg)
#         return True, msg, "SMS Service is not available"
#     else:
#         TEMPLATE_ID = "961350"
#         parameters = [
#             {
#                 "name": "code",
#                 "value": code,
#             },
#         ]
#         _send_sms.delay(
#             phone=phone,
#             template_id=TEMPLATE_ID,
#             params=parameters,
#             function_name="send_sms_code_signup_login",
#         )
#         return True, "Sent SMS Successfully", None
#
#
# def send_advertising_SMS(phone, template_id_, parameters_):
#     """send to user"""
#     if not phone or phone is None:
#         print(f"Error in -> send_advertising_SMS : Phone is None")
#         return False, "Phone is None", "Phone is None"
#
#     if not USE_SMS_SERVICE:
#         msg = f"USE_SMS_SERVICE Key in .env Config Not Set"
#         print(msg)
#         return True, msg, "SMS Service is not available"
#     else:
#         _send_sms.delay(
#             phone=phone,
#             template_id=template_id_,
#             params=parameters_,
#             function_name="send_advertising_SMS",
#         )
#         return True, "Sent SMS Successfully", None
#
#
# def send_sms_notif_to_pay(phone, _date, _time):
#     """send to customer"""
#     if not phone or phone is None:
#         print(f"Error in -> send_sms_notif_to_pay : Phone is None")
#         return False, "Phone is None", "Phone is None"
#
#     if not USE_SMS_SERVICE:
#         msg = (
#             f"USE_SMS_SERVICE Key in .env Config Not Set. date: {_date}, time: {_time}"
#         )
#         print(msg)
#         return True, msg, "SMS Service is not available"
#     else:
#         TEMPLATE_ID = "534412"
#         _date = datetime_to_jalali_date__month_day__str_month(_date)
#         _time = time_remove_seconds__str(_time)
#         parameters = [
#             {
#                 "name": "date",
#                 "value": _date,
#             },
#             {
#                 "name": "time",
#                 "value": _time,
#             },
#         ]
#         _send_sms.delay(
#             phone=phone,
#             template_id=TEMPLATE_ID,
#             params=parameters,
#             function_name="send_sms_notif_to_pay",
#         )
#         return True, "Sent SMS Successfully", None
#
#
# def send_sms_new_request(phone, _date, _time):
#     """send to barber"""
#     if not phone or phone is None:
#         print(f"Error in -> send_sms_new_request : Phone is None")
#         return False, "Phone is None", "Phone is None"
#
#     if not USE_SMS_SERVICE:
#         msg = (
#             f"USE_SMS_SERVICE Key in .env Config Not Set. date: {_date}, time: {_time}"
#         )
#         print(msg)
#         return True, msg, "SMS Service is not available"
#     else:
#         TEMPLATE_ID = "463443"
#         _date = datetime_to_jalali_date__month_day__str_month(_date)
#         _time = time_remove_seconds__str(_time)
#         parameters = [
#             {
#                 "name": "date",
#                 "value": _date,
#             },
#             {
#                 "name": "time",
#                 "value": _time,
#             },
#         ]
#         _send_sms.delay(
#             phone=phone,
#             template_id=TEMPLATE_ID,
#             params=parameters,
#             function_name="send_sms_new_request",
#         )
#         return True, "Sent SMS Successfully", None
#
#
# def send_sms_final_accept_order(phone, _date, _time):
#     """send to customer"""
#     if not phone or phone is None:
#         print(f"Error in -> send_sms_final_accept_order : Phone is None")
#         return False, "Phone is None", "Phone is None"
#
#     if not USE_SMS_SERVICE:
#         msg = (
#             f"USE_SMS_SERVICE Key in .env Config Not Set. date: {_date}, time: {_time}"
#         )
#         print(msg)
#         return True, msg, "SMS Service is not available"
#     else:
#         TEMPLATE_ID = "792930"
#         _date = datetime_to_jalali_date__month_day__str_month(_date)
#         _time = time_remove_seconds__str(_time)
#         parameters = [
#             {
#                 "name": "date",
#                 "value": _date,
#             },
#             {
#                 "name": "time",
#                 "value": _time,
#             },
#         ]
#         _send_sms.delay(
#             phone=phone,
#             template_id=TEMPLATE_ID,
#             params=parameters,
#             function_name="send_sms_final_accept_order",
#         )
#         return True, "Sent SMS Successfully", None
#
#
# def send_reject_sms_to_order_customers(order_list):
#     _count = 0
#     for order in order_list:
#         _status, msg, error = send_sms_reject_order(
#             order.customer.phone, order.date, order.time
#         )
#         if _status:
#             _count += 1
#         else:
#             print(error)
#     print(green_text(f"Rejected Successful {_count} sms orders"))
#     return order_list.count(), _count
#
#
# def send_sms_reject_order(phone, _date, _time):
#     """send to customer"""
#     if not phone or phone is None:
#         print(f"Error in -> send_sms_reject_order : Phone is None")
#         return False, "Phone is None", "Phone is None"
#
#     if not USE_SMS_SERVICE:
#         msg = (
#             f"USE_SMS_SERVICE Key in .env Config Not Set. date: {_date}, time: {_time}"
#         )
#         print(msg)
#         return True, msg, "SMS Service is not available"
#     else:
#         TEMPLATE_ID = "544802"
#         _date = datetime_to_jalali_date__month_day__str_month(_date)
#         _time = time_remove_seconds__str(_time)
#         parameters = [
#             {
#                 "name": "date",
#                 "value": _date,
#             },
#             {
#                 "name": "time",
#                 "value": _time,
#             },
#         ]
#         _send_sms.delay(
#             phone=phone,
#             template_id=TEMPLATE_ID,
#             params=parameters,
#             function_name="send_sms_reject_order",
#         )
#         return True, "Sent SMS Successfully", None
#
#
# def send_sms_cancel_order(phone, _date, _time):
#     """send to customer"""
#     if not phone or phone is None:
#         print(f"Error in -> send_sms_cancel_order : Phone is None")
#         return False, "Phone is None", "Phone is None"
#
#     if not USE_SMS_SERVICE:
#         msg = (
#             f"USE_SMS_SERVICE Key in .env Config Not Set. date: {_date}, time: {_time}"
#         )
#         print(msg)
#         return True, msg, "SMS Service is not available"
#     else:
#         TEMPLATE_ID = "613378"
#         _date = datetime_to_jalali_date__month_day__str_month(_date)
#         _time = time_remove_seconds__str(_time)
#         parameters = [
#             {
#                 "name": "date",
#                 "value": _date,
#             },
#             {
#                 "name": "time",
#                 "value": _time,
#             },
#         ]
#         _send_sms.delay(
#             phone=phone,
#             template_id=TEMPLATE_ID,
#             params=parameters,
#             function_name="send_sms_cancel_order",
#         )
#         return True, "Sent SMS Successfully", None
#
#
# def send_sms_change_final_amount_order(phone, _date, _time, _amount):
#     """send to customer"""
#     if not phone or phone is None:
#         print(f"Error in -> send_sms_change_final_amount_order : Phone is None")
#         return False, "Phone is None", "Phone is None"
#
#     if not USE_SMS_SERVICE:
#         msg = f"USE_SMS_SERVICE Key in .env Config Not Set. date: {_date}, time: {_time}, amount: {_amount}"
#         print(msg)
#         return True, msg, "SMS Service is not available"
#     else:
#         TEMPLATE_ID = "807014"
#         _date = datetime_to_jalali_date__month_day__str_month(_date)
#         _time = time_remove_seconds__str(_time)
#         _amount = three_digit_separator_without_decimal(_amount)
#         parameters = [
#             {
#                 "name": "date",
#                 "value": _date,
#             },
#             {
#                 "name": "time",
#                 "value": _time,
#             },
#             {
#                 "name": "amount",
#                 "value": _amount,
#             },
#         ]
#         _send_sms.delay(
#             phone=phone,
#             template_id=TEMPLATE_ID,
#             params=parameters,
#             function_name="send_sms_change_final_amount_order",
#         )
#         return True, "Sent SMS Successfully", None
#
#
# def send_sms_reminder_customer_order(phone, _time):
#     """send to customer"""
#     if not phone or phone is None:
#         print(f"Error in -> send_sms_reminder_customer_order : Phone is None")
#         return False, "Phone is None", "Phone is None"
#
#     if not USE_SMS_SERVICE:
#         msg = f"USE_SMS_SERVICE Key in .env Config Not Set. time: {_time}"
#         print(msg)
#         return True, msg, "SMS Service is not available"
#     else:
#         TEMPLATE_ID = "440701"
#         _time = time_remove_seconds__str(_time)
#         parameters = [
#             {
#                 "name": "time",
#                 "value": _time,
#             },
#         ]
#         _send_sms.delay(
#             phone=phone,
#             template_id=TEMPLATE_ID,
#             params=parameters,
#             function_name="send_sms_reminder_customer_order",
#         )
#         return True, "Sent SMS Successfully", None
#
#
# def send_sms_reminder_barber_order(phone, _time):
#     """send to barber"""
#     if not phone or phone is None:
#         print(f"Error in -> send_sms_reminder_barber_order : Phone is None")
#         return False, "Phone is None", "Phone is None"
#
#     if not USE_SMS_SERVICE:
#         msg = f"USE_SMS_SERVICE Key in .env Config Not Set. time: {_time}"
#         print(msg)
#         return True, msg, "SMS Service is not available"
#     else:
#         TEMPLATE_ID = "203677"
#         _time = time_remove_seconds__str(_time)
#         parameters = [
#             {
#                 "name": "time",
#                 "value": _time,
#             },
#         ]
#         _send_sms.delay(
#             phone=phone,
#             template_id=TEMPLATE_ID,
#             params=parameters,
#             function_name="send_sms_reminder_barber_order",
#         )
#         return True, "Sent SMS Successfully", None
#
#
# def send_sms_complete_order(phone, _order_code):
#     """send to customer"""
#     if not phone or phone is None:
#         print(f"Error in -> send_sms_complete_order : Phone is None")
#         return False, "Phone is None", "Phone is None"
#
#     if not USE_SMS_SERVICE:
#         msg = f"USE_SMS_SERVICE Key in .env Config Not Set. order_code: {_order_code}"
#         print(msg)
#         return True, msg, "SMS Service is not available"
#     else:
#         TEMPLATE_ID = "194790"
#         parameters = [
#             {
#                 "name": "order_code",
#                 "value": _order_code,
#             },
#         ]
#         _send_sms.delay(
#             phone=phone,
#             template_id=TEMPLATE_ID,
#             params=parameters,
#             function_name="send_sms_complete_order",
#         )
#         return True, "Sent SMS Successfully", None
#
#
# @shared_task()
# def _send_sms(phone, template_id, params, function_name=None):
#     try:
#         sms_ir = SmsIr(settings.SMS_SERVICE_KEY)
#         response = sms_ir.send_verify_code(
#             number=f"+98{phone}",
#             template_id=template_id,
#             parameters=params,
#         )
#         if response.status_code == 200:
#             print(f"Sent SMS Successfully to: {phone}")
#         else:
#             print(blue_text("*" * 50))
#             print(red_text(response.__dict__))
#             print(blue_text("*" * 50))
#     except Exception as e:
#         print(blue_text("*" * 50))
#         print(red_text(e))
#         print(blue_text("*" * 50))
