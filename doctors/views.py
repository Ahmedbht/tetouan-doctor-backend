from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import Doctor, Booking, TimeSlot

# Serializers
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'

# ========== CLIENT ==========

# كيجيب كل doctors
@api_view(['GET'])
def get_doctors(request):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)

# كيحفظ RDV جديد
@api_view(['POST'])
def create_booking(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        # نحجبو الـ slot
        slot_id = request.data.get('slot_id')
        if slot_id:
            TimeSlot.objects.filter(id=slot_id).update(is_booked=True)
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# كيجيب slots متاحة ديال doctor معين
@api_view(['GET'])
def get_slots(request, doctor_id):
    slots = TimeSlot.objects.filter(doctor_id=doctor_id, is_booked=False)
    serializer = TimeSlotSerializer(slots, many=True)
    return Response(serializer.data)

# ========== DOCTOR ==========

# login ديال doctor
@api_view(['POST'])
def doctor_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        # نجيبو doctor مرتبط بـ user
        try:
            doctor = Doctor.objects.get(email=user.email)
            return Response({'token': token.key, 'doctor_id': doctor.id, 'name': doctor.name})
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=404)
    return Response({'error': 'Invalid credentials'}, status=401)

# doctor كيضيف slot جديد
@api_view(['POST'])
def add_slot(request):
    serializer = TimeSlotSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# doctor كيشوف RDV ديالو
@api_view(['GET'])
def get_my_bookings(request, doctor_id):
    bookings = Booking.objects.filter(doctor_id=doctor_id)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)