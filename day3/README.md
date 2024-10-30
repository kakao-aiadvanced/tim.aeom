

## 4. Fine Tuning

[강의 자료](https://docs.google.com/presentation/d/13WYhEEbpM7ydIixcR-h_Dd_H5qk81kwrjW0T5MpEmU0/edit#slide=id.p)


### Quantization LoRA

Quantization - 정보 손실 압축과 같음  
연산 성능은 줄어들 수 있다...
각 비트 블럭마다 일정한 수를 나누어 ..
Normal float - 정보 손실의 성능을 최소화하기 위해 정규 분포를 따라 0과 가까운 곳 손실 줄임.  


### Open AI fine-tuning


## 5. Evaluation
벤치마크 결과의 해석은 잘 해야함.  
"작은 모델이 특정 벤치마크에서 좋았다."  
벤치마크 문제-답을 학습한 경우 가능.  
벤치마크 결과가 좋으면 좋은 모델은 아니지만,  
결과가 아주 나쁘면 좋은 모델이 아니다.

### 벤치마크 .. 지표 
ROUGE..X  
BLEU..X

목적에 따라 . 서비스에 따라 적당한 지표를 찾아야 한다.  

## 6. Function Call
LLM 에게 어떤 함수가 있는지 알려주고,   
어떻게 호출하는지 알려주고..  
프롬프트로!  


LLM 이 잘하지 못하는 것. 계산, 코딩.

### API Spec
인증이 필요한 경우에는 ?

### 스레딩..? 컨텍스트
어떻게 유지될까


## 추천 자료
https://www.cursor.com/
https://www.rewind.ai/
---
카카오 종목 코드 : `035720`