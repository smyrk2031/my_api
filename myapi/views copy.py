from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response


#from .serializers import ImageSerializer    # CLIPモデル


"""
APIの種類
img2img: opencvの画像変換
img2img: anime2sketchによる線画変換
img2img: SAMによる画像のセグメンテーションマスク変換
img2txt: openai-CLIPによる指定文字との類似度計算
img2txt: CLIP-interrogatorよる画像の文字変換
txt2img: Stable diffusionよる画像生成
txt2tex: LLMによる文章要約

"""


class TestView(APIView):
    def get(self, request):
        return Response({'message': 'test_ok'})


# opencvの画像変換
import io, json
import base64
from .src.Anime2Sketch import test
from PIL import Image
class cv_img_trans_View(APIView):
    print("API実行: opencvの画像変換")
    def post(self, request):
        print("-**- "*10)
        print("◆API実行: opencvの画像変換")
        try:
            # Pillowを使用して画像のグレースケール変換を行う
            data = json.loads(request.body.decode('utf-8'))
            base64_image_data = data.get('img')

            # base64デコードする
            binary_data = base64.b64decode(base64_image_data)
            # バイナリデータを画像データに変換する
            img = Image.open(io.BytesIO(binary_data))
            gray_img = img.convert('L')
            # 変換後の画像をメモリ上に一時的に保存
            buf = io.BytesIO()
            gray_img.save(buf, format='PNG')
            image_base64 = base64.b64encode(buf.getvalue()).decode().replace("'", "")
            print("◆API実行完了: anime2sketch_View")
            print("-**- "*10)
            return Response({'image_url': image_base64})
        except:
            print("実行エラー発生")
            return Response({'image_url': "error"})

# anime2sketchによる線画変換
import io, json
import base64
from .src.Anime2Sketch import test
from PIL import Image
class anime2sketch_View(APIView):
    print("API実行: anime2sketch_View")
    def post(self, request):
        print("-**- "*10)
        print("◆API実行: anime2sketch_View")
        try:
            # Pillowを使用して画像のグレースケール変換を行う
            data = json.loads(request.body.decode('utf-8'))
            base64_image_data = data.get('img')

            # base64デコードする
            binary_data = base64.b64decode(base64_image_data)
            # バイナリデータを画像データに変換する
            img = Image.open(io.BytesIO(binary_data))
            gray_img = img.convert('L')
            # 変換後の画像をメモリ上に一時的に保存
            buf = io.BytesIO()
            gray_img.save(buf, format='PNG')
            image_base64 = base64.b64encode(buf.getvalue()).decode().replace("'", "")
            print("◆API実行完了: anime2sketch_View")
            print("-**- "*10)
            return Response({'image_url': image_base64})
        except Exception as e:
            print("API実行でエラーが発生しました")
            # 例外が発生した場合に実行する処理
            print(f"エラーが発生しました: {e}")
            return Response({'image_url': "error"})

# openai-CLIPによる指定文字との類似度計算
from io import BytesIO
import numpy as np
import torch
import clip
from PIL import Image
class openaiCLIP_View(APIView):
    print("API実行: openaiCLIP_View")
    def post(self, request):
        print("-**- "*10)
        print("◆API実行: openaiCLIP_View")
        try:
            # モデルの読み込み
            device = "cuda" if torch.cuda.is_available() else "cpu"
            device = "cpu"
            print(device)
            model, preprocess = clip.load("ViT-B/32", device=device)

            # 入力画像取得
            data = json.loads(request.body.decode('utf-8'))
            base64_image_data = data.get('img')
            # base64データをデコードしてPillowデータに変換する
            decoded_image_data = base64.b64decode(base64_image_data)
            pil_image_data = Image.open(BytesIO(decoded_image_data))

            # CLIPの類似度確認
            #target_conf = ["a human", "a dog", "a cat"]
            #print(target_conf)
            target_conf = data.get('list_txt')
            # 取得した文字列のリストから空要素を除去する
            target_conf = [x for x in target_conf if x]
            print(target_conf)

            #target_conf_bin = data.get('list_txt_bin')
            #target_conf = [x for x in target_conf if x]
            #print(target_conf_bin)


            
            # 画像とテキストの準備
            #image = preprocess(Image.open(target_conf[0])).unsqueeze(0).to(device)
            image = preprocess(pil_image_data).unsqueeze(0).to(device)
            text = clip.tokenize(target_conf).to(device)

            with torch.no_grad():
                # 推論
                logits_per_image, logits_per_text = model(image, text)
                probs = logits_per_image.softmax(dim=-1).cpu().numpy()

            # 類似率の出力
            print("= - "*10)
            list_result = []
            for i in range(len(target_conf)):
                output_text = str(target_conf[i]) + " : " + str(probs[0][i])
                list_result.append(output_text)
                print(output_text)
            print("= - "*10)
            print(list_result)



            # Pillowを使用して画像のグレースケール変換を行う
            #data = json.loads(request.body.decode('utf-8'))
            #base64_image_data = data.get('img')

            ## base64デコードする
            #binary_data = base64.b64decode(base64_image_data)
            ## バイナリデータを画像データに変換する
            #img = Image.open(io.BytesIO(binary_data))
            #gray_img = img.convert('L')
            ## 変換後の画像をメモリ上に一時的に保存
            #buf = io.BytesIO()
            #gray_img.save(buf, format='PNG')
            #image_base64 = base64.b64encode(buf.getvalue()).decode().replace("'", "")
            print("◆API実行完了: openaiCLIP_View")
            print("-**- "*10)
            return Response({'clip_text': list_result})
        #except:
        #    print("実行エラー発生")
        #    return Response({'clip_text': "error"})
        except Exception as e:
            print("API実行でエラーが発生しました")
            # 例外が発生した場合に実行する処理
            print(f"エラーが発生しました: {e}")
            return Response({'clip_text': "error"})
        
#class CategoryView(generics.GenericAPIView):
#    serializer_class = ImageSerializer

#    def post(self, request, *args, **kwargs):
#        serializer = self.get_serializer(data=request.data)
#        serializer.is_valid(raise_exception=True)
#        image = serializer.validated_data['image']
#        category = predict_category(image.path)
#        return Response({'category': category})