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
  api_token = var.cloudflare_api_token
}

provider "google" {
  project = "celatone-production"
}
