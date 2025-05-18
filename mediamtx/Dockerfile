# MediaMTX Dockerfile (minimal)
FROM alpine:latest

RUN apk add --no-cache curl tar

# Download and install MediaMTX
RUN curl -L https://github.com/bluenviron/mediamtx/releases/latest/download/mediamtx_v1.12.2_linux_amd64.tar.gz \
    | tar xz && mv mediamtx /usr/local/bin/

EXPOSE 8554 8888 1935

# Start MediaMTX
CMD ["mediamtx"]