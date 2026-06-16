네이밍 규칙 확정

대상	규칙	예시

디렉터리/폴더	camelCase	agenticAi/ kisaRag/

Python 파일	snake\_case	red.py blue.py

JS 파일	camelCase	orderPanel.js

규약 파일	원본 유지	README.md .env setup.py docker-compose.yml





현재 tree 기준으로 발견된 문제점 5가지와 수정 방법을 정리했습니다.



필수 수정 4가지:

appfrontend/ → appFrontEnd/ (camelCase 불일치)

security\_pipeline/ → securityPipeline/ (camelCase 불일치)

kisa\_guidelines/ → kisaGuidelines/ (camelCase 불일치)

dashboard/static/ → 제거 (설계에 없는 불필요 폴더)



나머지 구조(agenticAi/, app/, dashboard/src/components/ 하위, infra/, data/, tests/, docs/)는 설계와 일치합니다.





네이밍 규칙: 서비스 → {도메인}\_service.py, 어댑터 → {소스}\_{역할}.py, 나머지 → {도메인}.py

