import logging

from sqlmodel import Session

from app.core.db import engine, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("开始创建初始数据")

    init()

    logger.info("初始数据创建完成")


def init() -> None:
    with Session(engine) as session:
        init_db(session)


if __name__ == "__main__":
    main()
