#!/usr/bin/python3
# -*- coding: utf-8 -*-
import uuid
import base64
import ftplib
from ftplib import FTP
import requests
import jwt
import logging

########################################################
########################################################
CONFIG_ADDR="config.rpinotify.it"
########################################################
########################################################
try:
    SERVER_ADDR = requests.get('http://' + CONFIG_ADDR + '/librpn/SERVER_ADDR')
    SERVER_ADDR="http://" + SERVER_ADDR.text
    LOG_LOC = requests.get('http://' + CONFIG_ADDR + '/librpn/LOG_LOC')
    LOG_LOC=LOG_LOC.text
except:
    print("Unable to get configuration to RpiNotify server")
    exit()

logging.basicConfig(filename='{}'.format(LOG_LOC),format='%(levelname)s - %(asctime)s -  %(message)s',
                    level=logging.INFO)
##################################################################################################
####                SendPhoto - Funzione che manda foto da client a smartphone                ####
####                                                                                          ####
####                                    Funzionamento:                                        ####
####                                                                                          ####
####                     1. Genera un id da assengare all'operazione                          ####
####      2. Richiede un upload al server, che lo registra e, se pronto, lo accettata         ####
####                 3. Carica l'immagine sul server FTP di RpiNotify                         ####
####       4. Richiede un invio dell'immagine appena caricata sulla chat dell'utente          ####
####             5. Se l'invio va a buon fine, risponde positivamente e chiude                ####
##################################################################################################
def SendPhoto(token, imgpath):

    logging.info("SENDPHOTO - Request received")
    try: # Prova a generare l'id da assegnare all'elaborazione
        idelab=uuid.uuid4().hex
    except:
        logging.error("SENDPHOTO - Error: Unable to create elaboration ID")
        print("SENDPHOTO - Error: Unable to create elaboration ID")
        return
    try: # Prova a richiedere un image-upload al server
        imgreq = requests.get('{}/imgreq/{}/{}/{}'.format(SERVER_ADDR, token, idelab, imgpath.split("/")[-1]))
    except:
        logging.error("SENDPHOTO - Error: Unable to connect to RpiNotify server")
        print("SENDPHOTO - Error: Unable to connect to RpiNotify server")
        return
    if imgreq.text=="pronto": # Se il server risponde che la richiesta è stata accettata
        try: # Prova a connettersi al server FTP di RpiNotify
            ftp = FTP("ftp.rpinotify.it")
            ftp.login("rpnupload", "rpinotify")
        except:
            logging.error("SENDPHOTO - Error: Unable to connect to files server")
            print("SENDPHOTO - Error: Unable to connect to files server")
            return
        try: # Prova ad apire il file indicato dall'utente
            file = open(imgpath, "rb")
        except:
            logging.error("SENDPHOTO - Error: Unable to open image")
            print("SENDPHOTO - Error: Unable to open image")
            return
        try: # Prova a caricare il file nella cartella remota FTP
            ftp.storbinary('STOR ' + "/files/" + imgpath.split("/")[-1], file)
            ftp.quit()
            file.close()
        except:
            logging.error("SENDPHOTO - Error: Unable to upload image")
            print("SENDPHOTO - Error: Unable to upload image")
            return
        print("Image uploated!")
    else: # Il server non ha accettato la richista di image-upload
        logging.error("SENDPHOTO - Server error: {}".format(str(imgreq.text.encode('utf-8'))))
        print "SENDPHOTO - Server error: {}".format(str(imgreq.text.encode('utf-8')))
        return
    try: # Prova a confermare l'upload al server RpiNotify
        imgsent = requests.get('{}/imgsent/{}/{}'.format(SERVER_ADDR, token, idelab))
        print("Image sent!")
    except:
        logging.error("SENDPHOTO - Error: Unable to connect to RpiNotify server")
        print("SENDPHOTO - Error: Unable to connect to RpiNotify server")
        return
    if(imgsent.text!="ok"): # Il server non riesca a elaborare la conferma di upload
        logging.error("SENDPHOTO - Elaboration error: {}".format(str(imgsent.text.encode('utf-8'))))
        print "SENDPHOTO - Elaboration error: {}".format(str(imgsent.text.encode('utf-8')))
        return
    logging.info("SENDPHOTO - Request managed correctly")

