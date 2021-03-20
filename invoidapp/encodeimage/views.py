from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import base64

# Create your views here.
@api_view(['GET','POST'])
@csrf_exempt
def imageEncode(request):
	if request.method == 'POST':
		dataFile = request.FILES['imageFile']
		print(dataFile.name)
		encoded_string = base64.b64encode(dataFile.read())
		print(encoded_string.decode('utf-8'))
		return JsonResponse({'info':'Django','name':"Abhishek","Str":encoded_string.decode('utf-8')})
	
	# return JsonResponse({'info':'Django React','name':"Abhishek"})
	return render(request,'upload.html')