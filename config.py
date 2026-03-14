from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")
group_id = env.str("group_id")
