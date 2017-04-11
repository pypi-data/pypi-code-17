import arrow
from collections import defaultdict


def generate(start_date: str, end_date: str, timeseries: tuple = ("hour", "day", "month")) -> dict:
    """Generate timeseries."""
    try:
        start = arrow.get(start_date, "YYYY-MM-DD HH:mm:ss")
        end = arrow.get(end_date, "YYYY-MM-DD HH:mm:ss")
    except Exception as e:
        raise(e)

    res = {
        "hour": defaultdict(list),
        "day": defaultdict(list),
        "month": []
    }

    # Helpers.
    start = start.replace(minute=0, second=0, microsecond=0)
    end = end.replace(minute=59, second=59, microsecond=999999)
    non_full_months = []
    non_full_days = []

    # Add full months.
    month_range = arrow.Arrow.span_range("month", start, end)

    if "month" in timeseries:
        for month in month_range:
            start_day = month[0]
            end_day = month[1]

            if start_day < start:
                if end_day > end:
                    non_full_months.append([start, end])
                else:
                    non_full_months.append([start, end_day])
                continue

            if end_day > end:
                non_full_months.append([start_day, end])
                continue

            res["month"].append(_convert("month", start_day))
    else:
        non_full_months.append([start, end])

    # Add full days.
    if "day" in timeseries and non_full_months:
        for non_full_month in non_full_months:
            start_day_month = non_full_month[0]
            end_day_month = non_full_month[1]

            day_range = arrow.Arrow.span_range("day", start_day_month, end_day_month)

            for day in day_range:
                start_day = day[0]
                end_day = day[1]
                month = _convert("month", start_day)

                if start_day < start_day_month:
                    non_full_days.append([start_day_month, end_day])
                    continue

                if end_day > end_day_month:
                    non_full_days.append([start_day, end_day_month])
                    continue

                res["day"][month].append(_convert("day", start_day))
    elif len(month_range) != len(res["month"]):
        non_full_days.append([start, end])

    # Add full hours.
    if "hour" in timeseries and non_full_days:
        for non_full_day in non_full_days:
            start_day_hour = non_full_day[0]
            end_day_hour = non_full_day[1]

            hour_range = arrow.Arrow.span_range("hour", start_day_hour, end_day_hour)

            for hour in hour_range:
                month = _convert("month", start_day_hour)
                res["hour"][month].append(_convert("hour", hour[0]))

    # Convert final result to normal dictionaries.
    final_res = {
        "hour": dict(res["hour"]),
        "day": dict(res["day"]),
        "month": res["month"]
    }

    return final_res


def _convert(type: str, date: str) -> int:
    """Convert dates to int representations."""
    res = None
    if type == "month":
        res = int(date.format("YYYYMM"))
    elif type == "day":
        res = int(date.format("YYYYMMDD"))
    elif type == "hour":
        res = int(date.format("YYYYMMDDHH"))
    return res
