# use Python image
FROM python:3.9

# create a working directory inside the container
WORKDIR /app

# copy project files to the container
COPY . .

# go to the copied backend directory
WORKDIR /app/backend

# install required python modules
RUN pip install -r requirements.txt

# expose the port to communicate with the container
EXPOSE 8080

# run the backend server
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]