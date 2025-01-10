from django.shortcuts import redirect
from django.contrib.auth.models import User

# Create your views here.

def delete_user(request, user_id):
    """
    View to delete a user account and clean up related data.
    """
    user = User.objects.get(pk=user_id)
    user.delete()
    return redirect('home')  # Redirect to the home page after deletion