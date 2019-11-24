"""Filters for app."""

import dateutil.parser
import babel


def format_datetime(value, date_format='medium'):
    date = dateutil.parser.parse(value)
    if date_format == 'full':
        date_format = "EEEE MMMM, d, y 'at' h:mma"
    elif date_format == 'medium':
        date_format = "EE MM, dd, y h:mma"

    return babel.dates.format_datetime(date, date_format)
