KAIST EE YHKim Lab wiki site

pip install -r requirements.txt/

mkdocs build
mkdocs serve

clone 시 자동으로 원격 저장소에 연결된다.
git clone https://github.com/yhkimlab/YHKimLabWiki.git
git remote -v

수정 후

git add .
git commit -m "update tutorial"
git push origin main

하면 수정 사항이 업데이트 된다.

[https://yhklab.github.io/YHKimLabWiki/site/](https://yhklab.github.io/YHKimLabWiki/site/)