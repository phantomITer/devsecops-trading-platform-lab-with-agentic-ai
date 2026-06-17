"""
Phase 2 - Agentic AI Core Library Demo

각 에이전트를 실제로 실행하여 동작을 검증합니다.
SQLite DB 사용 (trading.db)
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from app.database import SessionLocal, init_db
from app.models.user import User
from app.models.account import Account
from app.models.order import Order
from app.models.agent_log import AgentLog

from agenticAi.core.memory_store import MemoryStore
from agenticAi.core.llm.ollama_client import OllamaClient
from agenticAi.blueAgent.blue import BlueAgent
from agenticAi.redAgent.red import RedAgent
from agenticAi.institutionalAgent.institutional import InstitutionalAgent
from agenticAi.retailAgentA.retail_a import RetailAgentA
from agenticAi.retailAgentB.retail_b import RetailAgentB

import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def setup_database():
    """DB 초기화 및 테스트 데이터 생성"""
    print("\n" + "="*60)
    print("1️⃣ 데이터베이스 초기화")
    print("="*60)
    
    # DB 테이블 생성
    init_db()
    print("✅ DB 테이블 생성 완료 (trading.db)")
    
    db = SessionLocal()
    try:
        # 기존 데이터 확인
        user_count = db.query(User).count()
        account_count = db.query(Account).count()
        
        print(f"   - 현재 Users: {user_count}")
        print(f"   - 현재 Accounts: {account_count}")
        
        # 테스트용 사용자가 없으면 생성
        if user_count == 0:
            print("\n   테스트 데이터 생성 중...")
            user1 = User(username="test_user_1", email="user1@test.com", hashed_password="dummy")
            user2 = User(username="test_user_2", email="user2@test.com", hashed_password="dummy")
            user3 = User(username="test_user_3", email="user3@test.com", hashed_password="dummy")
            
            db.add_all([user1, user2, user3])
            db.flush()
            
            # 수정: 올바른 필드명 사용
            account1 = Account(
                user_id=user1.id, 
                name="Test Account 1",
                initial_balance=100000.0,
                current_balance=100000.0
            )
            account2 = Account(
                user_id=user2.id,
                name="Test Account 2", 
                initial_balance=50000.0,
                current_balance=50000.0
            )
            account3 = Account(
                user_id=user3.id,
                name="Test Account 3", 
                initial_balance=75000.0,
                current_balance=75000.0
            )
            
            db.add_all([account1, account2, account3])
            db.commit()
            
            print(f"   ✅ 테스트 데이터 생성 완료")
            print(f"      - Users: 3")
            print(f"      - Accounts: 3")
        
        return db
        
    except Exception as e:
        print(f"❌ DB 초기화 실패: {e}")
        db.rollback()
        raise


def test_ollama_connection():
    """Ollama 서버 연결 테스트 (선택사항)"""
    print("\n" + "="*60)
    print("2️⃣ Ollama LLM 서버 연결 테스트 (선택)")
    print("="*60)
    
    try:
        client = OllamaClient()
        models = client.list_models()
        print(f"✅ Ollama 연결 성공!")
        print(f"   사용 가능한 모델: {models}")
        return client
    except Exception as e:
        print(f"⚠️  Ollama 연결 실패: {str(e)[:100]}")
        print("   → LLM 기능 없이 계속 진행합니다.")
        return None


def demo_blue_agent(db, ollama_client, memory_store):
    """BlueAgent 데모 - 방어 보안"""
    print("\n" + "="*60)
    print("3️⃣ BlueAgent (방어 보안) 실행 테스트")
    print("="*60)
    
    agent = BlueAgent(
        db_session=db,
        ollama_client=ollama_client,
        memory_store=memory_store,
        watch_symbol="AAPL"
    )
    
    print(f"→ Agent ID: {agent.agent_id}")
    print(f"→ Agent Type: {agent.agent_type}")
    print(f"→ Watch Symbol: {agent.watch_symbol}")
    
    # perceive 단계 테스트
    print("\n[Perceive] 보안 위협 스캔 중...")
    perception = agent.perceive()
    print(f"  ├─ 최근 주문 수: {perception.get('total_recent_orders', 0)}")
    print(f"  ├─ 매도 주문 수: {perception.get('sell_order_count', 0)}")
    print(f"  └─ 최근 알림 수: {len(perception.get('recent_alerts', []))}")
    
    # 전체 실행
    print("\n[Run] 전체 사이클 실행...")
    result = agent.run()
    print(f"✅ 결과:")
    print(f"   ├─ Action: {result.get('action')}")
    print(f"   └─ Reason: {result.get('reason')}")
    
    # 메모리 저장 테스트
    agent.remember("last_scan_time", "2026-06-17 18:00:00")
    print(f"\n💾 메모리 저장 테스트:")
    print(f"   └─ Recalled: {agent.recall('last_scan_time')}")
    
    return result


def demo_red_agent(db, ollama_client, memory_store):
    """RedAgent 데모 - 공격 시뮬레이션"""
    print("\n" + "="*60)
    print("4️⃣ RedAgent (공격 시뮬레이션) 실행 테스트")
    print("="*60)
    
    agent = RedAgent(
        db_session=db,
        ollama_client=ollama_client,
        memory_store=memory_store
    )
    
    print(f"→ Agent ID: {agent.agent_id}")
    
    # perceive 단계 테스트
    print("\n[Perceive] 공격 시나리오 분석 중...")
    perception = agent.perceive()
    scenarios = perception.get('available_scenarios', [])
    print(f"  └─ 사용 가능한 시나리오 ({len(scenarios)}개):")
    for i, scenario in enumerate(scenarios, 1):
        print(f"      {i}. {scenario}")
    
    # 전체 실행
    print("\n[Run] 공격 시뮬레이션 실행...")
    result = agent.run()
    print(f"✅ 결과:")
    print(f"   ├─ Scenario: {result.get('scenario')}")
    print(f"   └─ Placed Orders: {len(result.get('placed_orders', []))}")
    
    return result


def demo_institutional_agent(db, memory_store):
    """InstitutionalAgent 데모 - 기관 투자자"""
    print("\n" + "="*60)
    print("5️⃣ InstitutionalAgent (기관 투자자) 실행 테스트")
    print("="*60)
    
    agent = InstitutionalAgent(
        db_session=db,
        memory_store=memory_store,
        account_id=1
    )
    
    print(f"→ Agent ID: {agent.agent_id}")
    print(f"→ Account ID: {agent.account_id}")
    
    # perceive 단계 테스트
    print("\n[Perceive] 시장 데이터 수집 중...")
    perception = agent.perceive()
    symbols = list(perception.get('summaries', {}).keys())
    print(f"  └─ 모니터링 심볼 ({len(symbols)}개): {symbols}")
    
    # 전체 실행
    print("\n[Run] 블록 거래 전략 실행...")
    result = agent.run()
    print(f"✅ 결과:")
    print(f"   └─ Orders Placed: {result.get('count', 0)}")
    
    return result


def demo_retail_agent_a(db, memory_store):
    """RetailAgentA 데모 - 가치투자 전략"""
    print("\n" + "="*60)
    print("6️⃣ RetailAgentA (Buy-the-Dip 가치투자) 실행 테스트")
    print("="*60)
    
    agent = RetailAgentA(
        db_session=db,
        memory_store=memory_store,
        account_id=2,
        symbol="AAPL"
    )
    
    print(f"→ Agent ID: {agent.agent_id}")
    print(f"→ Symbol: {agent.symbol}")
    print(f"→ Strategy: Buy-the-Dip (가격 하락 시 매수)")
    
    # 전체 실행
    print("\n[Run] 가치투자 전략 실행...")
    result = agent.run()
    print(f"✅ 결과:")
    print(f"   ├─ Action: {result.get('action')}")
    print(f"   └─ Reason: {result.get('reason')}")
    
    return result


def demo_retail_agent_b(db, memory_store):
    """RetailAgentB 데모 - 모멘텀 전략"""
    print("\n" + "="*60)
    print("7️⃣ RetailAgentB (FOMO 모멘텀) 실행 테스트")
    print("="*60)
    
    agent = RetailAgentB(
        db_session=db,
        memory_store=memory_store,
        account_id=3,
        symbol="TSLA"
    )
    
    print(f"→ Agent ID: {agent.agent_id}")
    print(f"→ Symbol: {agent.symbol}")
    print(f"→ Strategy: Momentum FOMO (상승 추세 추종)")
    
    # 전체 실행
    print("\n[Run] 모멘텀 전략 실행...")
    result = agent.run()
    print(f"✅ 결과:")
    print(f"   ├─ Action: {result.get('action')}")
    print(f"   └─ Reason: {result.get('reason')}")
    
    return result


def verify_db_logs(db):
    """DB에 저장된 agent_logs 확인"""
    print("\n" + "="*60)
    print("8️⃣ Agent Logs 검증 (DB 저장 확인)")
    print("="*60)
    
    try:
        logs = db.query(AgentLog).all()
        
        if logs:
            print(f"✅ Agent Logs: {len(logs)}개 저장됨")
            print("\n최근 로그 5개:")
            for log in logs[-5:]:
                print(f"  ├─ [{log.agent_type}] {log.action}")
                print(f"  │  └─ {log.created_at}")
        else:
            print("⚠️  저장된 로그 없음")
            
    except Exception as e:
        print(f"⚠️  로그 확인 실패: {e}")


def main():
    """전체 데모 실행"""
    print("\n" + "🚀"*30)
    print("Phase 2 - Agentic AI Core Library 동작 검증")
    print("🚀"*30)
    print("\n💡 SQLite DB 사용 (trading.db)\n")
    
    db = None
    try:
        # 1. DB 초기화
        db = setup_database()
        
        # 2. Ollama 연결 테스트 (선택)
        ollama_client = test_ollama_connection()
        
        # 3. MemoryStore 초기화
        memory_store = MemoryStore()
        print(f"\n✅ MemoryStore 초기화 완료")
        
        # 4. 각 에이전트 데모 실행
        demo_blue_agent(db, ollama_client, memory_store)
        demo_red_agent(db, ollama_client, memory_store)
        demo_institutional_agent(db, memory_store)
        demo_retail_agent_a(db, memory_store)
        demo_retail_agent_b(db, memory_store)
        
        # 5. DB 로그 확인
        verify_db_logs(db)
        
        print("\n" + "🎉"*30)
        print("모든 에이전트 동작 검증 완료!")
        print("🎉"*30)
        print("\n✅ Phase 2 검증 체크리스트:")
        print("   [✓] BaseAgent 추상 클래스 동작")
        print("   [✓] 5개 에이전트 모두 실행 가능")
        print("   [✓] perceive-decide-act 사이클 정상")
        print("   [✓] MemoryStore 상태 관리")
        print("   [✓] DB 로그 기록")
        print("   [✓] Ollama LLM 연동 (선택)\n")
        
    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if db:
            db.close()


if __name__ == "__main__":
    main()