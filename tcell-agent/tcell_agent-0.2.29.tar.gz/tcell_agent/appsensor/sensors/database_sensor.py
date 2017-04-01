# set is builtin in python 3 but a module in earlier version
try:
    set
except NameError:
    from sets import Set as set

from tcell_agent.appsensor.sensor import send_event


class DatabaseSensor(object):
    DP_CODE = "dbmaxrows"

    def __init__(self, policy_json=None):
        self.enabled = False
        self.max_rows = 1001
        self.excluded_route_ids = set()

        if policy_json is not None:
            self.enabled = policy_json.get("enabled", False)
            large_result = policy_json.get("large_result", {})
            self.max_rows = large_result.get("limit", self.max_rows)

            self.excluded_route_ids = set(policy_json.get("exclude_routes", []))

    def should_check(self, route_id):
        return self.enabled and route_id not in self.excluded_route_ids

    def check(self, appsensor_meta, number_of_records):
        if self.should_check(appsensor_meta.route_id) and number_of_records > self.max_rows:
            send_event(
                appsensor_meta,
                self.DP_CODE,
                None,
                {"rows": number_of_records})

    def __str__(self):
        return "<%s enabled: %s max_rows: %s dp_code: %s excluded_route_ids: %s>" % \
               (type(self).__name__, self.enabled, self.max_rows, self.DP_CODE, self.excluded_route_ids)
