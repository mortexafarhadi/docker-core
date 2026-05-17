from _0_utils.models.ip_address_model import IPAddress


class IPAddressMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        ip_address = IPAddress.objects.filter(ip_address=ip).first()
        if ip_address is None:
            ip_address = IPAddress(ip_address=ip)
            ip_address.save()
        request.ip_address = ip_address
        response = self.get_response(request)

        return response
