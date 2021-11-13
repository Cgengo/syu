from flask import Flask, request, render_template
app = Flask(__name__)
import json

from apiclient.discovery import build

import requests
import urllib.parse as parse
import csv

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input = request.form['input']
        API_KEY = "AIzaSyDuf9lxW1fjvYlWbYW-6t1fuGHaL5-pXQ4"
        URL_HEAD = "https://www.googleapis.com/youtube/v3/commentThreads?"
        nextPageToken = ''
        item_count = 0
        items_output = [
            ['videoId']+
            ['textDisplay']
        ]
        #繝代Λ繝｡繝ｼ繧ｿ險ｭ螳�
        video_id = "蜍慕判ID"
        channelId = "UC1l8jsqYmIj1bjCzN43UPfA"
        exe_num = 100
        for i in range(exe_num):
            #API繝代Λ繝｡繝ｼ繧ｿ繧ｻ繝�繝�
            param = {
                'key':API_KEY,
                'part':'snippet',
                #----竊薙ヵ繧｣繝ｫ繧ｿ�ｼ医＞縺壹ｌ縺�1縺､�ｼ俄��-------
                'allThreadsRelatedToChannelId':channelId,
                #'videoId':video_id,
                #----竊代ヵ繧｣繝ｫ繧ｿ�ｼ医＞縺壹ｌ縺�1縺､�ｼ俄��-------
                'maxResults':'100',
                'moderationStatus':'published',
                'order':'relevance',
                'pageToken':nextPageToken,
                'searchTerms':input,
                'textFormat':'plainText',
            }
            #繝ｪ繧ｯ繧ｨ繧ｹ繝�URL菴懈��
            target_url = URL_HEAD + (parse.urlencode(param))
            #繝�繝ｼ繧ｿ蜿門ｾ�
            res = requests.get(target_url).json()
            #莉ｶ謨ｰ
            try:
                item_count += len(res['items'])
            except KeyError:
                # KeyError繧堤┌隕悶☆繧�
                continue
            #print(target_url)
            print(str(item_count)+"回")
            #繧ｳ繝｡繝ｳ繝域ュ蝣ｱ繧貞､画焚縺ｫ譬ｼ邏�
            try:
                for item in res['items']:
                    items_output.append(
                        [str(item['snippet']['topLevelComment']['snippet']['videoId'])]+
                        [str(item['snippet']['topLevelComment']['snippet']['textDisplay'].replace('\n', ''))]
                    )
            except KeyError:
                # KeyError繧堤┌隕悶☆繧�
                continue
            #nextPageToken縺後↑縺上↑縺｣縺溘ｉ蜃ｦ逅�繧ｹ繝医ャ繝�
            if 'nextPageToken' in res:
                nextPageToken = res['nextPageToken']
            else:
                break
        #CSV縺ｧ蜃ｺ蜉�
        f = open('youtube-comments-list.csv', 'w', newline='', encoding='UTF-8')
        writer = csv.writer(f)
        writer.writerows(items_output)
        f.close()
        return render_template('index.html', items_output = items_output)
    else:
        return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
