# Azureの音声認識, 合成
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import azure.cognitiveservices.speech as speechsdk
speech_config = speechsdk.SpeechConfig(subscription="a64cf6b636ad4e0590a25b051a44adbc", region="japanwest")
speech_config.speech_recognition_language="ja-JP"
speech_config.speech_synthesis_voice_name='ja-JP-NanamiNeural'
audio_config = AudioOutputConfig(use_default_speaker=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

import time
import re
import random
import datetime
import winsound # 音声ファイルの再生

# 関数
# def fill(response):
# def filler(text):
# def Reviving_Lost_Words(rist):
# def mecab(text)
# def speech_recog(search_recom):
 # search_recomは　0:検索　1:おすすめ　をspeech_recogに送る

# 検索の際、and検索かor検索かを設定
and_or='or'

import MeCab
# MeCab.Tagger('') //オブジェクト
# tagger.parseToNode(text) //きりわけ
# pos = node.feature.split(',')[0] //品詞の判別

part_of_speech=['人名', '代名詞','固有名詞', '名詞']

tagger= MeCab.Tagger(r'-d"C:\mecab-ipadic-neologd"')

def filler(text):
    fillers_and_symbols = [
        '。', '？', '！', 'あー', 'あのー', 'あの', 'あれ', 'とー',
        'ええ', 'えーっと', 'えっと', 'えー', 'えっ', 'え', 'うーんと', 'うーんん', 'うーん', 
        'うー', 'うう', 'うん', 'そういう', 'のような', 'ような', 'みたいな', 'それで', 
        'それから', 'そんな', 'まあ', 'まぁ', 'あ ', ' ー', 'さん', 'さま ', '関する',
        'まじ ', 'マジ '
    ]
    # フィラーや記号を空白に置換
    for fs in fillers_and_symbols:
        text = text.replace(fs, ' ')
    return text

# '本'のような図書館検索に必要のない単語を消す
def delete_word(response):
    j=0
    # 削除するワードのリスト
    stop_words = ['系', '本','の','こと','検索','しよう','ん','さ','方','紹介'] # 日本や生態系などのワードに影響するため分けた。
    for fs in stop_words:
        if fs == response:
            response=''
    j+=1
    return response

# mecabで消されてしまう単語を呼び戻す
def Reviving_Lost_Words(rist):
    add_que=[]
    Lost_Words=[
        ''
    ]
    for fs in Lost_Words:
        if fs in rist[0]:
            rist[0]=rist[0].replace(fs, ' ')
            add_que.append(fs)
        add_text=" ".join(add_que)
    return add_text

# mecabで形態素解析
def mecab(text):
    node = tagger.parseToNode(text)
    # print(node)
    que=[]
    while node:
        term=node.surface
        term=delete_word(term)     # '本'のような図書館検索に必要のない単語を消す
        # print(node.feature.split())
        pos = node.feature.split(',')   # listになってる
        part_num=0
        for _ in part_of_speech:
            if _ in pos:
                if term in que:    # 単語を重複させない
                    break
                que.append(term)
                break
            part_num+=1
        node = node.next
    text_result = ' '.join(que)
    return text_result

# main文
def speech_recog(search_recom):
    # roop=2になったら聞き返すことを終了させる
    roop=0
    while 1:
        d = speech_recognizer.recognize_once_async().get()
        speechget=d.text
        rist=speechget.split(",")
        print(rist[0])

        #フィラー
        text=filler(speechget)

        #mecabで形態素解析
        text=mecab(text)
        print(text)
        
        if not not text:
            speech_synthesizer.speak_text(text+"に関する本をご紹介します")
            
            # or検索するなら空白を|に変換する <=> and検索は空白
            if and_or=='or':
                text = text.replace(' ', '|') # 空白を'|'に置換

            # "おすすめ"の場合
            if search_recom==1:
                if '小説' == text:
                    synthesizer.speak_text("最近入ったお勧めの小説を表示します。")
                    return text
                else:
                    synthesizer.speak_text("お勧めの本を表示します。")
                    return text

        # roop<3の間聞き取れない場合聞き返す
        if not text:
            roop+=1
            text=""
            if roop<3:
                # "もう一度お願いします"
                speech_synthesizer.speak_text("もう一度お願いします")
                # winsound.PlaySound('sound\mouitidoonegaisimasu2.wav',winsound.SND_FILENAME)
            else:
                speech_synthesizer.speak_text("すみません。初めからやり直してください")
                return text
        else:
            return text


# # デバッグ用
# synthesizer.speak_text("本の検索ですね。著者やキーワードを教えてください。")
# text=speech_recog(1)    # 0は検索　1はおすすめ