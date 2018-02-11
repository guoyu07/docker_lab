docker stop clamd
docker rm clamd
docker run -d -p 3310:3310 --name clamd -v `pwd`/clamd.conf:/etc/clamav/clamd.conf:ro mkodockx/docker-clamav
