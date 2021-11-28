host_port = 8551
container_port = 8501
version = latest
src_dir = src
config_dir = .streamlit

lint:
	poetry run flake8 ./src
	poetry run isort --check --diff ./src
	poetry run black --check ./src

format:
	poetry run isort ./src
	poetry run black ./src

build-local:
	@cp ./poetry.lock ${src_dir}
	@cp ./pyproject.toml ${src_dir}
	docker build -t stairlight-app:${version} ${src_dir}
	@rm ${src_dir}/poetry.lock
	@rm ${src_dir}/pyproject.toml

run-local:
	@docker run --rm \
		--name stairlight-app \
		-e PORT=${container_port} \
		-p ${host_port}:${container_port} \
		-v $(CURDIR)/${src_dir}:/app \
		-v $(CURDIR)/${config_dir}:/root/${config_dir} \
		-v ~/.config/gcloud/application_default_credentials.json:/root/.config/gcloud/application_default_credentials.json \
		-e GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT} \
		stairlight-app | sed -e "s/${container_port}/${host_port}/g"

build-gcr:
	@cp ./poetry.lock ${src_dir}
	@cp ./pyproject.toml ${src_dir}
	gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/stairlight-app ./src
	@rm ${src_dir}/poetry.lock
	@rm ${src_dir}/pyproject.toml

deploy:
	gcloud run deploy stairlight-app --image gcr.io/${GOOGLE_CLOUD_PROJECT}/stairlight-app --region us-central1
