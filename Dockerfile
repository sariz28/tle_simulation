FROM python:2.7

COPY modules modules/
COPY requirements.txt .

RUN pip install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:./modules/tle-simulation/src"
ENV DISPLAY=:1.0

ENTRYPOINT ["python", "/modules/tle-simulation/src/main.py"]