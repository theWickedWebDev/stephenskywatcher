import datetime


# ~~~~~~~ LOCATIONS ~~~~~~~ #
LAKESHORE_HORSESHOE_BAY = {
    "lat": 30.56235,
    "lon": -98.43058,
    "eclipse_starts": datetime.datetime(2024, 4, 8, 12, 16, 45),
    "totality_starts": datetime.datetime(2024, 4, 8, 13, 34, 12),
    "totality_ends": datetime.datetime(2024, 4, 8, 13, 38, 33),
    "eclipse_ends": datetime.datetime(2024, 4, 8, 14, 57, 24),
}


# ~~~~~~~ PRODUCTION ~~~~~~~ #
LOCATION = LAKESHORE_HORSESHOE_BAY
prod_times = {
    "C1":           LOCATION.get('eclipse_starts'),
    "C2":           LOCATION.get('totality_starts'),
    "C3":           LOCATION.get('totality_ends'),
    "C4":           LOCATION.get('eclipse_ends')
}

# ~~~~~~~ DEVELOPMENT ~~~~~~~ #
dev_times = {}
t_padding = 63
now = datetime.datetime.now()
t = t_padding

dev_times.update({"C1": now + datetime.timedelta(0, t)})

t += t_padding
dev_times.update({"C2": now + datetime.timedelta(0, t)})

t += t_padding
dev_times.update({"C3": now + datetime.timedelta(0, t)})

t += t_padding
dev_times.update({"C4": now + datetime.timedelta(0, t)})


def get_times(mode="development"):
    return dev_times if mode == 'development' else prod_times
