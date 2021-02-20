
from django.contrib.auth import get_user_model
from .models import *
from django.db.models import Q,F
import logging
from datetime import timedelta,datetime
from celery import Celery
logger = logging.getLogger(__name__)
User = get_user_model()
app = Celery('etm')
import os
from django.conf import settings
FileLocation = os.path.join(settings.BASE_DIR, 'Weekily reports')

from celery.schedules import crontab
from celery.decorators import periodic_task


import pandas as pd


@app.task
def create_report():
    df = pd.DataFrame(list(Tasks.objects.filter(createdtme__gte = datetime.now()-timedelta(weeks = 1)).annotate(assign_id =F('taskassign__assigned_to_id'),assign_name =F('taskassign__assigned_to__first_name')).values('id','name','assign_id','assign_name','createdby_id','createdby__first_name','createdtme','last_updated','start_time','end_time','note','status')))
    df['createdtme'] = df['createdtme'].dt.tz_localize(None)
    df['start_time'] = df['start_time'].dt.tz_localize(None)
    df['end_time'] = df['end_time'].dt.tz_localize(None)
    df['last_updated'] = df['last_updated'].dt.tz_localize(None)
    filename = datetime.now().strftime("%Y:%m:%d")+str("-")+(datetime.now()-timedelta(weeks = 1)).strftime("%Y:%m:%d")+".xlsx"
    path = os.path.join(FileLocation,filename)
    df.to_excel(path,index = False , header = True)
    logger.info(df)

