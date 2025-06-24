terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">=5.33.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# === moduleの呼び出し ===
module "database" {
  source = "./modules/database"
  region = var.region
}

module "gcs" {
  source = "./modules/gcs"
  region = var.region
}
