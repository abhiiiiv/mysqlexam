from rest_framework import serializers
from  datetime import datetime
from patients.models import Patient
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['patient_id']
    def validate(self, validated_data):
        age = validated_data['age']
        if age <= 0:
            raise serializers.ValidationError("Age must be a positive number.")
        appointment_date = validated_data['appointment_date']
        todays_date = datetime.now().date()
        if appointment_date < todays_date:
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        return validated_data