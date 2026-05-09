from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)
    experience = models.CharField(max_length=50)
    rating = models.FloatField(default=5.0)
    disponible = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name

class Booking(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    service = models.CharField(max_length=100)
    date = models.DateField()
    time = models.CharField(max_length=10)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.doctor.name} - {self.date}"

class TimeSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length =10)
    is_booked = models.BooleanField(default =False)
    def __str__(self):
        return f"{self.doctor.name} - {self.date} - {self.time}"
 

