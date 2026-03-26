# KAIST EE YHKimLab Wiki

YHKimLab 위키는 MkDocs 기반 문서 사이트입니다.  
연구실 공용 실습 문서(리눅스/HPC/Python/계산 툴)와 튜토리얼을 관리합니다.

- 배포 페이지: [https://yhklab.github.io/YHKimLab/site/](https://yhklab.github.io/YHKimLab/site/)

---

## 1. 문서 구조(시작하기)

아래 트리는 홈페이지 메뉴(`mkdocs.yml > nav`)의 기준입니다.

```text
Home
└── index.md

시작하기
├── 1. 리눅스
│   ├── A. 리눅스 환경 개요                 (docs/getting-started/linux-introduction.md)
│   ├── B. 개인 사용자 환경 (Windows/Unix)  (docs/getting-started/wsl.md)
│   ├── C. 리눅스 기초 사용법               (docs/getting-started/linux-tutorial.md)
│   └── D. 파이썬 패키지 관리 (Anaconda)    (docs/getting-started/python-setup.md)
└── 2. 원격 개발 환경 구축
    ├── A. SSH를 통한 클러스터 환경(HPC) 접속 (docs/getting-started/lab-cluster.md)
    └── B. X11 forwarding                    (docs/getting-started/x11-forwarding.md)
```

### 트리별 역할

- **Home**: 위키 입구(랩 소개, 핵심 페이지 링크)
- **1. 리눅스**: 로컬 환경 준비 + 기본 Linux 역량 확보
- **2. 원격 개발 환경 구축**: 실제 HPC 접속/원격 개발/GUI(X11) 설정

> 운영 원칙: 문서 파일 경로와 `mkdocs.yml`의 nav 경로를 항상 함께 수정합니다.

---

## 2. 시작하기 권장 동선

기본 동선:

`1-A → 1-B → 1-C → 1-D → 2-A → 2-B`

예외(중요):

- 이미 Linux/macOS 터미널 및 SSH 사용이 가능하면, **1-B(WSL)는 생략하고 2-A로 바로 진행 가능**합니다.

---

## 3. 로컬 개발/미리보기

### 의존성 설치

```bash
pip install -r requirements.txt
```

### 로컬 서버 실행

```bash
mkdocs serve
```

### 정적 사이트 빌드

```bash
mkdocs build
```

---

## 4. 저장소 연결 및 업데이트

```bash
git clone https://github.com/yhkimlab/YHKimLabWiki.git
cd YHKimLabWiki
git remote -v
```

수정 후:

```bash
git add .
git commit -m "update tutorial"
git push origin main
```

---

## 5. 문서 작성 규칙(요약)

1. 문서를 삭제하기보다 기존 설명을 유지/보강합니다.
2. 초심자용 문서는 “개요 → 준비물 → 단계 → 검증 → 트러블슈팅” 순서를 권장합니다.
3. 이미지 링크가 있는 기존 문서는 가능하면 그대로 유지합니다.
4. 메뉴명과 파일 주제가 맞지 않으면 파일 분리 또는 nav 경로를 수정합니다.
