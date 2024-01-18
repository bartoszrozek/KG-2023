FROM python:3.9

# Add user an change working directory and user
WORKDIR /home/app

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the app
COPY . .

# Run app on port 8080
EXPOSE 8080
CMD ["shiny", "run", "app.py", "--host", "0.0.0.0", "--port", "8080"]
