FROM python:3.7.1
ENV PYTHON_VERSION 3.7.1
WORKDIR /code
ADD . /code
RUN pip install -r requirements.txt --timeout=90000 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
CMD ["python", "app.py"]
EXPOSE 7000
