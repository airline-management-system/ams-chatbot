FROM golang:1.23-alpine
WORKDIR /app
COPY . .
ENV CGO_ENABLED=0
RUN go build -ldflags '-w -s -extldflags "-static"' -a -o application cmd/app/main.go

FROM scratch
COPY --from=0 /app/application ./
CMD ["./application"]
