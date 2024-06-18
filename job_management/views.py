from rest_framework import generics, status
from rest_framework.response import Response
from .models import Job,Application
from .serializer import JobSerializer,ApplicationSerializer,ApplicationListSerializer
from rest_framework import serializers
import os
from django.conf import settings


def handle_validation_error(e):
   
    response={}
   
    try:
        error_message = str(e).split("ErrorDetail(string='")[1].split("'")[0]

        return Response(
                {"message": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )
     
           
    except Exception as e:
        return Response(
            
           {"message":"Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
 
        )

class JobCreateAPIView(generics.CreateAPIView):
    serializer_class = JobSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            job_data = serializer.validated_data
            job = Job.objects.create(**job_data)
            return Response(JobSerializer(job).data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        
class ApplicationCreateAPIView(generics.GenericAPIView):
    serializer_class = ApplicationSerializer

    def post(self, request, *args, **kwargs):
        import pdb;pdb.set_trace()
        # Validate file format
        resume = request.FILES.get('resume')
        if resume and not resume.name.endswith('.pdf'):
            return Response({"resume": "The resume file must be in PDF format."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate the rest of the data
        serializer = self.get_serializer(data=request.data)
        try:

                serializer.is_valid(raise_exception=True)
                application_data = serializer.validated_data
                
                # Save the file locally
                if resume:
                    resume_name = resume.name
                    resume_path = os.path.join(settings.MEDIA_ROOT, 'resumes', resume_name)
                    os.makedirs(os.path.dirname(resume_path), exist_ok=True)
                    with open(resume_path, 'wb+') as destination:
                        for chunk in resume.chunks():
                            destination.write(chunk)

                job_id = int(request.data.get('job_id')) 
                job=Job.objects.get(id=job_id)
            
            
                application_data['job'] = job
                application = Application.objects.create(**application_data)   
                application_data['resume'] = os.path.join('resumes', resume_name)
                
             
                application = Application.objects.create(**application_data)
                return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
                return handle_validation_error(e)
        except Job.DoesNotExist:
            return Response({"message": "Job not found."}, status=status.HTTP_404_NOT_FOUND)
        

class JobUpdateAPIView(generics.UpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def put(self, request, *args, **kwargs):
        job_id = kwargs.get('pk')
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance=job, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        

class JobListAPIView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class ApplicationListAPIView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationListSerializer


class JobDeleteAPIView(generics.DestroyAPIView):
    queryset = Job.objects.all()

    def delete(self, request, *args, **kwargs):
        job_id = self.kwargs.get('id')
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)

        job.delete()
        return Response({"message": "Job deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

class ApplicationDetailsAPIView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = ApplicationSerializer

    def get(self, request, *args, **kwargs):
        application_id = self.kwargs.get('pk')

        try:
            application = Application.objects.get(id=application_id)
            serializer = ApplicationListSerializer(application)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Application.DoesNotExist:
            return Response({"error": "Application not found."}, status=status.HTTP_404_NOT_FOUND)

      
       
            
            
            
       