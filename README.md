# 目次
1. 初めに

   1.1 概要

   1.2 開発環境

   1.3 ハードウェア

2. システムの概要

3. コンポーネント

   1 Facedetection

   2 Select

   3 Voicerecog

   4 Selenium

   5 Controlestate

   6 Sota_Controle

   7 Log

   8 Callstaff

5. コンポーネントの接続
# 1. 初めに
## 1.1 概要
近年グループウェア，学習支援システム，窓口業務システムなど様々なサービスが， Webブラウザ上で利用されるいわゆるWebシステムとして提供されるようになり，クラウドAIサービスを利用することでコミュニケーションロボットを用いたシステムの構築が迅速，容易に行えるようになった．本稿では，音声認識・合成，RGBDカメラによる画像認識を活用したWeb検索支援システムをRTミドルウェアを用いて開発し，そのシステム構築例として示す.
## 1.2 開発環境
本システムの開発環境を以下に記す．

| OS       | Windows11                              |
| -------- | ----------------------------------------- |
| RTミドルウェア | OpenRTM-aist-2.0.0-RELESE(Python 版)       |
| 開発環境     |      Visual Studio Code 1.70|
| Python   | Python 3.10.8                                     |
| webブラウザ  | GoogleChrome 117.0.5938.150|
|ChromeDriver|ChromeDriver 117|
## 1.3ハードウェア
使用するハードウェアを以下に記す
|コミュニケーションロボット|Vstone Sota|
| -------- | ----------------------------------------- |
|カメラ|Intel RealSense D435i|
|マイク||
|カメラ||
## 1.4ライブラリ
pythonの使用するライブラリとインストール方法を以下に記す
|OpenCV|PyPIからライブラリをインストールする．|
| -------- | ----------------------------------------- |
|Selenium|PyPIからライブラリをインストールする．Chromeのバージョンに合うChromedriver を以下のURLからダウンロードしSeleniumフォルダに移す．https://chromedriver.chromium.org/downloads|
|Azure cognictive speech|PyPIからライブラリをインストールする．|
|Mediapipe|PyPIからライブラリをインストールする．|
|MeCab|PyPIからライブラリをインストールする．精度の高い形態素解析を行うために辞書Neologdを使用する．Neologdの導入方法は，以下を参照．https://github.com/neologd/mecab-ipadic-neologd/blob/master/README.ja.md|
|Pyrealsense2|PyPIからライブラリをインストールする．|
# 2 システムの概要
本システムは，本の借用や書庫の利用の対応，文献複写の受け取り，筆者の所属大学が大学の理念に基づき学生の評価認定するプロジェクトとして実施しているKONANライブラリーサーティフィケートの対応を行う機能をRTミドルウェアで実装したものである．処理の流れを以下の図に示す．

![image](https://github.com/sota2800/rtm/assets/141693046/7d2c72ee-c1f7-4a55-bb5e-06e157a1d4b2)
# 3 コンポーネント
## 1 Facedetection
人が存在するか否かを判断するコンポーネントであり，realsenceから距離と画像データを受け取る．また，Controlestateから受け取ったDatasetのメンバphaseに格納されている文字列によって異なる動作，出力をする．

・受け取った文字列がDetection-1の場合

・provider

| 名称   | 型  | 説明                              |
| -------- | ---------|-------------------------------- |
| facedetectionprovider | Dataset |人がいる場合のみDatasetのメンバPhaseに文字列“Select”を格納し出力する．|

・受け取った文字列がDetection-2の場合

・provider

| 名称   | 型  | 説明                              |
| -------- | ---------|-------------------------------- |
| facedetectionprovider | Dataset |人がいる場合は，contlolestateから受け取ったDataset型のデータをそのまま出力し，人がいない場合は，DatasetのメンバPhaseに文字列“STOP”を格納し出力する．|

Dataset型は以下のデータ構造からなる．
struct Dataset {

 string state;

 wstring recogdata;

 string command;

 string phase;

};
## 2. Select
　ユーザの要望を聞き取るコンポーネント． Controlestateから受け取ったDatasetのメンバphase 　
　に文字列”SELECT”,”AGAIN”,”REPEAT”が格納されている時に動作する．音声認識した文字列に
　よって異なる出力をする．　
・provider





















