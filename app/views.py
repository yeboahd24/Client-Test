from django import forms
from django.contrib import auth
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from django.views.generic import CreateView
from .forms import DeveloperSignupForm,ProjectManagerSignupForm,TicketCreateForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Developer, User,Ticket

# Create your views here.
def index(request):
    return render(request,'app/login_register_page.html')


class developer_register(CreateView):
    model = User
    form_class = DeveloperSignupForm
    template_name = 'app/dev_register.html'

    def form_valid(self,form):
        user = form.save()
        return redirect(reverse('developer_login'))


class manager_register(CreateView):
    model = User
    form_class = ProjectManagerSignupForm
    template_name = 'app/pm_register.html'

    def form_valid(self,form):
        user = form.save()
        return redirect(reverse('manager_login'))



def manager_login(request):
    current = User.objects.filter(is_manager = True)
    
    if request.method == 'POST':
        pm_form = AuthenticationForm(data=request.POST)

        if pm_form.is_valid():
            username = pm_form.cleaned_data.get('username')
            password = pm_form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)

            if user is not None:
                if user in current:
                    login(request,user)
                    return redirect(reverse('pm_dashboard'))
            else:
                messages.error(request,"Invalid Username or Password")

        else:
                messages.error(request,"Invalid Username or Password")
    return render(request, 'app/pm_login.html',context={'form':AuthenticationForm(),})


@login_required
def pm_dashboard(request):
    return render(request,'app/pm_dash.html')



def developer_login(request):
    current = User.objects.filter(is_developer = True)
    if request.method == 'POST':
        dev_form = AuthenticationForm(data=request.POST)

        if dev_form.is_valid():
            username = dev_form.cleaned_data.get('username')
            password = dev_form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)

            if user is not None:
                if user in current:
                    login(request,user)
                    return redirect(reverse('dev_dashboard'))

            else:
                messages.error(request,"Invalid Username or Password")

        else:
                messages.error(request,"Invalid Username or Password")
    return render(request, 'app/dev_login.html',context={'form':AuthenticationForm(),})


@login_required
def dev_dashboard(request):
    return render(request,'app/dev_dash.html')


@login_required
def ticket_create_view(request):

    if request.POST:
        form = TicketCreateForm(request.POST)

        if form.is_valid():
            obj = form.save()
            obj.created_by = request.user
            obj.status = "Opened"
            obj.save()

            return HttpResponseRedirect(reverse('pm_open_tickets'))

    else:
        form = TicketCreateForm()

    return render(request,'app/create_ticket.html',{'form': form,})

@login_required
def open_tickets_view(request):
    tickets_open = Ticket.objects.filter(status = 'Opened') 
    return render(request,'app/open_tickets.html',{"tickets": tickets_open})


@login_required
def accept_tickets_view(request,pk):
    ticket = Ticket.objects.get(id=pk)
    if ticket.status == 'Opened':
        ticket.status = 'Accepted'
        ticket.accepted_by = request.user
        ticket.save()
    return redirect(reverse('open_tickets'))


@login_required
def dev_accepted_ticket(request):
    ticket_complete = Ticket.objects.filter(status = 'Accepted',accepted_by = request.user)
    return render(request,'app/dev_accepted_ticket.html',{"tickets": ticket_complete})



@login_required
def mark_complete_tickets_view(request,pk):
    ticket = Ticket.objects.get(id=pk)
    if ticket.status == 'Accepted' and ticket.accepted_by == request.user:
        ticket.status = 'Completed'
        ticket.save()
        return redirect(reverse('accepted_tickets_view'))



@login_required
def dev_completed_ticket(request):
    tickets_completed = Ticket.objects.filter(status = 'Completed',accepted_by = request.user)
    return render(request,'app/dev_complete_ticket.html',{'tickets':tickets_completed})


@login_required
def dev_closed_tickets_view(request):
    tickets_closed = Ticket.objects.filter(status='Closed',accepted_by = request.user)
    return render(request,'app/dev_closed_tickets.html',{'tickets':tickets_closed})


@login_required
def pm_open_tickets_view(request):
    tickets_open = Ticket.objects.filter(status = 'Opened',created_by = request.user) 
    return render(request,'app/pm_open_tickets.html',{"tickets": tickets_open})


@login_required
def pm_accepted_tickets(request):
    ticket_complete = Ticket.objects.filter(status = 'Accepted',created_by = request.user)
    return render(request,'app/pm_accepted_tickets.html',{"tickets": ticket_complete})


@login_required
def pm_completed_tickets(request):
    tickets_completed = Ticket.objects.filter(status = 'Completed',created_by = request.user)
    return render(request,'app/pm_completed_tickets.html',{"tickets": tickets_completed})


@login_required
def pm_close_tickets(request,pk):
    ticket = Ticket.objects.get(id=pk)
    if ticket.status == 'Completed' and ticket.created_by == request.user:
        ticket.status = 'Closed'
        ticket.closed_date = datetime.datetime.now()
        ticket.save()
    return redirect(reverse("pm_completed_tickets_view"))


@login_required
def pm_closed_tickets(request):
    tickets_closed = Ticket.objects.filter(status = 'Closed',created_by = request.user)
    return render(request,'app/pm_closed_tickets.html',{"tickets": tickets_closed})


@login_required
def logout_view(request):
    current = User.objects.filter(is_developer = True)
    if request.user in current:
        logout(request)
        return redirect(reverse('developer_login'))
    else:
        logout(request)
        return redirect(reverse('manager_login'))
