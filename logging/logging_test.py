import logging
def log():
    # 로그 생성
    logger = logging.getLogger(__name__)
    # 로그의 출력 기준 설정
    logger.setLevel(logging.DEBUG)
    # log 출력 형식
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s : %(funcName)s")
    # log를 console에 출력
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    # log를 파일에 출력
    file_handler = logging.FileHandler("my.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    for i in range(10):
        logger.debug(f"{i}번째 방문입니다.")

    print(logger.name)

log()