#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####


##################################################################################################
####                SendVideo - Funzione che manda video da client a smartphone               ####
####                                                                                          ####
####                                    Funzionamento:                                        ####
####                                                                                          ####
####                     1. Genera un id da assengare all'operazione                          ####
####      2. Richiede un upload al server, che lo registra e, se pronto, lo accettata         ####
####                 3. Carica il video sul server FTP di RpiNotify                           ####
####       4. Richiede un invio del video appena caricata sulla chat dell'utente              ####
####             5. Se l'invio va a buon fine, risponde positivamente e chiude                ####
##################################################################################################
def SendVideo(token, vidpath):
    logging.info("SENDVIDEO - Request received")
    try: # Prova a generare l'id da assegnare all'elaborazione
        idelab=uuid.uuid4().hex
    except:
        logging.error("SENDVIDEO - Error: Unable to create elaboration ID")
        print("SENDVIDEO - Error: Unable to create elaboration ID")
        return
    try: # Prova a richiedere un video-upload al server
        vidreq = requests.get('{}/vidreq/{}/{}/{}'.format(SERVER_ADDR, token, idelab, vidpath.split("/")[-1]))
    except:
        logging.error("SENDVIDEO - Error: Unable to connect to RpiNotify server")
        print("SENDVIDEO - Error: Unable to connect to RpiNotify server")
        return
    if vidreq.text=="pronto": # Se il server risponde che la richiesta è stata accettata
        try: # Prova a connettersi al server FTP di RpiNotify
            ftp = FTP("51.254.210.41")
            ftp.login("rpnupload", "rpinotify")
        except:
            logging.error("SENDVIDEO - Error: Unable to connect to files server")
            print("SENDVIDEO - Error: Unable to connect to files server")
            return
        try: # Prova ad apire il file indicato dall'utente
            file = open(vidpath, "rb")
        except:
            logging.error("SENDVIDEO - Error: Unable to open video")
            print("SENDVIDEO - Error: Unable to open video")
            return
        try: # Prova a caricare il file nella cartella remota FTP
            ftp.storbinary('STOR ' + "/files/" + vidpath.split("/")[-1], file)
            ftp.quit()
            file.close()
        except:
            logging.error("SENDVIDEO - Error: Unable to upload video")
            print("SENDVIDEO - Error: Unable to upload video")
            return
        print("Video uploated!")
    else: # Il server non ha accettato la richista di video-upload
        logging.error("SENDVIDEO - Server error: {}".format(str(vidreq.text.encode('utf-8'))))
        print "SENDVIDEO - Server error: {}".format(str(vidreq.text.encode('utf-8')))
        return
    try: # Prova a confermare l'upload al server RpiNotify
        vidsent = requests.get('{}/vidsent/{}/{}'.format(SERVER_ADDR, token, idelab))
        print("Video sent!")
    except:
        logging.error("SENDVIDEO - Error: Unable to connect to RpiNotify server")
        print("SENDVIDEO - Error: Unable to connect to RpiNotify server")
        return
    if(vidsent.text!="ok"): # Il server non riesca a elaborare la conferma di upload
        logging.error("SENDVIDEO - Elaboration error: {}".format(str(vidsent.text.encode('utf-8'))))
        print "SENDVIDEO - Elaboration error: {}".format(str(vidsent.text.encode('utf-8')))
        return
    logging.info("SENDVIDEO - Request managed correctly")

#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####

