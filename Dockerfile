FROM python:2.7.17-stretch as builder
# Setup non root user with limit option
#
RUN adduser \
    --gecos \
    --disabled-password \
    --disabled-login \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid 80008 \
    mike

WORKDIR /opt/qs-backend
COPY src /opt/qs-backend/
RUN apt update && \
    apt-get install tzdata && \
    /bin/bash -c 'mkdir /opt/qs-backend/logs' && \
    /bin/bash -c '/opt/qs-backend/setup_runtime.sh'

#ADD https://busybox.net/downloads/binaries/1.21.1/busybox-x86_64 /opt/qs-backend/tools/busybox
#RUN chmod a+x /opt/qs-backend/tools/busybox && \
#    /opt/qs-backend/tools/busybox --install -s /opt/qs-backend/tools

##
## Build real docker image
##
FROM python:2.7.17-slim-stretch
WORKDIR /opt/qs-backend

# Copy main code
#
COPY --from=builder /opt/qs-backend /opt/qs-backend/

# Copy zoneinfo
#
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo

# Copy missed dynamic libraries
#
COPY --from=builder /usr/lib/x86_64-linux-gnu/libxml2.so.2 /usr/lib/x86_64-linux-gnu/
COPY --from=builder /usr/lib/x86_64-linux-gnu/libicui18n.so.57 /usr/lib/x86_64-linux-gnu/
COPY --from=builder /usr/lib/x86_64-linux-gnu/libicudata.so.57 /usr/lib/x86_64-linux-gnu/
COPY --from=builder /usr/lib/x86_64-linux-gnu/libicuuc.so.57 /usr/lib/x86_64-linux-gnu/

# Copy running user
#
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group

# Update ownership of logs folder
#
RUN chown -R mike:mike /opt/qs-backend/logs

# User non root user with limited privelege
#
USER mike:mike

EXPOSE 8889
VOLUME /opt/qs-backend/logs

ENTRYPOINT ["/opt/qs-backend/pyenv/bin/uwsgi", "--ini", "/opt/qs-backend/api.ini"]