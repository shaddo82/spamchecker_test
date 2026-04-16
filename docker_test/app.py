# 파이썬 웹 앱 개발 라이브러리
from flask import Flask
# Flask 애플리케이션 객체 생성
app = Flask(__name__)
# 라우팅(Route) 설정
# 사용자가 웹 브라우저에서 "/" (루트 경로)로 접속하면
# (http://localhost:5000)
# 아래의 hello() 함수가 실행됨
@app.route("/")
def hello():
    return "Hello, Docker! "
# if __name__ == "__main__": -> 이 파일이 직접 실행될 때만 실행됨
if __name__ == "__main__":
    # Flask 서버 실행
    # host="0.0.0.0" : 모든 네트워크 인터페이스에서 접속 허용
    # port=5000 : 5000번 포트에서 서비스 시작
    app.run(host="0.0.0.0", port=5000)