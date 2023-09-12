resource "google_cloud_run_v2_service" "celatone_api" {
  name     = "celatone-api-${var.environment}"
  location = "asia-southeast1"
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    scaling {
      max_instance_count = 2
    }

    containers {
      image = var.image_url

      env {
        name  = "LCD_DICT"
        value = var.lcd_dict
      }

      env {
        name  = "HIVE_DICT"
        value = var.hive_dict
      }

      env {
        name  = "GRAPHQL_DICT"
        value = var.graphql_dict
      }

      env {
        name  = "SCANWORKS_URL"
        value = var.scanworks_url
      }

      env {
        name  = "PRICE_CACHER_URL"
        value = var.price_cacher_url
      }

      env {
        name  = "GRAPHQL_TEST_DICT"
        value = var.graphql_test_dict
      }

      env {
        name  = "WLD_URL"
        value = var.wld_url
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

resource "google_cloud_run_v2_service_iam_binding" "binding" {
  location = google_cloud_run_v2_service.celatone_api.location
  name     = google_cloud_run_v2_service.celatone_api.name
  role     = "roles/run.invoker"
  members = [
    "allUsers",
  ]
}

# resource "google_cloud_run_domain_mapping" "celatone_api" {
#   location = google_cloud_run_v2_service.celatone_api.location
#   name     = "celatone-test.alleslabs.dev"

#   metadata {
#     namespace = "celatone-production"
#   }

#   spec {
#     route_name = google_cloud_run_v2_service.celatone_api.name
#   }
# }

# output "dns" {
#   value = google_cloud_run_domain_mapping.celatone_api.status
# }
