from rest_framework.response import Response
from rest_framework import status
from authuser.models import Appointment,AdditionalVisitor,RegularVisitor,GMTraffic
from vmsapp.serializers.AppointmentSerializers import AppointmentSerializer,RegularVisitorSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound
from django.core.paginator import EmptyPage
from django.db.models import Q
from django.utils import timezone





class BaseAuthentication(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]




class CustomPagination(PageNumberPagination):
    page_size = None
    page_size_query_param = 'page_size'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        self.page_size = self.get_page_size(request)
        paginator = self.django_paginator_class(queryset, self.page_size)

        page_number = request.query_params.get(self.page_query_param, 1)

        #  Invalid page numbers (like 0, -1, a, etc)
        try:
            if int(page_number) < 1:
                raise NotFound({"detail": "Page number must be 1 or greater."})
        except ValueError:
            raise NotFound({"detail": "Invalid page number format."})

        #  Catch out-of-range page numbers
        try:
            self.page = paginator.page(page_number)
        except EmptyPage:
            raise NotFound({"detail": "Invalid page number. Out of range."})

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        total_pages = self.page.paginator.num_pages  #  Add total_pages in response
        return Response({
            'count': self.page.paginator.count,
            'total_pages': total_pages,
            'next': self._add_page_param(self.get_next_link()),
            'previous': self._add_page_param(self.get_previous_link()),
            'results': data
        })

    def _add_page_param(self, url):
        if url and 'page=' not in url:
            return f"{url}&page=1"
        return url



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
        print(request.GET)
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
        print("data",serializer.data)
        return Response(serializer.data)





class GetRegularVisitor(BaseAuthentication):
    def list(self, request):
        phone = request.query_params.get('phone')
        # if not phone:
        #     return Response({"error": "Phone number is required"}, status=400)

        try:
            if phone:
                # visitors = RegularVisitor.objects.filter(name__iexact=phone)
                visitors = RegularVisitor.objects.filter(Q(name__icontains=phone) | Q(phone__icontains=phone))
            else:
                            # If phone not provided, filter all Inoffice visitors
                visitors = RegularVisitor.objects.filter(v_type="IN-OFFICE")
            return Response({"RES":True,"data":RegularVisitorSerializer(visitors, many=True).data})
        except RegularVisitor.DoesNotExist:
            return Response({"ERR": "Visitor not found"}, status=404)

from datetime import date

    
import logging

logger = logging.getLogger(__name__)

class GetGmBussyMode(BaseAuthentication):
    def list(self, request):
        # Get the gm_id from the request
        user = request.user
      
        try:
            logger.info("✅ Status updated successfully!1w")

            # Check GMTraffic for the given GM
            gm_traffic = GMTraffic.objects.get(gm=user.gm)
            logger.info("✅ Status updated successfully!1",gm_traffic)

            # If GMTraffic status is True, return 'busy'
            if gm_traffic.status:
                return Response({'status': 'busy'})
            
            # If GMTraffic status is False, check today's appointments
            # today = timezone.now().date()
            today = date.today()

            logger.info("✅ Status updated successfully!2",today)

            has_progress = Appointment.objects.filter(
                gm=user.gm,
                date=today,
                status__iexact="progress"
            ).exists()
            logger.info("✅ Status updated successfully!3",has_progress)

            # If there's an in-progress appointment today, return 'progress'
            if has_progress:
                return Response({'status': 'progress'})
            
            # If no in-progress appointments, return 'available'
            return Response({'status': 'available'})

        except GMTraffic.DoesNotExist:
            return Response({'error': 'GM Traffic record not found'}, status=404)


from django.shortcuts import render




def audio_call(request):
    return render(request, 'index.html', {
        'token': "b3d7ac56a9c1bb36e7b52fd28622da55c2edf1fe",
        'user_id': "81ff0ca0-4fc8-42a8-a1ec-e7f9e5944e63"  # Pass target user ID dynamically

    })

def audio_call2(request):
    # Assuming you want to send the token dynamically (you can pass the token or user-related data here)
    # user_token = request.user.auth_token.key if request.user.is_authenticated else None

    return render(request, 'check.html', {
        'token': "56b2abd4d84331d0149fbaaeac7afe7b799cf50d",
        'user_id': "d42a6d4f-1a0a-42f5-85af-08cd521e56c3"  # You can make this dynamic
    })
