# 1-B. 개인 사용자 환경 (Windows/Unix)

이 문서는 개인 PC에서 연구실 실습을 진행할 수 있도록 **터미널 기반 개발 환경을 준비**하는 문서입니다.

핵심 목표:

1. 내 운영체제(Windows/macOS/Linux)에서 어떤 방식으로 Linux 명령어를 사용할지 결정
2. VS Code + Terminal + SSH 기반의 공통 작업 흐름을 준비
3. 준비가 끝나면 1-C(리눅스 기초) 또는 2-A(HPC 접속)로 자연스럽게 이동

---

## 0. 이 문서를 꼭 봐야 하나?

아래 조건을 만족하면 **1-B를 생략하고 2-A(SSH 접속)로 바로 이동**할 수 있습니다.

- 이미 터미널 사용이 익숙함
- SSH 접속 경험이 있음 (`ssh user@host`)
- VS Code + Remote-SSH 또는 일반 SSH 클라이언트 사용 가능

즉, WSL 설치는 모든 사용자 필수 단계가 아닙니다.

---

## 1. 어떤 로컬 환경을 선택할까? (결정 가이드)

### 1.1 Windows 사용자

- Linux 명령어를 로컬에서 직접 연습하고 싶다 → **WSL2 + Ubuntu 권장**
- 로컬 Linux는 필요 없고 원격 서버(SSH)만 쓸 계획이다 → WSL 생략 가능

### 1.2 macOS/Linux(Unix) 사용자

- 이미 POSIX 계열 터미널 환경을 기본 제공
- 별도 WSL 불필요
- Terminal/iTerm2(맥) 또는 기본 Terminal(리눅스)로 바로 진행 가능

---

## 2. 공통 준비: VS Code 먼저 설치

VS Code는 이후 문서(2-A)에서 원격 서버 편집/실행의 중심 도구로 사용됩니다.

### 2.1 설치

- 다운로드: <https://code.visualstudio.com/download>

### 2.2 권장 확장

- **Remote - SSH**: HPC 원격 접속
- **Python**: Python 코드 편집/실행 지원
- (선택) **Jupyter**: 노트북 작업

### 2.3 초기 점검

- VS Code 실행 가능
- 확장 설치 완료
- 터미널(`Ctrl+``) 열리는지 확인

---

## 3. Windows: WSL2 + Ubuntu 설치 (권장 경로)

### 3.1 설치

PowerShell(관리자 권한):

```powershell
wsl --install
```

설치 후 재부팅, Ubuntu 실행, 사용자 계정 생성.

### 3.2 버전/상태 확인

PowerShell:

```powershell
wsl --status
wsl -l -v
```

권장 상태:

- 기본 버전: WSL2
- Ubuntu 배포판: Running/Stopped 정상 표시

### 3.3 Ubuntu 터미널 기본 점검

```bash
uname -a
whoami
pwd
ls
```

### 3.4 권장 업데이트

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 3.5 자주 만나는 오류 참고

- 공식 설치 가이드: <https://learn.microsoft.com/windows/wsl/install>
- `0x80370102` 오류 참고: <https://stackoverflow.com/questions/62340566/fix-wslregisterdistribution-failed-with-error-0x80370102>

---

## 4. Unix(macOS/Linux) 사용자 가이드

“iTerm 쓰면 끝” 수준을 넘어서, 실제 SSH/HPC 작업에 필요한 최소 점검 항목을 아래에 정리합니다.

### 4.1 터미널/쉘 점검

```bash
echo $SHELL
which ssh
ssh -V
```

### 4.2 홈 디렉터리/권한 감각 점검

```bash
pwd
cd ~
pwd
ls -al
```

### 4.3 SSH 키 생성(권장)

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

- 기본 경로(`~/.ssh/id_ed25519`) 사용 권장
- passphrase 설정 권장

### 4.4 macOS 추가 팁

- 기본 Terminal도 충분하지만, iTerm2를 쓰면 탭/분할/검색이 편리함
- X11 GUI가 필요하면 XQuartz 설치 후 [2-B. X11 forwarding](./x11-forwarding.md) 진행

---

## 5. 문서 역할 분리 (중요)

이 문서는 **개인 환경 준비**만 다룹니다.

- X11 forwarding 상세 설정 → [2-B. X11 forwarding](./x11-forwarding.md)
- Conda/Python/Jupyter 상세 설정 → [1-D. 파이썬 패키지 관리](./python-setup.md)

---

## 6. 다음 단계 추천

### 6.1 리눅스 명령어가 익숙하지 않다면

- [1-C. 리눅스 기초 사용법](./linux-tutorial.md)

### 6.2 바로 서버 접속부터 하고 싶다면

- [2-A. SSH를 통한 클러스터 환경(HPC) 접속](./lab-cluster.md)

### 6.3 Python 실행 환경까지 먼저 만들고 싶다면

- [1-D. 파이썬 패키지 관리 (Anaconda)](./python-setup.md)
