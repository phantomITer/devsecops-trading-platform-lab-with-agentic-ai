D-trading-platform-lab-with-agentic-ai/

│

├── .env

├── .gitignore

├── README.md

├── requirements.txt

├── docker-compose.yml

│

│

├── app/                                    # ✅ 백엔드 (기존 유지 + 확장)

│   ├── \_\_init\_\_.py

│   ├── main.py                             # ✅ 기존

│   ├── database.py                         # 🆕 SQLAlchemy 연결

│   │

│   ├── core/                               # 🆕 공통 설정/보안

│   │   ├── \_\_init\_\_.py

│   │   ├── config.py                       # 환경변수 로드

│   │   ├── security.py                     # API Key / JWT

│   │   └── dependencies.py                 # FastAPI Depends

│   │

│   ├── api/                                # ✅ 기존 + 확장

│   │   ├── \_\_init\_\_.py

│   │   ├── health.py                       # ✅ 기존 + heartbeat 흡수

│   │   ├── accounts.py                     # ✅ 기존

│   │   ├── orders.py                       # ✅ 기존

│   │   ├── instruments.py                  # ✅ 기존

│   │   └── websocket.py                    # 🆕 실시간 시세 브로드캐스트

│   │

│   ├── schemas/                            # ✅ 기존

│   │   ├── accounts.py

│   │   ├── orders.py

│   │   └── instruments.py

│   │

│   ├── models/                             # 🆕 SQLAlchemy ORM

│   │   ├── \_\_init\_\_.py

│   │   ├── accounts.py

│   │   ├── orders.py

│   │   └── instruments.py

│   │

│   ├── services/                           # ✅ 기존 (비즈니스 로직)

│   │   ├── accountsservice.py

│   │   └── ordersservice.py

│   │

│   └── adapters/                           # 🆕 외부 데이터 수집

│       ├── \_\_init\_\_.py

│       ├── krx\_fetcher.py                  # 국내주식 (pykrx)

│       ├── mock\_generator.py               # 개발용 Mock

│       └── future/                         # 향후 확장 예약

│           ├── binance\_ws.py               # (미구현) 코인

│           └── us\_stock\_fetcher.py         # (미구현) 미국주식

│

│

├── agenticAi/                              # 🆕 5개 AI 에이전트 통합

│   │

│   ├── core/                               # 공통 라이브러리 (허브)

│   │   ├── \_\_init\_\_.py

│   │   ├── setup.py                        # pip install -e .

│   │   ├── requirements.txt                # httpx, websockets, dotenv

│   │   ├── base.py                         # 공통 베이스 클래스

│   │   │                                   # TRADING\_SERVER\_URL

│   │   │                                   # AGENT\_API\_KEY

│   │   │                                   # OLLAMA\_URL

│   │   ├── llm/

│   │   │   ├── \_\_init\_\_.py

│   │   │   ├── ollama\_client.py            # Ollama 공통 클라이언트

│   │   │   └── prompts.py                  # AI별 프롬프트 템플릿

│   │   └── tools/

│   │       ├── \_\_init\_\_.py

│   │       ├── market\_data.py              # GET /instruments

│   │       ├── order.py                    # POST /orders

│   │       ├── portfolio.py                # GET /accounts

│   │       └── alert.py                    # 이벤트 알림

│   │

│   ├── red/                                # 🔴 OWASP 기반 공격자 (이식 가능)

│   │   ├── run.py                          # ← python run.py 실행

│   │   ├── .env.example

│   │   ├── requirements.txt                # agenticAi/core

│   │   ├── README.md                       # 설치/실행 3단계 가이드

│   │   ├── red.py                          # Red AI 오케스트레이터

│   │   ├── planner.py                      # Ollama 공격 전략 수립

│   │   ├── logger.py                       # 공격 이력 기록

│   │   └── owasp/

│   │       ├── \_\_init\_\_.py

│   │       ├── a01\_broken\_access\_control.py

│   │       ├── a02\_cryptographic\_failures.py

│   │       ├── a03\_injection.py

│   │       ├── a04\_insecure\_design.py

│   │       ├── a05\_security\_misconfiguration.py

│   │       ├── a06\_vulnerable\_components.py

│   │       ├── a07\_auth\_failures.py

│   │       ├── a08\_software\_integrity\_failures.py

│   │       ├── a09\_logging\_failures.py

│   │       └── a10\_ssrf.py

│   │

│   ├── blue/                               # 🔵 KISA 기반 방어자 (메인서버 고정)

│   │   ├── run.py

│   │   ├── .env.example

│   │   ├── requirements.txt                # agenticAi/core + chromadb

│   │   ├── README.md

│   │   ├── blue.py                         # Blue AI 오케스트레이터

│   │   ├── analyzer.py                     # LLM 기반 위협 분석

│   │   ├── detector.py                     # 실시간 이상탐지

│   │   ├── reporter.py                     # 점검 보고서 생성

│   │   ├── kisaRag/                        # KISA RAG 파이프라인

│   │   │   ├── \_\_init\_\_.py

│   │   │   ├── loader.py                   # KISA 문서 로드

│   │   │   ├── vector\_store.py             # ChromaDB

│   │   │   └── retriever.py                # 관련 항목 검색

│   │   ├── scanner/                        # 취약점 점검 모듈

│   │   │   ├── \_\_init\_\_.py

│   │   │   ├── web.py                      # 웹 취약점 점검

│   │   │   ├── api.py                      # API 보안 점검

│   │   │   ├── auth.py                     # 인증 점검

│   │   │   └── config.py                   # 설정 보안 점검

