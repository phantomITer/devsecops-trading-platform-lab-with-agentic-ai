📁 agenticAi/core/ — Phase 2 (공통 라이브러리)

text

📁 agenticAi/core/

&#x20;   📄 \_\_init\_\_.py

&#x20;   📄 base\_agent.py           # 모든 에이전트의 부모 클래스

&#x20;                              #  - run(), stop(), status() 인터페이스

&#x20;                              #  - API 클라이언트 공통 연결

&#x20;                              #  - 로그 전송 (→ app/api/agent\_logs)



&#x20;   📄 ollama\_client.py        # Ollama LLM 클라이언트 래퍼

&#x20;                              #  - 모델 선택 (llama3, mistral 등)

&#x20;                              #  - 스트리밍 응답 처리

&#x20;                              #  - 프롬프트 템플릿 관리



&#x20;   📄 rag\_engine.py           # RAG 엔진

&#x20;                              #  - KISA 문서 청킹/임베딩

&#x20;                              #  - ChromaDB or FAISS 벡터스토어

&#x20;                              #  - 쿼리 → 관련 문서 검색



&#x20;   📄 tool\_registry.py        # 에이전트 공통 툴 등록소

&#x20;                              #  - pykrx 시세 조회 툴

&#x20;                              #  - 주문 실행 툴 (→ app/api/orders)

&#x20;                              #  - 포지션 조회 툴

&#x20;                              #  - 보안 이벤트 전송 툴



&#x20;   📄 memory.py               # 에이전트 메모리/상태 관리

&#x20;                              #  - 단기 메모리 (대화 컨텍스트)

&#x20;                              #  - 장기 메모리 (투자 히스토리)

&#x20;                              #  - 상태 직렬화/복원

📁 agenticAi/redAgent/ — Phase 3-① 🔴

text

📁 agenticAi/redAgent/

&#x20;   📄 \_\_init\_\_.py

&#x20;   📄 run.py                  # 독립 실행 엔트리포인트

&#x20;   📄 red\_agent.py            # Red Agent 메인 클래스

&#x20;                              #  - base\_agent.BaseAgent 상속

&#x20;                              #  - OWASP Top 10 공격 시나리오 실행



&#x20;   📁 agenticAi/redAgent/attacks/

&#x20;       📄 \_\_init\_\_.py

&#x20;       📄 a01\_broken\_access.py     # A01 - Broken Access Control

&#x20;       📄 a02\_crypto\_failures.py   # A02 - Cryptographic Failures

&#x20;       📄 a03\_injection.py         # A03 - SQL/Command Injection

&#x20;       📄 a04\_insecure\_design.py   # A04 - Insecure Design

&#x20;       📄 a05\_security\_misconfig.py # A05 - Security Misconfiguration

&#x20;       📄 a06\_vulnerable\_components.py # A06 - Vulnerable Components

&#x20;       📄 a07\_auth\_failures.py     # A07 - Auth \& Session Failures

&#x20;       📄 a08\_integrity\_failures.py # A08 - Software Integrity Failures

&#x20;       📄 a09\_logging\_failures.py  # A09 - Logging \& Monitoring Failures

&#x20;       📄 a10\_ssrf.py              # A10 - SSRF



&#x20;   📄 report\_generator.py     # 공격 결과 리포트 생성

📁 agenticAi/blueAgent/ — Phase 3-② 🔵

text

📁 agenticAi/blueAgent/

&#x20;   📄 \_\_init\_\_.py

&#x20;   📄 run.py                  # 독립 실행 엔트리포인트

&#x20;   📄 blue\_agent.py           # Blue Agent 메인 클래스

&#x20;                              #  - base\_agent.BaseAgent 상속

&#x20;                              #  - RAG 기반 KISA 가이드라인 방어



&#x20;   📁 agenticAi/blueAgent/defense/

&#x20;       📄 \_\_init\_\_.py

&#x20;       📄 anomaly\_detector.py      # 이상행위 탐지

&#x20;       📄 kisa\_rag\_responder.py    # KISA 문서 기반 대응책 생성

