# from packaging.version import parse
#
#
# def check_version(current, last): return parse(last) > parse(current)
#
#
# def latest_version(product_list):
#     if product_list.count() == 0:
#         return None
#     elif product_list.count() == 1:
#         return product_list[0]
#     else:
#         _latest_version = product_list[0]
#         for product in product_list:
#             if check_version(_latest_version.version, product.version):
#                 _latest_version = product
#         return _latest_version
