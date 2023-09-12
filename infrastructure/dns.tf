# resource "cloudflare_record" "celatone_api" {
#   for_each = toset(google_cloud_run_domain_mapping.celatone_api.status.resource_records)
#   zone_id  = local.cloudflare_zone_id
#   name     = each.value.name
#   type     = each.value.type
#   value    = each.value.value
#   ttl      = 1
#   proxied  = true
# }
