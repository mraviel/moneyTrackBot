
# Return the API for the session
API_KEY = open('api_key.txt', 'r').readline()

# PSQL KEY
PSQL_KEY = open('psql_key.txt', 'r').readline().strip('\n')


def strip_all(s):
    """ Strip the string """

    strips = [' ', ',', 'שח', '$', '₪', '.', '"']
    for _ in strips:
        s = s.strip(_)

    return s
