from ..env_loader import load_env


def get_emailer_creds() -> dict[str, str]:
    return load_env()
