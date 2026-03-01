pending_withdraw = {}
user_token = {}

def reset_state(user_id: int):
    pending_withdraw.pop(user_id, None)