##################################################################################################
####               SendFile - Funzione che manda un file da client a smartphone               ####
####                                                                                          ####
####                                    Funzionamento:                                        ####
####                                                                                          ####
####                     1. Genera un id da assengare all'operazione                          ####
####      2. Richiede un upload al server, che lo registra e, se pronto, lo accetta           ####
####                 3. Carica il file sul server FTP di RpiNotify                            ####
####       4. Richiede un invio del file appena caricata sulla chat dell'utente               ####
####             5. Se l'invio va a buon fine, risponde positivamente e chiude                ####
##################################################################################################
def SendFile(token, filepath):
    logging.info("SENDFILE - Request received")
    try: # Prova a generare l'id da assegnare all'elaborazione
        idelab=uuid.uuid4().hex
    except:
        logging.error("SENDFILE - Error: Unable to create elaboration ID")
        print("SENDFILE - Error: Unable to create elaboration ID")
        return
    try: # Prova a richiedere un file-upload al server
        filereq = requests.get('{}/filereq/{}/{}/{}'.format(SERVER_ADDR, token, idelab, filepath.split("/")[-1]))
    except:
        logging.error("SENDFILE - Error: Unable to connect to RpiNotify server")
        print("SENDFILE - Error: Unable to connect to RpiNotify server")
        return
    if filereq.text=="pronto": # Se il server risponde che la richiesta è stata accettata
        try: # Prova a connettersi al server FTP di RpiNotify
            ftp = FTP("51.254.210.41")
            ftp.login("rpnupload", "rpinotify")
        except:
            logging.error("SENDFILE - Error: Unable to connect to files server")
            print("SENDFILE - Error: Unable to connect to files server")
            return
        try: # Prova ad apire il file indicato dall'utente
            file = open(filepath, "rb")
        except:
            logging.error("SENDFILE - Error: Unable to open file")
            print("SENDFILE - Error: Unable to open file")
            return
        try: # Prova a caricare il file nella cartella remota FTP
            ftp.storbinary('STOR ' + "/files/" + filepath.split("/")[-1], file)
            ftp.quit()
            file.close()
        except:
            logging.error("SENDFILE - Error: Unable to upload file")
            print("SENDFILE - Error: Unable to upload file")
            return
        print("File uploated!")
    else: # Il server non ha accettato la richista di file-upload
        logging.error("SENDFILE - Server error: {}".format(str(filereq.text.encode('utf-8'))))
        print "SENDFILE - Server error: {}".format(str(filereq.text.encode('utf-8')))
        return
    try: # Prova a confermare l'upload al server RpiNotify
        logging.error("")
        filesent = requests.get('{}/filesent/{}/{}'.format(SERVER_ADDR, token, idelab))
        print("File sent!")
    except:
        logging.error("SENDFILE - Error: Unable to connect to RpiNotify server")
        print("SENDFILE - Error: Unable to connect to RpiNotify server")
        return
    if(filesent.text!="ok"): # Il server non riesca a elaborare la conferma di upload
        logging.error("SENDFILE - Elaboration error: {}".format(str(filesent.text.encode('utf-8'))))
        print "SENDFILE - Elaboration error: {}".format(str(filesent.text.encode('utf-8')))
        return
    logging.info("SENDFILE - Request managed correctly")

#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####
#### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### ####

##################################################################################################
####           SendText - Funzione che manda un messaggio da client allo smartphone            ####
####                                                                                          ####
####                                    Funzionamento:                                        ####
####                                                                                          ####
####             1. Viene richiesta l'operazione al server specificando testo e token         ####
##################################################################################################
def SendText(token, messaggio):
    logging.info("SENDTEXT - Request received")
    messaggio=str(jwt.encode({'cmd': '{0}'.format(messaggio)}, 'secret', algorithm='HS256'))
    try:
        textreq = requests.get('{}/notification/{}/text/{}'.format(SERVER_ADDR, token, messaggio))
    except:
        logging.error("SENDTEXT - Error: Unable to connect to RpiNotify server")
        print("SENDTEXT - Error: Unable to connect to RpiNotify server")
        return
    if(textreq.text!="No error"): # Il server non riesca a elaborare la conferma di upload
        logging.error("SENDTEXT - Elaboration error: {}".format(str(textreq.text.encode('utf-8'))))
        print "SENDTEXT - Elaboration error: {}".format(str(textreq.text.encode('utf-8')))
        return
    logging.info("SENDTEXT - Request managed correctly")
