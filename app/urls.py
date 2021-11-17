from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('dev/signup/',views.developer_register.as_view(),name='developer_register'),
    path('pm/signup/',views.manager_register.as_view(),name='manager_register'),
    path('dev/signin',views.developer_login,name='developer_login'),
    path('pm/sigin/', views.Manager_Login.as_view(), name='manager_login'),
    path('dev/dasnboard/',views.dev_dashboard,name='dev_dashboard'),
    # path('pm/signin',views.manager_login,name='manager_login'),
    path('pm/dashboard/',views.pm_dashboard,name='pm_dashboard'),
    path('ticket/create',views.ticket_create_view,name='ticket_view'),
    path('logout/',views.logout_view,name='logout_view'),

    path('ticket/open',views.open_tickets_view,name='open_tickets'),
    # path('dev/ticket/accept/<int:pk>',views.accept_tickets_view,name='accept_tickets'),
    path('dev/ticket/reject/<int:pk>',views.Accept_Ticket.as_view(),name='accept_tickets'),
    path('dev/ticket/accepted/',views.dev_accepted_ticket,name='accepted_tickets_view'),
    path('dev/ticket/complete/<int:pk>',views.mark_complete_tickets_view,name='mark_complete'),
    path('dev/ticket/completed/',views.dev_completed_ticket,name='completed_tickets_view'),
    path('dev/ticket/closed/',views.dev_closed_tickets_view,name='dev_closed_tickets'),
    
    path('pm/ticket/open',views.pm_open_tickets_view,name='pm_open_tickets'),
    path('pm/ticket/accepted/',views.pm_accepted_tickets,name='pm_accepted_tickets_view'),
    path('pm/ticket/completed/',views.pm_completed_tickets,name='pm_completed_tickets_view'),
    path('pm/tickets/close',views.pm_close_tickets,name='mark_closed'),
    path('pm/ticket/closed/<int:pk>',views.pm_close_tickets,name='pm_close_ticket'),
    path('pm/ticket/closed/',views.pm_closed_tickets,name='pm_closed_tickets_view'),

    
]
