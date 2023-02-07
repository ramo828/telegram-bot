from command import Router, Dns
import settings as sett

router = Router()
dns = Dns()
router.getIp()
ip = router.IP()

dns.init_dns(sett.duckdns_api, sett.duckdns_domain_name, ip)
dns.run()