# face_collection

### 실행 순서

- git clone

```bash
git clone https://github.com/thsckdduq/face_collection.git
```
<br>

- git clone한 face collection 폴더로 이동
```bash
cd face_collection
```
<br>

- requirements 다운로드

```bash
pip install -U pip

pip install -r requirements.txt
```
<br>

- dlib 패키지 다운로드
```bash
python -m pip install models\dlib-19.22.99-cp37-cp37m-win_amd64.whl
```
<br>

- data folder 만들기

```bash
mkdir data
```

- 보정하고 싶은 이미지 파일 data folder에 넣기

<br>

- main.py 실행
```bash
python main.py
```
<br>

- 결과 파일 result 폴더로 저장 -> result 폴더 확인

### 접근 방법
- 처음에는 stable diffusion 모델을 활용하여 이미지 수정을 하려고 시도했지만, 모델이 너무 크고, finetuning을 하지 않을경우 결과가 좋게 나오지 않아 포기
- 2 번째로 얼굴의 각 부위를 segmentation을 통해 구분하고 특정 부분을 보정하는 작업을 진행하려 했지만, segmentation은 잘됐지만, 특정 부분의 명칭이 틀리거나, 좌표값을 얻기 어려워서 포기
- 마지막으로 dlib 패키지를 사용하여 face landmark를 통해 눈, 코의 좌표값을 얻은 후 눈은 볼록렌즈 효과를 통하여 확대, 코는 리퀴파이 변형을 통하여 축소 진행

++ 모든 실험 과정은 experiments.ipynb 파일에 저장해두었습니다.

### 참고 페이지
- dlib 패키지를 활용한 얼굴 랜드마크: https://webnautes.tistory.com/2049
- 리퀴파이 도구: https://bkshin.tistory.com/entry/OpenCV-16-%EB%AA%A8%EC%9E%90%EC%9D%B4%ED%81%AC-%EC%B2%98%EB%A6%ACMosaic-%EB%A6%AC%ED%80%B4%ED%8C%8C%EC%9D%B4Liquify-%EC%99%9C%EA%B3%A1-%EA%B1%B0%EC%9A%B8Distortion-Mirror
- 오목/볼록렌즈 효과: https://bkshin.tistory.com/entry/OpenCV-15-%EB%A6%AC%EB%A7%A4%ED%95%91Remapping-%EC%98%A4%EB%AA%A9%EB%B3%BC%EB%A1%9D-%EB%A0%8C%EC%A6%88-%EC%99%9C%EA%B3%A1Lens-Distortion-%EB%B0%A9%EC%82%AC-%EC%99%9C%EA%B3%A1Radial-Distortion?category=1148027
- face-segmentation 관련 코드: https://huggingface.co/spaces/taewon99/face-segmentation/blob/main/app.py , https://huggingface.co/jonathandinu/face-parsing
- stable-diffusion 관련 코드: https://huggingface.co/radames/stable-diffusion-x4-upscaler-img2img , https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0