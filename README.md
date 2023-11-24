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
  近年グループウェア，学習支援システム，窓口業務システムなど様々なサービスが， Webブラウザ上で利用されるいわゆるWebシステムとして提供されるようになった．一方既存サービスの変更の際には，従来システムへの影響を十分に考慮する必要があり，各機能の保守や改良への対応が困難である．本稿ではこれらを解決するために，既存システムの API や SDK を利用したプログラミングを使用せず，クラウドAIサービスを利用し短期間かつ容易に開発可能なシステムの一例として，
音声認識・合成，RGBDカメラによる画像認識を活用したWebブラウザ検索システムをRTミドルウェアを用いて開発し，そのシステム構築例として示す.
## 1.2 開発環境
本システムの開発環境を以下に記す．

|名称|バージョン|
| -------- | ----------------------------------------- |
| OS       | Windows11                              |
| RTミドルウェア | OpenRTM-aist-2.0.0-RELESE(Python 版)       |
| 開発環境     |      Visual Studio Code 1.70|
| Python   | Python 3.10.8                                     |
| webブラウザ  | GoogleChrome 117.0.5938.150|
|ChromeDriver|ChromeDriver 117|
## 1.3 ハードウェア
使用するハードウェアを以下に記す.

|コミュニケーションロボット|Vstone Sota|
| -------- | ----------------------------------------- |
|カメラ|Intel RealSense D435i|
|マイク||
|カメラ||
## 1.4 ライブラリ
pythonの使用するライブラリとインストール方法を以下に記す.

|名称|インストール方法|
| -------- | ----------------------------------------- |
|OpenCV|PyPIからライブラリをインストールする．|
|Selenium|PyPIからライブラリをインストールする．Chromeのバージョンに合うChromedriver を以下のURLからダウンロードしSeleniumフォルダに移す．https://chromedriver.chromium.org/downloads|
|Azure cognictive speech|PyPIからライブラリをインストールする．|
|Mediapipe|PyPIからライブラリをインストールする．|
|MeCab|PyPIからライブラリをインストールする．精度の高い形態素解析を行うために辞書Neologdを使用する．Neologdの導入方法は，以下を参照．https://github.com/neologd/mecab-ipadic-neologd/blob/master/README.ja.md|
|Pyrealsense2|PyPIからライブラリをインストールする．|
# 2. システムの概要
本システムは，本の借用や書庫の利用の対応，文献複写の受け取り，筆者の所属大学が大学の理念に基づき学生の評価認定するプロジェクトとして実施しているKONANライブラリーサーティフィケートの対応を行う機能をRTミドルウェアで実装したものである．処理の流れを以下の図に示す．

