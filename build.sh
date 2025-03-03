docker build . -t fullaware/ollama-pydantic:latest
docker push fullaware/ollama-pydantic:latest

helm upgrade ollama-pydantic ./ollama-pydantic/ -n ollama-pydantic --create-namespace
kubectl rollout restart deploy ollama-pydantic-app -n ollama-pydantic