# 1-C. 리눅스 기초 사용법

이 문서는 HPC 실습에 바로 필요한 Linux 기초 명령어를 단계적으로 정리한 문서입니다.

---

## 1. 목표

- 터미널 기반 작업 흐름 이해
- 파일/폴더 조작 명령어 습득
- 실행 권한과 간단한 스크립트 실행
- SSH 이후 원격 작업 시 실수 줄이기

---

## 2. 기본 개념

### 2.1 현재 위치와 경로

- 현재 위치 확인: `pwd`
- 현재 위치 목록 보기: `ls`
- 홈 디렉터리로 이동: `cd ~`

### 2.2 절대경로 vs 상대경로

- 절대경로: `/home/class/project`
- 상대경로: `./project`, `../project`

---

## 3. 가장 많이 쓰는 명령어

```bash
pwd                 # 현재 경로
ls                  # 파일 목록
ls -al              # 숨김 파일 포함 상세 목록
cd <path>           # 디렉터리 이동
mkdir <dir>         # 폴더 생성
touch <file>        # 빈 파일 생성
cp <src> <dst>      # 복사
mv <src> <dst>      # 이동/이름변경
rm <file>           # 파일 삭제 (주의)
cat <file>          # 파일 내용 출력
less <file>         # 페이지 단위로 보기
chmod +x <file>     # 실행권한 추가
```

---

## 4. 실습 1: 작업 폴더 만들기

```bash
mkdir -p ~/linux-practice
cd ~/linux-practice
pwd
ls -al
```

---

## 5. 실습 2: 파일 만들고 읽기

```bash
echo "Hello Linux" > hello.txt
cat hello.txt
```

추가 쓰기:

```bash
echo "Second line" >> hello.txt
cat hello.txt
```

---

## 6. 실습 3: 복사/이동/삭제

```bash
cp hello.txt hello_copy.txt
mv hello_copy.txt hello_moved.txt
ls
rm hello_moved.txt
ls
```

> `rm` 실행 전 `ls`로 대상 파일을 꼭 확인하세요.

---

## 7. 실습 4: 실행 권한과 셸 스크립트

`hello.sh` 생성:

```bash
cat > hello.sh <<'SH'
#!/bin/bash
echo "Hello Linux"
SH
```

실행권한 부여 및 실행:

```bash
chmod +x hello.sh
./hello.sh
```

---

## 8. 권한 보기 (`ls -l`)

```bash
ls -l hello.sh
```

예시 출력:

```text
-rwxr-xr-x 1 class class 28 ... hello.sh
```

- 앞의 `x`가 실행 가능 권한을 의미합니다.

---

## 9. 실수 방지 체크리스트

1. 작업 전에 `pwd` 확인
2. 삭제/이동 전에 `ls` 확인
3. 공용 경로에서 대량 삭제 금지
4. 실행 전 스크립트 내용 `cat`으로 확인

---

## 10. 다음 단계

- Python 환경/패키지 관리: [1-D. 파이썬 패키지 관리 (Anaconda)](./python-setup.md)
- 원격 SSH 실습: [2-A. SSH를 통한 클러스터 환경(HPC) 접속](./lab-cluster.md)
