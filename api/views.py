from rest_framework import status,filters
from django.contrib.auth import get_user_model
from django.db.models import Q,F

from .serializers import *
from .models import *

from rest_framework.decorators import api_view,permission_classes,renderer_classes
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import uuid
import datetime
import os
User = get_user_model()


import logging
logger = logging.getLogger(__name__)

from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

def add_notification(note,ntype,obj_id,nto):
    nottification_objs = Notification.objects.create(note = note,notification_type = ntype, object_id = obj_id,notifi_to = nto)
    return


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_admin(request):
    if request.method == 'POST':
        if request.user.user_type == 'AD' or request.user.is_superuser:
            if request.data.get('username',None):
                if request.data.get('password',None) and request.data.get('password1') and request.data.get('password') == request.data.get('password1'):
                    if not User.objects.filter(username = request.data['username']).exists():
                        user = User( user_type = 'AD',username = request.data['username'])
                        user.set_password(request.data['password'])
                        if request.data.get('first_name',None):
                            user.first_name = request.data['first_name']
                        if request.data.get('last_name',None):
                            user.last_name = request.data['last_name']
                        if request.data.get('email',None):
                            user.email = request.data['email']
                        user.save()
                    else:
                        return Response('Username already exists',status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("Check your password" , status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Provide a username" , status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied" , status = status.HTTP_400_BAD_REQUEST)
    return Response("all set",status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_empl(request):
    if request.method == 'POST':
        if request.user.user_type == 'AD' or request.user.is_superuser:
            if request.data.get('username',None):
                if request.data.get('password',None) and request.data.get('password1') and request.data.get('password') == request.data.get('password1'):
                    if not User.objects.filter(username = request.data['username']).exists():
                        user = User( user_type = 'EM',username = request.data['username'])
                        user.set_password(request.data['password'])
                        if request.data.get('first_name',None):
                            user.first_name = request.data['first_name']
                        if request.data.get('last_name',None):
                            user.last_name = request.data['last_name']
                        if request.data.get('email',None):
                            user.email = request.data['email']
                        user.save()
                    else:
                        return Response('Username already exists',status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("Check your password" , status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Provide a username" , status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied" , status = status.HTTP_400_BAD_REQUEST)
    return Response("all set",status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_manager(request):
    if request.method == 'POST':
        if request.user.user_type == 'AD' or request.user.is_superuser:
            if request.data.get('username',None):
                if request.data.get('password',None) and request.data.get('password1') and request.data.get('password') == request.data.get('password1'):
                    if not User.objects.filter(username = request.data['username']).exists():
                        user = User( user_type = 'MN',username = request.data['username'])
                        user.set_password(request.data['password'])
                        if request.data.get('first_name',None):
                            user.first_name = request.data['first_name']
                        if request.data.get('last_name',None):
                            user.last_name = request.data['last_name']
                        if request.data.get('email',None):
                            user.email = request.data['email']
                        user.save()
                    else:
                        return Response('Username already exists',status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("Check your password" , status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Provide a username" , status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied" , status = status.HTTP_400_BAD_REQUEST)
    return Response("all set",status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    if request.method == 'POST':
        if request.data.get("name",None):
            start_time = None
            end_time = None
            note = None
            if request.data.get("note",None):
                note = request.data["note"]
            if request.data.get("start_time",None):
                start_time = datetime.datetime.strptime(request.data["start_time"], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo = None)
            if  request.data.get("end_time",None):
                end_time = datetime.datetime.strptime(request.data["end_time"], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo = None)
                if start_time:
                    if end_time < start_time:
                        return Response('Check start time and end time',status = status.HTTP_400_BAD_REQUEST)
            task_obj = Tasks.objects.create(name =request.data["name"], createdby = request.user,start_time =start_time, end_time = end_time,note = note,createdtme = datetime.datetime.now())
            if request.data.get("assigne_list",None):
                user_list = User.objects.filter(id__in = request.data["assigne_list"])
                task_assign_objs = [TaskAssign(task = task_obj,assigned_to=user) for user in user_list]
                task_create = TaskAssign.objects.bulk_create(task_assign_objs)
                add_notification("A task  was created",1,task_obj.id,'SA')
            return Response('Task created', status = status.HTTP_200_OK)
        else:
            return Response('Must provide title',status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Methord not accepted',status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def EditTask(request):
    if request.method == 'POST':
        if request.data.get("task_id",None):
            if Tasks.objects.filter(id = request.data["task_id"] , createdby = request.user).exists():
                flag = False
                msg = "Nothing was updated"
                task_obj = task.objects.filter(id = request.data["task_id"] , teacher = request.user)
                if request.data.get("start_time",None) or request.data.get("end_time",None):
                    if request.data.get("start_time",None) and request.data.get("end_time",None):
                        start_time = datetime.datetime.strptime(request.data["start_time"], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo = None)
                        end_time = datetime.datetime.strptime(request.data["end_time"], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo = None)
                        if end_time > start_time:
                            task_obj.start_time = start_time
                            task_obj.end_time = end_time
                            flag = True
                        else:
                            msg = "start_time  ahead of ending time"
                    elif request.data.get("start_time",None):
                        start_time = datetime.datetime.strptime(request.data["start_time"], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo = None)
                        if task_obj.end_time:
                            if task_obj.end_time.replace(tzinfo = None) > start_time:
                                task_obj.start_time = start_time
                                flag = True
                            else:
                                msg = "start_time was bigger than ending time"
                        else:
                            task_obj.start_time = start_time
                            flag = True
                    else:
                        end_time = datetime.datetime.strptime(request.data["end_time"], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo = None)
                        if task_obj.start_time:
                            if end_time > task_obj.start_time.replace(tzinfo = None):
                                task_obj.end_time = end_time
                                flag = True
                            else:
                                msg = "start_time was bigger than ending time"
                        else:
                            task_obj.end_time = end_time
                            flag = True
                if request.data.get("note",None):
                    task_obj.note = request.data["note"]
                    flag = True
                if flag:
                    task_obj.save()
                    return Response("Task updated",status = status.HTTP_200_OK)
                else:
                    return Response(msg,status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response('Invalid task id',status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Must provide task id',status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Methord not accepted',status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def DeleteTask(request):
    if request.data.get("task_id",None):
        if Tasks.objects.filter(id = request.data["task_id"] , createdby = request.user).exists():
            task_obj = Tasks.objects.filter(id = request.data["task_id"] , createdby = request.user).delete()
            return Response("task deleteed",status = status.HTTP_200_OK)
        else:
            return Response("permission denied",status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Must provide task id',status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def TaskList(request):
    queryset = Tasks.objects.all()
    filter_search = request.query_params.get('search', None)
    order_by = request.query_params.get('ordering',None)
    assign_user_id = request.query_params.get('userid',None)
    task_id = request.query_params.get('taskid',None)
    if filter_search:
        queryset = queryset.filter( Q(name__contains  = filter_search) | Q(note__contains  = filter_search))
    if task_id:
        queryset = queryset.filter(id = task_id)
    if assign_user_id:
        queryset = queryset.filter(taskassign__assigned_to_id__in = assign_user_id)
    if order_by:
        queryset = queryset.order_by(order_by)
    data = {}
    data["result"] = queryset.annotate(assign_id =F('taskassign__assigned_to_id'),assign_name =F('taskassign__assigned_to__first_name')).values('id','name','assign_id','assign_name','createdby_id','createdby__first_name','createdtme','last_updated','start_time','end_time','note','status')
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserList(request):
    queryset = User.objects.all()
    filter_search = request.query_params.get('search', None)
    order_by = request.query_params.get('ordering',None)
    user_type = request.query_params.get('usertype',None)
    if user_type in ['AD','EM','MN']:
        queryset = queryset.filter(user_type = user_type)
    elif user_type == 'SA':
        queryset = queryset.filter(is_superuser = True)
    if filter_search:
        queryset = queryset.filter( Q(username__contains  = filter_search))
    if order_by:
        queryset = queryset.order_by(order_by)
    data = queryset.values('id','first_name','last_name','username','user_type','is_superuser')
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def NotificationList(request):
    queryset = Notification.objects.filter(notifi_to = request.user.user_type).order_by('-id')
    data = queryset.values('id','note','notification_type','object_id')
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request):
    if request.method == 'POST':
        if request.user.user_type in ['AD','SA','MN']:
            if request.data.get("task_id",None) and request.data.get("review",None):
                task_obj = Tasks.objects.filter(id = request.data["task_id"])
                if task_obj:
                    review_obj = Reviews.objects.create(review = request.data["review"],createdby = request.user , task = task_obj[0])
                    return Response('review created', status = status.HTTP_200_OK)
                else:
                    return Response('Provide a valid task_id',status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response('Provide a valid task_id and review',status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Methord not accepted',status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def EditReview(request):
    if request.method == 'POST':
        if request.data.get("review_id",None):
            if Reviews.objects.filter(id = request.data["review_id"] , createdby = request.user).exists():
                if request.data.get("review",None):
                    obj = Reviews.objects.filter(id = request.data["review_id"] , createdby = request.user).update(review = request.data["review"])
                    return Response("Task updated",status = status.HTTP_200_OK)
                else:
                    return Response("Nothing to update",status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response('Invalid review id',status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Must provide review id',status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Methord not accepted',status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def DeleteReview(request):
    if request.data.get("review_id",None):
        if Reviews.objects.filter(id = request.data["review_id"] , createdby = request.user).exists():
            task_obj = Reviews.objects.filter(id = request.data["review_id"] , createdby = request.user).delete()
            return Response("Review deleteed",status = status.HTTP_200_OK)
        else:
            return Response("Invalid id",status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Must provide review id',status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ReviewList(request):
    if request.data.get("task_id",None):
        if Reviews.objects.filter(task_id = request.data["task_id"]).exists():
            data = Reviews.objects.filter(task_id = request.data["task_id"]).values()
            return Response(data)
        else:
            return Response("Invalid task id",status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Must provide task id',status = status.HTTP_400_BAD_REQUEST)
