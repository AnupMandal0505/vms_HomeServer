from rest_framework.response import Response
from rest_framework import status
from authuser.models import Appointment,AdditionalVisitor
from vmsapp.serializers.AppointmentSerializers import AppointmentSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination





class BaseAuthentication(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]



class CustomPagination(PageNumberPagination):
    page_size = None
    page_size_query_param = 'page_size'
    max_page_size = 100

# http://127.0.0.1:8000/api/appointments/get-appointments/?status=PENDING&client=j


# def get_queryset(self):
#         queryset = super().get_queryset()
#         search = self.request.query_params.get("search")
#         date = self.request.query_params.get("date")

#         if search:
#             queryset = queryset.filter(visitor_name__icontains=search)
#         if date:
#             queryset = queryset.filter(date=date)

#         return queryset
class AppointmentListView(BaseAuthentication):
    """
    ViewSet for retrieving appointments with optional filtering.
    Includes related additional visitors.
    """
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        query_params = self.request.GET.dict()
        queryset = Appointment.objects.prefetch_related("additional_visitors").all()  #  Fix here!
        # print(queryset)
        for field, value in query_params.items():
            if hasattr(Appointment, field):
                queryset = queryset.filter(**{field: value})
        return queryset

    def get_serializer(self, *args, **kwargs):
        """Manually define `get_serializer()`."""
        return self.serializer_class(*args, **kwargs)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # If ?all=true → no pagination
        if request.GET.get('all') == 'true':
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        # If page_size is present → apply pagination
        paginator = CustomPagination()
        page_size = request.GET.get('page_size')
        if page_size:
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Default fallback: return all (or you can raise error if preferred)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




from django.http import JsonResponse
from collections import OrderedDict

class Get_unique_visitor_list(BaseAuthentication):
    def list(self,request):
        # Step 1: Get Appointment data
        appointment_data = Appointment.objects.values('visitor_name', 'phone')
        appointment_list = [
            {"name": a["visitor_name"], "phone": a["phone"]}
            for a in appointment_data
        ]
        
        # Step 2: Get AdditionalVisitor data
        additional_data = AdditionalVisitor.objects.select_related('participants').values(
            'name', 'participants__phone'
        )
        additional_list = [
            {"name": a["name"], "phone": a["participants__phone"]}
            for a in additional_data
        ]

        # Step 3: Combine & make unique based on (name, phone)
        combined = appointment_list + additional_list
        seen = set()
        unique_data = []
        for item in combined:
            key = (item["name"], item["phone"])
            if key not in seen:
                seen.add(key)
                unique_data.append(item)

        return JsonResponse(unique_data, safe=False)