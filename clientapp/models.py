from django.db import models

class Client(models.Model):
    client_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    client_code = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    url = models.URLField(blank=True)
    additional_link = models.URLField(blank=True, null=True)
    login_id = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    has_branches = models.BooleanField(default=False)
    strength = models.IntegerField(null=True, blank=True)
    payment_type = models.CharField(max_length=50)
    unit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.client_name
    
class SupportCall(models.Model):
    client_name = models.CharField(max_length=100)
    date = models.DateField()
    subject = models.CharField(max_length=200)
    reported_by = models.CharField(max_length=100)
    responded_by = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Closed', 'Closed')])
    time_taken = models.IntegerField(null=True, blank=True)
    solved_by = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return f"{self.client_name} - {self.subject}"

    
class AllPayments(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    payment_mode = models.CharField(max_length=50)
    paid_on = models.DateField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_to = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.client.client_name} - ₹{self.paid_amount} on {self.paid_on}"

class Branch(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    branch_name = models.CharField(max_length=100)
    branch_code = models.CharField(max_length=50)
    contact_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    weblink = models.URLField(blank=True)
    username = models.CharField(max_length=100)
    number_of_students = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.client.client_name} - {self.branch_name} ({self.client.name})"

class AllUsers(models.Model):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('admin', 'Admin'),
        ('superadmin', 'Super Admin'),
    ]

    user_id = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user_id} ({self.role})"
