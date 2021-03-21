from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import base64
import hashlib
import datetime
from Crypto.Cipher import AES
import binascii, os
# Create your views here.

def returnCurrentTimestamp():
	ct = datetime.datetime.now()
	ts = ct.timestamp()
	ts = bytes(str(ts),'utf-8')
	return ts

def encrypt_AES_GCM(msg, secretKey):
	aesCipher = AES.new(secretKey, AES.MODE_GCM)
	ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
	return (ciphertext, aesCipher.nonce, authTag)


@api_view(['GET','POST'])
@csrf_exempt
def imageEncode(request):
	if request.method == 'POST':
		dataFile = request.FILES['files']

		# check if uploaded file has valid extension
		file_extension = dataFile.name.split('.')[1]
		print(file_extension)
		allowed_file_types = ['jpeg','jpg','png']
		if(file_extension not in allowed_file_types):
			return JsonResponse(status = 400 , data = {"message":"file type not supported"})
		
		# base64 encryption
		encoded_string = base64.b64encode(dataFile.read())
		base64_str = encoded_string.decode('utf-8')

		# md5 hash generation
		hash_obj = hashlib.md5(encoded_string)
		md5_hash = hash_obj.hexdigest()

		# AES encryption of current timestamp
		current_timestamp = returnCurrentTimestamp()
		secretKey = os.urandom(32)  # 256-bit random encryption key
		encryptedMsg = encrypt_AES_GCM(current_timestamp, secretKey)
		AES_encrypted_timestamp = binascii.hexlify(encryptedMsg[0])
				
		return JsonResponse({"base64_str":base64_str,"md5":md5_hash,"timestamp":current_timestamp.decode('utf-8'),"AES_encrypted_timestamp":AES_encrypted_timestamp.decode('utf-8')})
	
	return render(request,'upload.html')