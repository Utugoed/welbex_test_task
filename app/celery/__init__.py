import logging
import random

from celery import Celery
from celery.schedules import crontab

from app.config import settings
from app.db import sync_engine, sync_session
from app.db.vehicles import Vehicles


celery_app = Celery('tasks', broker=settings.CELERY_BROKER_URL)


@celery_app.task
def update_vehicles_locations_task():
    logging.info("update_vehicles_locations_task: STARTED")
    
    with sync_engine.connect() as connection:
        
        logging.info("update_vehicles_locations_task: Getting vehicles data")
        with sync_session(bind=connection) as session:
            vehicles = Vehicles.sync_get_all(session=session)
        vehicles_list = list(vehicles)

        logging.info("update_vehicles_locations_task: Generating locations ids")
        locations_ids = [
            random.randint(1, settings.LOCATIONS_AMOUNT) 
            for _ in vehicles_list
        ]
        
        logging.info("update_vehicles_locations_task: Updating vehicle data")
        vehicles_ids = [vehicle.id for vehicle in vehicles_list]
        with sync_session(bind=connection) as session:
            _ = Vehicles.sync_move_vehicles(
                new_locations_ids=locations_ids, vehicles_ids=vehicles_ids, session=session
            )


celery_app.conf.beat_schedule = {
    'update_vehicles_locations_task': {
        'task': 'app.celery.update_vehicles_locations_task',
        'schedule': crontab(minute="*/3")
    }
}
