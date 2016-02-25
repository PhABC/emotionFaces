# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 8:39:18 2016
@author: PhABC
Title: Emoimages ~ Evaluation the emotional content of faces via the Oxford Project

"""
import httplib, pickle, os, time

# DESCRIPTION -----------------------------------------------------------------

"""
This script allows you to go trhough a list of face pictures and returns 
emotion scores using Microsoft's Oxford Project API. This script returns 
a dictionnary containing the value of the 8 defined emotions for each of 
the picture contained in the folder 'folderPath' :
    
    ~ neutral
    ~ happiness
    ~ disgust
    ~ anger
    ~ surprise
    ~ fear
    ~ sadness
    ~ contempt

To use the code, the only things you need to change are the path to the images,
the saveName and the subscription key. 

    folderPath = Location of the folder containing all the face images
    saveName   = The path of where you want to save the results + the name
    subKey     = Subscription key allowing you to use the Oxford Project API 
    
The subscription key can be obtained on your profile when you register (free) to 
microsoft azure. See below for how to get your subscription key.  This key allows 
20 requests of face processing per minutes up to a maximum of 5000 faces per months, 
hence the usage of time.sleep in thi scipt. 

Order in which faces are sorted might not be the same as the order desired. 
Edit the name so that they respect python's sorting conventions. To get the order
in which the pictures are sorted, look at 'fileList'.

"""
# SUBSCRIPTION KEY --------------------------------------------------------------
"""
	+Go on the following website:  projectoxford.ai/pricing
	+Click on "Get started today for free"
	+Register
	+Find Emotion API and subscribe
	+Click on "show" under the primary key and copy paste in this script
		at subkey.
Steps aren't precise, so you might have to play around a little.

"""
# EXAMPLES ----------------------------------------------------------------------

"""
    +To load the results in emoScores if not running code: 
    
        >>> emoScores =  pickle.load(open(saveName,'rb'))


    +Get the 'happiness' score of picture A001.png :
        
        >>> emoScores['A001.png']['happiness']
        0.9999996
           
       
   +To get all the emotion values of picture A001.png:
    
        >>> emoScores['A001.png'] 
        {'neutral' : 3.69326472e-07, 
        'happiness': 0.9999996,
        'disgust  ': 6.38040246e-11, 
        'anger'    : 9.923013e-15, 
        'surprise' : 4.60788e-13, 
        'fear'     : 9.729748e-15, 
        'sadness'  : 2.04710478e-15,
        'contempt' : 3.053343e-08}
        

"""

# Variables to set by user 

facesPath  = ('/home/phc/Dropbox/Education/University/'  # Path where all the pictures are 
              'Hiv2016/Labo2/emotionFaces/faces/')       
saveName   = ('/home/phc/Dropbox/Education/University/'  # Path where emotion scores will be saved
              'Hiv2016/Labo2/emotionFaces/emoScores.p')    
subKey     = ''          # Oxford API subscription key

# SCRIPT ---------------------------------------------------------------------

fileList   = sorted(os.listdir(facesPath))         # Sorted list of pictures name
emoScores  = dict()

for file in fileList:
    
    print 'Loading ' + file
    
    # Image to analyse (body of the request)
    filename = facesPath + file                # Path of specified picture
    f        = open(filename, "rb")  	       # Reading picture
    body     = f.read()                        # body of image for API
    f.close()
        
    # API request for Emotion Detection with subscription key
    headers = {'Content-type': 'application/octet-stream',
		'Ocp-Apim-Subscription-Key': subKey }
      
    try:
        conn     = httplib.HTTPSConnection('api.projectoxford.ai')    # API adress
        conn.request("POST", "/emotion/v1.0/recognize",body ,headers) # API access
        
        response = conn.getresponse()        # Extracting information from API      
        data     = eval(response.read())     # Storing information
        conn.close()                         # Closing read file
        
        emoScores[file] = data[0]['scores']  # Storing the emotion scores in a dictionnary
        
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        
    time.sleep(3) # API has a limit of 20 calls per minute....
    
pickle.dump(emoScores,open(saveName,'wb'))   # Saving the file in pickle format in to the specified path
