from dotenv import dotenv_values, find_dotenv

env_file = find_dotenv(".env.development", usecwd=True) or find_dotenv(
    ".env", usecwd=True
)

ENV_VARIABLES = dotenv_values(env_file)
ENV_VARIABLES["ALLOWED_EXTENSIONS"] = set(
    ENV_VARIABLES["ALLOWED_EXTENSIONS"].split(",")
)
ENV_VARIABLES["DOCUMENT_TYPES"] = set(ENV_VARIABLES["DOCUMENT_TYPES"].split(","))
