resource "cloudflare_record" "celatone_api" {
  count   = var.cloudflare_domain_binding ? 1 : 0
  zone_id = local.cloudflare_zone_id
  name    = "celatone-api-${var.environment}"
  type    = "CNAME"
  value   = "ghs.googlehosted.com."
  ttl     = 1
  proxied = true
}

// disable browser integrity check, turns off Automatic HTTPS rewrites
resource "cloudflare_page_rule" "acme" {
  count    = var.cloudflare_domain_binding ? 1 : 0
  zone_id  = local.cloudflare_zone_id
  target   = "celatone-api-${var.environment}.alleslabs.dev/.well-known/acme-challenge/*"
  priority = 2

  actions {
    automatic_https_rewrites = "off"
    browser_check            = "off"
  }
}

resource "cloudflare_page_rule" "full_ssl" {
  count    = var.cloudflare_domain_binding ? 1 : 0
  zone_id  = local.cloudflare_zone_id
  target   = "celatone-api-${var.environment}.alleslabs.dev/*"
  priority = 1

  actions {
    ssl = "full"
  }
}
