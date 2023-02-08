
import requests
import json
import os



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
    print(res_json)
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
