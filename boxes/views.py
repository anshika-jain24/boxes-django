# views.py
from datetime import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from boxes.serializers import BoxSerializer, BoxSerializerNonStaff
from .models import Box

import json
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .utils import validate_box_limits, validate_box_creation_limit

User = get_user_model()


@api_view(['POST'])
@permission_classes([])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    is_staff = request.data.get('is_staff')
    if username is None or email is None or password is None or is_staff is None:
        return Response({'error': 'Please provide all required fields'}, status=417)
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=409)
    user = User.objects.create_user(
        username=username, email=email, password=password, is_staff=is_staff)
    return JsonResponse({'status': 'success'})


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def add_box(request):
    data = json.loads(request.body)
    print(data)
    length = data['length']
    breadth = data['breadth']
    height = data['height']
    createdBy = request.user

    box = Box(length=length, breadth=breadth,
              height=height, area=float(length) * float(breadth), volume=float(length) * float(breadth) * float(height), created_by=createdBy)
    if validate_box_limits(box) and validate_box_creation_limit(box):
        box.save()
    else:
        return JsonResponse({'status': 'failed', 'message': 'box is going out of specified limits'}, status=406)
    return JsonResponse({'status': 'success'})


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_box(request, id):
    box = get_object_or_404(Box, id=id)
    data = json.loads(request.body)
    if "created_by" in data:
        return JsonResponse({'status': 'failed', 'message': 'Not Allowed'}, status=401)
    if "last_updated" in data:
        return JsonResponse({'status': 'failed', 'message': 'Not Allowed'}, status=401)
    if "length" in data:
        box.length = data['length']
        box.area = float(box.length) * float(box.breadth)
        box.volume = float(box.length) * float(box.breadth) * float(box.height)
    if "breadth" in data:
        box.breadth = data['breadth']
        box.area = float(box.length) * float(box.breadth)
        box.volume = float(box.length) * float(box.breadth) * float(box.height)
    if "height" in data:
        box.height = data['height']
        box.volume = float(box.length) * float(box.breadth) * float(box.height)

    if validate_box_limits(box) and validate_box_creation_limit(box):
        box.save()
    else:
        return JsonResponse({'status': 'failed', 'message': 'box is going out of specified limits'}, status=406)
    return JsonResponse({'status': 'success'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_boxes(request):
    length_more_than = request.data.get('length_more_than', None)
    length_less_than = request.data.get('length_less_than', None)
    breadth_more_than = request.data.get('breadth_more_than', None)
    breadth_less_than = request.data.get('breadth_less_than', None)
    height_more_than = request.data.get('height_more_than', None)
    height_less_than = request.data.get('height_less_than', None)
    area_more_than = request.data.get('area_more_than', None)
    area_less_than = request.data.get('area_less_than', None)
    volume_more_than = request.data.get('volume_more_than', None)
    volume_less_than = request.data.get('volume_less_than', None)
    created_by = request.data.get('created_by', None)
    created_before = request.data.get('created_before', None)
    created_after = request.data.get('created_after', None)

    boxes = Box.objects.all()

    if length_more_than:
        boxes = boxes.filter(length__gt=length_more_than)
    if length_less_than:
        boxes = boxes.filter(length__lt=length_less_than)
    if breadth_more_than:
        boxes = boxes.filter(breadth__gt=breadth_more_than)
    if breadth_less_than:
        boxes = boxes.filter(breadth__lt=breadth_less_than)
    if height_more_than:
        boxes = boxes.filter(height__gt=height_more_than)
    if height_less_than:
        boxes = boxes.filter(height__lt=height_less_than)
    if area_more_than:
        boxes = boxes.filter(area__gt=area_more_than)
    if area_less_than:
        boxes = boxes.filter(area__lt=area_less_than)
    if volume_more_than:
        boxes = boxes.filter(volume__gt=volume_more_than)
    if volume_less_than:
        boxes = boxes.filter(volume__lt=volume_less_than)
    if created_by:
        boxes = boxes.filter(created_by__username=created_by)
    if created_before:
        boxes = boxes.filter(created_at__lt=created_before)
    if created_after:
        boxes = boxes.filter(created_at__gt=created_after)

    is_staff = request.user.is_staff

    if is_staff:
        serializer = BoxSerializer(boxes, many=True)
    else:
        serializer = BoxSerializerNonStaff(boxes, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_box(request, id):
    box = get_object_or_404(Box, id=id)
    user = str(request.user)
    if user == box.created_by:
        box.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': "failed", 'message': 'only the creater of the box can delete it'}, status=401)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def list_my_boxes(request):
    user = request.user
    boxes = Box.objects.filter(created_by=user)
    length_more_than = request.data.get('length_more_than', None)
    length_less_than = request.data.get('length_less_than', None)
    breadth_more_than = request.data.get('breadth_more_than', None)
    breadth_less_than = request.data.get('breadth_less_than', None)
    height_more_than = request.data.get('height_more_than', None)
    height_less_than = request.data.get('height_less_than', None)
    area_more_than = request.data.get('area_more_than', None)
    area_less_than = request.data.get('area_less_than', None)
    volume_more_than = request.data.get('volume_more_than', None)
    volume_less_than = request.data.get('volume_less_than', None)
    created_before = request.data.get('created_before', None)
    created_after = request.data.get('created_after', None)

    if length_more_than:
        boxes = boxes.filter(length__gt=length_more_than)

    if length_less_than:
        boxes = boxes.filter(length__lt=length_less_than)

    if breadth_more_than:
        boxes = boxes.filter(breadth__gt=breadth_more_than)

    if breadth_less_than:
        boxes = boxes.filter(breadth__lt=breadth_less_than)

    if height_more_than:
        boxes = boxes.filter(height__gt=height_more_than)

    if height_less_than:
        boxes = boxes.filter(height__lt=height_less_than)
    if area_more_than:
        boxes = boxes.filter(area__gt=area_more_than)

    if area_less_than:
        boxes = boxes.filter(area__lt=area_less_than)

    if volume_more_than:
        boxes = boxes.filter(volume__gt=volume_more_than)

    if volume_less_than:
        boxes = boxes.filter(volume__lt=volume_less_than)

    if created_before:
        created_before_date = timezone.datetime.strptime(
            created_before, "%Y-%m-%d").date()
        boxes = boxes.filter(created_at__lt=created_before_date)

    if created_after:
        created_after_date = timezone.datetime.strptime(
            created_after, "%Y-%m-%d").date()
        boxes = boxes.filter(created_at__gt=created_after_date)

    serializer = BoxSerializer(boxes, many=True)
    return JsonResponse(serializer.data, safe=False)
