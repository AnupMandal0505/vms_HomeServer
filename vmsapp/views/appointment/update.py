from rest_framework.response import Response
from rest_framework import status
from authuser.models import Appointment
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated




class BaseAuthentication(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]


# http://127.0.0.1:8000/api/appointments/update-appointments/
class AppointmentUpdateView(BaseAuthentication):
    def create(self, request):
        visitor_id = request.data.get('visitor_id')
        new_description = request.data.get('remark')
        if not visitor_id:
            return Response({'error': 'visitor_id and remark are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            visitor_description = Appointment.objects.get(id=visitor_id)
            visitor_description.description = new_description
            visitor_description.save()
            return Response({'success': 'Remark updated successfully'}, status=status.HTTP_200_OK)

        except Appointment.DoesNotExist:
            return Response({'error': 'Visitor remark not found'}, status=status.HTTP_404_NOT_FOUND)
        







class CallVisitorView(BaseAuthentication):
    def list(self, request):
        visitor_id = request.query_params.get('visitor_id')  # Extract from query
        action = request.query_params.get('action')  # Extract action
        # print(visitor_id,action)
        if not visitor_id or not action:
            return Response({'error': 'visitor_id and call field are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            call_visi = Appointment.objects.get(id=visitor_id)
            call_visi.status = action
            call_visi.save()
            return Response({'success': 'calling....'}, status=status.HTTP_200_OK)

        except Appointment.DoesNotExist:
            return Response({'error': 'Visitor action not found'}, status=status.HTTP_404_NOT_FOUND)
   