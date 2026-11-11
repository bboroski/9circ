# Operations

## Local dependencies

Copy .env.example to .env and replace all development credentials before use. Start PostgreSQL, Qdrant and Redis with docker compose up -d --wait. PostgreSQL initializes schema files from migrations/postgres on an empty volume.

## API

Build with .NET 10 SDK and run the API project. The health endpoints are /healthz and /readyz. POST /api/v1/clusters accepts a flat row-major float array, dimensions, epsilon and minPoints. Input bounds are enforced in the API before scratch arrays are rented from ArrayPool.

## Swift module

Run swift test --package-path modules/buffer-swift. The mmap ring buffer is file-backed and process-local locking is used in this initial version. Do not assume cross-process atomicity yet.

## Ruby module

Run bundle install and bundle exec ruby -Itest test/test_ninecirc.rb from modules/lifecycle-ruby. Native components must export ninecirc_component_init and ninecirc_component_shutdown.

## Releases and rollback

CI builds and validates release artifacts on pushes and pull requests. No production registry, signing key or cluster credentials are configured in this repository. Publish only signed, digest-addressed artifacts to an approved registry. Record component version, ABI version and SHA-256 in ninecirc_artifacts before promotion. Roll back by deploying the previous immutable digest; never overwrite a released artifact tag.
