from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.shortcuts import render, redirect

# Create your views here.

@login_required(login_url='/accounts/login/')
def home(request):
    # You can retrieve the first name of the user from the request.user object
    first_name = ""
    if request.user.is_authenticated:
        first_name = request.user.first_name
    context = {'first_name': first_name}
    return render(request, 'registration/home.html', context=context)


class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('signup_complete')
    model = CustomUser

class SignUpCompleteView(TemplateView):
    template_name = 'registration/signup_complete.html'


@login_required(login_url='/accounts/login/')
def accounts_index_view(request):
    return render(request, 'registration/accounts_index.html')

@login_required(login_url='/accounts/login/')
def edit_profile_form_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Retrieve the user object
        user = request.user

        # Update the user fields with the form data
        user.email = email
        user.first_name = first_name
        user.last_name = last_name

        # Save the updated user object
        user.save()

        # Redirect to a success page or desired URL
        return redirect('edit_profile_done')

    return render(request, 'registration/edit_profile_form.html')

@login_required(login_url='/accounts/login/')
def edit_profile_done_view(request):
    return render(request, 'registration/edit_profile_done.html')