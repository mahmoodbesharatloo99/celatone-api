build-and-push:
	docker build -t celatone/api:latest .
	docker tag celatone/api:latest asia-southeast1-docker.pkg.dev/alles-share/shared-docker-images/celatone/api:latest
	docker push asia-southeast1-docker.pkg.dev/alles-share/shared-docker-images/celatone/api:latest

terraform-apply:
	cd infrastructure
	terraform init
	terraform apply -var="image_url=asia-southeast1-docker.pkg.dev/alles-share/shared-docker-images/celatone/api:latest"