\# Tests



이 디렉터리는 DevSecOps Trading Platform Lab의 테스트 코드를 관리합니다.



\## 디렉터리 구조



```text

tests/

&#x20; \_\_init\_\_.py

&#x20; README.md

&#x20; smoke/                        # 기본 동작 확인

&#x20;   \_\_init\_\_.py

&#x20;   test\_api\_smoke.py

&#x20; integration/                  # DB 연동 후 통합 테스트

&#x20;   \_\_init\_\_.py

&#x20;   test\_accounts.py

&#x20;   test\_orders.py

&#x20;   test\_instruments.py

&#x20; validation/                   # 검증 규칙 전용

&#x20;   \_\_init\_\_.py

&#x20;   test\_accounts\_validation.py

&#x20;   test\_orders\_validation.py

&#x20; security/                     # 보안 시나리오 (Blue/Red 팀)

&#x20;   \_\_init\_\_.py

&#x20;   test\_redteam.py

&#x20;   test\_blueteam.py

&#x20;   test\_audit\_log.py

&#x20; e2e/                          # 전체 흐름 End-to-End

&#x20;   \_\_init\_\_.py

&#x20;   test\_trading\_flow.py

&#x20;   test\_risk\_check.py

&#x20; performance/                  # 성능 테스트

&#x20;   \_\_init\_\_.py

&#x20;   test\_load.py

```



\## 테스트 유형



| 유형 | 폴더 | 목적 | 단계 |

|------|------|------|------|

| Smoke | `smoke/` | API 기본 동작, 상태 코드 확인 | ✅ 현재 |

| Validation | `validation/` | 검증 규칙 전용 | ✅ 현재 |

| Integration | `integration/` | DB 연동 후 데이터 흐름 확인 | DB 연동 후 |

| E2E | `e2e/` | 계좌→주문→체결→포지션 전체 흐름 | 도메인 확장 후 |

| Security | `security/` | Red/Blue 팀 시나리오 | 보안 단계 |

| Performance | `performance/` | 부하/응답속도 테스트 | 나중에 |



\## 명명 규칙





\### 파일명

test\_{대상}\_{테스트유형}.py

test\_api\_smoke.py

test\_accounts\_validation.py

test\_orders\_validation.py

test\_trading\_flow.py

test\_redteam.py



\### 함수명

test\_{행위}{대상}{기대결과}

```python

\# 정상 케이스

def test\_create\_account\_success():

def test\_get\_account\_by\_id\_success():

def test\_list\_instruments\_with\_market\_filter():



\# 에러/검증 케이스

def test\_create\_account\_with\_negative\_balance\_returns\_422():

def test\_create\_order\_without\_price\_for\_limit\_returns\_400():

def test\_create\_order\_with\_nonexistent\_account\_returns\_400():



\# 보안 케이스

def test\_sql\_injection\_on\_symbol\_returns\_400():

def test\_abnormal\_order\_quantity\_triggers\_alert():

```



\## 실행 방법



\### 전체 테스트

```bash

python -m pytest tests/

```

\### 유형별 실행



```bash

python -m pytest tests/smoke/

python -m pytest tests/validation/

python -m pytest tests/security/

python -m pytest tests/e2e/

```



\### 특정 파일 실행

```bash

python -m pytest tests/smoke/test\_api\_smoke.py

```



\### 직접 실행 (pytest 없이)

```bash

python tests/smoke/test\_api\_smoke.py

```



\## 버전 관리 원칙



\- 파일명은 역할/목적으로 \*\*고정\*\*

\- 변경 이력은 \*\*Git commit\*\* 으로 관리

\- 파일명에 버전 번호(`\_v1`, `\_v2`) 를 붙이지 않음



\## 현재 구현된 테스트



| 파일 | 테스트 수 | 설명 |

|------|-----------|------|

| `smoke/test\_api\_smoke.py` | 19개 | 전체 API 기본 동작 확인 |







