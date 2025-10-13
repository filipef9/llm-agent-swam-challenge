FROM python:3.13-slim

ENV PYTHONNUMBUFFERED=1
ENV TZ="America/Sao_Paulo"

WORKDIR /code

COPY requirements.txt /code/requirements.txt
COPY src/pipeline /code/pipeline
COPY entrypoint.sh /code/entrypoint.sh

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN python -c "from transformers import AutoTokenizer, AutoModel; AutoTokenizer.from_pretrained('sentence-transformers/paraphrase-multilingual-mpnet-base-v2'); AutoModel.from_pretrained('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')"
RUN ["chmod", "+x", "./entrypoint.sh"]

CMD ["./entrypoint.sh"]

