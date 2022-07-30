
# Return the API for the session
with open("api_key.txt", 'r') as file:
    api_key = file.readline()
    API_KEY = api_key


def strip_all(s):
    """ Strip the string """

    strips = [' ', ',', 'שח', '$', '₪', '.', '"']
    for _ in strips:
        s = s.strip(_)

    return s
