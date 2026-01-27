
# !/usr/bin/env python3
"""
Скрипт для запуска smoke-тестов.
Использование: python smoke_runner.py [--test-path PATH] [--allure-results DIR]
"""

import argparse
import logging
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_environment():
    """Настройка окружения для корректной работы."""
    # Добавляем текущую директорию в PYTHONPATH если нужно
    current_dir = Path(__file__).parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))

    logger.info(f"Рабочая директория: {current_dir}")
    logger.info(f"Python версия: {sys.version}")


def run_command(command: list, cwd: Optional[str] = None) -> int:
    """
    Запускает команду и возвращает код возврата.

    Args:
        command: Список аргументов команды
        cwd: Рабочая директория

    Returns:
        Код возврата команды
    """
    logger.info(f"Выполнение команды: {' '.join(command)}")

    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False
        )

        # Вывод результатов
        if result.stdout:
            logger.info("STDOUT:\n" + result.stdout)

        if result.stderr:
            logger.warning("STDERR:\n" + result.stderr)

        logger.info(f"Код возврата: {result.returncode}")
        return result.returncode

    except Exception as e:
        logger.error(f"Ошибка при выполнении команды: {e}")
        return 1


def install_dependencies(requirements_file: str = "requirements.txt") -> bool:
    """
    Устанавливает зависимости из requirements.txt.

    Args:
        requirements_file: Путь к файлу с зависимостями

    Returns:
        True если успешно, False если ошибка
    """
    if not Path(requirements_file).exists():
        logger.warning(f"Файл {requirements_file} не найден. Пропускаем установку зависимостей.")
        return True

    logger.info(f"Установка зависимостей из {requirements_file}")

    # Обновляем pip
    pip_update_code = run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    if pip_update_code != 0:
        logger.warning("Не удалось обновить pip, продолжаем...")

    # Устанавливаем зависимости
    install_code = run_command([sys.executable, "-m", "pip", "install", "-r", requirements_file])

    if install_code == 0:
        logger.info("Зависимости успешно установлены")
        return True
    else:
        logger.error("Ошибка установки зависимостей")
        return False


def run_smoke_tests(
        test_path: str = "./WS/smoke",
        allure_results_dir: str = "./allure-results",
        pytest_args: Optional[list] = None
) -> int:
    """
    Запускает smoke-тесты и генерирует Allure отчет.

    Args:
        test_path: Путь к тестам (директория или файл)
        allure_results_dir: Директория для сохранения результатов Allure
        pytest_args: Дополнительные аргументы для pytest

    Returns:
        Код возврата: 0 если успешно, 1 если тесты упали
    """
    # Создаем директорию для результатов
    results_path = Path(allure_results_dir)
    results_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Директория для результатов Allure: {results_path.absolute()}")

    # Формируем команду pytest
    command = [
        sys.executable, "-m", "pytest",
        test_path,
        "-v",
        "-m", "smoke",
        "--alluredir", allure_results_dir,
        "--tb=short",  # короткий формат traceback
        "--disable-warnings",  # отключаем warnings для чистоты вывода
        "--color=yes",  # цветной вывод
    ]

    # Добавляем дополнительные аргументы если есть
    if pytest_args:
        command.extend(pytest_args)

    # Проверяем существование тестов
    test_path_obj = Path(test_path)
    if not test_path_obj.exists():
        logger.error(f"Путь к тестам не найден: {test_path}")
        return 1

    logger.info(f"Запуск smoke-тестов из: {test_path}")

    # Запускаем тесты
    return_code = run_command(command)

    if return_code == 0:
        logger.info("✅ Все smoke-тесты прошли успешно!")

        # Проверяем, есть ли результаты Allure
        allure_files = list(results_path.glob("*.json"))
        if allure_files:
            logger.info(f"Сгенерировано {len(allure_files)} файлов результатов Allure")
        else:
            logger.warning("Не сгенерированы файлы результатов Allure")

    elif return_code == 5:
        logger.warning("⚠️ Тесты не найдены (код 5)")
    else:
        logger.error(f"❌ Тесты упали с кодом возврата: {return_code}")

    return 0 if return_code in [0, 5] else 1


