from rest_framework.response import Response
from rest_framework import status
from authuser.models import Appointment,AdditionalVisitor,RegularVisitor
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction  #  Import this at top
# from django.conf import settings
# from django.template.loader import render_to_string
# from django.core.mail import EmailMultiAlternatives
from vmsapp import tasks


import logging

logger = logging.getLogger(__name__)

class BaseAuthentication(viewsets.ViewSet):
    # def list(self, request):
    #     # token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    #     # print(token)  # Token ko print karega
    #     # ... baaki code
    #     return True
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]



class AppointmentCreateView(BaseAuthentication):
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        print(request.data)
        
        try:
            data = request.data.copy()
            files = request.FILES

            with transaction.atomic():  #  Start Atomic Transaction
                #  Extract Additional Visitors Data
                additional_visitors = []
                index = 0
                while f"additional_visitor[{index}][name]" in data:
                    additional_visitors.append({
                        "name": data[f"additional_visitor[{index}][name]"],
                        "img": files.get(f"additional_visitor[{index}][img]")  # Handle file upload
                    })
                    index += 1

                if request.user.groups.filter(name="SECRETARY").exists():

                    #  Create Main Appointment By SECRETARY
                    appointment_data = Appointment.objects.create(
                        visitor_name=data.get("visitor_name"),
                        email=data.get("email"),
                        phone=data.get("phone"),
                        date=data.get("date"),
                        gm=request.user.gm,
                        assigned_to=request.user,
                        company_name=data.get("company_name"),
                        company_address=data.get("company_address"),
                        purpose_of_visit=data.get("purpose_of_visit"),
                        visitor_img=files.get("visitor_img"),
                        v_type=data.get("visitor_type"),
                        created_by=request.user
                    )
                else:
                    logger.info(f"🟢 [INFO] Processing data: {request.user.secretary.id}")

                    #  Create Main Appointment By PA
                    appointment_data = Appointment.objects.create(
                        visitor_name=data.get("visitor_name"),
                        email=data.get("email"),
                        phone=data.get("phone"),
                        date=data.get("date"),
                        assigned_to=request.user.secretary,
                        company_name=data.get("company_name"),
                        company_address=data.get("company_address"),
                        purpose_of_visit=data.get("purpose_of_visit"),
                        visitor_img=files.get("visitor_img"),
                        v_type=data.get("visitor_type"),
                        created_by=request.user
                    )

                #  Prepare Additional Visitors List for Bulk Create
                additional_visitors_list = []
                for visitor in additional_visitors:
                    additional_visitors_list.append(
                        AdditionalVisitor(
                            participants=appointment_data,  # ForeignKey relation
                            name=visitor['name'],
                            img=visitor['img']
                        )
                    )

                #  Bulk Create Additional Visitors
                if additional_visitors_list:
                    AdditionalVisitor.objects.bulk_create(additional_visitors_list)

                #  Serialize only names
            additional_visitors_name = [visitor.name for visitor in additional_visitors_list]

            if request.user.groups.filter(name="PA").exists():

                tasks.create_appointment_mail.delay(
                    appointment_data.visitor_name,
                    appointment_data.email,
                    appointment_data.date,
                    f"{request.user.secretary.first_name} {request.user.secretary.last_name}",
                    additional_visitors_name,
                    "Appointment Confirmation",
                    "message"
                )

            #  Return success response if everything went fine
            return Response({"message": "Appointment and Additional Visitors created successfully."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(" Error Occurred:", e)
            logger.info(f"🟢 Error: {e}")

            return Response({"message": "Appointment Not created successfully."}, status=status.HTTP_400_BAD_REQUEST)
        


class AppointmentForwardGmView(BaseAuthentication):

    def create(self, request):
        try:
            appoint=Appointment.objects.get(id=request.data.get("id"))
            appoint.gm=request.user.gm
            appoint.save()
        
            #  Return success response if everything went fine
            return Response({"message": "Appointment forward successfully."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(" Error Occurred:", e)
            return Response({"message": "Appointment forward fail successfully."}, status=status.HTTP_400_BAD_REQUEST)
        




class RegularVisitorCreate(BaseAuthentication):
    def create(self, request):
        print(request.POST)
        try:
            data = request.data.copy()
            files = request.FILES
            if RegularVisitor.objects.filter(phone=data.get('phone')).exists():
                return Response({"ERR": False, "msg": "Already Registered Phone"}, status=status.HTTP_200_OK)
            
            RegularVisitor.objects.create(
                name=data.get('name'),
                v_type=data.get('v_type', 'outside'),
                phone=data.get('phone'),
                email=data.get('email'),
                company_name=data.get('company_name', 'Na'),
                company_address=data.get('company_address', 'NA'),
                image=files.get("visitor_img"),
                created_by=request.user            )
            return Response({"RES": True}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"error": False}, status=status.HTTP_400_BAD_REQUEST)