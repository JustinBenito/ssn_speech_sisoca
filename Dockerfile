# step 1 is installing espnet
FROM espnet/espnet:cpu-latest

# Environment
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Copy repo
WORKDIR /workspace
COPY . /workspace

# Install requirements in ESPnet venv
RUN . /espnet/tools/venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Make scripts executable
RUN chmod +x activate_python.sh path_try.sh main_run.sh main_run_mild.sh main_run_punitha.sh

# Entrypoint
COPY docker_entrypoint.sh /docker_entrypoint.sh
RUN chmod +x /docker_entrypoint.sh
ENTRYPOINT ["/docker_entrypoint.sh"]
