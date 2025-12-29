FROM python:3.13.8-slim
COPY --from=ghcr.io/astral-sh/uv:0.9.18 /uv /uvx /bin/

ARG RUN_ENV=local
ARG LANG=en_US.UTF-8
ARG LC_ALL=en_US.UTF-8
ARG BASE_DIR=/code 

# Setup uv environment outside BASE_DIR
# This prevents it from being hidden when docker compose mounts over /code
ENV UV_PROJECT_ENVIRONMENT=/.venv

# Install the project into BASE_DIR
WORKDIR $BASE_DIR

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    UV_NO_DEV=$([ "$RUN_ENV" = "local" ] && echo 0 || echo 1) \
    uv sync --locked --no-install-project

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . $BASE_DIR
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

COPY ./docker-entrypoint.sh /docker-entrypoint.sh


# Place executables in the environment at the front of the path
ENV PATH="$UV_PROJECT_ENVIRONMENT/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

RUN chmod +x $BASE_DIR/tests-start.sh
RUN chmod +x /docker-entrypoint.sh

# Use the non-root user to run our application
CMD ["/docker-entrypoint.sh"]
