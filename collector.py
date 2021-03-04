print("collector 프로그램이 시작 되었습니다!")

# mysql이라는 데이터베이스를 사용하기 위해 필요한 패키지들 ->
from sqlalchemy import create_engine
import pymysql

pymysql.install_as_MySQLdb()


class Collector:
    def __init__(self):
        print("__init__ 함수에 들어왔습니다.")
        self.engine_bot = None

    def db_setting(self, db_name, db_id, db_passwd, db_ip, db_port):
        print("db_setting 함수에 들어왔습니다.")
        # mysql 데이터베이스랑 연동하는 방식.
        self.engine_bot = create_engine("mysql+mysqldb://" + db_id + ":" + db_passwd + "@"
                                        + db_ip + ":" + db_port + "/" + db_name, encoding='utf-8')


print("collector.py 의 __name__ 은?: ", __name__)
if __name__ == "__main__":
    print("__main__에 들어왔습니다.")
    # c = collector() 이렇게 c라는 collector라는 클래스의 인스턴스를 만든다.
    # 아래 클래스를 호출하자마다 __init__ 함수가 실행이 된다.
    c = Collector()
    # db_name 이라는 변수에 우리가 조회 하고자 하는 데이터베이스의 이름을 넣는다.
    db_name = 'test1'
    # mysql db 계정
    db_id = 'bot'
    # mysql db ip (자신의 PC에 DB를 구축 했을 경우 별도 수정 필요 없음)
    db_ip = 'localhost'  # localhost : 자신의 컴퓨터를 의미
    # mysql db 패스워드
    db_passwd = '1232'
    # db port가 3306이 아닌 다른 port를 사용 하시는 분은 아래 변수에 포트에 맞게 수정하셔야 합니다.
    db_port = '3306'

    c.db_setting(db_name, db_id, db_passwd, db_ip, db_port)

    # 데이터베이스에 실행 할 쿼리
    sql = "select * from test1.class1;"

    # 위의 sql 문을 데이터베이스에 실행한 결과를 rows라는 변수에 담는다.
    rows = c.engine_bot.execute(sql).fetchall()
    print(rows)
