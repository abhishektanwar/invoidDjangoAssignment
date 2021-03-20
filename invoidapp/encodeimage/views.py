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
	# ts = str(ts)
	return ts

def encrypt_AES_GCM(msg, secretKey):
	aesCipher = AES.new(secretKey, AES.MODE_GCM)
	ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
	return (ciphertext, aesCipher.nonce, authTag)

# secretKey = os.urandom(32)  # 256-bit random encryption key
# print("Encryption key:", binascii.hexlify(secretKey))
# msg = returnCurrentTimestamp()
# encryptedMsg = encrypt_AES_GCM(msg, secretKey)
# print("encryptedMsg", {
# 	'ciphertext': binascii.hexlify(encryptedMsg[0])
# })

@api_view(['GET','POST'])
@csrf_exempt
def imageEncode(request):
	if request.method == 'POST':
		dataFile = request.FILES['imageFile']
		print(dataFile.name.split('.')[1])
		encoded_string = base64.b64encode(dataFile.read())
		base64_str = encoded_string.decode('utf-8')
		hash_obj = hashlib.md5(encoded_string)
		md5_hash = hash_obj.hexdigest()
		current_timestamp = returnCurrentTimestamp()
		secretKey = os.urandom(32)  # 256-bit random encryption key
		encryptedMsg = encrypt_AES_GCM(current_timestamp, secretKey)
		AES_encrypted_timestamp = binascii.hexlify(encryptedMsg[0])
		print("encryptedMsg",AES_encrypted_timestamp)
		return JsonResponse(status = 200, data = {"base64_str":base64_str,"md5":md5_hash,"timestamp":current_timestamp.decode('utf-8'),"AES_encrypted_timestamp":AES_encrypted_timestamp.decode('utf-8')})
	
	return render(request,'upload.html')