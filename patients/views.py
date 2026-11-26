from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count
from rest_framework.views import APIView
from django.shortcuts import  get_object_or_404
from patients.models import Patient
from patients.serializers import PatientSerializer
from django.db.models import Q
class PatientListCreate(APIView):
    def post(self, request):
        serializer_instance = PatientSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)
class PatientSearch(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = request.query_params.get('search')
        patients = Patient.objects.filter(
            Q(patient_name__icontains=data) |
            Q(doctor_name__icontains=data)
            )
        serializer_instance = PatientSerializer(patients,many=True)
        return Response(serializer_instance.data,status=status.HTTP_200_OK)
class ViewAppointment(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        p = get_object_or_404(Patient, patient_id=pk)
        serializer_instance = PatientSerializer(p)
        return Response(serializer_instance.data,status=status.HTTP_200_OK)
class PatientUpdateAppointment(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk):
        p = get_object_or_404(Patient,patient_id=pk)
        serializer_instance = PatientSerializer(instance=p,data=request.data,partial=True)
        if serializer_instance.is_valid():
            serializer_instance.save()
            response = {
                "message": "Appointment date updated successfully"}
            return Response(response,status=status.HTTP_200_OK)
        else:
            return Response(serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST )
class PatientDelete(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        p = get_object_or_404(Patient,patient_id=pk)
        p.delete()
        return Response({"message": "Patient deleted successfully"},status=status.HTTP_200_OK
        )
class DepartmentSummary(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        total_patients = Patient.objects.count()
        average_age = Patient.objects.aggregate(average_age=Avg('age'))
        department_count = Patient.objects.values('department').annotate(total=Count('patient_id'))
        response = {"total_patients": total_patients,"average_age": average_age['average_age'],"department_summary": department_count}
        return Response(response,status=status.HTTP_200_OK)
