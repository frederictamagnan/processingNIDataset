from VaeEncoderDecoder import VaeEncoderDecoder
import pypianoroll as ppr
from pypianoroll import Track,Multitrack
from utils import numpy_drums_save_to_midi
from DrumsDataset import EmbeddingsDataset
from DrumReducerExpander import DrumReducerExpander



import numpy as np


mu=np.zeros((10,32,1))
sigma=np.ones((10,32,1))

lol=np.concatenate((mu,sigma),axis=2)

print(lol.shape)
decoder= DrumReducerExpander()

# dataset=EmbeddingsDataset(lol)
#
# print(dataset)

decoderVAE = VaeEncoderDecoder()

drums_reduced=decoderVAE.decode_to_reduced_drums(lol)

print(drums_reduced)
print(drums_reduced.shape)
drums_reduced=drums_reduced>0.76

expanded_drums=decoder.decode(drums_reduced)
filepath='/home/ftamagna/Documents/_AcademiaSinica/dataset/temp/'

for i in range(len(expanded_drums)):
    numpy_drums_save_to_midi(np.concatenate((expanded_drums[i],expanded_drums[i])),filepath,str(i))




