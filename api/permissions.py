from rest_framework import permissions
from .models import *

class AdminPermission(permissions.BasePermission):
    """
    Global permission check for Admins.
    """
    def has_permission(self, request, view):
        account_type = UserAccount.objects.get(user=request.user).account_type
        return account_type == 'ad'

class HRRermission(permissions.BasePermission):
    """
    Global permission check for Internal Hiring Manager.
    """
    def has_permission(self, request, view):

        account_type = UserAccount.objects.get(user=request.user).account_type
        return account_type == 'hr'
