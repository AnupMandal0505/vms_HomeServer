from rest_framework.response import Response
from rest_framework import status
from authuser.models import Appointment,AdditionalVisitor,RegularVisitor
from vmsapp.serializers.AppointmentSerializers import AppointmentSerializer,RegularVisitorSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound
from django.core.paginator import EmptyPage





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
            print(serializer.data)
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
                visitors = RegularVisitor.objects.filter(phone=phone)
            else:
                # If phone not provided, filter all Inoffice visitors
                visitors = RegularVisitor.objects.filter(v_type="IN OFFICE")
            return Response({"RES":True,"data":RegularVisitorSerializer(visitors, many=True).data})
        except RegularVisitor.DoesNotExist:
            return Response({"ERR": "Visitor not found"}, status=404)


# from django.http import JsonResponse
# from collections import OrderedDict
# from django.conf import settings

# class Get_unique_visitor_list(BaseAuthentication):
#     def list(self,request):
#         # Step 1: Get Appointment data
#         appointment_data = Appointment.objects.values('visitor_name', 'phone')
#         appointment_list = [
#             {"name": a["visitor_name"], "phone": a["phone"]}
#             for a in appointment_data
#         ]
        
#         # Step 2: Get AdditionalVisitor data
#         additional_data = AdditionalVisitor.objects.select_related('participants').values(
#             'name', 'participants__phone'
#         )
#         additional_list = [
#             {"name": a["name"], "phone": a["participants__phone"]}
#             for a in additional_data
#         ]

#         # Step 3: Combine & make unique based on (name, phone)
#         combined = appointment_list + additional_list
#         seen = set()
#         unique_data = []
#         for item in combined:
#             key = (item["name"], item["phone"])
#             if key not in seen:
#                 seen.add(key)
#                 unique_data.append(item)

#         return JsonResponse(unique_data, safe=False)


# class Get_unique_visitor_list(BaseAuthentication):
#     def list(self, request):
#         # Step 1: Get Appointment data
#         appointment_data = Appointment.objects.values('visitor_name', 'phone', 'visitor_img')
#         appointment_list = [
#             {
#                 "name": a["visitor_name"],
#                 "phone": a["phone"],
#                 "img": f"{settings.API_BASE_URL}/{a['visitor_img']}" if a["visitor_img"] else None
#             }
#             for a in appointment_data
#         ]
        
#         # Step 2: Get AdditionalVisitor data
#         additional_data = AdditionalVisitor.objects.select_related('participants').values(
#             'name', 'img', 'participants__phone'
#         )
#         additional_list = [
#             {
#                 "name": a["name"],
#                 "phone": a["participants__phone"],
#                 "img": f"{settings.API_BASE_URL}/{a['img']}" if a["img"] else None
#             }
#             for a in additional_data
#         ]

#         # Step 3: Combine & make unique based on (name, phone)
#         combined = appointment_list + additional_list
#         seen = set()
#         unique_data = []
#         for item in combined:
#             key = (item["name"], item["phone"])
#             if key not in seen:
#                 seen.add(key)
#                 unique_data.append(item)

#         return JsonResponse(unique_data, safe=False)
    

