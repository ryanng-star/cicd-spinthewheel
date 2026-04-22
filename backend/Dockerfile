# 1. The Base Engine: Start with a lightweight version of Python
FROM python:3.11-slim

# 2. The Workspace: Create a folder inside the container called /app
WORKDIR /app

# 3. The Supplies: Copy your requirements list first
COPY requirements.txt .

# 4. The Installation: Tell the container to download your 4 packages
RUN pip install --no-cache-dir -r requirements.txt

# 5. The Code: Copy your main.py file into the container
COPY . .

# 6. The Ignition: Start the production server (Gunicorn) on port 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]