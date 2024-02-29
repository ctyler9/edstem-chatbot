terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.82.0"
    }
  }
}

provider "google" {
  credentials = file("~/.gcp_keys/edstem-chatbot-983bb556436a.json")
  project     = "edstem-chatbot"
  region      = "us-central" # Choose your desired region
  zone        = "us-central1-b"
}

resource "google_compute_instance" "edstem-chatbot" {
  name         = "edstem-chatbot"
  machine_type = "n1-standard-8"
  zone         = "us-central1-b"

  boot_disk {
    initialize_params {
      size  = 100
      image = "deeplearning-platform-release/pytorch-latest-gpu-debian-11-py310"
    }
  }

  # Attach 4 GPUs 
  guest_accelerator {
    #type = "nvidia-l4"
    type = "nvidia-tesla-t4"
    #type = "nvidia-tesla-p4"
    #type = "nvidia-tesla-v100"
    #type = "nvidia-tesla-p100"
    #type  = "nvidia-tesla-k80"
    count = 1
  }

  network_interface {
    network = "default"
    access_config {
    }
  }

  #  metadata = {
  #    install-nvidia-driver = "True"
  #    #proxy-mode            = "service_account"
  #  }

  scheduling {
    automatic_restart   = "true"
    on_host_maintenance = "TERMINATE"
  }
  tags = ["server-port"]
}

resource "google_compute_firewall" "server-firewall" {
  name    = "allow-http"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["8000"]
  }

  target_tags   = ["server-port"] # Apply the rule only to instances with this tag
  source_ranges = ["0.0.0.0/0"]
}