![image](https://github.com/sota2800/rtm/assets/141693046/7d2c72ee-c1f7-4a55-bb5e-06e157a1d4b2)
# 3. コンポーネント
## 1 Facedetection
人が存在するか否かを判断するコンポーネントであり，realsenceから距離と画像データを受け取る．また，Controlestateから受け取ったDatasetのメンバphaseに格納されている文字列によって異なる動作，出力をする．

**受け取った文字列がDetection-1の場合**

**serviceport**

  - provider

	| 名称   | 型（引数・返り値）  | 説明                              |
	| -------- | ---------|-------------------------------- |
	| facedetectionprovider | Dataset |人がいる場合のみDataset型のメンバPhaseに文字列“Select”を格納し出力する．その他の出力するDataset型のメンバには，受け取ったDataset型のメンバの値をそれぞれ代入する．|

**受け取った文字列がDetection-2の場合**

**serviceport**

- provider

	| 名称   | 型（引数・返り値）  | 説明                              |
	| -------- | ---------|-------------------------------- |
	| facedetectionprovider | Dataset |人がいる場合は，contlolestateから受け取ったDataset型のデータをそのまま出力し，人がいない場合は，DatasetのメンバPhaseに文字列“STOP”を格納し出力する．その他の出力するDataset型のメンバには，受け取ったDataset型のメンバの値をそれぞれ代入する．|

Dataset型は以下のデータ構造からなる．

		struct Dataset {
		
			 string state;
			
			 wstring recogdata;
			
			 string command;
			
			 string phase;
		
		};
## 2. Select
ユーザの要望を聞き取るコンポーネント．Controlestateから受け取ったDatasetのメンバphaseに文字列”SELECT”,”AGAIN”,”REPEAT”が格納されている時に動作する．音声認識した文字列によって異なる出力をする．

**serviceport**
 
- provider
  
	| 名称   | 型 （引数・返り値）| 説明                              |
	| -------- | ---------|-------------------------------- |
	|selectprovider|Dataset|ユーザが検索を行う場合は”SEARCH”,お勧めの本を紹介してほしい場合は”RECOM”,甲南ライブラリーサーティフィケイトを利用する場合は” CERTIFICATE”,図書職員を読んでほしい場合は” STAFFCALL”の４種類の文字Datasetのメンバphaseに格納し出力する．その他の出力するDataset型のメンバには，受け取ったDataset型のメンバの値をそれぞれ代入する．|
## 3. Voicerecog
Controlestateから受け取ったDatasetのメンバphase に文字列”SEARCH”，“RECOM”が格納されている時に動作するコンポーネント．音声認識によって得られた文字列から，名詞，固有名詞を取り出すために形態素解析を行う．

 **serviceport**
 
- provider

	| 名称   | 型（引数・返り値） | 説明                              |
	| -------- | ---------|-------------------------------- |
	|voicerecogprovider|Dataset|形態素解析によって得られた名詞，固有名詞をDatasetのメンバrecogdataに格納し出力する.その他の出力するDataset型のメンバには，受け取ったDataset型のメンバの値をそれぞれ代入する．|
## 4. Select
Webページを制御するコンポーネント．Webページの制御にはSeleniiumを使用する．

**serviceport**

- provider

	| 名称   | 型 (引数・返り値） | 説明                              |
	| -------- | ---------|-------------------------------- |
	|seleniumprovider|Dataset|処理が終了したことをDatasetのメンバphaseに格納して出力する.その他の出力するDataset型のメンバには，受け取ったDataset型のメンバの値をそれぞれ代入する．|
## 5. controlestate
コンポーネントから受け取ったデータを別のコンポーネントに出力する．また，コンポーネント“Controlsota”,“Callstaff”,“Log”にデータを出力する．

**Dataport**
　　
- Outport
 
	| 名称   | 型  | 説明                              |
	| -------- | ---------|-------------------------------- |
	|Controlsota|string|Sotaを動かすためのコマンドをstring型で出力する.|
	|Callstaff|boolean|職員を呼び出すときにTrueを送る.|
	|Log|string|ユーザの使用したサービス名をstring型で出力する.|

**Serviceport**

- Consumer

   | 名称   | 型 (引数・返り値） | 説明                              |
   | -------- | ---------|-------------------------------- |
   |Facedetectionconsumer|Dataset|Datasetのメンバphaseに文字列を格納して出力する．その他の出力するDataset型のメンバには，受け取ったDataset型のメンバの値をそれぞれ代入する．|
   |Selectnconsumer|Dataset|Datasetのメンバphaseに文字列を格納して出力する．その他の出力するDataset型のメンバには，受け取ったDataset型のメンバの値をそれぞれ代入する．|
   |Voicerecogconsumer|Dataset|Datasetのメンバphaseに文字列を格納して出力する．その他の出力するDataset型のメンバには，受け取ったDataset型のメンバの値をそれぞれ代入する．|
   |Seleniumconsumer|Dataset|Datasetのメンバphase，recogdataに文字列を格納して出力する．その他の出力するDataset型のメンバには，受け取ったDataset型のメンバの値をそれぞれ代入する．|

## 6. Sota_control
コミュニケーションロボットSotaを動かすためのコンポーネント．

**Dataport**

- Outport

| 名称   | 型  | 説明                              |
| -------- | ---------|-------------------------------- |
|text|string|Sotaを動かすためのコマンドを受け取る．|

## 7. Log
ユーザが使用したサービスを日にちごとにcsvファイルに記録するコンポーネント．

**Dataport**

- Outport

| 名称   | 型  | 説明                              |
| -------- | ---------|-------------------------------- |
|Log|string|ユーザが使用したサービス名をstringで受け取る.|

## 8. Callstaff
職員を呼び出すコンポーネント

**Dataset**

- Outport

| 名称   | 型  | 説明                              |
| -------- | ---------|-------------------------------- |
|Callstaff|boolean|Trueを受け取るとIoTデバイスに通信を送り職員を呼び出す．|

# 3. コンポーネントの接続
本コンポーネントは以下のように接続する．各コンポーネントにあるoutportのcontrolesotaはコンポーネントSota_controleのinportのtextにつなげる.
  
![image](https://github.com/sota2800/rtm/assets/141693046/6bf2ebc5-70bc-4983-9279-b53df679c435)






































