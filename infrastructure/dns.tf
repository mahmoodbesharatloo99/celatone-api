resource "cloudflare_record" "celatone_api" {
  zone_id = local.cloudflare_zone_id
  name    = "celatone-api-${var.environment}"
  type    = "CNAME"
  value   = "ghs.googlehosted.com."
  ttl     = 1
  proxied = true
}
