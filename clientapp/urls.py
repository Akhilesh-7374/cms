from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('Homepage/', views.homepage_display, name='Homepage'),
    path('addclients/', views.addclient, name='addclients'),
    path('allclients/', views.allclients, name='allclients'),
    path('editclient/<int:client_id>/', views.edit_client, name='edit_client'),
    path('deleteclient/<int:client_id>/', views.delete_client, name='delete_client'),
    path('addcall/', views.add_call, name='add_call'),
    path('callhistory/', views.callhistory, name='callhistory'),
    path('editcall/<int:call_id>/', views.edit_call, name='edit_call'),
    path('deletecall/<int:call_id>/', views.delete_call, name='delete_call'),
    path('addpayments/', views.add_payment, name='addpayments'),
    path('allpayments/', views.all_payments, name='all_payments'),
    path('edit-payment/<int:pid>/', views.edit_payment, name='edit_payment'),
    path('deletepayment/<int:pid>/', views.deletepayment, name='deletepayment'),
    path('addbranch/', views.add_branch, name='addbranch'),
    path('allbranches/', views.all_branches, name='all_branches'),
    path('editbranch/<int:id>/', views.edit_branch, name='edit_branch'),
    path('deletebranch/<int:branch_id>/', views.delete_branch, name='delete_branch'),
    path('adduser/',views.adduser,name="users"),
    path('allusers/',views.allusers,name="allusers"),
    path('edituser/<int:uid>/', views.edituser, name='edituser'),
    path('deleteuser/<int:uid>/', views.deleteuser, name='deleteuser'),
    path('login/', views.login_view, name='login'),
    path('logout/',views.Logout_view, name='logout'),
]
