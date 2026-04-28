# import pycountry
# import reverse_geocoder as rg
# from geopy.geocoders import Nominatim
#
#
# def get_country_code_offline_from_coordinate(coordinate=None):
#     if coordinate is None:
#         return None
#     else:
#         result = rg.search(coordinate)
#         return result[0]['cc'] if result else "Unknown"
#
#
# def get_country_name_offline_from_coordinate(coordinate=None):
#     country_code = get_country_code_offline_from_coordinate(coordinate)
#     if country_code is None or country_code == "Unknown":
#         return None
#     country = pycountry.countries.get(alpha_2=country_code)
#     return country.name if country else country_code
#
#
# def get_address_online_from_coordinate(coordinate=None):
#     if coordinate is None:
#         return None
#     else:
#         geolocator = Nominatim(user_agent="geoapiExercises")
#         location = geolocator.reverse(coordinate, exactly_one=True)
#         return location.raw.get('address', {}) if location else "Unknown"
#
#
# def get_country_code_online_from_coordinate(coordinate=None):
#     if coordinate is None:
#         return None
#     else:
#         address = get_address_online_from_coordinate(coordinate)
#         return address.get('country_code', 'Unknown').lower() if address != 'Unknown' else "Unknown"
#
#
# def get_country_name_online_from_coordinate(coordinate=None):
#     if coordinate is None:
#         return None
#     else:
#         address = get_address_online_from_coordinate(coordinate)
#         return address.get('country', 'Unknown') if address != 'Unknown' else "Unknown"
