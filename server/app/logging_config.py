import logging
import sys
import structlog

# Configure the standard logging
logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)

logging.getLogger("tortoise").setLevel(logging.DEBUG)
logging.getLogger("tortoise.engine").setLevel(logging.DEBUG)
logging.getLogger("tortoise.query").setLevel(logging.DEBUG)
logging.getLogger("tortoise.transactions").setLevel(logging.DEBUG)
logging.getLogger("tortoise.transactions").setLevel(logging.DEBUG)

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(),
    ],
)
