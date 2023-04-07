from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .models import *
from .forms import RoomForm, MessageForm


class HomeListView(ListView):
    model = Room
    template_name = 'base/index.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        q = self.request.GET.get('q') if self.request.GET.get('q') is not None else ''

        return Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(head__icontains=q) |
            Q(description__icontains=q)
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)

        q = self.request.GET.get('q') if self.request.GET.get('q') is not None else ''
        data['rooms_messages'] = Message.objects.filter(Q(room__topic__name__icontains=q))[:8]
        data['topics'] = Topic.objects.all()
        data['rooms_total'] = Room.objects.count()
        return data


class ProfileDetailView(DetailView):
    model = User
    template_name = 'base/profile.html'
    # context_object_name = 'user'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        user = self.get_object()
        data['rooms'] = Room.objects.filter(participants__id=user.id)
        data['topics'] = Topic.objects.all()
        data['rooms_messages'] = user.message_set.all()[:10]
        data['rooms_total'] = Room.objects.count()
        return data


class RoomDetailView(DetailView):
    model = Room
    template_name = 'base/room.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['room_messages'] = self.get_object().message_set.all()
        data['form'] = MessageForm()
        data['participants'] = self.get_object().participants.all()
        return data

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            form = MessageForm(data=self.request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.author = self.request.user
                message.room = self.get_object()
                self.get_object().participants.add(self.request.user.id)
                message.save()
                messages.success(self.request, "Your message is added.")
                return redirect('room', pk=self.get_object().pk)
        return redirect('room', pk=self.get_object().pk)


class RoomCreateView(LoginRequiredMixin, CreateView):
    template_name = 'base/create_room.html'
    form_class = RoomForm
    success_url = reverse_lazy('home')
    login_url = '/login/'
    extra_context = {
        'topics': Topic.objects.all()
    }

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {
            "initial": self.get_initial(),
            "prefix": self.get_prefix(),
        }

        if self.request.method in ("POST", "PUT"):
            topic_name = self.request.POST.get('topic')
            topic, created = Topic.objects.get_or_create(name=topic_name)

            data = self.request.POST.copy()
            data['topic'] = f'{topic.id}'
            data['host'] = f'{self.request.user.id}'

            kwargs.update(
                {
                    "data": data,
                    "files": self.request.FILES,
                }
            )
        return kwargs

    def form_valid(self, form):
        room = form.save(commit=False)
        room.host = self.request.user
        room.save()
        messages.success(self.request, "Room is created.")
        return super().form_valid(form)


class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'base/create_room.html'
    success_url = reverse_lazy('home')
    login_url = '/login/'
    extra_context = {
        'topics': Topic.objects.all()
    }

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user != self.get_object().host:
            messages.error(request, "You do not have a permission to modify not owned room.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {
            "initial": self.get_initial(),
            "prefix": self.get_prefix(),
        }

        if hasattr(self, "object"):
            kwargs.update({"instance": self.object})

        if self.request.method in ("POST", "PUT"):
            topic_name = self.request.POST.get('topic')
            topic, created = Topic.objects.get_or_create(name=topic_name)

            data = self.request.POST.copy()
            data['topic'] = f'{topic.id}'

            kwargs.update(
                {
                    "data": data,
                    "files": self.request.FILES,
                }
            )
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Room is modified.")
        return super().form_valid(form)


class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'base/delete.html'
    success_url = reverse_lazy('home')
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user != self.get_object().host:
            messages.error(request, "You do not have a permission to delete not owned room.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj'] = self.object
        return context

    def get_success_url(self):
        messages.info(self.request, "Room is deleted.")
        return super().get_success_url()


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'base/delete.html'
    success_url = reverse_lazy('room')
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user != self.get_object().author:
            messages.error(request, "You do not have a permission to delete not own message.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj'] = self.object
        return context

    def get_success_url(self):
        messages.info(self.request, "Message is deleted.")
        return reverse('room', kwargs={'pk': self.object.room.id})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username').lower()
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are logged in as {username}.')
                return redirect('home')

        messages.error(request, "Not correct credentials.")

    form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'base/login.html', context)


def logoutPage(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        messages.error(request, "Unsuccessful registration.")

    form = UserCreationForm()
    return render(request, 'base/register.html', {'form': form})
