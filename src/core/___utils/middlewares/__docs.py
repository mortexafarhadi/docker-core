class MySimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # اینجا فقط یکبار اجرا میشه (در زمان لود سرور)

    def __call__(self, request):
        # قبل از اجرا شدن view
        print("Before view")

        response = self.get_response(request)

        # بعد از اجرا شدن view و قبل از ارسال response
        print("After view")

        return response
