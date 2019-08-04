import pyaudio
import wave
import cv2
import os
import pickle
import time
import numpy as np
import python_speech_features as mfcc
from sklearn import preprocessing
from sklearn.mixture import GaussianMixture as GMM
from scipy.io.wavfile import read
#from IPython.display import Audio, display, clear_output
pa=pyaudio.PyAudio()
print(pa.get_device_count())
#from main_functions import *
def calculate_delta(array):
    """Calculate and returns the delta of given feature vector matrix"""

    rows,cols = array.shape
    deltas = np.zeros((rows,20))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i-j < 0:
                first = 0
            else:
                first = i-j
            if i+j > rows -1:
                second = rows -1
            else:
                second = i+j
            index.append((second,first))
            j+=1
        deltas[i] = ( array[index[0][0]]-array[index[0][1]] + (2 * (array[index[1][0]]-array[index[1][1]])) ) / 10
    return deltas

def extract_features(audio,rate):
    """extract 20 dim mfcc features from an audio, performs CMS and combines 
    delta to make it 40 dim feature vector"""    
    
    mfcc_feat = mfcc.mfcc(audio,rate, 0.025, 0.01,20,appendEnergy = True)
    
    mfcc_feat = preprocessing.scale(mfcc_feat)
    delta = calculate_delta(mfcc_feat)
    combined = np.hstack((mfcc_feat,delta)) 
    return combined
def add_user():
    
    name = input("Enter Name:")

     # check for existing database
    if os.path.exists('./face_database/embeddings.pickle'):
        with open('./face_database/embeddings.pickle', 'rb') as database:
            db = pickle.load(database)   
            
            if name in db or name == 'unknown':
                print("Name Already Exists! Try Another Name...")
                return
    else:
        #if database not exists than creating new database
        db = {}
    
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    
     
    
    #Voice authentication
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 3
    
    source = r"C:\Users\Atul\Downloads\#3 Voice Authentication and Face Recognition\voice_database\unknown" + name
    
   
    os.mkdir(source)

    for i in range(3):
        audio = pyaudio.PyAudio()

        if i == 0:
            j = 3
            while j>=0:
                time.sleep(1.0)
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Speak your name in {} seconds".format(j))
                j-=1

        elif i ==1:
            time.sleep(2.0)
            print("Speak your name one more time")
            time.sleep(0.8)
        
        else:
            time.sleep(2.0)
            print("Speak your name one last time")
            time.sleep(0.8)

        # start Recording
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

        print("recording...")
        frames = []

        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # saving wav file of speaker
        waveFile = wave.open(source + '/' + str((i+1)) + '.wav', 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        print("Done")

    dest =  r"C:\Users\Atul\Downloads\#3 Voice Authentication and Face Recognition\gmm_models"
    count = 1

    for path in os.listdir(source):
        path = os.path.join(source, path)
    

        features = np.array([])
        
        # reading audio files of speaker
        (sr, audio) = read(path)
        
        # extract 40 dimensional MFCC & delta MFCC features
        vector   = extract_features(audio,sr)

        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))
            
        # when features of 3 files of speaker are concatenated, then do model training
        if count == 3:    
            gmm = GMM(n_components = 16, covariance_type='diag', n_init = 3)
            gmm.fit(features)

            # saving the trained gaussian model
            pickle.dump(gmm, open(dest + name + '.gmm', 'wb'))
            print(name + ' added successfully') 
            
            features = np.asarray(())
            count = 0
        count = count + 1

if __name__ == '__main__':
    add_user()