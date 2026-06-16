# fix_init_accounts.py
code = '''
def init_all_accounts(db):
    from app.models.accounts import Account as AccountModel
    agent_ids = ["red", "blue", "institutional", "retail_a", "retail_b"]
    for agent_id in agent_ids:
        exists = db.query(AccountModel).filter(
            AccountModel.agent_id == agent_id
        ).first()
        if not exists:
            obj = AccountModel(
                agent_id=agent_id,
                balance=10_000_000.0,
                equity=10_000_000.0,
            )
            db.add(obj)
    db.commit()
'''

with open("app/services/accounts_service.py", "a", encoding="utf-8") as f:
    f.write(code)
print("✅ init_all_accounts 추가 완료")