import numpy as np
import os
from MultiDrumOneHotEncoding import MultiDrumOneHotEncoding
from pypianoroll import Multitrack
import pypianoroll as ppr
import sys
ROOTDIR="/home/ftamagna/Documents/_AcademiaSinica/dataset//NI_Drum_Studio_Midi_encoded/MIDI Files"

newdir="/home/ftamagna/Documents/_AcademiaSinica/dataset/NI_fills_summarized/"

import logging

from logging.handlers import RotatingFileHandler

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()
# on met le niveau du logger à DEBUG, comme ça il écrit tout
logger.setLevel(logging.DEBUG)

# création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
# création d'un handler qui va rediriger une écriture du log vers
# un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
# créé précédement et on ajoute ce handler au logger
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# création d'un second handler qui va rediriger chaque écriture de log
# sur la console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)




class DatasetBuilder:



    def __init__(self):


        self.rootdir=ROOTDIR
        self.drum_encoding = MultiDrumOneHotEncoding()







    def folders_to_clean_numpy(self):
        filldifferent1=0
        filldifferent2=0
        beat_resolution=True

        X=np.zeros((1,96,9))
        y=np.zeros((1,2,1))
        i=0
        error=0
        for subdir,dirs, files in os.walk(self.rootdir):
            for file in files:
                try:

                    filepath = os.path.join(subdir, file)
                    multi= ppr.parse(filepath)
                    multi.binarize()

                    if "Fill" in subdir:
                        label=np.array([[0],[1]])
                        multi = self.crop_or_pad_fill(multi)

                    else:
                        label=np.array([[1],[0]])
                        multi=self.crop_groove(multi)

                    encoded = self.drum_encoding.multitrack_to_encoded_pianoroll(multi)
                    encoded = encoded.reshape(1, encoded.shape[0], encoded.shape[1])
                    label=label.reshape(1,label.shape[0],label.shape[1])
                    X=np.concatenate((X,encoded))
                    y=np.concatenate((y,label))
                    i+=1
                    logger.debug("new track encoded stacked")

                except:
                    logger.debug("--FAILED TO LOAD THE MIDI FILE ERROR#"+str(i))
                    error+=1

        X=X[1:,:,:]
        y=y[1:,:,:]

        np.savez(newdir+'dataset_fill.npz',X=X,y=y)
        print("errors count : ",error)
        print(i)
        print("fill different less",filldifferent2,"mre",filldifferent1)
        print(beat_resolution)

    def load_dataset(self,filepath):

        data=np.load(filepath)
        return data['X'],data['y']

    def crop_or_pad_fill(self,multi):

        logger.debug("try to crop or pad")
        length=multi.tracks[0].pianoroll.shape[0]
        height=multi.tracks[0].pianoroll.shape[1]


        if length>96:
            multi.tracks[0].pianoroll=multi.tracks[0].pianoroll[-96:]

        elif length<96:
            padding=np.zeros((96-length,height))
            multi.tracks[0].pianoroll=np.concatenate(padding,multi.tracks[0].pianoroll)

        logger.debug("crop or pad finished and shape " +str(multi.tracks[0].pianoroll.shape))


        return multi
    def crop_groove(self,multi):

        multi.tracks[0].pianoroll = multi.tracks[0].pianoroll[:96]

        return multi






datasetBuilder=DatasetBuilder()
# datasetBuilder.folders_to_clean_numpy()

X,y=datasetBuilder.load_dataset(filepath=newdir+'dataset_fill.npz')
#
print(X.shape)
print(y.shape)
print(y[:,0,:].sum())
print(y[:,1,:].sum())
