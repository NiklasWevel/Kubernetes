
```mermaid
flowchart LR

WAN["WAN"]
LAN["LAN"]
Cloudflare("Cloudflare")

subgraph Home["Home"]
    opnSense["opnSense"]
    LAN

    subgraph KubernetesCluster["Kubernetes Cluster"]
        CloudflareDDNS["Cloudflare-DDNS"]

        subgraph Traefik["Traefik"]
            wan-ep["websecure-wan-traffic :9443"]
            lan-ep["websecure :443"]
        end

        OAuth2-Proxy["OAuth2-Proxy"]
        Pocketid["PocketID"]
        Application["Application"]
    end
end

%% DNS
CloudflareDDNS -- "updates IP" --> Cloudflare
WAN -. "NS Lookup" .-> Cloudflare

%% Traffic
WAN -- ":443" --> opnSense
LAN -- ":443" --> opnSense
opnSense -- ":443" --> lan-ep
opnSense -- "NAT → :9443" --> wan-ep
lan-ep --> Application
wan-ep --> OAuth2-Proxy
OAuth2-Proxy -- "not authed → redirect" --> Pocketid
Pocketid -- "token callback" --> OAuth2-Proxy
OAuth2-Proxy -- "authed" --> Application

```

# The Facts

I get a public, but dynamic IPv4 address from my ISP. Normally I access my homelab over a WireGuard connection. This setup is tested and works, but after testing I disabled the port forward on my OPNsense because I have no reason to switch from WireGuard to an arguably larger attack surface.
This was just a fun little side project to explore the technical possibilities of WAN access without WireGuard.

# The Goal

I want to separate external and internal traffic to keep internal access easy for non technical users like my wife, while still using secure means to access my Kubernetes cluster from the outside.

# ToDo

- [ ] Implement mTLS
