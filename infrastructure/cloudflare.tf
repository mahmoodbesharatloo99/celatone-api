resource "cloudflare_record" "celatone_api" {
  zone_id = local.cloudflare_zone_id
  name    = "celatone-api-${var.environment}"
  type    = "CNAME"
  value   = "ghs.googlehosted.com."
  ttl     = 1
  proxied = true
}

// disable browser integrity check, turns off Automatic HTTPS rewrites
resource "cloudflare_page_rule" "acme" {
  zone_id  = local.cloudflare_zone_id
  target   = "celatone-api-${var.environment}.alleslabs.dev/.well-known/acme-challenge/*"
  priority = 2

  actions {
    automatic_https_rewrites = "off"
    browser_check            = "off"
  }
}

resource "cloudflare_page_rule" "full_ssl" {
  zone_id  = local.cloudflare_zone_id
  target   = "celatone-api-${var.environment}.alleslabs.dev/*"
  priority = 1

  actions {
    ssl = "full"
  }
}

resource "cloudflare_ruleset" "rate_limit" {
  zone_id     = local.cloudflare_zone_id
  name        = "celatone-api-${var.environment}-rate-limit"
  description = "Rate limit Celatone API requests to 1000 per minute"
  kind        = "zone"
  phase       = "http_ratelimit"

  rules {
    action = "block"
    action_parameters {
      response {
        status_code  = 429
        content      = "{\"message\": \"rate limit reached\"}"
        content_type = "application/json"
      }
    }

    ratelimit {
      characteristics     = ["cf.colo.id", "ip.src"]
      period              = 60
      requests_per_period = 3
      mitigation_timeout  = 60
      requests_to_origin  = false
    }

    expression  = "(http.host eq \"celatone-api-${var.environment}.alleslabs.dev\")"
    description = "Rate limit Celatone API requests to 1000 per minute"
    enabled     = true
  }
}

