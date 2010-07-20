#!/usr/bin/python

import sys, os, shelve, logging,string
import flickr

existingSets = None
user = None

def  creatSet(photoSet, setName):
    setName = string.strip(setName.replace('\\',' '))
    photos = [] #real photo objects
    for p in photoSet:
            photos.append( flickr.Photo(id = p))

    fset = None
    #check if set with the name exists already 
    for s in existingSets:
            if(s.title == setName):
                    fset= s
                    logging.debug('Found existing set %s' % setName)
                   # return
                    break
    try:                  
        if(fset == None):
                print photos[0]
                print setName
                fset = flickr.Photoset.create(photos[0], setName, 'autogen')
                logging.debug('Creating new set %s' % setName)
    except:
        logging.error('Cannot create set %s' % setName)
        logging.error(sys.exc_info()[0])

    try:    
        fset.editPhotos(photos)
    except:
        logging.error('Cannot edit set %s' % setName)
        logging.error(sys.exc_info()[0])

        
    logging.debug('...added %d photos' % len(photos)  )
    return fset


def createSets( historyFile):
     global existingSets
     global user
    
     logging.debug('Started tags2set')
     try:
         user = flickr.test_login()
         logging.debug(user.id)
         existingSets=user.getPhotosets()
     except:
         logging.error(sys.exc_info()[0])
         return None
     
     uploaded = shelve.open( historyFile )
     keys = uploaded.keys()
     keys.sort()
     lastSetName =''
     photoSet =[]
     setName = ''
     for image in keys:
        if(image.startswith('\\')): #filter out photoid keys
            setName = os.path.dirname(image) #set name is realy a directory
            logging.debug("Adding image %s" % image)
            photoSet.append( uploaded.get(image))
            if(not lastSetName == setName and not lastSetName == ''):
                #new set is starting so save last
                logging.debug( "Creating set %s with %d pictures" % lastSetName, len(photoSet) )
                creatSet(photoSet, lastSetName)
                photoSet = []
                photoSet.append(uploaded.get(image))
            lastSetName = setName
          
                
    #dont forget to create last set
     logging.debug( "Creating set %s with %d pictures" % setName, len(photoSet) )
     creatSet(photoSet, setName)
     

