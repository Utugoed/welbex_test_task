import logging

from fastapi import FastAPI

from app.api import api_router
from app.db import init_models
from app.helpers.load_data import load_default_vehicles, load_locations


log_conf = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(process)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": "DEBUG",
        }
    },
    "root": {"handlers": ["console"], "level": "DEBUG"},
    "loggers": {
        "gunicorn": {"propagate": True},
        "uvicorn": {"propagate": True},
        "uvicorn.access": {"propagate": True},
        "events": {"propagate": True},
    },
}
logging.config.dictConfig(log_conf)

app = FastAPI()

app.add_event_handler("startup", init_models)
app.add_event_handler("startup", load_locations)
app.add_event_handler("startup", load_default_vehicles)

app.include_router(api_router, prefix="/api")
