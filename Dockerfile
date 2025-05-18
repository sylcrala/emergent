#-# python import #-#
FROM python:3.13.3

#-# system dependencies #-#
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    g++ \
    nano \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

#-# disabling output buffering
ENV PYTHONUNBUFFERED=1

#-# creating working directory #-#
WORKDIR /app

#-# copying required modules #-#
COPY requirements.txt .

#-# installing required modules #-#
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

#-# copying rest of app #-#
COPY . .

#-# launch iris live #-#
CMD bash -c "python main.py"

