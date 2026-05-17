from urllib.parse import urlparse, parse_qs


class RequestParamsMiddleware:
    """
    Middleware to parse URL query parameters and attach them to the request object.
    Uses standard Python library for robust query string parsing.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Get the full path and parse the URL
        full_path = request.get_full_path()
        parsed_url = urlparse(full_path)

        # 2. Parse the query string into a dictionary
        # parse_qs returns a dictionary where values are lists (for multiple values of the same key)
        query_params = parse_qs(parsed_url.query)

        # 3. Initialize the parameters dictionary
        params_dic = {"has_params": bool(parsed_url.query)}

        # 4. Process the parsed parameters
        for key, values in query_params.items():
            # For simplicity and common use cases, we take the *last* value if multiple exist.
            # You might need to adjust this logic based on how you want to handle multiple values.
            value = values[-1] if values else None

            if value is not None:
                # Apply your specific logic for "on"/'de-active'
                if value == "on":
                    params_dic[key] = True
                elif value == "off":
                    params_dic[key] = False
                else:
                    # Original code only added the parameter if the *value* was non-empty.
                    # parse_qs handles empty values differently, but we keep the assignment if value is present.
                    params_dic[key] = value

        # 5. Attach the processed parameters to the request
        request.params = params_dic

        # 6. Continue the request chain
        response = self.get_response(request)
        return response
