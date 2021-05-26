from record_screen_rs.celery import app
from celery.utils.log import get_task_logger
from grabaciones.models import Grabaciones
from django.conf import settings
import time
from grabaciones.logtasks import GrabAditLog
import requests
import json

logger = get_task_logger(__name__)

retries = 3
max_retries = 5


@app.task(name='record_init')
def record_init(date=None, grabacionesId=None, success=False, retries=3, max_retries=3):
    logger.info("Record Task init")
    lograb = GrabAditLog(task_name='record_init')
    if grabacionesId is not None:
        grabacion = Grabaciones.objects.get(name=grabacionesId)
        if grabacion is not None:
            namesession = grabacion.name
            datasession = {
                "outputMode": "COMPOSED",
                "hasAudio": True,
                "hasVideo": True,
                "session": "{}".format(namesession),
                "name": "{}".format(namesession)
            }
            headers = {'Content-Type': 'application/json'}
            lograb.update(task_by='record_init', value=namesession, status='SENDING')
            while not success:
                try:
                    url_api = settings.SECRETS['URL_APP'] + '/api/recordings/start'
                    response = requests.post(url_api, headers=headers,
                                             auth=(settings.SECRETS['URL_USER'], settings.SECRETS['URL_PASS']),
                                             data=json.dumps(datasession))
                    if response.status_code == 200:
                        success = True
                        lograb.update(task_by='record_init', value=namesession, status='RUNNING')
                        graba = Grabaciones.objects.update_or_create(grabacionesId=namesession, status="ready",
                                                                     defaults={'status': 'recording',
                                                                               'size': 0})
                    elif max_retries <= 5:
                        wait = retries + 1
                        logger.info("Retry task {} in wait {}".format(namesession, wait))
                        time.sleep(wait)
                        max_retries += 1
                    else:
                        lograb.update(task_by='record_init', value=namesession, status='ERROR')
                        raise RuntimeError('Error en cantidad de retries: ' + str(max_retries))
                        return False
                except Exception as e:
                    raise RuntimeError('Error en cantidad de retries: ' + str(e))
                    return False
            return True
        else:
            return False
    return False


@app.task(name='stop_init')
def stop_init(date=None, grabacionesId=None, success=False, retries=3, max_retries=3):
    logger.info("Record task stop")
    lograb = GrabAditLog(task_name='stop_init')
    if grabacionesId is not None:
        grabacion = Grabaciones.objects.get(name=grabacionesId)
        if grabacion is not None:
            namesession = grabacion.name
            headers = {'Content-Type': 'application/json'}
            lograb.update(task_by='stop_init', value=namesession, status='STOP')
            while not success:
                try:
                    url_api = settings.SECRETS['URL_APP'] + '/api/recordings/stop/' + namesession
                    response = requests.post(url_api, headers=headers,
                                             auth=(settings.SECRETS['URL_USER'], settings.SECRETS['URL_PASS']))
                    if response.status_code == 200:
                        content = json.loads(response.content)
                        success = True
                        lograb.update(task_by='stop_init', value=namesession, status='STOP')
                        graba = Grabaciones.objects.update_or_create(grabacionesId=grabacion.grabacionesId,
                                                                     defaults={'status': 'record',
                                                                               'size': content['size'],
                                                                               'duration': content['duration'],
                                                                               'url': content['url'].replace(':4443', ''),
                                                                               'hasAudio': content['hasAudio'],
                                                                               'hasVideo': content['hasVideo']})
                        url_stop = settings.SECRETS['URL_APP'] + '/api/sessions/' + namesession
                        stopsesion = requests.delete(url_stop, headers=headers,
                                                     auth=(settings.SECRETS['URL_USER'], settings.SECRETS['URL_PASS']))
                    elif max_retries <= 5:
                        wait = retries + 1
                        logger.info("Retry task {} in wait {}".format(namesession, wait))
                        time.sleep(wait)
                        max_retries += 1
                    else:
                        lograb.update(task_by='stop_init', value=namesession, status='ERROR')
                        raise RuntimeError('Error en cantidad stop de retries: ' + str(max_retries))
                        return False
                except Exception as e:
                    raise RuntimeError('Error en cantidad stop de retries: ' + str(e))
                    return False
            return True
        else:
            return False
    return False

