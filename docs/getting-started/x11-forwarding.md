# 2-B. X11 forwarding

이 문서는 HPC에서 GUI 프로그램(예: `ase gui`, `xclock`)을 로컬 PC 화면으로 전달하는 X11 forwarding 설정 가이드입니다.

---

## 1. 언제 필요한가?

- GUI 앱을 원격 서버에서 띄울 때 필요
- CLI 계산/편집만 할 경우 생략 가능

---

## 2. 운영체제별 준비

### 2.1 Windows

- X 서버 설치: **VcXsrv** 또는 **Xming**
- 실행 상태에서 SSH 접속

### 2.2 macOS

- **XQuartz** 설치/실행

### 2.3 Linux

- 일반적으로 기본 X11 환경 사용 가능

---

## 3. SSH 옵션

터미널 접속 시:

```bash
ssh -X <계정>@<호스트>
```

신뢰 포워딩이 필요하면:

```bash
ssh -Y <계정>@<호스트>
```

`~/.ssh/config` 예시:

```ssh-config
Host yhklab-hpc-x11
    HostName gold.kaist.ac.kr
    User class
    ForwardX11 yes
    ForwardX11Trusted yes
```

---

## 4. 동작 확인

원격 접속 후:

```bash
echo $DISPLAY
xclock
```

또는

```bash
xeyes
```

창이 로컬 PC에 뜨면 정상입니다.

---

## 5. 자주 발생하는 문제

1. `Error: Can't open display`
   - X 서버 미실행(Windows/macOS)
   - `ssh -X` 없이 접속함
2. 너무 느림
   - 네트워크 지연이 큰 경우 CLI 위주 사용 권장
3. VS Code Remote에서 GUI 안 뜸
   - 터미널 세션에서 `DISPLAY` 값 확인

---

## 6. 참고

- SSH/HPC 기본 접속은 [2-A. SSH를 통한 클러스터 환경(HPC) 접속](./lab-cluster.md) 문서를 먼저 완료한 뒤 진행하세요.
