FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

ENV PYTHONUNBUFFERED 1

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# Poetry
USER vscode
# RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 - && \
#     cd /usr/local/bin && \
#     ln -s /opt/poetry/bin/poetry && \
#     poetry config virtualenvs.create true
# RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 - && \
#     cd /usr/local/bin && \
#     ln -s /opt/poetry/bin/poetry && \
#     poetry config virtualenvs.create true
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && export PATH="/home/vscode/.local/bin:$PATH" \
    && poetry config virtualenvs.create true
USER root
