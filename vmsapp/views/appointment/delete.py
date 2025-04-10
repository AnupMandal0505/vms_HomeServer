from rest_framework.response import Response
from rest_framework import status
from authuser.models import Appointment,AdditionalVisitor
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated



class BaseAuthentication(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]


class DeleteAppointmentView(BaseAuthentication):
    """
    Delete an existing appointment.
    """
    def list(self, request):
        if not request.GET.get("visitorId"):
            return Response({"error": "Missing 'id' parameter"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            appointment = Appointment.objects.get(id=request.GET.get("visitorId"))
            AdditionalVisitor.objects.filter(participants=appointment).delete()
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        appointment.delete()
        return Response({"message": "Appointment deleted successfully"}, status=status.HTTP_200_OK)

