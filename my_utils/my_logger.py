import logging
from pathlib import Path


def get_logger(name: str) -> logging.Logger:
    # 创建Logger实例
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 设置最低日志级别

    # 创建控制台处理器并设置级别为INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    logger_dir = Path("logs")
    logger_dir.mkdir(parents=True, exist_ok=True)

    # 创建文件处理器并设置级别为DEBUG
    file_handler = logging.FileHandler(
        "logs/records.log", mode="a"
    )  # 默认模式为追加，可改为'w'覆盖
    file_handler.setLevel(logging.DEBUG)

    # 定义日志格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # 将处理器添加到Logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
