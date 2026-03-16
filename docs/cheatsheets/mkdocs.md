# MkDocs Cheat Sheet


## 정적 사이트 빌드

```bash
mkdocs build
```

- 결과물은 `site/` 디렉터리에 생성된다.
- 배포 전에 링크나 nav 구성이 맞는지 확인할 때 사용한다.

## 로컬 미리보기

```bash
mkdocs serve
```

- 기본 주소: `http://127.0.0.1:8000`
- 문서를 수정하면 자동으로 다시 반영된다.


## 배포

```bash
mkdocs gh-deploy
```

- GitHub Pages로 배포할 때 사용하는 명령이다.
- 배포 전에 먼저 `mkdocs build`로 로컬 확인을 권장한다.

## 자주 쓰는 작업 흐름

```bash
pip install -r requirements.txt
mkdocs serve
mkdocs build
```

## Markdown 작성법

MkDocs 문서는 기본적으로 Markdown으로 작성한다. 아래 내용은 `how-to-write-by-markdown.md` 내용을 기준으로, MkDocs 문서 작성에 바로 사용할 수 있게 정리한 것이다. 사진 예시는 제외했다.

### 1. Markdown이란?

[Markdown](https://www.markdownguide.org/getting-started/)은 텍스트 기반 마크업 언어로, 쉽게 쓰고 읽을 수 있으며 HTML로 변환이 가능하다. 특수기호와 문자를 이용한 단순한 구조의 문법을 사용하기 때문에 문서를 빠르게 작성하고 가독성 있게 정리할 수 있다.

MkDocs에서도 문서 본문은 대부분 Markdown으로 작성하며, 필요하면 HTML 태그를 함께 사용할 수도 있다.

### 2. Markdown의 장단점

장점:

1. 간결하다.
2. 별도 도구 없이 작성 가능하다.
3. 다양한 형태로 변환 가능하다.
4. 텍스트 파일이라 용량이 작고 보관이 쉽다.
5. 버전 관리 시스템으로 변경 이력을 관리하기 좋다.
6. 지원하는 프로그램과 플랫폼이 다양하다.

단점:

1. 표준이 완전히 하나로 통일되어 있지 않다.
2. 도구에 따라 변환 방식이나 결과가 조금씩 다를 수 있다.
3. 모든 HTML 표현을 완전히 대체하지는 못한다.

---

### 3. Markdown 사용법

#### 3.1 제목 Headers

큰 제목:

```md
This is an H1
=============
```

작은 제목:

```md
This is an H2
-------------
```

일반적으로는 `#` 문법을 더 많이 사용한다.

```md
# This is a H1
## This is a H2
### This is a H3
#### This is a H4
##### This is a H5
###### This is a H6
```

MkDocs 문서에서는 보통 아래처럼 사용한다.

```md
# 문서 제목
## 섹션 제목
### 하위 섹션 제목
```

#### 3.2 인용문 BlockQuote

이메일에서 사용하는 `>` 문자를 이용한다.

```md
> This is a first blockquote.
> > This is a second blockquote.
> > > This is a third blockquote.
```

인용문 안에 다른 Markdown 요소를 포함할 수도 있다.

````md
> ### This is a H3
> - List
> - Another item
>
> ```bash
> mkdocs serve
> ```
````

#### 3.3 목록

순서 있는 목록은 숫자와 점을 사용한다.

```md
1. 첫번째
2. 두번째
3. 세번째
```

순서 없는 목록은 `*`, `+`, `-`를 사용할 수 있다.

```md
* 빨강
  * 녹색
    * 파랑
```

```md
+ 빨강
  + 녹색
    + 파랑
```

```md
- 빨강
  - 녹색
    - 파랑
```

혼합해서 사용하는 것도 가능하다.

```md
* 1단계
  - 2단계
    + 3단계
      + 4단계
```

#### 3.4 코드

들여쓰기 방식:

```md
This is a normal paragraph:

    This is a code block.

end code block.
```

코드 블록은 두 가지 방식이 많이 쓰인다.

`<pre><code>` 사용:

```md
<pre>
<code>
public class Main {
  public static void main(String[] args) {
    System.out.println("Hello");
  }
}
</code>
</pre>
```

백틱 3개 사용:

````md
```java
public class Main {
  public static void main(String[] args) {
    System.out.println("Hello");
  }
}
```
````

실제로 MkDocs에서는 백틱 3개 코드 블록을 가장 많이 쓴다.

예:

````md
```bash
mkdocs serve
mkdocs build
mkdocs gh-deploy
```
````

언어 이름을 함께 적으면 문법 강조가 적용된다.

인라인 코드는 다음처럼 쓴다.

```md
`mkdocs serve`
```

#### 3.5 수평선

아래 예시는 모두 수평선을 만든다.

```md
* * *

***

*****

- - -

---------------------------------------
```

문서 구간을 나누거나 큰 섹션을 구분할 때 자주 사용한다.

#### 3.6 링크

참조 링크:

```md
[link keyword][id]

[id]: https://google.com "Optional Title here"
```

예:

```md
Link: [Google][googlelink]

[googlelink]: https://google.com "Go google"
```

일반 링크:

```md
[MkDocs](https://www.mkdocs.org/)
```

자동 링크:

```md
<http://example.com/>
<address@example.com>
```

#### 3.7 강조

```md
*single asterisks*
_single underscores_
**double asterisks**
__double underscores__
~~cancelline~~
```

자주 쓰는 형태만 보면 아래와 같다.

```md
*기울임*
**굵게**
~~취소선~~
```

문장 중간에서 강조를 사용할 때는 가독성을 위해 띄어쓰기를 적절히 넣는 편이 좋다.

#### 3.8 줄바꿈

문장 끝에 공백 2칸 이상을 넣으면 줄바꿈된다.

```md
첫 번째 줄  
두 번째 줄
```

또는 문단을 분리하려면 한 줄을 비우면 된다.

```md
첫 번째 문단

두 번째 문단
```

---

### 4. MkDocs에서 자주 쓰는 작성 예시

````md
# 실험 환경 설정

## 설치

```bash
pip install -r requirements.txt
```

## 실행

```bash
mkdocs serve
```

## 참고 링크

- [MkDocs 공식 문서](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)

> 로컬 서버 기본 주소는 `http://127.0.0.1:8000` 이다.
````
