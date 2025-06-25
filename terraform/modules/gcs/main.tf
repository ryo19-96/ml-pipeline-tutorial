resource "google_storage_bucket" "pipeline_bucket" {
  name     = var.pipeline_bucket_name
  location = var.region
}

resource "google_storage_bucket" "house_prices_data" {
  name     = var.house_prices_data_bucket_name
  location = var.region
}
