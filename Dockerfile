# 1️⃣ Base image (stable & compatible)
FROM python:3.11-slim

# 2️⃣ Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3️⃣ Set working directory
WORKDIR /app

# 4️⃣ Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 5️⃣ Create a virtual environment INSIDE the container
RUN python -m venv /opt/venv

# 6️⃣ Activate virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# 7️⃣ Upgrade pip inside venv
RUN pip install --upgrade pip

# 8️⃣ Copy requirements first (for layer caching)
COPY requirements.txt .

# 9️⃣ Install Python dependencies inside venv
RUN pip install --no-cache-dir -r requirements.txt

# 🔟 Copy application code
COPY . .

# 1️⃣1️⃣ Expose Streamlit port
EXPOSE 8501

# 1️⃣2️⃣ Streamlit environment config
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# 1️⃣3️⃣ Run Streamlit app using venv python
CMD ["streamlit", "run", "app.py"]
