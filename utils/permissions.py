from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from api.models import UserActivityConstraints
from django.utils import timezone



class HasRequestLimit(permissions.BasePermission):

    '''
        check user has enough credits or not to create new business
    '''

    def has_permission(self, request, view):

        constraints = UserActivityConstraints.objects.filter(user=request.user)
        if constraints.exists():
            constraints = constraints.first()
            updated_at = constraints.updated_at
            current_time = timezone.now()

            # Calculate the time difference in minutes
            time_diff_seconds = (current_time - updated_at).total_seconds()
            time_diff_minutes = time_diff_seconds / 60

            limit = constraints.request_limit
            if time_diff_minutes <=1:
                if limit > 0:
                    return True
                else:
                    raise PermissionDenied("Friend Request Limit exceded")
            constraints.request_limit = 3
            constraints.save()
        return True
