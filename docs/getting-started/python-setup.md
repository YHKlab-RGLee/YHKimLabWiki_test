# 1-D. 파이썬 패키지 관리 (Anaconda)

이 문서는 연구실 실습에서 Python 환경이 사람마다 달라서 생기는 문제를 줄이기 위해,  
**Conda 기반으로 재현 가능한 실행 환경을 구성**하는 방법을 설명합니다.

핵심 목표:

1. Anaconda/Miniconda 설치
2. 프로젝트용 가상환경 생성
3. 필수 패키지 설치
4. Python/Jupyter 실행
5. 환경 내보내기/복원으로 재현성 확보

---

## 0. 왜 conda를 쓰는가?

연구실에서는 다음 문제가 자주 발생합니다.

- A 학생은 실행되는데 B 학생은 실행이 안 됨
- 패키지 버전 충돌(`numpy`, `scipy`, `matplotlib` 등)
- OS가 달라 동일 코드가 다르게 동작

Conda 환경을 사용하면 프로젝트 단위로 버전을 고정하고 공유할 수 있어, 실습/과제/연구 재현성이 높아집니다.

---

## 1. 배포판 선택: Anaconda vs Miniconda

- **Anaconda**: 패키지가 많이 포함된 풀 배포판 (초심자 친화적, 용량 큼)
- **Miniconda**: 최소 설치 후 필요한 패키지만 추가 (가볍고 유연)

권장 기준:

- 처음 시작 / 설치 편의 우선 → Anaconda
- 환경 가벼움 / 팀 프로젝트 표준화 우선 → Miniconda

---

## 2. 설치 단계

### 2.1 설치 파일 다운로드

- Miniconda: <https://docs.conda.io/en/latest/miniconda.html>
- Anaconda: <https://www.anaconda.com/download>

기존 실습 이미지(Windows 예시):

![Py_001](../../getting-started/img/python-setup-01.png)

### 2.2 설치 실행

installer를 실행해 기본 설정으로 설치합니다.

![Py_002](../../getting-started/img/python-setup-02.png)
![Py_003](../../getting-started/img/python-setup-03.png)

설치 후 Anaconda Prompt(또는 macOS/Linux Terminal)를 실행합니다.

![Py_004](../../getting-started/img/python-setup-04.png)

### 2.3 설치 검증

```bash
conda --version
python --version
```

![Py_005](../../getting-started/img/python-setup-05.png)

---

## 3. 연구실 권장 기본 환경 만들기

### 3.1 새 환경 생성

```bash
conda create -n yhklab-py311 python=3.11 -y
```

### 3.2 환경 활성화

```bash
conda activate yhklab-py311
```

프롬프트 앞에 `(yhklab-py311)`가 보이면 활성화된 상태입니다.

### 3.3 필수 패키지 설치

```bash
conda install ipython numpy scipy pandas matplotlib jupyter -y
```

![Py_006](../../getting-started/img/python-setup-06.png)

필요 시 pip 패키지 추가:

```bash
pip install ase
```

### 3.4 현재 환경 확인

```bash
conda list
```

---

## 4. Python 실행 방법 3가지

### 4.1 IPython 셸

빠르게 한 줄 테스트할 때 유용합니다.

```bash
ipython
```

```python
print("Hello World")
```

![Py_007](../../getting-started/img/python-setup-07.png)

### 4.2 `.py` 스크립트 실행

`hello_world.py` 예시:

```python
print("Hello World")
```

실행:

```bash
python hello_world.py
```

![Py_008](../../getting-started/img/python-setup-08.png)
![Py_009](../../getting-started/img/python-setup-09.png)

### 4.3 Jupyter Notebook

```bash
jupyter notebook
```

![Py_010](../../getting-started/img/python-setup-10.png)
![Py_011](../../getting-started/img/python-setup-11.png)

---

## 5. WSL/원격 환경에서 Jupyter 설정 (보강)

WSL 또는 원격 환경에서는 브라우저 자동 실행이 오히려 불편할 수 있습니다.

### 5.1 설정 파일 생성

```bash
jupyter notebook --generate-config
```

### 5.2 설정 파일 수정

파일: `~/.jupyter/jupyter_notebook_config.py`

다음 중 하나를 설정합니다.

#### 옵션 A) 브라우저 경로를 명시

```python
c.NotebookApp.browser = '/usr/bin/firefox %s'
```

#### 옵션 B) 자동 브라우저 실행 끄기 (권장)

```python
c.NotebookApp.open_browser = False
```

옵션 B를 사용하면 `jupyter notebook` 실행 후 터미널에 나타난 URL을 복사해 직접 접속합니다.

---

## 6. 환경 저장/복원 (팀 작업 필수)

### 6.1 환경 내보내기

```bash
conda env export --no-builds > environment.yml
```

### 6.2 환경 복원

```bash
conda env create -f environment.yml
```

### 6.3 환경 관리 명령 모음

```bash
conda env list
conda activate yhklab-py311
conda deactivate
conda env remove -n yhklab-py311
```

---

## 7. 트러블슈팅 빠른 점검

1. `conda` 명령이 안 잡힘
   - 터미널 재시작
   - 설치 경로/초기화(`conda init`) 확인
2. 패키지 설치 충돌
   - 새 환경을 다시 생성해서 설치
3. Jupyter 접속 실패
   - `open_browser=False` 설정 후 URL 직접 접속

---

## 8. 다음 문서

환경 준비가 끝났다면 원격 실습으로 이동하세요.

- [2-A. SSH를 통한 클러스터 환경(HPC) 접속](./lab-cluster.md)

(참고) Python 철학:

```python
import this
```
