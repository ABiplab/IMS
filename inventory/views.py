from django.shortcuts import render,redirect,get_object_or_404
from django.template.loader import get_template
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from account.models import *
from .forms import *
@login_required
def dashboard(request):
    return render(request,'inventory/dashboard.html',{'section': 'dashboard'})
@login_required
def create_inventory_item(request):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        is_store_manager = user_profile.roles.filter(name='Store Manager').exists()
        create_item_form = CreateInventoryItemForm(request.POST, user=request.user)
        if create_item_form.is_valid():
            inventory_item = InventoryItem.objects.create(
                product_id=create_item_form.cleaned_data['product_id'],
                product_name=create_item_form.cleaned_data['product_name'],
                vendor=create_item_form.cleaned_data['vendor'],
                mrp=create_item_form.cleaned_data['mrp'],
                batch_num=create_item_form.cleaned_data['batch_num'],
                batch_date=create_item_form.cleaned_data['batch_date'],
                quantity=create_item_form.cleaned_data['quantity'],
            )
            if is_store_manager:
                change_request = InventoryChangeRequest.objects.create(
                inventory_item=inventory_item,
                store_manager=request.user,
                request_type=InventoryChangeRequest.RequestType.ADD,
                status = InventoryChangeRequest.Status.APPROVED
            )
            else:
                change_request = InventoryChangeRequest.objects.create(
                inventory_item=inventory_item,
                department_manager=request.user,
                request_type=InventoryChangeRequest.RequestType.ADD,
            )

            return redirect('inventory_list')  
    else:
        create_item_form = CreateInventoryItemForm(user=request.user)

    return render(request, 'inventory/create_inventory_item.html', {'create_item_form': create_item_form})

@login_required
def inventory_list(request):
    user_profile = UserProfile.objects.get(user=request.user)
    is_store_manager = user_profile.roles.filter(name='Store Manager').exists()
    status_filter = request.GET.get('status_filter')
    print(status_filter)

    if is_store_manager:
        inventory_items = InventoryChangeRequest.objects.all()
    else:
        inventory_items = InventoryChangeRequest.approved_objects.all()

    if status_filter:
        inventory_items = inventory_items.filter(status=status_filter)

    # Configure pagination
    page = request.GET.get('page', 1)
    items_per_page = 5  
    paginator = Paginator(inventory_items, items_per_page)

    try:
        inventory_items = paginator.page(page)
    except PageNotAnInteger:
        inventory_items = paginator.page(1)
    except EmptyPage:
        inventory_items = paginator.page(paginator.num_pages)

    return render(request, 'inventory/inventory_list.html', {'inventory_items': inventory_items, 'is_store_manager': is_store_manager})

@login_required
def update_status(request, item_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in (InventoryChangeRequest.Status.APPROVED, InventoryChangeRequest.Status.PENDING):
            item = InventoryChangeRequest.objects.get(id=item_id)
            item.status = new_status
            item.save()
            if item.request_type ==InventoryChangeRequest.RequestType.DELETE:
                return redirect('delete_inventory_item', item_id=item.inventory_item.id)
            else:
                return redirect('inventory_list')
    
    return redirect('inventory_list')
@login_required
def update_inventory_item(request, item_id):
    item = get_object_or_404(InventoryItem, pk=item_id)
    change_request = InventoryChangeRequest.objects.get(inventory_item=item)
    user_profile = UserProfile.objects.get(user=request.user)
    is_store_manager = user_profile.roles.filter(name='Store Manager').exists()
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            if change_request:
                if is_store_manager:
                    print("this")
                    change_request.request_type = InventoryChangeRequest.RequestType.UPDATE
                    change_request.store_manager = request.user
                    change_request.status = InventoryChangeRequest.Status.APPROVED
                    change_request.save()
                else:
                    change_request.request_type = InventoryChangeRequest.RequestType.UPDATE
                    change_request.department_manager = request.user
                    change_request.status = InventoryChangeRequest.Status.PENDING
                    change_request.save()
            return redirect('inventory_list')
    else:
        form = InventoryItemForm(instance=item)
    return render(request, 'inventory/update_inventory_item.html', {'form': form, 'item': item})

@login_required
def delete_inventory_item(request, item_id):
    user_profile = UserProfile.objects.get(user=request.user)
    is_store_manager = user_profile.roles.filter(name='Store Manager').exists()
    item = get_object_or_404(InventoryItem, pk=item_id)
    change_request = InventoryChangeRequest.objects.get(inventory_item=item)
    if request.method == 'POST':
        if is_store_manager:
            item.delete()
            return redirect('inventory_list')
        else:
            change_request.request_type = InventoryChangeRequest.RequestType.DELETE
            change_request.department_manager = request.user
            change_request.status = InventoryChangeRequest.Status.PENDING
            change_request.save()
            return redirect('inventory_list')
    return render(request, 'inventory/delete_inventory_item.html', {'item': item})