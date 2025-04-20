from django.db import models
from authuser.models import User
from uuid import uuid4
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Modification(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_created_by",limit_choices_to={'groups__name__in': ['PA', 'SECRETARY']})
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_updated_by")  # User who last updated the appointment
    updated_at = models.DateTimeField(auto_now=True)  
    
    class Meta:
        abstract = True 



class Appointment(Modification):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    visitor_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20,default="pending")
    
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_appointments",limit_choices_to={'groups__name': 'SECRETARY'}
    ) 

    gm = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="gm_appointments",limit_choices_to={'groups__name': 'GM'}
    ) 
    company_name = models.CharField(max_length=100,default="NA")
    company_address = models.CharField(max_length=100,default="NA")
    purpose_of_visit = models.CharField(max_length=100,default="NA")
    visitor_img = models.FileField(upload_to='visitor_img/%Y/%m/%d/',blank=True) 
    v_type = models.CharField(max_length=100, default="OUTSIDE",blank=True,null=True)


    def save(self, *args, **kwargs):
        # Convert text fields to uppercase
        if self.visitor_name:
            self.visitor_name = self.visitor_name.upper()
        if self.company_name:
            self.company_name = self.company_name.upper()
        if self.company_address:
            self.company_address = self.company_address.upper()
        if self.purpose_of_visit:
            self.purpose_of_visit = self.purpose_of_visit.upper()
        if self.v_type:
            self.v_type = self.v_type.upper()
        super().save(*args, **kwargs)
    class Meta:
        db_table = "appointment_table"

    def __str__(self):
        return f"{self.visitor_name} - {self.date}"
    
class AdditionalVisitor(models.Model):
    name = models.CharField(max_length=100)
    participants = models.ForeignKey(Appointment,on_delete=models.CASCADE, related_name="additional_visitors",default=None)  # Multiple participants
    img = models.FileField(upload_to='additional_visitor_img/%Y/%m/%d/', blank=True)  # 'product_images/' is the folder where the image will be saved

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.upper()  # Convert name to uppercase before saving
        super().save(*args, **kwargs)  # Call the original save method

    class Meta:
            db_table = "additional_visitor_table"
            
    def __str__(self):
        return self.name
    
@receiver(post_delete, sender=AdditionalVisitor)
def delete_file(sender, instance, **kwargs):
    if instance.img:
        instance.img.delete(save=False)
    




class RegularVisitor(Modification):
    name = models.CharField(max_length=100)
    v_type = models.CharField(max_length=100, default="outside",blank=True,null=True)
    phone = models.CharField(max_length=15,unique=True)
    email = models.EmailField(blank=True,null=True)
    company_name = models.CharField(max_length=100,blank=True,null=True)
    company_address = models.CharField(max_length=255,blank=True,null=True)
    image = models.FileField(upload_to='regular_visitor/%Y/%m/%d/',blank=True,null=True) 

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.upper()
        if self.v_type:
            self.v_type = self.v_type.upper()
        if self.company_name:
            self.company_name = self.company_name.upper()
        if self.company_address:
            self.company_address = self.company_address.upper()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "regular_visitor_table"

    def __str__(self):
        return f"{self.name} ({self.phone})"
    