terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  type = string
  default = "enterprise-ai-copilot"
}

variable "region" {
  type = string
  default = "us-central1"
}

resource "google_storage_bucket" "documents" {
  name     = "${var.project_id}-documents"
  location = var.region
}

resource "google_bigquery_dataset" "sales" {
  dataset_id = "sales"
  location   = var.region
}

resource "google_secret_manager_secret" "api_key" {
  secret_id = "llm-api-key"
  replication {
    automatic = true
  }
}
