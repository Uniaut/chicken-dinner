"""Telemetry objects."""
import json

from chicken_dinner.util import camel_to_snake
from chicken_dinner.util import remove_from_dict


class TelemetryObject(object):
    """Telemetry object model.

    Generic object for telemetry event objects.

    Provides an object-attribute based model for telemetry objects, creating
    embedded telemetry objects recursively. Converts all event and object keys
    to snake-cased key names.

    :param data: the JSON object data associated with the telemetry object
    """

    def __init__(self, data, reference):
        #: The key name that references this object
        self.reference = camel_to_snake(reference)
        for k, v in data.items():
            if isinstance(v, dict):
                setattr(self, camel_to_snake(k), TelemetryObject(v, k))
            elif isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
                setattr(self, camel_to_snake(k), [TelemetryObject(e, k) for e in v])
            else:
                setattr(self, camel_to_snake(k), v)

    def __getitem__(self, key):
        return getattr(self, camel_to_snake(key))

    def __str__(self):
        return "TelemetryObject " + self.reference + " object"

    def __repr__(self):
        return "TelemetryObject({d}, {r})".format(d=self.dumps(), r=self.reference)

    def dumps(self):
        """Serialize the event object to a JSON string."""
        return json.dumps(
            self,
            default=lambda x: remove_from_dict(x.__dict__, ["reference"]),
            sort_keys=True,
            indent=4
        )

    def to_dict(self):
        """Get the event object as a dict."""
        return json.loads(self.dumps())
