ATOM 설치
===============================
## Contents
1. `xmlf90`와 `libGridXC` 설치
2. `ATOM` 설치

## 1. 필수 라이브러리 다운로드

`ATOM` 프로그램은 밀도범함수론 코드 `SIESTA`, `abinit`, 또는 `Quantum Esspresso`에 활용할 수 있는 다양한 형식(`psf`,`vps`, `psml`)의 원자 슈도포텐셜(pseudopential) 파일 만들 수 있다. 그 외에도 `ATOM`을 통해 온-전자(all-electron) 계산, 슈도포텐셜 테스트 등 다양한 계산을 수행할 수 있다. 

`xmlf90`은 Fortran 기반 프로그램에서 XML 형식의 파일을 읽고 쓰기 위한 라이브러리이다.
SIESTA 계열 코드에서는 계산 결과나 입력 정보를 XML 형태로 저장하거나 읽어들이는 기능이 사용되는데, 이를 위해 `xmlf90` 라이브러리가 필요하다.

`libGridXC`는 격자(grid) 기반에서 교환-상관(exchange-correlation) 에너지와 퍼텐셜을 계산하기 위한 라이브러리이다.
밀도범함수론(DFT) 계산에서 전자 밀도에 대한 교환-상관 항은 수치적 적분을 통해 계산되는데, `libGridXC`는 이러한 계산을 효율적으로 수행하기 위한 다양한 루틴을 제공한다.

`ATOM`를 설치하기 앞서 다음과 같은 패키지를 준비해야한다.  

`xmlf90`: <https://launchpad.net/xmlf90/+download> (1.5.0. 버전)

`libGridXC`: <https://launchpad.net/libgridxc/+download> (0.8.5 버전)

리눅스 환경에 다운로드한 후 압축을 풀어주는 명령어는 다음과 같다.

```bash
$ wget https://launchpad.net/xmlf90/trunk/1.5/+download/xmlf90-1.5.0.tgz // 1.5.0버전
$ wget https://launchpad.net/libgridxc/trunk/0.8/+download/libgridxc-0.8.5.tgz // 0.8.5버전
$ tar -xvzf xmlf90-1.5.0.tgz
$ tar -xvzf libgridxc-0.8.5.tgz
```

`tar` 명령어를 사용할 때에 `not in gzip format` 에러가 일어나는 경우 아래 명령어를 통해 `file`이 `tgz`형식인지 확인한다.
```bash
$ file (FileName)
```  


압축을 풀어준 위치에서 다음과 같은 과정을 통해 컴파일을 진행한다.

## 2. 설치

### `xmlf90` 설치:

```bash
$ cd xmlf90-1.5.0
$ mkdir Gfortran
$ cd Sys
$ cp gfortran.make ../Gfortran/fortran.mk
```

`gfortran.make` 파일이 없는 경우 홈페이지에서 다른 버전의 xmlf90을 다운받는다.


라이브러리를 생성하기 전에 fortran.mk을 (intel의 경우) 다음과 같이 수정해준다.

```bash  
LDFLAGS=-mkl=cluster
AR=/usr/bin/ar
```

이후 make명령어로 라이브러리를 빌드해준다.

```bash  
$ cd ../Gfortran
$ sh ../config.sh
$ make
```
- [x] `xmlf90.mk` 생성확인

### `libgridxc` 설치:

```bash
(설치한 위치로 돌아와서)
$ cd libgridxc-0.8.5
$ mkdir Gfortran
$ cd Gfortran
$ cp ../extra/fortran.mk .
```
마찬가지로 make를 하기 전 fortran.mk을 다음과 같이 수정해준다.

```bash  
LDFLAGS=-mkl=cluster
AR=/usr/bin/ar
```

```bash
$ sh ../src/config.sh
$ make clean
$ make
```


- [x]  `gridxc.mk` 생성확인

## 3. `ATOM` 설치

`ATOM`를 위한 라이브러리가 준비되었으니 이제 `ATOM`을 설치한다.  
`ATOM`: <https://siesta-project.org/SIESTA_MATERIAL/Pseudos/Code/downloads.html> (4.2.7 버전)

```bash
$ wget https://siesta-project.org/SIESTA_MATERIAL/Pseudos/Code/atom-4.2.7-100.tgz // 4.2.7버전
$ tar xvzf atom-4.2.7-100.tgz
```

`ATOM`도 마찬가지로 컴파일을 해야 한다. 압축을 풀어준 위치에서 컴파일을 진행한다.

### `ATOM` 설치:
```bash
$ cd atom-4.2.7-100
$ cp arch.make.sample arch.make
$ vi arch.make  # arch.make 파일 편집
```
`arch.make` 파일이 열리면 아래 부분에 ROOT를 수정한다. path는 '/' root 부터 절대 경로를 쓰고, 리눅스 명령어 *$ pwd* 로 절대경로를 확인할 수 있다.

```bash
XMLF90_ROOT= <설치한 xmlf90 위치>/xmlf90-1.5.0/Gfortran
GRIDXC_ROOT= <설치한 libgridxc 위치>/libgridxc-0.8.5/Gfortran
include $(XMLF90_ROOT)/xmlf90.mk
include $(GRIDXC_ROOT)/gridxc.mk
$ make
```

- [x]  `atm` 생성확인


이로서, `ATOM` 프로그램이 준비되었다.

