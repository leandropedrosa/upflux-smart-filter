import logging
import json
import os
import google.cloud.logging
from google.cloud.logging_v2.handlers import CloudLoggingHandler


class LOGGER:

    def __init__(self):
        self.agciLogger = logging.getLogger("agci-logger")

        # In development MODE, use default logging
        if os.getenv("MODE") != "development":
            # Instantiates a client
            client = google.cloud.logging.Client()

            # Retrieves a Cloud Logging handler and integrates it with the Python logging module
            client.setup_logging()

            handler = CloudLoggingHandler(client)

            self.agciLogger.addHandler(handler)

    def info(self, message: str, extra: dict, **others):
        self.agciLogger.info(f"{message} - {json.dumps(extra)}", extra=extra, **others)

    def error(self, message: str, extra: dict, **others):
        dump = None

        try:
            dump = json.dumps(extra)
        except:
            dump = json.dumps(extra.__dict__)

        self.agciLogger.error(f"{message} - {dump}", extra=extra, **others)


logger = LOGGER()
