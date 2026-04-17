from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import CreateCustomUserForm, LoginForm, UpdateUserForm
from django.contrib.sites.shortcuts import get_current_site
from . token import user_tokenizer_generate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from payment.forms import ShippingForm
from payment.models import Order, OrderItem

def register(request):

    form = CreateCustomUserForm()

    if request.method == 'POST':
        form = CreateCustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            # email verification

            current_site = get_current_site(request)
            subject = 'Account verification email'

            message = render_to_string('account/registration/email-verification.html', {

                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),

            })

            user.email_user(subject=subject, message=message)


            return redirect('email-verification-sent')
            


    context = {'form': form}
    return render(request, 'account/register.html', context)

def login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('index')
    context = {'form': form}

    return render(request, 'account/login.html', context)

def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')

def dashboard(request):
    return render(request, 'account/dashboard.html')

@login_required(login_url='login')
def profile_management(request):    

    # Updating our user's username and email

    user_form = UpdateUserForm(instance=request.user)

    if request.method == 'POST':

        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():

            user_form.save()

            messages.info(request, "Update success!")

            return redirect('dashboard')

   

    context = {'user_form':user_form}

    return render(request, 'account/profile-management.html', context=context)

@login_required(login_url='login')
def delete_account(request):
    user = CustomUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        messages.error(request, "Account deleted")
        return redirect('index')
    return render(request, 'account/account-delete.html')

#region email verification views


def email_verification(request, uidb64, token):

    # uniqueid

    unique_id = force_str(urlsafe_base64_decode(uidb64))

    user = CustomUser.objects.get(pk=unique_id)
    
    # Success

    if user and user_tokenizer_generate.check_token(user, token):

        user.is_active = True

        user.save()

        return redirect('email-verification-success')


    # Failed 

    else:

        return redirect('email-verification-failed')

def email_verification_sent(request):
    return render(request, 'account/registration/email-verification-sent.html')

def email_verification_success(request):
    return render(request, 'account/registration/email-verification-success.html')

def email_verification_failed(request):
    return render(request, 'account/registration/email-verification-failed.html')

#endregion

from payment.models import ShippingAddress

@login_required(login_url='login')
def manage_shipping(request):
    
    try:
        ShippingAddress.objects.get(user=request.user.id)
    except ShippingAddress.DoesNotExist:
        shipping = None

    form = ShippingForm(instance=shipping)

    if request.method == 'POST':
        form = ShippingForm(request.POST, instance = shipping)
        if form.is_valid():
            shipping_user = form.save(commit=False)
            shipping_user.user = request.user
            shipping_user.save()

            return redirect('dashboard')
    context = {'form': form}
    
    return render(request, 'account/manage-shipping.html', context)

@login_required(login_url='my-login')
def track_orders(request):

    try:

        # orders = OrderItem.objects.filter(user=request.user)
        orders = Order.objects.filter(user=request.user)

        context = {'orders':orders}

        return render(request, 'account/track-orders.html', context=context)

    except:

        return render(request, 'account/track-orders.html')




