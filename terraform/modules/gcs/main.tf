resource "google_storage_bucket" "pipeline_bucket" {
  name     = "pipeline_tutorial_house_prices"
  location = var.region
}
