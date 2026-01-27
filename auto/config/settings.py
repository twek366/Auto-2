import logging
import os
from pathlib import Path

from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]

if os.getenv("CI"):
    logger.info("CI среда обнаружена, загрузка переменных из окружения CI")

    base_url = os.getenv("BASE_URL") or os.getenv("base_url")
    login_owner = os.getenv("LOGIN_OWNER") or os.getenv("login_owner")
    pass_owner = os.getenv("PASS_OWNER") or os.getenv("pass_owner")
    timeout = os.getenv("TIMEOUT") or os.getenv("timeout", 10)
    timeout = int(timeout)
else:
    logger.info ("Локальная разработка: загружаем из .env файла")
    env = os.getenv("ENV", "local")
    env_file = BASE_DIR / f".env.{env}"

    if env_file.exists():
        load_dotenv(env_file)
        logger.info(f"ENV = {env}")
        logger.info(f"Загружен файл: {env_file}")
    else:
        logger.info(f"Файл {env_file} не найден, загружаем из .env")
        load_dotenv(BASE_DIR / ".env")

    base_url = os.getenv("base_url")
    login_owner = os.getenv("login_owner")
    pass_owner = os.getenv("pass_owner")
    timeout = int(os.getenv("timeout", 10))

logger.info ("Проверка переменных")
if not all([base_url, login_owner, pass_owner]):
    missing = []
    if not base_url:
        missing.append("BASE_URL/base_url")
    if not login_owner:
        missing.append("LOGIN_OWNER/login_owner")
    if not pass_owner:
        missing.append("PASS_OWNER/pass_owner")
    raise ValueError(f"Не все обязательные переменные окружения заданы! Отсутствуют: {', '.join(missing)}")

if os.getenv("CI"):
    logger.info(f"CI: Подключение к: {base_url}")
    logger.info(f"CI: Timeout: {timeout} сек")
else:
    logger.info(f"Подключение к: {base_url}")
    logger.info(f"Timeout: {timeout} сек")