# NTA_lab3

- download docker from remote: `docker pull mansteinorguderian/ntathird:latest`
- run docker from remote: `docker run --rm -it mansteinorguderian/ntathird:latest`
- build from git repository: `docker build -t 'mansteinorguderian/ntathird' .`
- run cli: `docker run --rm -it 'mansteinorguderian/ntathird'`
- stop container: `docker stop $(docker ps | grep "mansteinorguderian/ntathird" | cut -d " " -f1)`
- remove image: `docker image rm 'mansteinorguderian/ntathird`
