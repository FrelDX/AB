from python
copy requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
copy ./*/ /app/
CMD ["python /app/main.py runserver"]