│   │   └── securityPipeline/               # Blue 전용 (함께 고정)

│   │       ├── kisaGuidelines/             # KISA 원본 문서 저장

│   │       ├── vectors/                    # ChromaDB 벡터 저장소

│   │       └── reports/                    # 점검 결과 보고서

│   │

│   ├── institutional/                      # 🏦 기관투자자 AI (이식 가능)

│   │   ├── run.py                          # ← python run.py 실행

│   │   ├── .env.example

│   │   ├── requirements.txt                # agenticAi/core만

│   │   ├── README.md

│   │   └── institutional.py               # 롱/숏 자동매매

│   │

│   ├── retailA/                            # 👤 개미A AI (이식 가능)

│   │   ├── run.py                          # ← python run.py 실행

│   │   ├── .env.example

│   │   ├── requirements.txt                # agenticAi/core만

│   │   ├── README.md

│   │   └── retail\_a.py                    # 롱/숏 자동매매

│   │

│   └── retailB/                            # 👤 개미B AI (이식 가능)

│       ├── run.py                          # ← python run.py 실행

│       ├── .env.example

│       ├── requirements.txt                # agenticAi/core만

│       ├── README.md

│       └── retail\_b.py                    # 롱/숏 자동매매

│

│

├── appFrontEnd/                            # 💹 증권 프론트엔드 (투자자 시각)

│   ├── public/

│   │   └── index.html

│   ├── src/

│   │   ├── main.js

│   │   ├── components/

│   │   │   ├── chart/

│   │   │   │   ├── candlestickChart.js     # 캔들스틱 차트

│   │   │   │   ├── volumeChart.js          # 거래량 차트

│   │   │   │   └── orderBook.js            # 호가창

│   │   │   ├── trading/

│   │   │   │   ├── orderPanel.js           # 롱/숏 주문 패널

│   │   │   │   ├── positionPanel.js        # 포지션 현황

│   │   │   │   └── tradeHistory.js         # 체결 내역

│   │   │   └── portfolio/

│   │   │       ├── accountSummary.js       # 계좌 요약

│   │   │       └── pnl.js                  # 손익 현황

│   │   └── services/

│   │       ├── websocket.js                # 실시간 시세 연결

│   │       ├── api.js                      # REST API 호출

│   │       └── auth.js                     # 인증 처리

│   └── package.json

│

│

├── dashboard/                              # 📊 통합 운영 관제 (Azure 포털 수준)

│   ├── public/

│   │   └── index.html

│   ├── src/

│   │   ├── main.js

│   │   └── components/

│   │       ├── agenticMonitor/             # AI 에이전트 상태

│   │       │   ├── agentStatusCard.js      # 5개 AI 온라인/오프라인

│   │       │   ├── agentTimeline.js        # AI 활동 타임라인

│   │       │   └── agentLog.js             # AI 실행 로그

│   │       ├── hardwareMonitor/            # 하드웨어 자원 현황

│   │       │   ├── cpuGauge.js             # CPU 사용률

│   │       │   ├── memoryGauge.js          # 메모리 사용률

│   │       │   ├── diskGauge.js            # 디스크 사용률

│   │       │   └── gpuGauge.js             # GPU (Ollama LLM용)

│   │       ├── networkMonitor/             # 통신 상태

│   │       │   ├── connectionStatus.js     # 에이전트 연결 상태

│   │       │   ├── latencyChart.js         # API 응답 지연

│   │       │   ├── trafficChart.js         # 인/아웃바운드 트래픽

│   │       │   └── heartbeatPanel.js       # AI heartbeat 현황

│   │       ├── securityPanel/              # 보안 현황

│   │       │   ├── owaspHeatmap.js         # OWASP Top10 히트맵

│   │       │   ├── attackFeed.js           # Red AI 공격 실시간 피드

│   │       │   └── kisaReport.js           # Blue AI KISA 점검 현황

│   │       └── systemHealth/              # 서버 상태

│   │           ├── apiHealthCard.js        # API 엔드포인트 상태

│   │           ├── dbStatus.js             # DB 연결 상태

│   │           └── serverMetrics.js        # 전체 서버 메트릭

│   └── package.json

│

│

├── infra/                                  # 🐳 인프라

│   ├── Dockerfile

│   ├── docker-compose.yml

│   └── cloud/

│       └── githubActions/

│           └── red\_runner.yml              # Red AI 무료 클라우드 실행

│

│

├── data/                                   # 데이터

│   ├── instruments.json                    # ✅ 기존 종목 정보

│   └── historical/

│       └── krx/                            # 국내주식 시세 캐시

│

│

├── tests/                                  # ✅ 기존 전체 유지

│   ├── smoke/

│   │   ├── testapismoke.py

│   │   └── smokeTESTHISTORY20260616175018.md

│   ├── integration/

│   │   ├── testintegration.py

│   │   └── integrationTESTHISTORY20260616175018.md

│   ├── validation/

│   │   ├── testvalidation.py

│   │   └── validationTESTHISTORY20260616175018.md

│   ├── security/

│   │   ├── testsecurity.py

│   │   └── securityTESTHISTORY20260616175018.md

│   ├── e2e/

├── tests/

│   ├── e2e/

│   │   ├── teste2e.py

│   │   └── e2eTESTHISTORY20260616175018.md

│   ├── utils/

│   │   └── base.py

│   ├── execution.txt

│   ├── rule.txt

│   └── README.md

└── docs/

&#x20;   ├── architecture.md

&#x20;   ├── owaspMapping.md

&#x20;   ├── kisaChecklistMapping.md

&#x20;   └── agenticAiDesign.md

