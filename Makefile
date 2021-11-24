host_port = 8551
container_port = 8501
version = latest
src_dir = src/lighthouse

build-local:
	@cp ./poetry.lock ${src_dir}
	@cp ./pyproject.toml ${src_dir}
	docker build -t lighthouse:${version} ${src_dir}
	@rm ${src_dir}/poetry.lock
	@rm ${src_dir}/pyproject.toml

run-local:
	@docker run --rm \
		--name lighthouse \
		-e PORT=${container_port} \
		-p ${host_port}:${container_port} \
		-v $(CURDIR)/${src_dir}:/app \
		-v ~/.config/gcloud/application_default_credentials.json:/root/.config/gcloud/application_default_credentials.json \
		lighthouse | sed -e "s/${container_port}/${host_port}/g"

build-gcr:
	@gcloud builds submit --tag gcr.io/${GCP_PROJECT}/lighthouse ./src/lighthouse
