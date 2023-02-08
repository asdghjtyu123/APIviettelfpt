import requests
import json
import os
import time
import os
import json
import requests
import pandas as pd

def requestviettel(filename): 
    url = "https://viettelgroup.ai/voice/api/asr/v1/rest/decode_file"
    # payload = open(filename, 'rb').read()
    headers = {
        'token': 'anonymous',
        # 'sample_rate': 16000,
        # 'format':'S16LE',      
        # 'num_of_channels':1,
        # 'asr_model': 'model code'
    }
    files = {'file': open(filename,'rb')}
    response = requests.post(url,files=files, headers=headers,timeout=None)
    ref_=response.json()
    if (len(ref_)==1):
        transcript=ref_[0]['result']['hypotheses'][0]['transcript']
        # print(transcript)    
    else:
        transcript=ref_[0]['result']['hypotheses'][0]['transcript']+' '+ref_[0]['result']['hypotheses'][0]['transcript']
        # print(transcript) 
    return transcript
def viettel(audio_dir):
    for i in os.listdir(audio_dir):
        # print(folder+file)
        a=requestviettel('{}{}'.format(audio_dir,i))  
        print(a)
viettel('F:\\data\\')
def requestFPT(filename):
    url = 'https://api.fpt.ai/hmi/asr/general'
    payload = open(filename, 'rb').read()
    headers = {'api-key': 'E7WVMDd26dtKm5Q7tRo1MORnwsUDOzik'} #examle: 'api-key': '3ISvE45DVemWTvrMTIgMtyfIjHnd8yAz'
    response = requests.post(url=url, data=payload, headers=headers,timeout=None)
    res_json = response.json()
    # print(res_json,"***")

    if res_json['status'] == 0:
        transcript = res_json['hypotheses'][0]['utterance']
        #print('request FPT success')

        print('FPT transcript:',transcript)
        return transcript
    else:
        return None


def FPT(audio_dir_path , transcript_out_dir,transcript_out_dir1):
    audio_dir = audio_dir_path + '\\'
    transcript_dir = transcript_out_dir + '\\'
    transcript_dir1 = transcript_out_dir1 + '\\'
    if not os.path.exists(transcript_dir):
        os.mkdir(transcript_dir)
    if not os.path.exists(transcript_dir1):
        os.mkdir(transcript_dir1)          
    for f in os.listdir(audio_dir):
        name_label_file = transcript_dir + f.split('.')[0]+ '.txt'         
        audio_path = audio_dir + f
        label_file = open(name_label_file, 'w', encoding='utf-8')
        res = requestFPT(audio_path)
        if (res !=None):         
            break
        label_file.write(res)
        print(name_label_file)
     

# requestAndWriteFile('F:\\data\\', 'cuted_transcript','cuted_transcript1')
