# Choose docker image upon your environment
docker build -f ./docker/Dockerfile \
    --build-arg PIP_INDEX=https://pypi.org/simple \
    -t cybersim:latest .