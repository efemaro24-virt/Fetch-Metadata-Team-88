# Admin libraries
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .forms import FileUpload
from django.views.generic import TemplateView, ListView, View
from .models import User, UserPost
# Fetch metadata packages
from Fetch_Meta_Data_App.utils_functions.functions import handle_uploaded_file
from Fetch_Meta_Data_App.utils_functions.extract_meta_data import get_metadata

# Export filetype library
import csv
import json
# Create your views here.


class LandingPageView(TemplateView):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


class SignUpPageView(View):
    template_name = 'signup.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['pwd2']

        # print(username)
       # print(password)
       # print(confirm_password)

        if password == confirm_password:
            add_user = User(username=username,
                            email=email, password=password)
            add_user.save()
            messages.info(request, "Account Created Successful")
            return redirect("login")
        else:
            messages.info(request, 'Passwords are not same.')
            return redirect('signup')

        # return render(request, 'signup.html')


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user_exists = User.objects.filter(
                username=username, password=password).exists()
            if user_exists:
                request.session['user'] = username
                messages.info(request, 'You are logged in successfully.')
                return redirect('landing')
        else:
            messages.info(request, 'Invalid Username or Password.')
            return redirect('login')

        return render(request, 'index.html')


class LogOutView(View):

    def get(self, request):
        auth.logout(request)
        return redirect('/')


def upload_file(request):
    '''Uploading File'''
    context = {}
    tags = []
    values = []
    file_path = ""
    if request.method == 'POST':
        form = FileUpload(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['user_file'])
            uploaded_file = request.FILES['user_file']
            file_path = 'Fetch_Meta_Data_App/static/upload/'
            meta_data = get_metadata(file_path+str(uploaded_file))
            for key, value in meta_data.items():
                tags.append(key)
                values.append(value)
            context['metadata'] = zip(tags, values)
            context_dict = meta_data

           # model_instance = form.save(commit=False)
            # model_instance.save()

            request.session['metadata_session'] = context_dict

            return render(request, 'metadata.html', context)
    else:
        form = FileUpload()

    #meta_data_json = json.dumps(meta_data, indent=4)

    context['form'] = form
    return render(request, 'uploadfile.html', context)  # {'form': form})


def result_display():
    metadata = request.session.get("metadata_session")
    context = metadata
    return render(request, "index.html", context)


def save_metadata(request):
    metadata = request.session.get("metadata_session")


def download_metadata(request):
    metadata = request.session.get("metadata_session")
    json_writer = json.dumps(metadata, indent=4)
    response = HttpResponse(json_writer, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="metadata.json"'

    return response


def share_metadata():
    pass


def get_file():
    pass


def download_file():
    pass


def delete_file():
    pass


def export_pdf():
    pass


############################
# USer Profile

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
