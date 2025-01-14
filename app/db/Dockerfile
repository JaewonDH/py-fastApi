# PostgreSQL 공식 이미지 사용
FROM postgres:latest

# 환경 변수 설정
ENV POSTGRES_DB=Sample
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=1234

# 데이터 저장을 위한 볼륨 설정
VOLUME ["/var/lib/postgresql/data"]

# 로그 파일을 외부로 마운트할 수 있도록 설정 (옵션)
VOLUME ["/var/log/postgresql"]

# 포트 5432를 열기
EXPOSE 5432

# 컨테이너 시작 시 PostgreSQL이 자동으로 실행되도록 설정
CMD ["postgres"]