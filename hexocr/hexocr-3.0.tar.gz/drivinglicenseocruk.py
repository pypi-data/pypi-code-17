from PIL import Image
import pytesseract
import cv2
import numpy as np
import sys,os
import re

DEBUG=True

def Log(debug=False,msg=None,*args):



    

    if(debug):
        
        if(msg):
            
            print(msg)  #"debug :",debug," , ",
            for a in args:
                print(a)
            print()
            print()
        else:
            print()
            print()


#extract text from licenseid
def getTextFromLicenseId(img,tesseract_path=r'C:/Program Files (x86)/Tesseract-OCR/tesseract'):

    ret=False
    message=""
    text=None
    pytesseract.pytesseract.tesseract_cmd=tesseract_path

    try:
        
        if(not cv2.Laplacian(img, cv2.CV_64F).var() > 350):
            ret=False
            message="this image is too blurry"
            return(ret,message,text)


        grey_id=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        print("constructing image from data")
        pilimg=Image.fromarray(img)
		
        print("extracting text from image")
        text=pytesseract.image_to_string(pilimg)

        ret=True
        message="successfully extracted data"
        Log(DEBUG,message)
        Log()
        Log()

        return(ret,message,text)
    
    except Exception as e:
        ret=False
        message=e.__str__()
        text=None

        Log(DEBUG,"error occured while processing licence id data")
        Log(DEBUG,"error : ",e.__str__())

        return(ret,message,text)

def generateUKIdFromData(textdict):

    message=""
    

    try:
        
        Log(DEBUG,"generating id")
        fname=textdict["firstname"]
        midname=None
        lname=textdict["lastname"]
        mlnames=fname.split(" ")
        if len(mlnames)>=2:
            midname=mlnames[1]
        dob=textdict["dob"]
        rlid=textdict["licenseid"]

        lid=""

        lname=lname+"99999"
        lname=lname[0:5]

        lid=lid+lname  # 1–5: The first five characters of the surname (padded with 9s if less than 5 characters)

        doby=dob.split(".")[-1].strip()
        dobm=dob.split(".")[1].strip()
        dobd=dob.split(".")[0].strip()

        lid=lid+doby[-2]  #  6: The decade digit from the year of birth (e.g. for 1987 it would be 8)
        
        try:
            
            gender=rlid[6:8]
            if((gender[0]=="o") or (gender[0]=="O") or (gender[0]=="0")):
                gender=dobm
            gender=int(gender)

            
            
            if((gender<=12)and(gender>=1) ):
                lid+=dobm    # 7–8: The month of birth (7th character incremented by 5 if driver is female i.e. 51–62 instead of 01–12)
            elif((gender<=62)and(gender>=51)):
                dobm=str(int(dobm[0])+5)+dobm[1]
                lid+=dobm    # 7–8: The month of birth (7th character incremented by 5 if driver is female i.e. 51–62 instead of 01–12)
            else:
            
                message="valid numeric digit in place 7-8 not available"
                lid=""
                
                return (lid,message)
            

            
        except Exception as e:
            message="valid numeric digit in place 7-8 not available"
            Log(DEBUG,"Error : ",e)

            if(DEBUG):
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                Log(True,exc_type, fname, exc_tb.tb_lineno)
            lid=""
            
            return (lid,message)

        dobm=dob.split(".")[0].strip()

        lid+=dobm         # 9–10: The date within the month of birth
        lid=lid+doby[-1]        # 11: The year digit from the year of birth (e.g. for 1987 it would be 7)


        

        lid+=fname[0]    # 12–13: The first two initials of the first names, padded with a 9 if no middle name
        
        
        
        if midname:
            lid+=midname[0]
        else:
            lid+="9"

        Log(DEBUG,"generated License id [first 13 Digits] : ",lid)
        message="success"
        
        
        return(lid,message)
    
    except Exception as e:
        Log(DEBUG,"Error : ",e)
        if(DEBUG):
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            Log(True,exc_type, fname, exc_tb.tb_lineno)
        message="error occured trying to format the license id "
        lid=""
        
        return (lid,message)


