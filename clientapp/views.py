from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .forms import SupportCallForm
from .models import SupportCall
from django.template import loader
from .decorators import role_required
from .models import AllPayments
from .forms import AllPaymentsForm
from .forms import BranchForm
from .models import Branch
from django.contrib.auth import logout
from .forms import ClientForm  
from .models import Client
from .forms import AllUsersForm
from .models import AllUsers


def homepage_display(request):
    myname = "Akhilesh"
    return render(request, "home.html", {'username': myname})


def addclient(request):
    client = None
    if request.method == "POST":
        client_id = request.POST.get('client_id')
        if client_id:
            client = get_object_or_404(Client, id=client_id)
        else:
            client = Client()

        client.client_name = request.POST['client_name']
        client.contact_name = request.POST['contact_name']
        client.client_code = request.POST['client_code']
        client.contact_number = request.POST['contact_number']
        client.address = request.POST['address']
        client.url = request.POST.get('url', '')
        client.additional_link = request.POST.get('additional_link', '')
        client.login_id = request.POST['login_id']
        client.password = request.POST['password']
        client.has_branches = 'has_branches' in request.POST
        client.strength = request.POST.get('strength') or None
        client.payment_type = request.POST['payment_type']
        client.unit_amount = request.POST['unit_amount']
        client.description = request.POST.get('description', '')
        client.save()

        return redirect('allclients')

    return render(request, 'addclient.html', {'client': client})


def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == "POST":
        client.client_name = request.POST['client_name']
        client.contact_name = request.POST['contact_name']
        client.client_code = request.POST['client_code']
        client.contact_number = request.POST['contact_number']
        client.address = request.POST['address']
        client.url = request.POST.get('url', '')
        client.additional_link = request.POST.get('additional_link', '')
        client.login_id = request.POST['login_id']
        client.password = request.POST['password']
        client.has_branches = 'has_branches' in request.POST
        client.strength = request.POST.get('strength') 
        client.payment_type = request.POST['payment_type']
        client.unit_amount = request.POST['unit_amount']
        client.description = request.POST.get('description', '')

        client.save()
        return redirect('allclients')
    return render(request, 'addclient.html', {'client': client})

def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    client.delete()
    return redirect('allclients')

def allclients(request):
    query = request.GET.get('search', '')
    if query:
        clients = Client.objects.filter(client_name__icontains=query)
    else:
        clients = Client.objects.all()
    
    return render(request, 'allclients.html', {'clients': clients, 'search': query})

def add_call(request):
    if request.method == 'POST':
        data = request.POST
        raw_time = data.get('time_taken')
        if raw_time.strip() == '':
            time_taken = None
        else:
            try:
                time_taken = float(raw_time)
            except ValueError:
                time_taken = None
        SupportCall.objects.create(
            client_name=data.get('client_name'),
            date=data.get('date'),
            subject=data.get('subject'),
            reported_by=data.get('reported_by'),
            responded_by=data.get('responded_by'),
            status=data.get('status'),
            time_taken=time_taken,
            solved_by=data.get('solved_by'),
            description=data.get('description')
        )
        return redirect('callhistory')

    return render(request, 'add_call.html')

def callhistory(request):
    status_filter = request.GET.get('status')
    
    if status_filter == "Pending":
        calls = SupportCall.objects.filter(status="Pending")
    elif status_filter == "Closed":
        calls = SupportCall.objects.filter(status="Closed")
    else:
        calls = SupportCall.objects.all()

    return render(request, 'callhistory.html', {'calls': calls, 'status_filter': status_filter})

def edit_call(request, call_id):
    call = get_object_or_404(SupportCall, id=call_id)

    if request.method == 'POST':
        call.client_name = request.POST['client_name']
        call.date = request.POST['date']
        call.subject = request.POST['subject']
        call.reported_by = request.POST['reported_by']
        call.responded_by = request.POST['responded_by']
        call.status = request.POST['status']
        call.time_taken = request.POST.get('time_taken')
        call.solved_by = request.POST['solved_by']
        call.description = request.POST['description']
        call.save()
        return redirect('callhistory')

    return render(request, 'add_call.html', {'call': call})

def delete_call(request, call_id):
    call = get_object_or_404(SupportCall, id=call_id)
    call.delete()
    return redirect('callhistory')
