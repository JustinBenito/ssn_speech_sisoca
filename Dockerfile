# 1. Start from ESPnet official CPU image (already has Kaldi + ESPnet preinstalled)
FROM espnet/espnet:cpu

# 2. Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV KALDI_ROOT=/kaldi

# 3. Copy your repo into container
WORKDIR /workspace
COPY . /workspace

# 4. Install API dependencies in ESPnet's virtualenv
RUN . /espnet/tools/venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# 5. Make scripts executable
RUN chmod +x activate_python.sh path_try.sh main_run.sh main_run_mild.sh main_run_punitha.sh

# 6. Entry point (can be uvicorn/gunicorn for API)
COPY docker_entrypoint.sh /docker_entrypoint.sh
RUN chmod +x /docker_entrypoint.sh
ENTRYPOINT ["/docker_entrypoint.sh"]
