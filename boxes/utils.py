from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from .models import Box


def validate_box_limits(box):
    """
    Validates if the average area of all added boxes and the average volume of boxes added by the current user
    are within the specified limits.

    Average area of all added boxes should not exceed A1
    Average volume of all boxes added by the current user shall not exceed V1
    """
    user_boxes = Box.objects.filter(created_by=box.created_by)
    if user_boxes.exists():
        user_volume = sum([(b.length * b.breadth * b.height)
                          for b in user_boxes]) / user_boxes.count()
    else:
        user_volume = 0

    all_boxes = Box.objects.all()
    if all_boxes.exists():
        all_area = sum([b.length * b.breadth
                       for b in all_boxes]) / all_boxes.count()
    else:
        all_area = 0

    if user_volume > settings.V1 or all_area > settings.A1:
        return False
    return True


def validate_box_creation_limit(box):
    """
    Validates if the total number of boxes added in a week and the total number of boxes added in a week by a user
    are within the specified limits. 

    Total Boxes added in a week cannot be more than L1
    Total Boxes added in a week by a user cannot be more than L2
    """
    week_ago = timezone.now() - timedelta(days=7)

    user_boxes = Box.objects.filter(
        created_by=box.created_by, created_at__gte=week_ago)
    if user_boxes.count() >= settings.L2:
        return False

    all_boxes = Box.objects.filter(created_at__gte=week_ago)
    if all_boxes.count() >= settings.L1:
        return False
    return True
