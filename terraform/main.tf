provider "google" {
  project = var.project
  region  = var.region
  zone    = var.zone
}

terraform {
  backend "gcs" {
  }
}

##############################################
# Cloud Run
##############################################
resource "google_cloud_run_service" "stairlight-app" {
  name     = "stairlight-app"
  location = var.region
  template {
    spec {
      containers {
        image = "gcr.io/${var.project}/stairlight-app:latest"
        resources {
          limits = {
            "cpu" : "1000m"
            "memory" : "512Mi"
          }
        }
      }
      container_concurrency = "100"
      service_account_name  = google_service_account.sa-stairlight-app.email
    }
    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale" = "10"
        "autoscaling.knative.dev/minScale" = "0"
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_domain_mapping" "domain-mapping" {
  location = var.region
  name     = var.run-domain

  metadata {
    namespace = var.project
  }

  spec {
    route_name = google_cloud_run_service.stairlight-app.name
  }
}

##############################################
# Service Account
##############################################
resource "google_service_account" "sa-stairlight-app" {
  account_id   = "sa-stairlight-app"
  display_name = "sa-stairlight-app"
}

##############################################
# Cloud IAM
##############################################
resource "google_cloud_run_service_iam_member" "noauth" {
  location = google_cloud_run_service.stairlight-app.location
  project  = google_cloud_run_service.stairlight-app.project
  service  = google_cloud_run_service.stairlight-app.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_storage_bucket_iam_member" "gcs-bucket-policy" {
  bucket = var.bucket
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.sa-stairlight-app.email}"
}

resource "google_storage_bucket_iam_member" "gcs-bucket-custom-policy" {
  bucket = var.bucket
  role   = "projects/${var.project}/roles/CustomStorageObjectViewer"
  member = "serviceAccount:${google_service_account.sa-stairlight-app.email}"
}
