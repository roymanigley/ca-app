FROM alpine:latest
COPY CA.pem /usr/local/share/ca-certificates/CA.crt
RUN apk update \
	&& apk upgrade --available \
	&& apk add ca-certificates curl \
	&& update-ca-certificates

WORKDIR /app
RUN addgroup -S app-group && adduser -S app-user -G app-group

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

USER app-user

CMD ["./entrypoint.sh"]