def formatTextToUKPrivateLicense_2016(text):
    textlist=[]
    ret=False
    message=""
    formateddata={}
    try:
        Log(DEBUG,"Formatting data")
        text=text.replace("\n\n","\n")
        
        textlist=text.split("\n")
        
        listlen=len(textlist)
        x=0
        while(x<listlen):
            #Log(listlen,"/",x+1)
            if (textlist[x]==None or not textlist[x] or not textlist[x].strip()):
                textlist.pop(x)
                listlen=listlen-1
                x-=1
            x+=1


        Log(DEBUG,textlist)
        


                
        
        
        

        if(len(textlist)<8):
            ret=False
            message="all data was not extracted properly"
            Log(DEBUG,message)
            Log()
            Log()
            
            Log()
            Log()
            formateddata={}
            return(ret,message,formateddata)


        
        
        if "1" in textlist[1]:
            textlist[1]=textlist[1].split(" ")[-1]
        else:
            textlist[1]=textlist[1].strip(".").strip()
        textlist[1]=" ".join(re.findall("[A-Za-z]+",textlist[1]))
        if "2" in textlist[2]:
            textlist[2]=textlist[2].split(" ")[-1]
        else:
            textlist[2]=textlist[2].strip(".").strip()

        if(not ("." in textlist[3])):
            textlist[2]=textlist[2]+ " " + textlist.pop(3).strip()
        if "3" in textlist[3]:
            tmp=textlist[3].strip("3").strip(".").split()
            tt=""
            for t in tmp:
                if ("." in t) or ("," in t):
                    tt+=t
            textlist[3]=tt
        else:
             
            tmp=textlist[3].strip().strip(".").split()
            tt=""
            for t in tmp:
                if ("." in t) or ("," in t):
                    tt+=t
            textlist[3]=tt

        if "4b" in textlist[5]:
            textlist[5]=textlist[5].strip().split()[-1]
        tmp=textlist[5]
        tmp=tmp.split(" ")
        if len(tmp)>1:
            textlist[5]=tmp[1].strip()

        if "5" in textlist[6] :
            textlist[6]=textlist[6].strip("5").replace(".", " ").strip()
        tmp=textlist[6]
        tmp=tmp.strip().split(" ")
        if(len(tmp)>2):
            tmp=[tmp[0],tmp[1]]
            tmp=" ".join(tmp)
            textlist[6]=tmp

        if "8" in textlist[8]:
            textlist[8]=textlist[8].strip("8").replace("."," ").strip().strip("-").strip()
            address=textlist[8]
        else:
            address=textlist[8]

        
        if(len(textlist)>=10):
            textlist[9]=textlist[9].strip()
            address=address+" "+textlist[9]
        
        formateddata={"firstname":textlist[2],"lastname":textlist[1],"licenseid":textlist[6].rstrip("\\"),"dob":textlist[3],"expirydate":textlist[5],"address":address}


##        Log(DEBUG,"prepre formated Data : ",formateddata)
##        if(formateddata["licenseid"][11]!=formateddata["firstname"][0]):
##            tmp=formateddata["lastname"]
##            formateddata["lastname"]=formateddata["firstname"]
##            formateddata["firstname"]=tmp
        Log(DEBUG,"pre formated Data : ",formateddata)
        glid,message=generateUKIdFromData(formateddata)
        
        if(not message=="success"):
            ret=False
            message="could not generate license id"
            Log(DEBUG,message)
            Log()
            Log()
            formateddata={}
            return(ret,message,formateddata)

        tmpdata=list(formateddata["licenseid"])
        tmpdata[0:13]=list(glid)

        formateddata["licenseid"]="".join(tmpdata).upper()

        


            
        ret=True
        message="All data formatted correctly"
        Log(DEBUG,message)
        Log()
        Log()
        return(ret,message,formateddata)

    except Exception as e:
        ret=False
        message="An Error occured while formatting data"
        Log(DEBUG,message)
        Log(DEBUG,"Error : ",e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Log(True,exc_type, fname, exc_tb.tb_lineno)
        formateddata={}

        return(ret,message,formateddata)
        



##def formatTextToCommercialLicense(text):
##
##    pass
##


def testImage(imgpath):
    
    try:

        img=cv2.imread(imgpath)
        ret,m,data=getTextFromLicenseId(img)

        if(ret):
            Log(DEBUG," raw data from text : ",data)
            Log()
            Log()
            
            ret,m,fd=formatTextToUKPrivateLicense_2016(data)
            Log(DEBUG,"formated data : ",fd)
                
    except:
        pass
            


import json
def testImageInDir(imdir):

    try:
        for filename in os.listdir(imdir):
            if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
                filename=os.path.join(imdir,filename)
                print("trying to extract data from : ",filename)
                img=cv2.imread(filename)
                ret,m,data=getTextFromLicenseId(img)
                if(ret):
                    ret,m,fd=formatTextToUKPrivateLicense_2016(data)
                f=open(filename+".dat","w")
                json.dump(fd,f)
                f.flush()
                f.close()

                
    except Exception as e:
        
        
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Log(True,exc_type, fname, exc_tb.tb_lineno)

##if __name__=="__main__":
##    testImageInDir(r"C:\Users\CHIKI\Desktop\img")
##
##    
                        
