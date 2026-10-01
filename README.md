# TkRTSP Viewer

OpenCV로 RTSP 영상을 읽고 Tkinter 창에 표시하는 Python 예제입니다. 영상 수신 스레드와 화면 갱신을 나누고 시작·정지 및 종료 처리를 구현합니다.

## 구성과 실행

핵심 구현은 [main.py](main.py)에 있습니다. 기존 개발 환경은 Python 3.9이며 OpenCV, Pillow와 Tkinter가 필요합니다.

```bash
python -m pip install -r requirements.txt
python main.py
```

먼저 코드의 RTSP 입력을 사용 가능한 카메라 주소로 설정해야 합니다. GUI를 표시할 수 있는 환경이 필요하며, `requirements.txt`는 당시 환경의 의존성 목록이므로 현재 Python과의 호환성을 확인하세요.
