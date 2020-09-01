from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Topic, Webpage, AccessRecord
from . import forms


def index(request):
    # forward slash in "template_name" is platform independent as its going to be read by browser
    # Over template, access values by CONTEXT dictionary keys being passed or iterate over it. It make sense also.
    access_record_dict = {"access_record": AccessRecord.objects.order_by('date'), "insert_text": "Hola! I am from Mars"}
    return render(request, template_name="first_app/index.html", context=access_record_dict)


def form_name_view(request):
    form = forms.FormName()
    if request.method == "POST":
        form = forms.FormName(request.POST)

        if form.is_valid():
            print("Validation Success!")
            print("Name: " + form.cleaned_data['name'])
            print("Email: " + form.cleaned_data['email'])

    return render(request, 'first_app/form_page.html', {'form': form})


def form_topic_view(request):
    form = forms.TopicForm()

    # If form is posted (someone click on submit over form) then below code will handle, return will remain same
    if request.method == "POST":
        form = forms.TopicForm(request.POST)

        # if form is valid the save it to our model and commit the transaction to our DB
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print("Error!")

    return render(request, 'first_app/form_page.html', {'form': form})


def register(request):
    registered = False

    user_form = forms.UserForm()
    user_profile_form = forms.UserProfileForm()

    if request.method == "POST":
        user_form = forms.UserForm(request.POST)
        user_profile_form = forms.UserProfileForm(request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = user_profile_form.save(commit=False)
            profile.user = user

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            profile.save()

            registered = True

        else:
            print(user_form.errors, user_profile_form.errors)

    return render(request, 'first_app/registration.html', {'user_form': user_form,
                                                           'user_profile_form': user_profile_form,
                                                           'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('first_app:index'))

            else:
                return HttpResponse("Account not active")

        else:
            print("Someone try to login and failed")
            print("Username: {} and Password: {}".format(username, password))

            return HttpResponse("Invalid login details")

    else:
        return render(request, 'first_app/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('first_app:index'))