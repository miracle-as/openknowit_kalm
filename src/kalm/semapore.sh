curl -X 'POST' \
  'https://semaphore.openknowit.com/api/auth/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "auth": "knowit",
  "password": "ixj90j2s"
}'

curl -X 'GET' \
  'https://semaphore.openknowit.com/api/projects' \
  -H 'accept: application/json' \
  -d '{
  "auth": "knowit",
  "password": "ixj90j2s"
}'
