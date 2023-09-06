from django import forms
from .models import *
from account.models import *
class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = '__all__'  

class InventoryChangeRequestForm(forms.ModelForm):
    class Meta:
        model = InventoryChangeRequest
        fields = '__all__'  
class CreateInventoryItemForm(forms.Form):
    product_id = forms.CharField(max_length=50)
    product_name = forms.CharField(max_length=100)
    vendor = forms.CharField(max_length=100)
    mrp = forms.DecimalField(max_digits=10, decimal_places=2)
    batch_num = forms.CharField(max_length=50)
    batch_date = forms.DateField()
    quantity = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CreateInventoryItemForm, self).__init__(*args, **kwargs)

        # Check if the user is a Department Manager
        if user:
            user_profile = UserProfile.objects.get(user=user)
            is_department_manager = user_profile.roles.filter(name='Department Manager').exists()

            # Conditionally add the store_manager field if the user is a Department Manager
            if is_department_manager:
                self.fields['store_manager'] = forms.ModelChoiceField(
                    queryset=User.objects.filter(userprofile__roles__name='Store Manager'),
                    label='Store Manager',
                    required=True,
                )

# class InventoryChangeRequestForm(forms.ModelForm):
#     class Meta:
#         model = InventoryChangeRequest
#         fields = ('request_type', 'store_manager') 