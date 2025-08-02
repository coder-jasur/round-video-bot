from environs import Env

env = Env()
env.read_env()

class Settings:
    bot_token = env.str("BOT_TOKEN")
    admins_ids = env.list("ADMINS_IDS")
    db_name = env.str("DB_NAME")
    db_user = env.str("DB_USER")
    db_password = env.str("DB_PASSWORD")
    db_host = env.str("DB_HOST")
    db_port = env.str("DB_PORT")
