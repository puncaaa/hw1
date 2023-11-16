from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from .models import Advertisement, Comment, Profile
from .forms import AdvertisementForm, CommentForm, CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.signing import Signer, loads, SignatureExpired
from django.contrib.auth.models import User
from django.conf import settings

def nt_list(request):
    nts = Advertisement.objects.all()
    return render(request, 'nts/nt_list.html', {'nts': nts})

def nt_detail(request, pk):
    nt = get_object_or_404(Advertisement, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.advertisement = nt
            comment.author = request.user
            comment.save()
            return redirect('nt_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'nts/nt_detail.html', {'nt': nt, 'form': form})

@login_required
def create_nt(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            nt = form.save(commit=False)
            nt.author = request.user
            nt.save()
            return redirect('nt_list')
    else:
        form = AdvertisementForm()

    return render(request, 'nts/nt_form.html', {'form': form})

@login_required
def edit_nt(request, pk):
    nt = get_object_or_404(Advertisement, pk=pk)

    if request.user != nt.author:
        return redirect('nt_detail', pk=pk)

    if request.method == 'POST':
        form = AdvertisementForm(request.POST, instance=nt)
        if form.is_valid():
            nt = form.save(commit=False)
            nt.save()
            return redirect('nt_detail', pk=pk)
    else:
        form = AdvertisementForm(instance=nt)

    return render(request, 'nts/nt_form.html', {'form': form})

@login_required
def create_comment(request, pk):
    nt = get_object_or_404(Advertisement, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.advertisement = nt
            comment.author = request.user
            comment.save()

            comments = nt.comments.all()
            return render(request, 'nts/comments_section.html', {'comments': comments})

    return JsonResponse({'error': 'Invalid form data.'})





@login_required
def delete_nt(request, pk):
    nt = get_object_or_404(Advertisement, pk=pk)
    if request.user == nt.author:
        nt.delete()
        return redirect('nt_list')
    else:
        return redirect('nt_detail', pk=pk)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.author:
        nt_pk = comment.advertisement.pk
        comment.delete()
        return redirect('nt_detail', pk=nt_pk)
    else:
        return redirect('nt_detail', pk=comment.advertisement.pk)




def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('nt_list')
    else:
        form = CustomUserCreationForm()

    return render(request, 'nts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('nt_list')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'nts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('nt_list')




def confirm_email(request, token):
    signer = Signer()
    try:
        user_email = loads(signer.unsign(token))
        user = User.objects.get(email=user_email)
        user.is_active = True
        user.save()
        return HttpResponse('Успешно')
    except Profile.DoesNotExist:
        return HttpResponse('Ошибка')