&#x20;       📄 incident\_handler.py      # 침해사고 대응 절차

&#x20;       📄 vulnerability\_scanner.py # 취약점 스캐닝



&#x20;   📁 agenticAi/blueAgent/docs/

&#x20;       📄 kisa\_guidelines.pdf      # KISA 주요정보통신기반시설

&#x20;                                   # 기술적 취약점 분석 가이드

&#x20;       📄 README.md



&#x20;   📄 alert\_manager.py        # 보안 알림 관리

📁 agenticAi/institutionalAgent/ — Phase 3-③ 🏦

text

📁 agenticAi/institutionalAgent/

&#x20;   📄 \_\_init\_\_.py

&#x20;   📄 run.py                  # 독립 실행 엔트리포인트

&#x20;   📄 institutional\_agent.py  # 기관투자자 에이전트

&#x20;                              #  - 대량 주문, 분할매수 전략

&#x20;                              #  - 리스크 관리 (VaR, 포트폴리오 최적화)



&#x20;   📁 agenticAi/institutionalAgent/strategies/

&#x20;       📄 \_\_init\_\_.py

&#x20;       📄 portfolio\_optimizer.py   # 포트폴리오 최적화 (MPT)

&#x20;       📄 risk\_manager.py          # VaR, CVaR 리스크 계산

&#x20;       📄 order\_splitter.py        # 대량주문 분할 (TWAP/VWAP)

&#x20;       📄 market\_analyzer.py       # KRX 시장 분석



&#x20;   📄 config.py               # 기관투자자 설정 (자본금, 전략)

📁 agenticAi/retailAgentA/ — Phase 3-④ 👤

text

📁 agenticAi/retailAgentA/

&#x20;   📄 \_\_init\_\_.py

&#x20;   📄 run.py                  # 독립 실행 엔트리포인트

&#x20;   📄 retail\_agent\_a.py       # 개인투자자 A (공격적 단타 성향)



&#x20;   📁 agenticAi/retailAgentA/strategies/

&#x20;       📄 \_\_init\_\_.py

&#x20;       📄 momentum\_trader.py       # 모멘텀 기반 단타 매매

&#x20;       📄 news\_sentiment.py        # 뉴스 감성 분석 기반 매매

&#x20;       📄 technical\_indicator.py   # RSI, MACD, 볼린저밴드



&#x20;   📄 config.py               # A 투자자 설정 (소액, 고빈도)

📁 agenticAi/retailAgentB/ — Phase 3-⑤ 👤

text

📁 agenticAi/retailAgentB/

&#x20;   📄 \_\_init\_\_.py

&#x20;   📄 run.py                  # 독립 실행 엔트리포인트

&#x20;   📄 retail\_agent\_b.py       # 개인투자자 B (보수적 장기 성향)



&#x20;   📁 agenticAi/retailAgentB/strategies/

&#x20;       📄 \_\_init\_\_.py

&#x20;       📄 value\_investor.py        # 가치투자 (PER, PBR 분석)

&#x20;       📄 dividend\_tracker.py      # 배당주 추적 전략

&#x20;       📄 fundamental\_analyzer.py  # 재무제표 기반 분석



&#x20;   📄 config.py               # B 투자자 설정 (중액, 저빈도)🗂️ appFrontEnd/ (Phase 4 대상 - 미구현)

text

📁 appFrontEnd/

&#x20;   📁 src/

&#x20;       📁 components/

&#x20;       📁 pages/

&#x20;   📄 package.json

🗂️ dashboard/ (Phase 4 대상 - 미구현)

text

📁 dashboard/

&#x20;   📁 src/

&#x20;       📁 components/

&#x20;           📄 securityPanel.js    # 보안 이벤트 시각화

&#x20;           📄 agentMonitor.js     # 에이전트 상태 모니터링

&#x20;       📁 pages/

&#x20;   📄 package.json



🗂️ infra/ (Phase 5 대상 - 미구현)

text

📁 infra/

&#x20;   📄 docker-compose.yml

&#x20;   📄 Dockerfile

&#x20;   📁 k8s/

&#x20;   📁 terraform/