def generate_allure_report(
        allure_results_dir: str = "./allure-results",
        report_dir: str = "./allure-report"
) -> bool:
    """
    Генерирует HTML отчет Allure (если установлен allure).

    Args:
        allure_results_dir: Директория с сырыми результатами
        report_dir: Директория для HTML отчета

    Returns:
        True если успешно, False если ошибка
    """
    # Проверяем, есть ли результаты
    results_path = Path(allure_results_dir)
    if not results_path.exists() or not any(results_path.glob("*.json")):
        logger.warning(f"Нет результатов Allure в {allure_results_dir}")
        return False

    logger.info(f"Генерация Allure отчета из {allure_results_dir}")

    # Пробуем сгенерировать отчет через allure командную строку
    try:
        # Вариант 1: Используем allure если установлен
        import allure
        from allure.report import generator

        logger.info("Генерация отчета через python allure...")
        generator.generate_report(allure_results_dir, report_dir, clean=True)
        logger.info(f"Отчет Allure сгенерирован: {report_dir}")
        return True

    except ImportError:
        logger.warning("Модуль allure не установлен для генерации HTML")

        # Вариант 2: Проверяем установлен ли allure командной строкой
        allure_cmd = "allure"
        try:
            # Пробуем найти allure в системе
            result = subprocess.run(
                [allure_cmd, "--version"],
                capture_output=True,
                text=True,
                check=False
            )

            if result.returncode == 0:
                logger.info(f"Найден Allure CLI: {result.stdout.strip()}")

                # Генерируем отчет
                cmd = [
                    allure_cmd, "generate",
                    allure_results_dir,
                    "-o", report_dir,
                    "--clean"
                ]

                gen_result = subprocess.run(cmd, capture_output=True, text=True)
                if gen_result.returncode == 0:
                    logger.info(f"HTML отчет Allure сгенерирован: {report_dir}")

                    # Создаем index.html для удобного открытия
                    index_file = Path(report_dir) / "index.html"
                    if index_file.exists():
                        logger.info(f"Отчет доступен по пути: {index_file.absolute()}")

                    return True
                else:
                    logger.error(f"Ошибка генерации отчета: {gen_result.stderr}")
                    return False

        except FileNotFoundError:
            logger.info("Allure CLI не установлен. Для генерации HTML отчета установите Allure:")
            logger.info("  Windows: scoop install allure")
            logger.info("  Mac: brew install allure")
            logger.info("  Linux: sudo apt-get install allure")
            return False

    return False


def main():
    """Основная функция запуска."""
    parser = argparse.ArgumentParser(
        description='Запуск smoke-тестов проекта с генерацией Allure отчета.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python smoke_runner.py
  python smoke_runner.py --test-path tests/smoke
  python smoke_runner.py --allure-results ./test-results
  python smoke_runner.py --install-deps --generate-report
        """
    )

    parser.add_argument(
        '--test-path',
        default='./smoke',
        help='Путь к директории или файлу с тестами (по умолчанию: ./smoke)'
    )
    parser.add_argument(
        '--allure-results',
        default='./allure-results',
        help='Директория для результатов Allure (по умолчанию: ./allure-results)'
    )
    parser.add_argument(
        '--install-deps',
        action='store_true',
        help='Установить зависимости перед запуском тестов'
    )
    parser.add_argument(
        '--generate-report',
        action='store_true',
        help='Сгенерировать HTML отчет Allure после тестов'
    )
    parser.add_argument(
        '--requirements',
        default='requirements.txt',
        help='Путь к файлу с зависимостями (по умолчанию: requirements.txt)'
    )
    parser.add_argument(
        '--report-dir',
        default='./allure-report',
        help='Директория для HTML отчета Allure (по умолчанию: ./allure-report)'
    )
    parser.add_argument(
        '--pytest-args',
        nargs='*',
        help='Дополнительные аргументы для pytest'
    )

    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Запуск smoke-тестов")
    logger.info("=" * 60)

    # Настраиваем окружение
    setup_environment()

    # Устанавливаем зависимости если нужно
    if args.install_deps:
        if not install_dependencies(args.requirements):
            logger.error("Не удалось установить зависимости. Завершение.")
            return 1

    # Запускаем smoke-тесты
    exit_code = run_smoke_tests(
        test_path=args.test_path,
        allure_results_dir=args.allure_results,
        pytest_args=args.pytest_args
    )

    # Генерируем отчет если нужно
    if args.generate_report and exit_code in [0, 5]:
        generate_allure_report(args.allure_results, args.report_dir)

    logger.info("=" * 60)
    logger.info(f"Завершено с кодом: {exit_code}")
    logger.info("=" * 60)

    return exit_code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("\nПрервано пользователем")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}", exc_info=True)
        sys.exit(1)