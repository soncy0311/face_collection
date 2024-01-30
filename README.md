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

- result 폴더 확인

### 접근 방법
- 처음에는 stable diffusion 모델을 활용하여 이미지 수정을 하려고 시도했지만, 모델이 너무 크고, finetuning을 하지 않을경우 결과가 좋게 나오지 않아 포기
- 2 번째로 얼굴의 각 부위를 segmentation을 통해 구분하고 특정 부분을 보정하는 작업을 진행하려 했지만, segmentation은 잘됐지만, 특정 부분의 명칭이 틀리거나, 좌표값을 얻기 어려워서 포기
- 마지막으로 dlib 패키지를 사용하여 face landmark를 통해 눈, 코의 좌표값을 얻은 후 눈은 볼록렌즈 효과를 통하여 확대, 코는 리퀴파이 변형을 통하여 축소 진행

++ 모든 실험 과정은 experiments.ipynb 파일에 저장해두었습니다.