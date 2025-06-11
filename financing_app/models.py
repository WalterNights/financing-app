from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('rol', 'user')

        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)
    
    
class User(AbstractUser):
    ROL_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='user')
    user_id = models.CharField(max_length=20, unique=True) #Cedula de Ciudadanía
    
    objects = UserManager()

    def __str__(self):
        return f"{self.username} - {self.user_id}"
 
 
class Career(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
      
    
class CareerPeriodPricing(models.Model):
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    period = models.CharField(max_length=50)
    tuition_fee = models.DecimalField(max_digits=12, decimal_places=2) #Valor Matrícula
    base_discount = models.FloatField()
    deadline = models.DateField()
    penalty = models.FloatField()
    
    def get_applicable_discount(self, request_data: date):
        """
        Check if the discount is applicable based on the current date and the deadline.
        """
        if request_data <= self.deadline:
            return self.base_discount
        else:
            return max(0, self.base_discount - self.penalty)
        
    def get_discount_value(self, request_data: date) -> float:
        """
        Calculate the discount value based on the tuition fee and the applicable discount.
        """
        applicable_discount = self.get_applicable_discount(request_data)
        return round(self.tuition_fee * (1 - applicable_discount / 100), 2)

    def __str__(self):
        return f"{self.career.name} - {self.period}"
    

class FinancingRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tuition_value = models.ForeignKey(CareerPeriodPricing, on_delete=models.CASCADE) #Valor Matrícula
    date_initial_period = models.DateField() #Fecha de Inicio del Período
    date_start = models.DateTimeField(auto_now_add=True) #Fecha de Inicio del Financiamiento
    
    #Financing Date Fields
    down_payment = models.DecimalField(max_digits=12, decimal_places=2) #Pago Inicial
    interest_rate = models.FloatField(default=1.8) #Tasa de Interés
    administration_fee = models.FloatField(default=5.0) #Gastos Administrativos
    number_installments = models.IntegerField(default=6) #Número de Cuotas
    
    #Applicable Discount Field
    discount_applied = models.FloatField(default=0.0) #Descuento Aplicado
    
    @property
    def tuition_fee_without_discount(self):
        return self.tuition_value.tuition_fee
    
    @property
    def tuition_fee_with_discount(self):
        return self.tuition_value.get_discount_value(self.date_start.date())
    
    @property
    def financed_value(self):
        return self.tuition_fee_with_discount - self.down_payment
        
    @property
    def calculate_payment_plan(self):
        i = self.interest_rate / 100
        n = self.number_installments
        value = float(self.financed_value)
        
        if i == 0:
            fee = value / n
        else:
            fee = value * ((i * (1 + i) ** n) / (1 + i) ** n -1)
            
        admin_fee = fee * (self.administration_fee / 100)
        total_fee = round(fee + admin_fee, 2)
    
        return {
            "value_financed": round(value, 2),
            "monthly_fee": round(fee, 2),
            "administration_fee ": round(admin_fee, 2),
            "total_fee": total_fee,
            "number_fee": n
        }
    
    def __str__(self):
        return f"Request by {self.user} for {self.tuition_value.career.name} - {self.tuition_value.period}"