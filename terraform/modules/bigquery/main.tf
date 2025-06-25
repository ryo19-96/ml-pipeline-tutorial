resource "google_bigquery_dataset" "house_prices_dataset" {
  dataset_id  = "house_prices_dataset"
  description = "Dataset for house prices data"
  location    = var.region
}

resource "google_bigquery_table" "train_data" {
  dataset_id          = google_bigquery_dataset.house_prices_dataset.dataset_id
  table_id            = "train_data"
  deletion_protection = false
}
