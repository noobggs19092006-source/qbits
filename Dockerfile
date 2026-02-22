FROM python:3.11-slim

# Install build dependencies
RUN apt-get update && apt-get install -y \
    cmake ninja-build libssl-dev pkg-config git build-essential \
    && rm -rf /var/lib/apt/lists/*

# Build and install liboqs C library from source (latest main branch)
RUN git clone --depth 1 https://github.com/open-quantum-safe/liboqs.git /tmp/liboqs \
    && cmake -S /tmp/liboqs -B /tmp/liboqs/build \
        -DOQS_DIST_BUILD=ON \
        -DBUILD_SHARED_LIBS=ON \
        -DCMAKE_BUILD_TYPE=Release \
        -GNinja \
    && ninja -C /tmp/liboqs/build \
    && ninja -C /tmp/liboqs/build install \
    && ldconfig \
    && rm -rf /tmp/liboqs

# Set library path so Python can find liboqs
ENV LD_LIBRARY_PATH=/usr/local/lib

# Install Python dependencies (liboqs-python will find the pre-installed C library)
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Expose port (Render sets $PORT env var at runtime)
EXPOSE 10000

CMD ["python", "src/app.py"]
