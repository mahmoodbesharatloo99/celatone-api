terraform {
  backend "gcs" {
    bucket = "celatone-tf-states"
    prefix = "celatone-api"
  }

  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.73.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = ">= 4.73.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4"
    }
  }
}

provider "cloudflare" {
  api_token = data.google_secret_manager_secret_version.cloudflare_api_token.secret_data
}

provider "google" {
  project = var.project_id
}

data "google_secret_manager_secret_version" "cloudflare_api_token" {
  project = "alles-share"
  secret  = "cloudflare-alleslabs-dev-admin-token"
}
