import random
import string
from tabnanny import check

from asyncpg import Connection

from src.app.database.queries.referals import RefferralActions


async def generate_referal_id(conn: Connection, length: int = 10):
    referral_actions = RefferralActions(conn)
    referrals_id = await referral_actions.get_all_referrals()

    if referrals_id:
        for referral_id in referrals_id:
            characters = string.ascii_letters + string.digits
            if characters != referral_id:
                check_id = characters
                return "".join(random.choice(check_id) for _ in range(length))
    else:
        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for _ in range(length))


