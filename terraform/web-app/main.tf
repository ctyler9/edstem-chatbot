terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.82.0"
    }
  }
}

provider "google" {
  credentials = file("")
  project     = "edstem-chatbot"
  region      = "us-central" # Choose your desired region
  zone        = "us-central1-c"
}

resource "google_compute_instance" "edstem-chatbot" {
  name         = "edstem-chatbot"
  machine_type = "n1-standard-16"
  zone         = "us-central1-c"
  boot_disk {
    initialize_params {
      size  = 100
      image = "debian-cloud/debian-12"
    }
  }
  network_interface {
    network = "default"
    access_config {
    }
  }
  tags = ["web-app-firewall"]
}

resource "google_compute_firewall" "web-app-firewall" {
  name    = "allow-http"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["8501"]
  }

  target_tags   = ["web-app-firewall"] # Apply the rule only to instances with this tag
  source_ranges = ["0.0.0.0/0"]
}

