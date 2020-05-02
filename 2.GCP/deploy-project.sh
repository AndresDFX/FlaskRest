#!/usr/bin/env bash

REMOTE="34.83.147.81:8000"
TOKEN="1217795cd102feffcd28841ca315e9ebddf5ac923a5f44ad9dc728ea717918e6"
DIGEST="sha256:e1ae8711fa5a7ee30bf577d665a7a91bfe35556f83264c06896765d75b84a990"
UPSTREAM="localhost:5000"
docker run \
--interactive --tty \
--net=host \
--env=REMOTE=${REMOTE} \
--env=TOKEN=${TOKEN} \
inlets/inlets@${DIGEST} \
client \
--remote=${REMOTE} \
--upstream=${UPSTREAM} \
--token=${TOKEN} 