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
# === apiの有効化 ===
resource "google_project_service" "required_apis" {
  for_each = toset([
    "aiplatform.googleapis.com",
    "storage.googleapis.com",
    "bigquery.googleapis.com",
    "compute.googleapis.com",
    "artifactregistry.googleapis.com"
  ])
  project = var.project_id
  service = each.key
}

# === moduleの呼び出し ===
module "bigquery" {
  source = "./modules/bigquery"
  region = var.region
}

module "gcs" {
  source                        = "./modules/gcs"
  region                        = var.region
  pipeline_bucket_name          = var.pipeline_bucket_name
  house_prices_data_bucket_name = var.house_prices_data_bucket_name
}

module "vertex_ai" {
  source     = "./modules/vertex_ai"
  project_id = var.project_id
}


