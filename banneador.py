#-*- coding: utf8 -*-
import os
import time
from PIL import Image, ImageFilter
from threading import Timer
import tweepy
import sys
#import os
os.system("uname -a")

# Importamos las credenciales de @watchbot_ (CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
import config
print "Comenzamos"

auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_KEY, config.ACCESS_SECRET)
api = tweepy.API(auth)
print "Creando el objeto Twitter"
min = 0
def imgReloj(m, h):
		d = os.getcwd()
		print "Actualizando Banner... "
		#print "Minutos: %s.png" % m
		#print "Horas: %s.png" % h
		fondo = Image.open(d+"/images/fondo.png")
		#minutos = Image.open("%s.png" % s)
		minutos = Image.open("images/%s/m%s.png" % (d,m))
		horas = Image.open("images/%s/%s.png" % (d,h))
		reloj = Image.open(d+"/images/reloj.png")
		offset = (0,0)
		
		print fondo.format, fondo.size, fondo.mode
		print minutos.format, minutos.size, minutos.mode
		print horas.format, horas.size, horas.mode
		print reloj.format, reloj.size, reloj.mode

		fondo.paste(minutos, offset, mask=minutos)
		fondo.paste(horas, offset, mask=horas)
		fondo.paste(reloj, offset, mask=reloj)
		fondo.save(d+"/Out.png")
		return d+"/Out.png"

def reloj():
	print "Creando el reloj"
	global min
	h = int(time.strftime("%I"))
	H = int(time.strftime("%H"))
	m = int(time.strftime("%M"))
	ts = int(time.time())
	s = int(m/5)*5
	print "¿Que hora es?"
	print "Son las %s y %s" %(h, s)
	if min != s:
		try:
			print "Intentando actualizar el cover"
			api.update_profile_banner(imgReloj(s, h))
			# Mensajes que se lanzan cuando se cumple la hora.
			if H == 10:
				api.update_status("Son las %s y 0%s #%s, ¿Has rellenado ya tu botella de agua!" %(H, s, ts))
			elif H == 12:
				api.update_status("Son las %s y 0%s #%s, Tu botella tendría que estar a la mitad!" %(H, s, ts))
			elif H == 14:
				api.update_status("Son las %s y 0%s #%s, Deberías de estar rellenando la botella nº2!" %(H, s, ts))
			elif H == 16:
				api.update_status("Son las %s y 0%s #%s, Tu segunda botella debería ir por la mitad!" %(H, s, ts))
			elif H == 18:
				api.update_status("Son las %s y 0%s #%s, Si tu botella está vacía ¡Has logrado el objetivo de hoy!" %(H, s, ts))
			else:
				api.update_status("Son las %s y %s #%s" %(H, s, ts))


			print "¡BANNER actualizado!"
			min = m
		except:
			"Algo salio mal" + str(sys.exc_info())
	else:
		print 

	Timer(60.0, reloj).start()

reloj()
