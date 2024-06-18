from rest_framework import serializers
from .models import Job,Application
from datetime import datetime
from django.utils import timezone

class JobSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255,error_messages={
        "blank": "Title cannot be blank.",
        "required": "Title is required"
    })
    description= serializers.CharField(max_length=255,error_messages={
        "blank": "Description cannot be blank.",
        "required": "Description cannot be blank."
    })
    location= serializers.CharField(max_length=255,error_messages={
        "blank": "Location cannot be blank.",
        "required": "Location cannot be blank."
    })
    department= serializers.CharField(max_length=255,error_messages={
        "blank": "Department cannot be blank.",
        "required": "Department cannot be blank."
    })
    date_posted= serializers.DateTimeField(default=datetime.now(),error_messages={
        "blank": "Date posted cannot be blank.",
        "required": "Date posted cannot be blank."
    })
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'location', 'department', 'date_posted']
    
    def validate_date_posted(self, value):
        if value > timezone.now():
            raise serializers.ValidationError("The date posted cannot be in the future.")
        return value
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.location = validated_data.get('location', instance.location)
        instance.department = validated_data.get('department', instance.department)
        instance.date_posted = validated_data.get('date_posted', instance.date_posted)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
    

class ApplicationSerializer(serializers.Serializer):
    applicant_name = serializers.CharField(max_length=255,error_messages={
        "required": "Applicant name cannot be blank."
    })
    email= serializers.EmailField(error_messages={
       
        "required": "Email cannot be blank."
    })
    phone_number= serializers.CharField(max_length=10,error_messages={
      
        "required": "Phone number cannot be blank.",
        "max_length": "Phone number cannot be more than 10 characters."
    })
    application_date= serializers.DateTimeField(default=datetime.now(),error_messages={
       
        "required": "Application date cannot be blank."
    })
    class Meta:
        model = Application
        fields = ['id', 'applicant_name', 'email', 'phone_number', 'resume', 'application_date']
       

    def validate_application_date(self, value):
        if value > timezone.now():
            raise serializers.ValidationError("The application date cannot be in the future.")
        return value
    

class ApplicationListSerializer(serializers.ModelSerializer):
    job = serializers.StringRelatedField()

    class Meta:
        model = Application
        fields = ['id', 'applicant_name', 'email', 'phone_number', 'resume', 'job', 'application_date']
  
