from decouple import config

# Return the API for the session
API_KEY = config("API_KEY")

# PSQL KEY
PSQL_KEY = config("PSQL_KEY")

# My telegram id
MY_ID = config("TELEGRAM_ID")


def strip_all(s):
    """ Strip the string """

    strips = [' ', ',', 'שח', '$', '₪', '.', '"']
    for _ in strips:
        s = s.strip(_)

    return s
