FROM swift:6.0-jammy AS build
WORKDIR /build
COPY Package.swift ./
COPY Sources ./Sources
COPY Tests ./Tests
RUN swift test -c release
RUN swift build -c release --product ninecirc-server

FROM ubuntu:22.04 AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates libatomic1 && rm -rf /var/lib/apt/lists/* \
    && useradd --system --uid 10001 --create-home app
WORKDIR /app
COPY --from=build /build/.build/release/ninecirc-server /usr/local/bin/ninecirc-server
USER 10001:10001
EXPOSE 8080
ENV HOST=0.0.0.0 PORT=8080
ENTRYPOINT ["/usr/local/bin/ninecirc-server"]
