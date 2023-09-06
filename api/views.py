from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from account.models import *
from inventory.models import *
from .serializers import *

@csrf_exempt
@api_view(['POST'])  
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        if not username or not password:
            return Response({'error': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Generate or retrieve the user's authentication token
            token, created = Token.objects.get_or_create(user=user)

            return Response({'message': 'Login successful', 'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Login failed. Please check your username and password.'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_inventory(request):
    # Get the user's profile and roles
    user_profile = UserProfile.objects.get(user=request.user)
    user_roles = user_profile.roles.all()
    if user_roles.filter(name='Department Manager').exists():
        serializer = InventoryItemSerializer(data=request.data)
        if serializer.is_valid():
            inventory_item = serializer.save()
            # Create an InventoryChangeRequest record
            change_request_data = {
                'inventory_item': inventory_item.pk,  
                'department_manager': user_profile.user.pk,  
                'store_manager': None, 
                'request_type': InventoryChangeRequest.RequestType.ADD,
                'status': InventoryChangeRequest.Status.PENDING,
            }
            change_request_serializer = InventoryChangeRequestSerializer(data=change_request_data)
            
            if change_request_serializer.is_valid():
                change_request_serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                inventory_item.delete()
                return Response(change_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif user_roles.filter(name='Store Manager').exists():
        serializer = InventoryItemSerializer(data=request.data)
        if serializer.is_valid():
            inventory_item = serializer.save()
            change_request_data = {
                'inventory_item': inventory_item.pk,  
                'department_manager': None,  
                'store_manager': user_profile.user.pk, 
                'request_type': InventoryChangeRequest.RequestType.ADD,
                'status': InventoryChangeRequest.Status.APPROVED,
            }
            change_request_serializer = InventoryChangeRequestSerializer(data=change_request_data)
            
            if change_request_serializer.is_valid():
                change_request_serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                inventory_item.delete()
                return Response(change_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # If the user doesn't have the required role
    return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_inventory(request):
    # Get the user's profile and roles
    user_profile = UserProfile.objects.get(user=request.user)
    user_roles = user_profile.roles.all()
    # Check if the user is a Store Manager
    if user_roles.filter(name='Store Manager').exists():
        # Retrieve the pending change requests
        pending_requests = InventoryChangeRequest.objects.filter(status=InventoryChangeRequest.Status.PENDING)
        store_manager = User.objects.get(username=user_profile.user.username)
        if pending_requests : 
            for request in pending_requests:
                request.status = InventoryChangeRequest.Status.APPROVED
                request.store_manager = store_manager 
                if request.request_type == InventoryChangeRequest.RequestType.UPDATE:
                    request.inventory_item.quantity += 1  # Adjust the quantity as needed
                request.save()

            return Response({'message': 'Inventory items approved successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No items to approve'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_inventory(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_roles = user_profile.roles.all()
    if user_roles.filter(name='Store Manager').exists() or user_roles.filter(name='Department Manager').exists():
        if user_roles.filter(name='Store Manager').exists():
            inventory_items = InventoryItem.objects.all()
        else:
            inventory_items = InventoryItem.objects.filter(status='Approved')
        
        # Serialize the inventory items
        serializer = InventoryItemSerializer(inventory_items, many=True)
        return Response({'inventory': serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)