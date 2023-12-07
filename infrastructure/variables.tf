variable "aldus_url" {
  type = string
}

variable "environment" {
  type = string
}

variable "image_url" {
  type = string
}

variable "price_cacher_url" {
  type = string
}

variable "wld_url" {
  type = string
}

variable "endpoint_bucket_name" {
  type = string
}

variable "cloudflare_domain_binding" {
  type    = bool
  default = false
}

variable "project_id" {
  type    = string
  default = "alles-playground"
}