@role_required(['superadmin','admin'])
def add_payment(request):
    if request.method == "POST":
        client_id = request.POST.get("client")
        payment_mode = request.POST.get("payment_mode")
        paid_on = request.POST.get("paid_on")
        amount = request.POST.get("amount")
        paid_to = request.POST.get("paid_to")
        transaction_id = request.POST['transaction_id']
        description = request.POST.get("description")

        client_obj = Client.objects.get(id=client_id)

        AllPayments.objects.create(
            client=client_obj,
            payment_mode=payment_mode,
            paid_on=paid_on,
            paid_amount=amount,
            paid_to=paid_to,
            transaction_id=transaction_id,
            description=description
        )
        return redirect('all_payments')

    clients = Client.objects.all()
    return render(request, "addpayment.html", {"clients": clients})


@role_required(['superadmin','admin'])
def all_payments(request):
    payments = AllPayments.objects.select_related('client').order_by('-paid_on')
    return render(request, 'all_payments.html', {'payments': payments})
@role_required(['superadmin','admin'])
def edit_payment(request, pid):
    payment = get_object_or_404(AllPayments, id=pid)
    clients = Client.objects.all()

    if request.method == "POST":
        payment.client_id = request.POST.get('client')
        payment.payment_mode = request.POST.get('payment_mode')
        payment.paid_on = request.POST.get('paid_on')
        payment.paid_amount = request.POST.get('amount')
        payment.paid_to = request.POST.get('paid_to')
        payment.transaction_id = request.POST.get('transaction_id')
        payment.description = request.POST.get('description')
        payment.save()
        return redirect('all_payments')

    return render(request, 'addpayment.html', {
        'payment': payment,
        'clients': clients,
        'edit_mode': True
    })

@role_required(['superadmin','admin'])
def deletepayment(request, pid):
    payment = get_object_or_404(AllPayments, id=pid)
    payment.delete()
    return redirect('all_payments')


def add_branch(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_branches')
    else:
        form = BranchForm()
    return render(request, 'add_branch.html', {'form': form})

def all_branches(request):
    selected_client_id = request.GET.get('client')
    
    if selected_client_id and selected_client_id != 'all':
        branches = Branch.objects.filter(client__id=selected_client_id)
    else:
        branches = Branch.objects.all()

    clients = Client.objects.all()
    return render(request, 'all_branches.html', {
        'branches': branches,
        'clients': clients,
        'selected_client_id': selected_client_id or 'all'
    })
def edit_branch(request, id):  
    from .models import Branch 
    branch = get_object_or_404(Branch, id=id)

    if request.method == 'POST':
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            return redirect('all_branches')
    else:
        form = BranchForm(instance=branch)

    return render(request, 'add_branch.html', {
        'form': form,
        'edit_mode': True,
        'id': id
    })

def delete_branch(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    branch.delete()
    return redirect('all_branches')

@role_required(['superadmin'])
def adduser(request):
    if request.method == 'POST':
        form = AllUsersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allusers')
    else:
        form = AllUsersForm()

    return render(request, 'adduser.html', {'form': form})

@role_required(['superadmin'])
def allusers(request):
    query = request.GET.get('query', '')
    role = request.GET.get('role', '')

    users = AllUsers.objects.all()

    if query:
        users = users.filter(user_id__icontains=query)

    if role:
        users = users.filter(role=role)

    roles = AllUsers.objects.values_list('role', flat=True).distinct()

    return render(request, 'allusers.html', {
        'users': users,
        'query': query,
        'role': role,
        'roles': roles
    })
@role_required(['superadmin'])
def edituser(request, uid):
    user = AllUsers.objects.get(id=uid)
    if request.method == 'POST':
        form = AllUsersForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('allusers')
    else:
        form = AllUsersForm(instance=user)
    return render(request, 'adduser.html', {'form': form})
@role_required(['superadmin'])
def deleteuser(request, uid):
    user = AllUsers.objects.get(id=uid)
    user.delete()
    return redirect('allusers')


def login_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        try:
            user = AllUsers.objects.get(user_id=user_id, password=password)
            request.session['user_id'] = user.user_id
            request.session['role'] = user.role

            return redirect('Homepage')

        except AllUsers.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')
    return render(request, 'login.html')

def Logout_view(request):
    logout(request)
    return redirect('login')  
