
import requests
import json
import os

import time
import os
import json
import requests # pip install requests
import pandas as pd # pip install pandas




class AssemblyAI:
    BASE_URL = 'https://api.assemblyai.com/v2/'
    
    def __init__(self, api_key):
        self.api_key = api_key

    def headers(self):
        return {'authorization': self.api_key}

    def upload_audio_by_url(self, url_link, remove_filler_word=True, format_text=True, **kwarg):
        request_body = {
            'audio_url': url_link,
            'disfluencies': remove_filler_word,
            'format_text': format_text
        }

        for key, val in kwarg.items():
            request_body[key] = val

        response = requests.post(self.BASE_URL + 'transcript', headers=self.headers, json=request_body)
        return response

    def upload_audio_by_file(self, audio_file_path, chunk_size=5241880, remove_filler_word=True, format_text=True, **kwarg):
        if not os.path.exists(audio_file_path) or not os.path.isfile(audio_file_path):
            print('File is not found')
            return
        
        def read_file(file_path):
            with open(file_path, mode='rb') as _file:
                while True:
                    data = _file.read()
                    if not data:
                        break
                    yield data
        
        audio_data = read_file(audio_file_path)
        headers = self.headers
        headers['content-type'] = 'application/json'
        upload_response = requests.post(self.BASE_URL + 'upload', headers=headers, data=audio_data)
        
        response = self.upload_audio_by_url(upload_response.json()['upload_url'], remove_filler_word=remove_filler_word, format_text=format_text, **kwarg)
        return response

    def retrieve_transcript(self, transcript_id):
        response = requests.get(self.BASE_URL + 'transcript/' + transcript_id, headers=self.headers)
        return response.json()


# API_KEY = 'E7WVMDd26dtKm5Q7tRo1MORnwsUDOzik'

# ai1 = AssemblyAI(API_KEY)


# media_file_path ='https://drive.google.com/file/d/1JxC99XbYN_8TsAw91guNekA36LhvjqIJ/view?usp=share_link'
# response_upload = ai1.upload_audio_by_file(media_file_path)
# print(response_upload)
# response_json_output = response_upload.json()
# transcript_id = response_json_output['id']

# response_status = ai1.retrieve_transcript(transcript_id)
# print(response_status)
# print(response_status['status'])
# print(response_status['text'])


def requestFPT(filename):
    url = 'https://api.fpt.ai/hmi/asr/general'
    payload = open(filename, 'rb').read()
    headers = {'api-key': 'E7WVMDd26dtKm5Q7tRo1MORnwsUDOzik'} #examle: 'api-key': '3ISvE45DVemWTvrMTIgMtyfIjHnd8yAz'
    response = requests.post(url=url, data=payload, headers=headers)
    res_json = response.json()
    # print(res_json,"***")

    if res_json['status'] == 0:
        transcript = res_json['hypotheses'][0]['utterance']
        #print('request FPT success')

        print('FPT transcript:',transcript)
        return transcript
    else:
        return None
def assemblyAI(filename):

    endpoint = "https://api.assemblyai.com/v2/transcript"

    json = {
    "audio_url": filename
    }

    headers = {
    "Authorization": "33a5dc23d04340a08f585b54282bb760",
    "Content-Type": "application/json"
    }

    response = requests.post(endpoint, json=json, headers=headers)
    res_json = response.json()
    print(res_json['status'])
assemblyAI("https://drive.google.com/file/d/1JxC99XbYN_8TsAw91guNekA36LhvjqIJ/view?usp=share_link")

def requestAndWriteFile(audio_dir_path , transcript_out_dir):

    audio_dir = audio_dir_path + '\\'
    if not os.path.exists(audio_dir):
        print('Audio dir: "{}" not found! Plase check input dir'.format(audio_dir_path))
        exit()
    transcript_dir = transcript_out_dir + '\\'
    if not os.path.exists(transcript_dir):
        os.mkdir(transcript_dir)
    print('Input audio files dir: {}'.format(audio_dir))
    print('Output transcript files dir: {}'.format(transcript_dir))
    for f in os.listdir(audio_dir):
        name_label_file = transcript_dir + f.split('.')[0]+ '.txt'
        audio_path = audio_dir + f
        if os.path.isfile(name_label_file):
            print('Transript for: {} is exist in: {}. Skipped'.format(audio_path,name_label_file))
            continue
        else:
            label_file = open(name_label_file, 'w', encoding='utf-8')
            res = requestFPT(audio_path)
            requestFPT(audio_path)     
            if res == None:
                print('request vtc api failed. trying fpt api')
            label_file.write(res)
            print('Transript success, file:{}'.format(name_label_file))

        #break

# requestAndWriteFile('F:\\data\\', 'cuted_transcript')
