resource "google_service_account" "pipeline_sa" {
  account_id   = "vertex-pipeline-sa"
  display_name = "Vertex AI Pipeline Service Account"
}


# サービスアカウントが Vertex AI を使えるようにする
resource "google_project_iam_member" "pipeline_vertex_ai" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
}

# Metadata 作成／取得用のロール
resource "google_project_iam_member" "pipeline_metadata_admin" {
  project = var.project_id
  role    = "roles/aiplatform.admin"
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
}

# GCS 読み書き用
resource "google_project_iam_member" "pipeline_storage" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
}

resource "google_project_iam_member" "pipeline_sa_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
}

resource "google_project_iam_member" "pipeline_bigquery" {
  project = var.project_id
  role    = "roles/bigquery.admin"
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
}
