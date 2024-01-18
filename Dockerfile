FROM python:3.9

# Add user an change working directory and user
RUN addgroup --system app && adduser --system --ingroup app app
WORKDIR /home/app
RUN chown app:app -R /home/app
USER app

RUN virtualenv /ve

# Install requirements
COPY requirements.txt .
RUN /ve/bin/pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the app
COPY . .

# Run app on port 8080
EXPOSE 8080
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]