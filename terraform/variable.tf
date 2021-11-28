variable "project" {
  description = "A name of a GCP Project"
  type        = string
  default     = null
}

variable "region" {
  description = "A region to use the module"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "A zone to use the module"
  type        = string
  default     = "us-central1-a"
}

variable "run-domain" {
  description = "Cloud Run domain"
  type        = string
  default     = "example.com"
}

variable "bucket" {
  description = "GCS bucket"
  type        = string
  default     = "stairlight"
}
