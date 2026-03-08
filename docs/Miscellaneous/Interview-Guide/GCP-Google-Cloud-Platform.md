## GCP (Google Cloud Platform)

### Advanced Networking & Security

##### Q. How do you create a custom VPC network with multiple subnets in different regions?

**Answer:**
In GCP, VPC networks are global resources, and subnets are regional. Here's how to create a custom VPC with multiple subnets:

**Steps:**
1. Create a custom VPC network
2. Create subnets in different regions
3. Configure firewall rules

**Commands:**
```bash
# Create custom VPC network
gcloud compute networks create my-custom-vpc \
    --subnet-mode=custom \
    --bgp-routing-mode=regional

# Create subnet in us-central1
gcloud compute networks subnets create subnet-us-central \
    --network=my-custom-vpc \
    --region=us-central1 \
    --range=10.0.1.0/24

# Create subnet in europe-west1
gcloud compute networks subnets create subnet-europe \
    --network=my-custom-vpc \
    --region=europe-west1 \
    --range=10.0.2.0/24

# List subnets
gcloud compute networks subnets list --network=my-custom-vpc
```

---

##### Q. Explain VPC Peering in GCP and how to configure it securely?

**Answer:**
VPC Network Peering allows private communication between VPC networks across projects or organizations. Traffic stays within Google's network and doesn't traverse the public internet.

**Key Security Features:**
- Private IP connectivity
- No external IP addresses required
- No network bandwidth bottlenecks
- Lower network latency

**Steps:**
1. Create peering connection from both VPCs
2. Configure firewall rules
3. Verify connectivity

**Commands:**
```bash
# From VPC Network 1
gcloud compute networks peerings create peer-1-to-2 \
    --network=vpc-network-1 \
    --peer-project=PROJECT_ID_2 \
    --peer-network=vpc-network-2 \
    --auto-create-routes

# From VPC Network 2
gcloud compute networks peerings create peer-2-to-1 \
    --network=vpc-network-2 \
    --peer-project=PROJECT_ID_1 \
    --peer-network=vpc-network-1 \
    --auto-create-routes

# List peering connections
gcloud compute networks peerings list --network=vpc-network-1

# Verify peering status
gcloud compute networks peerings list-routes peer-1-to-2 \
    --network=vpc-network-1 \
    --region=us-central1
```

---

##### Q. How do you implement Cloud NAT for private instances to access the internet securely?

**Answer:**
Cloud NAT enables private instances without external IP addresses to access the internet securely while maintaining security by blocking inbound connections.

**Steps:**
1. Create Cloud Router
2. Configure Cloud NAT
3. Verify NAT gateway

**Commands:**
```bash
# Create Cloud Router
gcloud compute routers create nat-router \
    --network=my-vpc \
    --region=us-central1

# Create Cloud NAT configuration
gcloud compute routers nats create my-nat-config \
    --router=nat-router \
    --region=us-central1 \
    --nat-all-subnet-ip-ranges \
    --auto-allocate-nat-external-ips

# Create NAT with specific IP addresses
gcloud compute addresses create nat-ip-1 nat-ip-2 \
    --region=us-central1

gcloud compute routers nats create my-nat-config \
    --router=nat-router \
    --region=us-central1 \
    --nat-custom-subnet-ip-ranges=subnet-us-central \
    --nat-external-ip-pool=nat-ip-1,nat-ip-2

# Describe NAT configuration
gcloud compute routers nats describe my-nat-config \
    --router=nat-router \
    --region=us-central1

# View NAT gateway logs
gcloud logging read "resource.type=nat_gateway" \
    --limit=50 \
    --format=json
```

---

##### Q. Configure Cloud Armor security policies for DDoS protection and WAF rules?

**Answer:**
Cloud Armor provides DDoS protection and WAF capabilities at the edge of Google's network. It integrates with Cloud Load Balancing.

**Steps:**
1. Create security policy
2. Add rules (allow/deny)
3. Configure rate limiting
4. Attach to backend service

**Commands:**
```bash
# Create security policy
gcloud compute security-policies create my-security-policy \
    --description="DDoS and WAF protection"

# Add rule to block specific IP range
gcloud compute security-policies rules create 1000 \
    --security-policy=my-security-policy \
    --expression="origin.ip == '203.0.113.0/24'" \
    --action=deny-403 \
    --description="Block malicious IP range"

# Add rule to allow specific countries
gcloud compute security-policies rules create 2000 \
    --security-policy=my-security-policy \
    --expression="origin.region_code == 'US' || origin.region_code == 'CA'" \
    --action=allow \
    --description="Allow US and Canada"

# Add rate limiting rule
gcloud compute security-policies rules create 3000 \
    --security-policy=my-security-policy \
    --expression="true" \
    --action=rate-based-ban \
    --rate-limit-threshold-count=100 \
    --rate-limit-threshold-interval-sec=60 \
    --ban-duration-sec=600 \
    --conform-action=allow \
    --exceed-action=deny-429 \
    --enforce-on-key=IP

# Add SQL injection protection
gcloud compute security-policies rules create 4000 \
    --security-policy=my-security-policy \
    --expression="evaluatePreconfiguredExpr('sqli-stable')" \
    --action=deny-403 \
    --description="Block SQL injection attempts"

# Add XSS protection
gcloud compute security-policies rules create 5000 \
    --security-policy=my-security-policy \
    --expression="evaluatePreconfiguredExpr('xss-stable')" \
    --action=deny-403 \
    --description="Block XSS attacks"

# Attach to backend service
gcloud compute backend-services update my-backend-service \
    --security-policy=my-security-policy \
    --global

# List security policies
gcloud compute security-policies list

# Describe policy
gcloud compute security-policies describe my-security-policy
```

---

##### Q. How do you set up Private Google Access and Private Service Connect?

**Answer:**
**Private Google Access:** Allows VMs without external IPs to access Google APIs
**Private Service Connect:** Enables private connectivity to Google services and third-party services

**Private Google Access Setup:**
```bash
# Enable Private Google Access on subnet
gcloud compute networks subnets update subnet-us-central \
    --region=us-central1 \
    --enable-private-ip-google-access

# Verify Private Google Access
gcloud compute networks subnets describe subnet-us-central \
    --region=us-central1 \
    --format="get(privateIpGoogleAccess)"

# Create custom route to Google APIs
gcloud compute routes create route-to-google-apis \
    --network=my-vpc \
    --destination-range=199.36.153.8/30 \
    --next-hop-gateway=default-internet-gateway
```

**Private Service Connect Setup:**
```bash
# Create Private Service Connect endpoint
gcloud compute addresses create psc-endpoint-ip \
    --global \
    --purpose=PRIVATE_SERVICE_CONNECT \
    --addresses=10.0.3.10 \
    --network=my-vpc

# Create forwarding rule for Private Service Connect
gcloud compute forwarding-rules create psc-forwarding-rule \
    --global \
    --network=my-vpc \
    --address=psc-endpoint-ip \
    --target-google-apis-bundle=all-apis \
    --service-directory-registration=projects/PROJECT_ID/locations/us-central1

# List Private Service Connect endpoints
gcloud compute forwarding-rules list \
    --filter="loadBalancingScheme:INTERNAL"
```

---

##### Q. Implement Cloud VPN with high availability and configure BGP routing?

**Answer:**
Cloud VPN provides encrypted connectivity between on-premises network and GCP VPC. HA VPN provides 99.99% availability.

**Steps:**
1. Create Cloud Router with BGP
2. Create HA VPN Gateway
3. Create VPN tunnels
4. Configure BGP sessions

**Commands:**
```bash
# Create Cloud Router with BGP
gcloud compute routers create vpn-router \
    --region=us-central1 \
    --network=my-vpc \
    --asn=65001

# Create HA VPN Gateway
gcloud compute vpn-gateways create ha-vpn-gateway \
    --network=my-vpc \
    --region=us-central1

# Get gateway details
gcloud compute vpn-gateways describe ha-vpn-gateway \
    --region=us-central1

# Create peer VPN gateway
gcloud compute external-vpn-gateways create peer-gateway \
    --interfaces=0=PEER_IP_ADDRESS_1,1=PEER_IP_ADDRESS_2

# Create VPN tunnels (2 tunnels for HA)
gcloud compute vpn-tunnels create tunnel-1 \
    --peer-external-gateway=peer-gateway \
    --peer-external-gateway-interface=0 \
    --region=us-central1 \
    --ike-version=2 \
    --shared-secret=SECRET_1 \
    --router=vpn-router \
    --vpn-gateway=ha-vpn-gateway \
    --interface=0

gcloud compute vpn-tunnels create tunnel-2 \
    --peer-external-gateway=peer-gateway \
    --peer-external-gateway-interface=1 \
    --region=us-central1 \
    --ike-version=2 \
    --shared-secret=SECRET_2 \
    --router=vpn-router \
    --vpn-gateway=ha-vpn-gateway \
    --interface=1

# Configure BGP sessions
gcloud compute routers add-interface vpn-router \
    --interface-name=if-tunnel-1 \
    --ip-address=169.254.1.1 \
    --mask-length=30 \
    --vpn-tunnel=tunnel-1 \
    --region=us-central1

gcloud compute routers add-bgp-peer vpn-router \
    --peer-name=bgp-peer-1 \
    --interface=if-tunnel-1 \
    --peer-ip-address=169.254.1.2 \
    --peer-asn=65002 \
    --region=us-central1

# Verify VPN tunnel status
gcloud compute vpn-tunnels describe tunnel-1 \
    --region=us-central1

# Check BGP routes
gcloud compute routers get-status vpn-router \
    --region=us-central1
```

---

##### Q. How do you configure Cloud Load Balancing with SSL/TLS termination and backend security?

**Answer:**
GCP offers various load balancers (HTTP(S), TCP/SSL Proxy, Network). HTTPS Load Balancing provides SSL termination, CDN, and Cloud Armor integration.

**Steps:**
1. Create SSL certificate
2. Create backend service with health check
3. Create URL map
4. Create target HTTPS proxy
5. Create forwarding rule

**Commands:**
```bash
# Create managed SSL certificate
gcloud compute ssl-certificates create my-ssl-cert \
    --domains=example.com,www.example.com \
    --global

# Or upload self-managed certificate
gcloud compute ssl-certificates create my-ssl-cert \
    --certificate=PATH_TO_CERT.crt \
    --private-key=PATH_TO_KEY.key \
    --global

# Create health check
gcloud compute health-checks create https https-health-check \
    --port=443 \
    --request-path=/health \
    --check-interval=10s \
    --timeout=5s \
    --unhealthy-threshold=3 \
    --healthy-threshold=2

# Create backend service with security features
gcloud compute backend-services create my-backend-service \
    --protocol=HTTPS \
    --health-checks=https-health-check \
    --port-name=https \
    --timeout=30s \
    --enable-cdn \
    --enable-logging \
    --logging-sample-rate=1.0 \
    --connection-draining-timeout=300 \
    --global

# Add instance group to backend
gcloud compute backend-services add-backend my-backend-service \
    --instance-group=my-instance-group \
    --instance-group-zone=us-central1-a \
    --balancing-mode=UTILIZATION \
    --max-utilization=0.8 \
    --capacity-scaler=1.0 \
    --global

# Configure Cloud Armor on backend
gcloud compute backend-services update my-backend-service \
    --security-policy=my-security-policy \
    --global

# Create URL map
gcloud compute url-maps create my-url-map \
    --default-service=my-backend-service

# Add path matcher for advanced routing
gcloud compute url-maps add-path-matcher my-url-map \
    --path-matcher-name=my-matcher \
    --default-service=my-backend-service \
    --path-rules="/api/*=api-backend-service,/static/*=static-backend-service"

# Create target HTTPS proxy with SSL policy
gcloud compute ssl-policies create my-ssl-policy \
    --profile=MODERN \
    --min-tls-version=1.2

gcloud compute target-https-proxies create my-https-proxy \
    --url-map=my-url-map \
    --ssl-certificates=my-ssl-cert \
    --ssl-policy=my-ssl-policy

# Create global forwarding rule
gcloud compute forwarding-rules create my-https-forwarding-rule \
    --address=my-static-ip \
    --global \
    --target-https-proxy=my-https-proxy \
    --ports=443

# Enable HTTP to HTTPS redirect
gcloud compute url-maps import my-url-map \
    --source=url-map-redirect.yaml \
    --global
```

---

##### Q. Set up VPC Service Controls to create security perimeters for GCP services?

**Answer:**
VPC Service Controls provide security perimeters around GCP resources to prevent data exfiltration.

**Steps:**
1. Create access policy
2. Define service perimeter
3. Configure access levels
4. Set up ingress/egress rules

**Commands:**
```bash
# Create access policy (one-time setup per organization)
gcloud access-context-manager policies create \
    --organization=ORGANIZATION_ID \
    --title="My Access Policy"

# Set default policy
export POLICY_NAME=$(gcloud access-context-manager policies list \
    --organization=ORGANIZATION_ID \
    --format="value(name)")

# Create access level
gcloud access-context-manager levels create trusted_network \
    --policy=$POLICY_NAME \
    --title="Trusted Network Access" \
    --basic-level-spec=access-level.yaml

# access-level.yaml content:
# combiningFunction: AND
# conditions:
#   - ipSubnetworks:
#       - "203.0.113.0/24"
#     regions:
#       - US
#     members:
#       - "user:admin@example.com"

# Create service perimeter (dry-run mode first)
gcloud access-context-manager perimeters create my_perimeter \
    --policy=$POLICY_NAME \
    --title="Production Perimeter" \
    --resources=projects/PROJECT_NUMBER \
    --restricted-services=storage.googleapis.com,bigquery.googleapis.com \
    --access-levels=trusted_network \
    --enable-vpc-accessible-services \
    --vpc-allowed-services=storage.googleapis.com \
    --perimeter-type=regular

# Create perimeter with dry-run config
gcloud access-context-manager perimeters dry-run create my_perimeter \
    --policy=$POLICY_NAME \
    --perimeter-title="Test Perimeter" \
    --perimeter-resources=projects/PROJECT_NUMBER \
    --perimeter-restricted-services=storage.googleapis.com

# Add ingress rule
gcloud access-context-manager perimeters update my_perimeter \
    --policy=$POLICY_NAME \
    --set-ingress-policies=ingress-policy.yaml

# Add egress rule
gcloud access-context-manager perimeters update my_perimeter \
    --policy=$POLICY_NAME \
    --set-egress-policies=egress-policy.yaml

# List perimeters
gcloud access-context-manager perimeters list \
    --policy=$POLICY_NAME

# Monitor VPC-SC violations
gcloud logging read "protoPayload.metadata.@type=\"type.googleapis.com/google.cloud.audit.VpcServiceControlAuditMetadata\"" \
    --limit=50 \
    --format=json
```

---

##### Q. Configure Identity-Aware Proxy (IAP) for secure application access without VPN?

**Answer:**
IAP provides application-level access control, verifying user identity and context before granting access to applications.

**Steps:**
1. Enable IAP API
2. Configure OAuth consent screen
3. Enable IAP on backend service
4. Grant IAP roles

**Commands:**
```bash
# Enable IAP API
gcloud services enable iap.googleapis.com

# Configure IAP for App Engine
gcloud iap web enable \
    --resource-type=app-engine \
    --service=default

# Configure IAP for Compute Engine
gcloud iap web enable \
    --resource-type=backend-services \
    --service=my-backend-service

# Grant IAP access to user
gcloud iap web add-iam-policy-binding \
    --resource-type=backend-services \
    --service=my-backend-service \
    --member=user:user@example.com \
    --role=roles/iap.httpsResourceAccessor

# Grant IAP access to group
gcloud iap web add-iam-policy-binding \
    --resource-type=backend-services \
    --service=my-backend-service \
    --member=group:developers@example.com \
    --role=roles/iap.httpsResourceAccessor

# Configure access levels with context-aware access
gcloud iap settings set \
    --project=PROJECT_ID \
    --resource-type=backend-services \
    --service=my-backend-service \
    --access-levels=trusted_network

# Set OAuth client credentials
gcloud iap oauth-brands create \
    --application_title="My Application" \
    --support_email=support@example.com

# Get IAP settings
gcloud iap settings get \
    --project=PROJECT_ID \
    --resource-type=backend-services \
    --service=my-backend-service

# View IAP access logs
gcloud logging read "resource.type=gce_backend_service AND protoPayload.resourceName:iap" \
    --limit=50 \
    --format=json
```

---

##### Q. Implement Cloud Firewall rules with hierarchical firewall policies?

**Answer:**
Firewall rules control traffic to/from VM instances. Hierarchical firewall policies allow organization-level policy management.

**Steps:**
1. Create firewall rules at VPC level
2. Create hierarchical policies at org/folder level
3. Apply security best practices

**Commands:**
```bash
# VPC-level firewall rules

# Allow SSH from specific IP
gcloud compute firewall-rules create allow-ssh-from-office \
    --network=my-vpc \
    --action=ALLOW \
    --rules=tcp:22 \
    --source-ranges=203.0.113.0/24 \
    --priority=1000 \
    --description="Allow SSH from office IP"

# Allow internal traffic
gcloud compute firewall-rules create allow-internal \
    --network=my-vpc \
    --action=ALLOW \
    --rules=all \
    --source-ranges=10.0.0.0/8 \
    --priority=2000 \
    --description="Allow internal VPC traffic"

# Allow HTTPS with specific service account
gcloud compute firewall-rules create allow-https-from-lb \
    --network=my-vpc \
    --action=ALLOW \
    --rules=tcp:443 \
    --source-ranges=130.211.0.0/22,35.191.0.0/16 \
    --target-service-accounts=backend-sa@PROJECT_ID.iam.gserviceaccount.com \
    --priority=1000

# Deny all egress to specific IP
gcloud compute firewall-rules create deny-egress-to-restricted \
    --network=my-vpc \
    --action=DENY \
    --rules=all \
    --direction=EGRESS \
    --destination-ranges=192.0.2.0/24 \
    --priority=900

# Hierarchical Firewall Policies

# Create organization-level policy
gcloud compute firewall-policies create my-org-policy \
    --organization=ORGANIZATION_ID \
    --description="Organization-wide security policy"

# Add rule to block malicious IPs
gcloud compute firewall-policies rules create 1000 \
    --firewall-policy=my-org-policy \
    --organization=ORGANIZATION_ID \
    --action=deny \
    --direction=INGRESS \
    --src-ip-ranges=198.51.100.0/24,203.0.113.0/24 \
    --layer4-configs=all \
    --description="Block known malicious IPs"

# Add rule to allow monitoring
gcloud compute firewall-policies rules create 2000 \
    --firewall-policy=my-org-policy \
    --organization=ORGANIZATION_ID \
    --action=allow \
    --direction=INGRESS \
    --src-ip-ranges=35.191.0.0/16 \
    --layer4-configs=tcp:80,tcp:443 \
    --target-service-accounts=monitoring-sa@PROJECT_ID.iam.gserviceaccount.com

# Associate policy with folder
gcloud compute firewall-policies associations create \
    --firewall-policy=my-org-policy \
    --organization=ORGANIZATION_ID \
    --folder=FOLDER_ID \
    --name=production-policy

# Enable firewall logging
gcloud compute firewall-rules update allow-ssh-from-office \
    --enable-logging \
    --logging-metadata=include-all

# List firewall rules
gcloud compute firewall-rules list --filter="network:my-vpc"

# Describe firewall rule
gcloud compute firewall-rules describe allow-ssh-from-office
```

---

##### Q. Configure Cloud DNS with DNSSEC and private DNS zones?

**Answer:**
Cloud DNS provides managed DNS with DNSSEC support for security and private zones for internal name resolution.

**Steps:**
1. Create public/private DNS zones
2. Enable DNSSEC
3. Configure DNS records
4. Set up DNS forwarding

**Commands:**
```bash
# Create public DNS zone
gcloud dns managed-zones create my-public-zone \
    --dns-name=example.com. \
    --description="Public DNS zone for example.com" \
    --visibility=public

# Enable DNSSEC on public zone
gcloud dns managed-zones update my-public-zone \
    --dnssec-state=on

# Get DNSSEC key details for parent zone
gcloud dns managed-zones describe my-public-zone \
    --format="get(dnssecConfig.state)"

gcloud dns dns-keys list --zone=my-public-zone

# Create private DNS zone
gcloud dns managed-zones create my-private-zone \
    --dns-name=internal.example.com. \
    --description="Private DNS zone" \
    --visibility=private \
    --networks=my-vpc

# Add DNS records to public zone
gcloud dns record-sets create www.example.com. \
    --zone=my-public-zone \
    --type=A \
    --ttl=300 \
    --rrdatas=203.0.113.10

# Add MX record
gcloud dns record-sets create example.com. \
    --zone=my-public-zone \
    --type=MX \
    --ttl=3600 \
    --rrdatas="10 mail.example.com."

# Add TXT record for SPF
gcloud dns record-sets create example.com. \
    --zone=my-public-zone \
    --type=TXT \
    --ttl=3600 \
    --rrdatas="v=spf1 include:_spf.google.com ~all"

# Add CNAME record
gcloud dns record-sets create blog.example.com. \
    --zone=my-public-zone \
    --type=CNAME \
    --ttl=300 \
    --rrdatas=www.example.com.

# Add records to private zone
gcloud dns record-sets create db.internal.example.com. \
    --zone=my-private-zone \
    --type=A \
    --ttl=300 \
    --rrdatas=10.0.1.10

# Create DNS forwarding zone
gcloud dns managed-zones create forward-zone \
    --dns-name=onprem.local. \
    --description="Forward to on-premises DNS" \
    --visibility=private \
    --networks=my-vpc \
    --forwarding-targets=192.168.1.53,192.168.1.54

# Create DNS peering zone
gcloud dns managed-zones create peering-zone \
    --dns-name=peer.example.com. \
    --description="DNS peering zone" \
    --visibility=private \
    --networks=my-vpc \
    --target-network=projects/PEER_PROJECT/global/networks/peer-vpc

# Update record set
gcloud dns record-sets update www.example.com. \
    --zone=my-public-zone \
    --type=A \
    --ttl=300 \
    --rrdatas=203.0.113.20

# List DNS zones
gcloud dns managed-zones list

# List records in zone
gcloud dns record-sets list --zone=my-public-zone

# Export zone file
gcloud dns record-sets export zone-file.txt \
    --zone=my-public-zone

# Import zone file
gcloud dns record-sets import zone-file.txt \
    --zone=my-public-zone \
    --zone-file-format
```

---

##### Q. Set up Binary Authorization for container image security in GKE?

**Answer:**
Binary Authorization ensures only trusted container images are deployed to GKE clusters.

**Steps:**
1. Enable Binary Authorization API
2. Create attestors
3. Create policy
4. Sign images with attestation

**Commands:**
```bash
# Enable required APIs
gcloud services enable \
    binaryauthorization.googleapis.com \
    containeranalysis.googleapis.com \
    container.googleapis.com

# Create attestor
gcloud container binauthz attestors create my-attestor \
    --attestation-authority-note=my-note \
    --attestation-authority-note-project=PROJECT_ID

# Create note for attestor
cat > note.json <<EOF
{
  "name": "projects/PROJECT_ID/notes/my-note",
  "attestation": {
    "hint": {
      "human_readable_name": "Security Team Attestation"
    }
  }
}
EOF

curl -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    --data-binary @note.json \
    "https://containeranalysis.googleapis.com/v1/projects/PROJECT_ID/notes?noteId=my-note"

# Generate key pair for signing
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem

# Add public key to attestor
gcloud container binauthz attestors public-keys add \
    --attestor=my-attestor \
    --public-key-file=public.pem \
    --public-key-id-override=my-key-id

# Create Binary Authorization policy
cat > policy.yaml <<EOF
admissionWhitelistPatterns:
- namePattern: gcr.io/google_containers/*
- namePattern: gcr.io/google-containers/*
- namePattern: k8s.gcr.io/*
- namePattern: gke.gcr.io/*
defaultAdmissionRule:
  requireAttestationsBy:
  - projects/PROJECT_ID/attestors/my-attestor
  enforcementMode: ENFORCED_BLOCK_AND_AUDIT_LOG
  evaluationMode: REQUIRE_ATTESTATION
globalPolicyEvaluationMode: ENABLE
EOF

# Import policy
gcloud container binauthz policy import policy.yaml

# Create attestation for image
IMAGE_URL="gcr.io/PROJECT_ID/my-app:v1.0"
IMAGE_DIGEST=$(gcloud container images describe $IMAGE_URL --format='get(image_summary.digest)')

# Generate signature
echo -n "$IMAGE_DIGEST" | openssl dgst -sha256 -sign private.pem | base64 > signature.txt

# Create attestation
cat > attestation.json <<EOF
{
  "resourceUri": "$IMAGE_URL",
  "noteReference": "projects/PROJECT_ID/notes/my-note",
  "attestation": {
    "signature": {
      "publicKeyId": "my-key-id",
      "signature": "$(cat signature.txt)"
    }
  }
}
EOF

curl -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    --data-binary @attestation.json \
    "https://containeranalysis.googleapis.com/v1/projects/PROJECT_ID/occurrences"

# Enable Binary Authorization on GKE cluster
gcloud container clusters update my-cluster \
    --zone=us-central1-a \
    --enable-binauthz

# Verify policy
gcloud container binauthz policy export
```

---

##### Q. Configure GKE Private Cluster with authorized networks and Private Google Access?

**Answer:**
GKE Private Clusters keep nodes and control plane endpoints private, enhancing security.

**Steps:**
1. Create private GKE cluster
2. Configure authorized networks
3. Enable Private Google Access
4. Set up workload identity

**Commands:**
```bash
# Create GKE private cluster
gcloud container clusters create my-private-cluster \
    --region=us-central1 \
    --enable-ip-alias \
    --enable-private-nodes \
    --enable-private-endpoint \
    --master-ipv4-cidr=172.16.0.0/28 \
    --enable-master-authorized-networks \
    --master-authorized-networks=203.0.113.0/24 \
    --network=my-vpc \
    --subnetwork=my-subnet \
    --cluster-secondary-range-name=pod-range \
    --services-secondary-range-name=service-range \
    --enable-shielded-nodes \
    --enable-network-policy \
    --enable-workload-identity \
    --workload-pool=PROJECT_ID.svc.id.goog

# Update authorized networks
gcloud container clusters update my-private-cluster \
    --region=us-central1 \
    --enable-master-authorized-networks \
    --master-authorized-networks=203.0.113.0/24,198.51.100.0/24

# Create bastion host for cluster access
gcloud compute instances create bastion-host \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --network=my-vpc \
    --subnet=my-subnet \
    --no-address \
    --metadata=enable-oslogin=TRUE \
    --scopes=cloud-platform

# Connect to cluster from bastion
gcloud container clusters get-credentials my-private-cluster \
    --region=us-central1 \
    --internal-ip

# Configure Workload Identity for pod
kubectl create serviceaccount my-ksa

gcloud iam service-accounts create my-gsa

gcloud iam service-accounts add-iam-policy-binding \
    my-gsa@PROJECT_ID.iam.gserviceaccount.com \
    --role=roles/iam.workloadIdentityUser \
    --member="serviceAccount:PROJECT_ID.svc.id.goog[default/my-ksa]"

kubectl annotate serviceaccount my-ksa \
    iam.gke.io/gcp-service-account=my-gsa@PROJECT_ID.iam.gserviceaccount.com

# Deploy pod with Workload Identity
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: workload-identity-test
spec:
  serviceAccountName: my-ksa
  containers:
  - name: test
    image: google/cloud-sdk:slim
    command: ["sleep", "infinity"]
EOF

# Enable maintenance windows
gcloud container clusters update my-private-cluster \
    --region=us-central1 \
    --maintenance-window-start=2024-01-01T00:00:00Z \
    --maintenance-window-duration=4h \
    --maintenance-window-recurrence="FREQ=WEEKLY;BYDAY=SU"

# Configure cluster autoscaling
gcloud container clusters update my-private-cluster \
    --region=us-central1 \
    --enable-autoscaling \
    --min-nodes=1 \
    --max-nodes=10

# Enable vertical pod autoscaling
gcloud container clusters update my-private-cluster \
    --region=us-central1 \
    --enable-vertical-pod-autoscaling
```

---

##### Q. Implement Cloud Key Management Service (KMS) for encryption key management?

**Answer:**
Cloud KMS provides centralized key management for encryption keys with hardware security modules (HSM) support.

**Steps:**
1. Create key ring
2. Create encryption keys
3. Manage key versions and rotation
4. Use keys for encryption/decryption

**Commands:**
```bash
# Create key ring
gcloud kms keyrings create my-keyring \
    --location=us-central1

# Create symmetric encryption key
gcloud kms keys create my-encryption-key \
    --location=us-central1 \
    --keyring=my-keyring \
    --purpose=encryption \
    --rotation-period=90d \
    --next-rotation-time=2024-04-01T00:00:00Z

# Create HSM-backed key
gcloud kms keys create my-hsm-key \
    --location=us-central1 \
    --keyring=my-keyring \
    --purpose=encryption \
    --protection-level=hsm

# Create asymmetric signing key
gcloud kms keys create my-signing-key \
    --location=us-central1 \
    --keyring=my-keyring \
    --purpose=asymmetric-signing \
    --default-algorithm=rsa-sign-pkcs1-4096-sha512

# Create asymmetric encryption key
gcloud kms keys create my-asymmetric-key \
    --location=us-central1 \
    --keyring=my-keyring \
    --purpose=asymmetric-encryption \
    --default-algorithm=rsa-decrypt-oaep-4096-sha512

# Grant encryption/decryption permissions
gcloud kms keys add-iam-policy-binding my-encryption-key \
    --location=us-central1 \
    --keyring=my-keyring \
    --member=serviceAccount:my-sa@PROJECT_ID.iam.gserviceaccount.com \
    --role=roles/cloudkms.cryptoKeyEncrypterDecrypter

# Encrypt data
echo "Sensitive data" > plaintext.txt

gcloud kms encrypt \
    --location=us-central1 \
    --keyring=my-keyring \
    --key=my-encryption-key \
    --plaintext-file=plaintext.txt \
    --ciphertext-file=ciphertext.enc

# Decrypt data
gcloud kms decrypt \
    --location=us-central1 \
    --keyring=my-keyring \
    --key=my-encryption-key \
    --ciphertext-file=ciphertext.enc \
    --plaintext-file=decrypted.txt

# Sign data
gcloud kms asymmetric-sign \
    --location=us-central1 \
    --keyring=my-keyring \
    --key=my-signing-key \
    --version=1 \
    --digest-algorithm=sha512 \
    --input-file=document.txt \
    --signature-file=signature.sig

# Verify signature
gcloud kms asymmetric-verify \
    --location=us-central1 \
    --keyring=my-keyring \
    --key=my-signing-key \
    --version=1 \
    --digest-algorithm=sha512 \
    --input-file=document.txt \
    --signature-file=signature.sig

# Create new key version
gcloud kms keys versions create \
    --location=us-central1 \
    --keyring=my-keyring \
    --key=my-encryption-key

# Disable key version
gcloud kms keys versions disable 1 \
    --location=us-central1 \
    --keyring=my-keyring \
    --key=my-encryption-key

# Destroy key version (scheduled destruction)
gcloud kms keys versions destroy 1 \
    --location=us-central1 \
    --keyring=my-keyring \
    --key=my-encryption-key

# List keys
gcloud kms keys list \
    --location=us-central1 \
    --keyring=my-keyring

# Use KMS with Cloud Storage
gsutil kms encryption \
    -k projects/PROJECT_ID/locations/us-central1/keyRings/my-keyring/cryptoKeys/my-encryption-key \
    gs://my-bucket

# Use KMS with Compute Engine disk
gcloud compute disks create my-disk \
    --size=100GB \
    --zone=us-central1-a \
    --kms-key=projects/PROJECT_ID/locations/us-central1/keyRings/my-keyring/cryptoKeys/my-encryption-key
```

---

##### Q. Configure Secret Manager for secure secrets storage and access control?

**Answer:**
Secret Manager stores API keys, passwords, certificates, and other sensitive data with automatic replication and versioning.

**Steps:**
1. Create secrets
2. Add versions
3. Grant access permissions
4. Access secrets from applications

**Commands:**
```bash
# Enable Secret Manager API
gcloud services enable secretmanager.googleapis.com

# Create secret
gcloud secrets create my-api-key \
    --replication-policy="automatic" \
    --labels=env=production,team=backend

# Create secret with specific replication
gcloud secrets create my-db-password \
    --replication-policy="user-managed" \
    --locations=us-central1,us-east1

# Add secret version from file
echo -n "mysecretapikey12345" | gcloud secrets versions add my-api-key \
    --data-file=-

# Add secret version from file
gcloud secrets versions add my-db-password \
    --data-file=password.txt

# Grant access to service account
gcloud secrets add-iam-policy-binding my-api-key \
    --member=serviceAccount:my-app@PROJECT_ID.iam.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor

# Grant access to user
gcloud secrets add-iam-policy-binding my-api-key \
    --member=user:developer@example.com \
    --role=roles/secretmanager.secretVersionManager

# Access secret
gcloud secrets versions access latest \
    --secret=my-api-key

# Access specific version
gcloud secrets versions access 2 \
    --secret=my-api-key

# List secrets
gcloud secrets list

# Describe secret
gcloud secrets describe my-api-key

# List versions
gcloud secrets versions list my-api-key

# Disable version
gcloud secrets versions disable 1 \
    --secret=my-api-key

# Enable version
gcloud secrets versions enable 1 \
    --secret=my-api-key

# Destroy version
gcloud secrets versions destroy 1 \
    --secret=my-api-key

# Update secret labels
gcloud secrets update my-api-key \
    --update-labels=version=v2

# Use in Cloud Run
gcloud run deploy my-app \
    --image=gcr.io/PROJECT_ID/my-app \
    --update-secrets=API_KEY=my-api-key:latest \
    --region=us-central1

# Use in GKE with Secret Manager add-on
kubectl create secret generic app-secrets \
    --from-literal=database-url="gcpsm://projects/PROJECT_ID/secrets/my-db-password"

# Python code to access secret
cat > access_secret.py <<EOF
from google.cloud import secretmanager

def access_secret(project_id, secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Usage
api_key = access_secret("PROJECT_ID", "my-api-key")
EOF

# Audit secret access
gcloud logging read "resource.type=secretmanager.googleapis.com/Secret" \
    --limit=50 \
    --format=json
```

---

##### Q. Set up Organization Policy constraints for security compliance?

**Answer:**
Organization Policies enforce compliance and security requirements across GCP resources.

**Steps:**
1. Define organization policies
2. Apply constraints at org/folder/project level
3. Monitor compliance

**Commands:**
```bash
# List available constraints
gcloud resource-manager org-policies list \
    --organization=ORGANIZATION_ID

# Restrict VM external IPs
cat > restrict-external-ips.yaml <<EOF
constraint: constraints/compute.vmExternalIpAccess
listPolicy:
  deniedValues:
  - "*"
EOF

gcloud resource-manager org-policies set-policy restrict-external-ips.yaml \
    --organization=ORGANIZATION_ID

# Allow specific external IPs for certain projects
cat > allow-external-ips.yaml <<EOF
constraint: constraints/compute.vmExternalIpAccess
listPolicy:
  allowedValues:
  - "projects/PROJECT_ID/zones/us-central1-a"
EOF

gcloud resource-manager org-policies set-policy allow-external-ips.yaml \
    --project=PROJECT_ID

# Require OS Login
cat > require-os-login.yaml <<EOF
constraint: constraints/compute.requireOsLogin
booleanPolicy:
  enforced: true
EOF

gcloud resource-manager org-policies set-policy require-os-login.yaml \
    --organization=ORGANIZATION_ID

# Disable service account key creation
cat > disable-sa-key-creation.yaml <<EOF
constraint: constraints/iam.disableServiceAccountKeyCreation
booleanPolicy:
  enforced: true
EOF

gcloud resource-manager org-policies set-policy disable-sa-key-creation.yaml \
    --organization=ORGANIZATION_ID

# Restrict resource locations
cat > restrict-locations.yaml <<EOF
constraint: constraints/gcp.resourceLocations
listPolicy:
  allowedValues:
  - "in:us-locations"
  - "in:eu-locations"
EOF

gcloud resource-manager org-policies set-policy restrict-locations.yaml \
    --organization=ORGANIZATION_ID

# Disable automatic IAM grants for default service accounts
cat > disable-auto-iam.yaml <<EOF
constraint: constraints/iam.automaticIamGrantsForDefaultServiceAccounts
booleanPolicy:
  enforced: true
EOF

gcloud resource-manager org-policies set-policy disable-auto-iam.yaml \
    --organization=ORGANIZATION_ID

# Restrict protocol forwarding
cat > restrict-protocol-forwarding.yaml <<EOF
constraint: constraints/compute.restrictProtocolForwardingCreationForTypes
listPolicy:
  deniedValues:
  - "EXTERNAL"
EOF

gcloud resource-manager org-policies set-policy restrict-protocol-forwarding.yaml \
    --organization=ORGANIZATION_ID

# Enforce uniform bucket-level access
cat > uniform-bucket-access.yaml <<EOF
constraint: constraints/storage.uniformBucketLevelAccess
booleanPolicy:
  enforced: true
EOF

gcloud resource-manager org-policies set-policy uniform-bucket-access.yaml \
    --organization=ORGANIZATION_ID

# Restrict shared VPC projects
cat > restrict-shared-vpc.yaml <<EOF
constraint: constraints/compute.restrictSharedVpcSubnetworks
listPolicy:
  allowedValues:
  - "projects/HOST_PROJECT_ID/regions/us-central1/subnetworks/allowed-subnet"
EOF

gcloud resource-manager org-policies set-policy restrict-shared-vpc.yaml \
    --folder=FOLDER_ID

# Get effective policy
gcloud resource-manager org-policies describe \
    constraints/compute.vmExternalIpAccess \
    --project=PROJECT_ID \
    --effective

# List all policies for organization
gcloud resource-manager org-policies list \
    --organization=ORGANIZATION_ID

# Delete policy
gcloud resource-manager org-policies delete \
    constraints/compute.vmExternalIpAccess \
    --organization=ORGANIZATION_ID
```

---

##### Q. Configure Cloud Logging and Cloud Monitoring for security event detection?

**Answer:**
Cloud Logging and Monitoring provide comprehensive visibility into security events and system health.

**Steps:**
1. Configure log sinks
2. Create log-based metrics
3. Set up alerts
4. Create monitoring dashboards

**Commands:**
```bash
# Create log sink to export to BigQuery
gcloud logging sinks create security-logs-sink \
    bigquery.googleapis.com/projects/PROJECT_ID/datasets/security_logs \
    --log-filter='protoPayload.methodName:"iam.googleapis.com" OR
                  protoPayload.authenticationInfo.principalEmail!=""'

# Create log sink to Cloud Storage
gcloud logging sinks create audit-logs-sink \
    storage.googleapis.com/audit-logs-bucket \
    --log-filter='logName:"logs/cloudaudit.googleapis.com"'

# Create log sink to Pub/Sub
gcloud logging sinks create security-events-sink \
    pubsub.googleapis.com/projects/PROJECT_ID/topics/security-events \
    --log-filter='severity>=WARNING'

# Grant necessary permissions to sink service account
PROJECT_NUMBER=$(gcloud projects describe PROJECT_ID --format="value(projectNumber)")
SINK_SA="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-logging.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding PROJECT_ID \
    --member=$SINK_SA \
    --role=roles/bigquery.dataEditor

# Create log-based metric for failed login attempts
gcloud logging metrics create failed_logins \
    --description="Count of failed login attempts" \
    --log-filter='protoPayload.methodName="google.identity.scp.v1.Login" AND
                  protoPayload.status.code!=0'

# Create log-based metric for privilege escalation
gcloud logging metrics create privilege_escalation \
    --description="IAM role binding changes" \
    --log-filter='protoPayload.methodName="SetIamPolicy" AND
                  protoPayload.serviceData.policyDelta.bindingDeltas.action="ADD" AND
                  protoPayload.serviceData.policyDelta.bindingDeltas.role:"roles/owner"' \
    --value-extractor='EXTRACT(protoPayload.authenticationInfo.principalEmail)'

# Create alerting policy for failed logins
cat > alert-policy.yaml <<EOF
displayName: "Failed Login Attempts Alert"
conditions:
  - displayName: "Failed login threshold"
    conditionThreshold:
      filter: 'metric.type="logging.googleapis.com/user/failed_logins" AND resource.type="global"'
      comparison: COMPARISON_GT
      thresholdValue: 5
      duration: 300s
      aggregations:
        - alignmentPeriod: 60s
          perSeriesAligner: ALIGN_RATE
notificationChannels:
  - projects/PROJECT_ID/notificationChannels/CHANNEL_ID
alertStrategy:
  autoClose: 604800s
EOF

gcloud alpha monitoring policies create --policy-from-file=alert-policy.yaml

# Create notification channel for email
gcloud alpha monitoring channels create \
    --display-name="Security Team Email" \
    --type=email \
    --channel-labels=email_address=security@example.com

# Create notification channel for Slack
gcloud alpha monitoring channels create \
    --display-name="Security Slack Channel" \
    --type=slack \
    --channel-labels=url=SLACK_WEBHOOK_URL

# Create uptime check for endpoint
gcloud monitoring uptime create my-https-check \
    --display-name="Website Uptime Check" \
    --resource-type=uptime-url \
    --monitored-resource=host=example.com,path=/health \
    --period=60 \
    --timeout=10

# Query logs for security events
gcloud logging read "protoPayload.methodName:SetIamPolicy" \
    --limit=50 \
    --format=json \
    --freshness=7d

# Query logs for unauthorized access attempts
gcloud logging read 'protoPayload.status.code=7 AND
                      protoPayload.authenticationInfo.principalEmail!=""' \
    --limit=50 \
    --format=json

# Query logs for data access
gcloud logging read 'protoPayload.methodName:"storage.objects.get" OR
                      protoPayload.methodName:"storage.objects.list"' \
    --limit=50 \
    --format=json

# Create custom dashboard
cat > dashboard.json <<EOF
{
  "displayName": "Security Dashboard",
  "mosaicLayout": {
    "columns": 12,
    "tiles": [
      {
        "width": 6,
        "height": 4,
        "widget": {
          "title": "Failed Login Attempts",
          "xyChart": {
            "dataSets": [{
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "metric.type=\"logging.googleapis.com/user/failed_logins\""
                }
              }
            }]
          }
        }
      }
    ]
  }
}
EOF

gcloud monitoring dashboards create --config-from-file=dashboard.json

# Export logs for analysis
gcloud logging read "resource.type=gce_instance" \
    --format=json \
    --freshness=1d > exported-logs.json

# Create log exclusion to reduce costs
gcloud logging exclusions create exclude-debug-logs \
    --log-filter='severity<WARNING'
```

---

##### Q. Implement Shared VPC for centralized network management?

**Answer:**
Shared VPC allows organization to connect resources from multiple projects to a common VPC network.

**Steps:**
1. Enable Shared VPC on host project
2. Attach service projects
3. Grant IAM permissions
4. Create resources in service projects

**Commands:**
```bash
# Enable Shared VPC on host project
gcloud compute shared-vpc enable HOST_PROJECT_ID

# Attach service project to host
gcloud compute shared-vpc associated-projects add SERVICE_PROJECT_ID \
    --host-project=HOST_PROJECT_ID

# Grant Shared VPC Admin role at organization level
gcloud organizations add-iam-policy-binding ORGANIZATION_ID \
    --member=user:admin@example.com \
    --role=roles/compute.xpnAdmin

# Grant Network User role for specific subnet
gcloud compute networks subnets add-iam-policy-binding shared-subnet \
    --project=HOST_PROJECT_ID \
    --region=us-central1 \
    --member=serviceAccount:SERVICE_PROJECT_NUMBER@cloudservices.gserviceaccount.com \
    --role=roles/compute.networkUser

# Grant Network User role for service account
gcloud projects add-iam-policy-binding HOST_PROJECT_ID \
    --member=serviceAccount:my-app@SERVICE_PROJECT_ID.iam.gserviceaccount.com \
    --role=roles/compute.networkUser

# Create instance in service project using Shared VPC
gcloud compute instances create my-instance \
    --project=SERVICE_PROJECT_ID \
    --zone=us-central1-a \
    --network=projects/HOST_PROJECT_ID/global/networks/shared-vpc \
    --subnet=projects/HOST_PROJECT_ID/regions/us-central1/subnetworks/shared-subnet

# Create GKE cluster with Shared VPC
gcloud container clusters create my-gke-cluster \
    --project=SERVICE_PROJECT_ID \
    --region=us-central1 \
    --network=projects/HOST_PROJECT_ID/global/networks/shared-vpc \
    --subnetwork=projects/HOST_PROJECT_ID/regions/us-central1/subnetworks/shared-subnet \
    --cluster-secondary-range-name=pod-range \
    --services-secondary-range-name=service-range \
    --enable-ip-alias

# List associated projects
gcloud compute shared-vpc list-associated-resources HOST_PROJECT_ID

# Get Shared VPC status
gcloud compute shared-vpc get-host-project SERVICE_PROJECT_ID

# Disable Shared VPC (must remove all associated projects first)
gcloud compute shared-vpc associated-projects remove SERVICE_PROJECT_ID \
    --host-project=HOST_PROJECT_ID

gcloud compute shared-vpc disable HOST_PROJECT_ID
```

---

##### Q. Configure Cloud Interconnect for dedicated private connectivity?

**Answer:**
Cloud Interconnect provides low-latency, highly available connections between on-premises and GCP.

**Types:**
- **Dedicated Interconnect:** Direct physical connection (10 Gbps or 100 Gbps)
- **Partner Interconnect:** Connection through supported service provider

**Steps:**
1. Create VLAN attachments
2. Configure Cloud Router
3. Establish BGP sessions
4. Verify connectivity

**Commands:**
```bash
# Create Cloud Router for Interconnect
gcloud compute routers create interconnect-router \
    --region=us-central1 \
    --network=my-vpc \
    --asn=65001

# Create Dedicated Interconnect VLAN attachment
gcloud compute interconnects attachments dedicated create my-vlan-attachment \
    --region=us-central1 \
    --router=interconnect-router \
    --interconnect=my-interconnect \
    --vlan=100

# Create Partner Interconnect VLAN attachment
gcloud compute interconnects attachments partner create my-partner-attachment \
    --region=us-central1 \
    --router=interconnect-router \
    --edge-availability-domain=AVAILABILITY_DOMAIN_1 \
    --admin-enabled

# Get pairing key for partner
gcloud compute interconnects attachments describe my-partner-attachment \
    --region=us-central1 \
    --format="get(pairingKey)"

# Configure BGP session on router
gcloud compute routers add-interface interconnect-router \
    --interface-name=if-vlan-100 \
    --interconnect-attachment=my-vlan-attachment \
    --region=us-central1

gcloud compute routers add-bgp-peer interconnect-router \
    --peer-name=bgp-peer-vlan-100 \
    --interface=if-vlan-100 \
    --peer-ip-address=169.254.100.2 \
    --peer-asn=65002 \
    --region=us-central1 \
    --advertised-route-priority=100

# Add custom route advertisements
gcloud compute routers update interconnect-router \
    --region=us-central1 \
    --advertisement-mode=CUSTOM \
    --set-advertisement-ranges=10.0.0.0/8,172.16.0.0/12

# View router status and BGP routes
gcloud compute routers get-status interconnect-router \
    --region=us-central1 \
    --format=json

# List interconnects
gcloud compute interconnects list

# List VLAN attachments
gcloud compute interconnects attachments list

# Monitor interconnect metrics
gcloud monitoring time-series list \
    --filter='metric.type="interconnect.googleapis.com/network/sent_bytes_count"' \
    --format=json

# Create redundant attachment for HA
gcloud compute interconnects attachments dedicated create my-vlan-attachment-2 \
    --region=us-central1 \
    --router=interconnect-router \
    --interconnect=my-interconnect-2 \
    --vlan=101
```

---

##### Q. Set up Network Intelligence Center for network monitoring and troubleshooting?

**Answer:**
Network Intelligence Center provides comprehensive network monitoring, topology visualization, and troubleshooting tools.

**Features:**
- Network Topology
- Connectivity Tests
- Performance Dashboard
- Firewall Insights

**Commands:**
```bash
# Enable Network Management API
gcloud services enable networkmanagement.googleapis.com

# Create connectivity test (VM to VM)
gcloud network-management connectivity-tests create vm-to-vm-test \
    --source-instance=projects/PROJECT_ID/zones/us-central1-a/instances/source-vm \
    --destination-instance=projects/PROJECT_ID/zones/us-east1-b/instances/dest-vm \
    --protocol=TCP \
    --destination-port=443

# Create connectivity test (VM to external IP)
gcloud network-management connectivity-tests create vm-to-external \
    --source-instance=projects/PROJECT_ID/zones/us-central1-a/instances/my-vm \
    --destination-ip-address=8.8.8.8 \
    --protocol=TCP \
    --destination-port=53

# Create connectivity test (VM to Google API)
gcloud network-management connectivity-tests create vm-to-google-api \
    --source-instance=projects/PROJECT_ID/zones/us-central1-a/instances/my-vm \
    --destination-network=projects/PROJECT_ID/global/networks/my-vpc \
    --destination-ip-address=storage.googleapis.com \
    --protocol=HTTPS

# Run connectivity test
gcloud network-management connectivity-tests rerun vm-to-vm-test

# Get test results
gcloud network-management connectivity-tests describe vm-to-vm-test \
    --format=json

# List all connectivity tests
gcloud network-management connectivity-tests list

# Delete connectivity test
gcloud network-management connectivity-tests delete vm-to-vm-test

# View Network Topology (use Console UI)
# https://console.cloud.google.com/net-intelligence/topology

# View Performance Dashboard
# https://console.cloud.google.com/net-intelligence/performance

# Get Firewall Insights recommendations
gcloud compute firewall-rules list \
    --format="table(
        name,
        network,
        direction,
        priority,
        sourceRanges.list():label=SRC_RANGES,
        allowed[].map().firewall_rule().list():label=ALLOW,
        denied[].map().firewall_rule().list():label=DENY,
        targetTags.list():label=TARGET_TAGS
    )"

# Analyze firewall rules for shadowed rules
# (Use Console Network Intelligence Center > Firewall Insights)

# Monitor VPC Flow Logs
gcloud compute networks subnets update my-subnet \
    --region=us-central1 \
    --enable-flow-logs \
    --logging-aggregation-interval=interval-5-sec \
    --logging-flow-sampling=0.5 \
    --logging-metadata=include-all

# Query VPC Flow Logs
gcloud logging read "resource.type=gce_subnetwork AND
                      logName:compute.googleapis.com%2Fvpc_flows" \
    --limit=50 \
    --format=json

# Create metric from VPC Flow Logs
gcloud logging metrics create vpc_traffic_volume \
    --description="VPC traffic volume" \
    --log-filter='resource.type="gce_subnetwork"
                  logName:"vpc_flows"' \
    --value-extractor='EXTRACT(jsonPayload.bytes_sent)'
```

---

##### Q. Configure Packet Mirroring for network traffic analysis?

**Answer:**
Packet Mirroring clones traffic of specified instances and forwards it to collector instances for analysis, security monitoring, and troubleshooting.

**Steps:**
1. Create collector instance or load balancer
2. Create packet mirroring policy
3. Apply policy to instances or subnets
4. Analyze mirrored traffic

**Commands:**
```bash
# Create collector instance
gcloud compute instances create packet-collector \
    --zone=us-central1-a \
    --machine-type=n2-standard-4 \
    --network=my-vpc \
    --subnet=collector-subnet \
    --can-ip-forward \
    --tags=packet-collector

# Create internal load balancer as collector
gcloud compute forwarding-rules create packet-collector-lb \
    --region=us-central1 \
    --load-balancing-scheme=INTERNAL \
    --network=my-vpc \
    --subnet=collector-subnet \
    --ip-protocol=TCP \
    --ports=ALL \
    --backend-service=collector-backend-service

# Create packet mirroring policy
gcloud compute packet-mirrorings create my-mirroring-policy \
    --region=us-central1 \
    --network=my-vpc \
    --collector-ilb=packet-collector-lb \
    --mirrored-subnets=monitored-subnet \
    --filter-cidr-ranges=0.0.0.0/0 \
    --filter-protocols=tcp,udp,icmp

# Mirror specific instances
gcloud compute packet-mirrorings create instance-mirroring \
    --region=us-central1 \
    --network=my-vpc \
    --collector-ilb=packet-collector-lb \
    --mirrored-instances=instance-1,instance-2 \
    --filter-protocols=tcp \
    --filter-direction=INGRESS

# Mirror with specific tags
gcloud compute packet-mirrorings create tag-based-mirroring \
    --region=us-central1 \
    --network=my-vpc \
    --collector-ilb=packet-collector-lb \
    --mirrored-tags=web-server,app-server

# Update mirroring policy
gcloud compute packet-mirrorings update my-mirroring-policy \
    --region=us-central1 \
    --add-mirrored-instances=instance-3

# Enable/Disable mirroring
gcloud compute packet-mirrorings update my-mirroring-policy \
    --region=us-central1 \
    --no-enable

gcloud compute packet-mirrorings update my-mirroring-policy \
    --region=us-central1 \
    --enable

# List packet mirroring policies
gcloud compute packet-mirrorings list

# Describe mirroring policy
gcloud compute packet-mirrorings describe my-mirroring-policy \
    --region=us-central1

# Delete mirroring policy
gcloud compute packet-mirrorings delete my-mirroring-policy \
    --region=us-central1

# Install traffic analysis tools on collector
sudo apt-get update
sudo apt-get install -y tcpdump wireshark-common tshark

# Capture mirrored traffic
sudo tcpdump -i eth0 -w captured-traffic.pcap

# Analyze with tshark
tshark -r captured-traffic.pcap -q -z io,stat,1
```

---

##### Q. Implement Security Command Center for centralized security management?

**Answer:**
Security Command Center (SCC) provides centralized visibility into security and compliance across GCP resources.

**Features:**
- Asset inventory and discovery
- Vulnerability scanning
- Threat detection
- Compliance monitoring

**Commands:**
```bash
# Enable Security Command Center API
gcloud services enable securitycenter.googleapis.com

# Grant SCC admin role
gcloud organizations add-iam-policy-binding ORGANIZATION_ID \
    --member=user:security-admin@example.com \
    --role=roles/securitycenter.admin

# List all findings
gcloud scc findings list ORGANIZATION_ID \
    --source=SOURCE_ID

# List findings by category
gcloud scc findings list ORGANIZATION_ID \
    --source=SOURCE_ID \
    --filter="category=\"OPEN_FIREWALL\""

# List high severity findings
gcloud scc findings list ORGANIZATION_ID \
    --source=SOURCE_ID \
    --filter="severity=\"HIGH\""

# List findings for specific project
gcloud scc findings list ORGANIZATION_ID \
    --source=SOURCE_ID \
    --filter="resourceName:\"projects/PROJECT_ID\""

# Update finding state
gcloud scc findings update FINDING_ID \
    --organization=ORGANIZATION_ID \
    --source=SOURCE_ID \
    --state=INACTIVE

# Create finding
gcloud scc findings create FINDING_ID \
    --organization=ORGANIZATION_ID \
    --source=SOURCE_ID \
    --category=CUSTOM_FINDING \
    --resource-name=//compute.googleapis.com/projects/PROJECT_ID/zones/us-central1-a/instances/my-instance \
    --event-time=2024-01-01T00:00:00Z \
    --state=ACTIVE

# List assets
gcloud scc assets list ORGANIZATION_ID \
    --filter="securityCenterProperties.resourceType=\"google.compute.Instance\""

# Get asset details
gcloud scc assets describe ASSET_ID \
    --organization=ORGANIZATION_ID

# List sources
gcloud scc sources list ORGANIZATION_ID

# Create notification config
gcloud scc notifications create my-notification \
    --organization=ORGANIZATION_ID \
    --description="High severity findings" \
    --pubsub-topic=projects/PROJECT_ID/topics/security-notifications \
    --filter="severity=\"HIGH\" OR severity=\"CRITICAL\""

# Update notification
gcloud scc notifications update my-notification \
    --organization=ORGANIZATION_ID \
    --description="Updated notification" \
    --filter="category=\"OPEN_FIREWALL\" OR category=\"WEAK_PASSWORD\""

# Delete notification
gcloud scc notifications delete my-notification \
    --organization=ORGANIZATION_ID

# Export findings to BigQuery
gcloud scc bqexports create my-export \
    --organization=ORGANIZATION_ID \
    --dataset=projects/PROJECT_ID/datasets/security_findings \
    --description="Export all findings" \
    --filter="state=\"ACTIVE\""

# Monitor using Cloud Monitoring
gcloud alpha monitoring policies create \
    --notification-channels=CHANNEL_ID \
    --display-name="SCC Critical Findings" \
    --condition-display-name="Critical findings threshold" \
    --condition-threshold-value=1 \
    --condition-threshold-duration=0s \
    --condition-filter='resource.type="scc.googleapis.com/Finding" AND severity="CRITICAL"'
```

---

### Theoretical Concepts & Design Patterns

##### Q. When would you choose Cloud Interconnect over Cloud VPN, and what are the trade-offs?

**Answer:**
This is actually a question I get asked a lot in real-world scenarios. The choice really depends on your bandwidth requirements, latency sensitivity, and budget.

I'd recommend Cloud Interconnect when you're dealing with large-scale data transfers or latency-critical applications. For example, if you're migrating terabytes of data regularly or running real-time analytics workloads that can't tolerate the variable latency of internet-based VPN, Interconnect is the way to go. It gives you dedicated 10 Gbps or 100 Gbps circuits with consistent performance.

On the other hand, Cloud VPN is perfect for smaller workloads or when you're just starting out. It's much easier to set up - you can have it running in under an hour - and the costs are predictable. I've used it successfully for hybrid cloud setups where we needed to connect a handful of on-premises servers to GCP for disaster recovery.

The main trade-offs are:
- **Cost:** Interconnect requires a significant upfront investment and monthly charges, while VPN is pay-as-you-go
- **Bandwidth:** Interconnect offers much higher throughput (10-100 Gbps vs VPN's 3 Gbps per tunnel)
- **Latency:** Interconnect provides consistent low latency since it doesn't go over the public internet
- **Setup time:** VPN can be configured in minutes, while Interconnect takes weeks to provision

In my experience, most organizations start with VPN and migrate to Interconnect as their cloud footprint grows. You can also use both - VPN as a backup for Interconnect to ensure redundancy.

---

##### Q. Explain the concept of Shared VPC and when you should use it versus VPC Peering?

**Answer:**
Shared VPC and VPC Peering solve different organizational challenges, and I've implemented both in various enterprise environments.

Shared VPC is really about centralized management and administration. Think of it as having a central networking team that manages all the network infrastructure, while different application teams can use those networks without having admin access. It's perfect for large organizations with strict security and governance requirements.

For instance, in my previous project with a financial services organization, we used Shared VPC where the network security team owned the host project with all the VPC networks, firewall rules, and routing. Individual business units had service projects where they deployed their applications. This way, developers couldn't accidentally misconfigure firewall rules or create security holes, but they still had the flexibility to deploy resources.

VPC Peering, on the other hand, is about connecting independent networks. Use it when you have separate organizations or teams that need to maintain their own network administration but still need private connectivity. I've used this when connecting a customer's VPC to our SaaS platform's VPC - both parties maintain full control over their own networks.

Key differences:
- **Administration:** Shared VPC centralizes control; Peering keeps networks independent
- **IAM:** With Shared VPC, you can grant granular permissions at the subnet level; Peering is all-or-nothing at the network level
- **Quotas:** Shared VPC shares quotas across projects; Peering keeps them separate
- **Pricing:** Shared VPC traffic is considered internal; Peering has egress charges

Bottom line: Use Shared VPC for centralized governance within your organization, and VPC Peering when connecting separate entities that need to maintain independence.

---

##### Q. How do you design a multi-region GCP architecture for high availability and disaster recovery?

**Answer:**
Designing for multi-region HA and DR in GCP is something I'm really passionate about because I've seen both successful implementations and costly failures.

The first thing I always tell people is to distinguish between high availability (handling failures gracefully) and disaster recovery (recovering from catastrophic events). They require different strategies.

For high availability, I typically design with at least two regions - primary and secondary. Here's my approach:

**Compute Layer:**
- Use regional managed instance groups (MIGs) that span multiple zones within a region
- Set up Global Load Balancer to distribute traffic across regions
- Implement health checks that automatically route traffic away from unhealthy instances or entire regions
- I usually aim for N+1 redundancy at minimum, N+2 for critical workloads

**Data Layer:**
This is where it gets interesting. You have to balance between consistency and availability:
- For databases, I use Cloud Spanner for globally distributed relational data with strong consistency
- Cloud SQL with cross-region read replicas for read-heavy workloads
- Firestore in Datastore mode for flexible, multi-region NoSQL
- Regular automated backups with versioning, stored in multi-region Cloud Storage buckets

**Network Layer:**
- Deploy Cloud Armor at the edge for DDoS protection
- Use Cloud CDN to cache content closer to users
- Implement Cloud DNS with low TTL values for quick failover
- Set up VPN or Interconnect in multiple regions for hybrid connectivity

**Disaster Recovery Strategy:**
I follow the RPO (Recovery Point Objective) and RTO (Recovery Time Objective) framework:
- **RPO < 1 hour:** Continuous replication using tools like Actifio or native replication
- **RTO < 15 minutes:** Active-active multi-region setup with automated failover
- Regular DR drills - I schedule these quarterly because theoretical plans often fail in practice

One lesson I learned the hard way: always test your failover procedures. In one incident, we had perfect replication, but the failover took 4 hours instead of 15 minutes because DNS propagation wasn't properly configured.

Also, don't forget about data egress costs - they can be significant in multi-region setups. I've seen bills skyrocket when teams didn't account for cross-region data transfer.

---

##### Q. What are the security best practices for managing service accounts in GCP, and how do you prevent privilege escalation?

**Answer:**
Service account security is one of those areas where small mistakes can have huge consequences. I've had to clean up after incidents where overly permissive service accounts were compromised, so I'm pretty strict about this now.

**Principle of Least Privilege:**
This is non-negotiable. Every service account should have exactly the permissions it needs - nothing more. I never use primitive roles like Owner, Editor, or Viewer in production. Instead, I create custom roles tailored to specific functions.

For example, if a Cloud Run service only needs to read from Cloud Storage, I grant it `roles/storage.objectViewer` on specific buckets, not `roles/storage.admin` across the entire project.

**Key Management:**
Here's my controversial take: I avoid service account keys whenever possible. They're essentially long-lived credentials that can be stolen or leaked. Instead, I use:
- Workload Identity for GKE - this is a game changer
- Service Account impersonation for admin tasks
- Default service accounts with IAM bindings for Compute Engine and Cloud Run

When keys are absolutely necessary (like for on-premises applications), I rotate them every 90 days and store them in Secret Manager, never in code repositories or environment variables in plain text.

**Preventing Privilege Escalation:**
This requires multiple layers of defense:

1. **Organization Policies:** I enable `constraints/iam.disableServiceAccountKeyCreation` to prevent developers from creating keys
2. **IAM Conditions:** Use time-based or IP-based restrictions on sensitive permissions
3. **Service Account Separation:** Never reuse service accounts across environments (dev/staging/prod)
4. **Audit Logging:** Monitor for suspicious activities like `iam.serviceAccounts.actAs` or `iam.serviceAccountKeys.create`

I also implement the "break glass" pattern for emergency access. Instead of giving people broad permissions, I have a documented process for temporary privilege elevation that's automatically logged and reviewed.

**Real-world example:**
In one organization, A developer with `roles/iam.serviceAccountUser` on a highly privileged service account could essentially impersonate that account and gain admin access. We caught it during a security review and implemented conditional IAM policies that restricted impersonation to specific IP ranges and working hours.

The key is continuous monitoring. I set up Cloud Monitoring alerts for any service account permission changes and review Cloud Asset Inventory reports monthly to catch permission creep.

---

##### Q. How does VPC Service Controls differ from firewall rules, and when would you use one over the other?

**Answer:**
This is a great question because people often confuse these two security mechanisms, but they work at completely different layers and solve different problems.

**Firewall Rules** are network-layer controls. They work at the IP and port level - basically allowing or denying traffic based on source/destination IPs, protocols, and ports. Think of them as your traditional network security that's been around forever. They're perfect for:
- Controlling ingress/egress traffic to VMs
- Segmenting your network (like preventing dev VMs from talking to production)
- Allowing only specific IP ranges to access your infrastructure

**VPC Service Controls** operate at the API/service layer. They create security perimeters around Google Cloud services like Cloud Storage, BigQuery, or Cloud SQL. This is data exfiltration prevention - ensuring that even if someone has valid credentials, they can't access resources from unauthorized networks or locations.

Here's where it clicked for me: Firewall rules protect your VMs and network traffic. VPC Service Controls protect your data in managed services.

**Real-world scenario:**
Imagine an employee's laptop gets compromised, and an attacker gains access to their GCP credentials. With just firewall rules:
- The attacker could still access Cloud Storage buckets from anywhere in the world
- An insider could copy sensitive data from BigQuery to an external project
- An attacker could exfiltrate data through legitimate API calls

With VPC Service Controls in place:
- Access to protected services is limited to authorized VPC networks or on-premises networks
- Data can't be copied to projects outside the security perimeter
- Even with valid credentials, the attacker can't access resources from their location

**When to use what:**

I use **Firewall Rules** for:
- VM-to-VM communication control
- Allowing/blocking specific ports and protocols
- Traditional network segmentation
- Quick, granular traffic control

I use **VPC Service Controls** for:
- Protecting sensitive data in managed services (GCS, BQ, Cloud SQL)
- Compliance requirements (PCI-DSS, HIPAA, GDPR)
- Preventing data exfiltration and unauthorized data access
- Creating secure perimeters around critical resources

**In practice, I use both together.** For a healthcare application I worked on:
- Firewall rules controlled access to application servers and databases
- VPC Service Controls created a perimeter around all PHI data in Cloud Storage and BigQuery
- This layered approach meant that even if one control failed, we had defense in depth

One caveat: VPC Service Controls can be tricky to implement because they're quite restrictive by default. I always recommend starting with dry-run mode to see what would be blocked before enforcing the policies. I've seen organizations lock themselves out of their own resources by applying too-restrictive policies without testing first!

---

### MLOps, AIOps, Data Engineering & Security

##### Q. How do you implement an end-to-end MLOps pipeline on GCP using Vertex AI with automated retraining?

**Answer:**
Vertex AI Pipelines provides a comprehensive MLOps platform on GCP for building, deploying, and managing ML models at scale.

**Architecture Components:**
1. **Vertex AI Workbench** - Managed Jupyter notebooks
2. **Vertex AI Pipelines** - Kubeflow-based orchestration
3. **Vertex AI Feature Store** - Centralized feature management
4. **Vertex AI Model Registry** - Versioned model storage
5. **Vertex AI Endpoints** - Managed model serving
6. **Cloud Build** - CI/CD automation
7. **Cloud Composer (Airflow)** - Workflow orchestration

**Implementation:**

```python
# vertex_mlops_pipeline.py
from google.cloud import aiplatform
from kfp.v2 import dsl, compiler
from kfp.v2.dsl import component, pipeline, Input, Output, Dataset, Model, Metrics
from typing import NamedTuple

# Initialize Vertex AI
aiplatform.init(
    project='my-project',
    location='us-central1',
    staging_bucket='gs://mlops-staging'
)

# Define pipeline components
@component(
    base_image='python:3.9',
    packages_to_install=['pandas', 'scikit-learn', 'google-cloud-aiplatform']
)
def load_data(
    dataset_name: str,
    output_dataset: Output[Dataset]
):
    """Load training data from BigQuery"""
    from google.cloud import bigquery
    import pandas as pd
    
    client = bigquery.Client()
    
    query = f"""
        SELECT 
            customer_id,
            age,
            tenure_months,
            monthly_charges,
            total_charges,
            churn_label
        FROM `{dataset_name}`
        WHERE partition_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
    """
    
    df = client.query(query).to_dataframe()
    
    # Save dataset
    df.to_csv(output_dataset.path, index=False)
    
    print(f"Loaded {len(df)} records")

@component(
    base_image='python:3.9',
    packages_to_install=['pandas', 'great-expectations']
)
def validate_data(
    input_dataset: Input[Dataset],
    validation_report: Output[Metrics]
) -> NamedTuple('Outputs', [('is_valid', bool), ('quality_score', float)]):
    """Validate data quality with Great Expectations"""
    import pandas as pd
    import great_expectations as ge
    
    df = pd.read_csv(input_dataset.path)
    ge_df = ge.from_pandas(df)
    
    # Define expectations
    results = []
    results.append(ge_df.expect_column_values_to_not_be_null('customer_id'))
    results.append(ge_df.expect_column_values_to_be_between('age', 18, 100))
    results.append(ge_df.expect_column_values_to_be_between('monthly_charges', 0, 10000))
    
    # Calculate quality score
    successful = sum([1 for r in results if r.success])
    quality_score = successful / len(results)
    
    validation_report.log_metric('quality_score', quality_score)
    validation_report.log_metric('total_checks', len(results))
    validation_report.log_metric('passed_checks', successful)
    
    from collections import namedtuple
    output = namedtuple('Outputs', ['is_valid', 'quality_score'])
    return output(quality_score >= 0.95, quality_score)

@component(
    base_image='gcr.io/deeplearning-platform-release/sklearn-cpu.0-24',
    packages_to_install=['google-cloud-aiplatform']
)
def train_model(
    input_dataset: Input[Dataset],
    model: Output[Model],
    metrics: Output[Metrics],
    learning_rate: float = 0.01,
    n_estimators: int = 100
):
    """Train ML model with hyperparameter tuning"""
    import pandas as pd
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    import pickle
    
    # Load data
    df = pd.read_csv(input_dataset.path)
    
    # Prepare features
    X = df[['age', 'tenure_months', 'monthly_charges', 'total_charges']]
    y = df['churn_label']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train model
    clf = GradientBoostingClassifier(
        learning_rate=learning_rate,
        n_estimators=n_estimators,
        random_state=42
    )
    clf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = clf.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    # Log metrics
    metrics.log_metric('accuracy', accuracy)
    metrics.log_metric('precision', precision)
    metrics.log_metric('recall', recall)
    metrics.log_metric('f1_score', f1)
    
    # Save model
    with open(model.path, 'wb') as f:
        pickle.dump(clf, f)
    
    print(f"Model trained - Accuracy: {accuracy:.4f}, F1: {f1:.4f}")

@component(
    base_image='python:3.9',
    packages_to_install=['google-cloud-aiplatform']
)
def register_model(
    model: Input[Model],
    accuracy: float,
    model_name: str = 'churn-predictor'
) -> str:
    """Register model in Vertex AI Model Registry"""
    from google.cloud import aiplatform
    
    aiplatform.init(project='my-project', location='us-central1')
    
    # Upload model
    uploaded_model = aiplatform.Model.upload(
        display_name=model_name,
        artifact_uri=model.uri,
        serving_container_image_uri='us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.0-24:latest',
        labels={'accuracy': str(accuracy), 'framework': 'sklearn'}
    )
    
    return uploaded_model.resource_name

@component(
    base_image='python:3.9',
    packages_to_install=['google-cloud-aiplatform']
)
def deploy_model(
    model_resource_name: str,
    endpoint_name: str = 'churn-prediction-endpoint',
    traffic_split: int = 100
):
    """Deploy model to Vertex AI endpoint with traffic splitting"""
    from google.cloud import aiplatform
    
    aiplatform.init(project='my-project', location='us-central1')
    
    # Get or create endpoint
    endpoints = aiplatform.Endpoint.list(
        filter=f'display_name="{endpoint_name}"'
    )
    
    if endpoints:
        endpoint = endpoints[0]
        print(f"Using existing endpoint: {endpoint.resource_name}")
    else:
        endpoint = aiplatform.Endpoint.create(display_name=endpoint_name)
        print(f"Created new endpoint: {endpoint.resource_name}")
    
    # Get model
    model = aiplatform.Model(model_resource_name)
    
    # Deploy with traffic splitting (blue-green deployment)
    deployed_model = endpoint.deploy(
        model=model,
        deployed_model_display_name=f'deployment-{model.version_id}',
        machine_type='n1-standard-4',
        min_replica_count=1,
        max_replica_count=5,
        traffic_percentage=traffic_split,
        sync=True
    )
    
    print(f"Model deployed: {deployed_model}")

# Define complete MLOps pipeline
@pipeline(
    name='churn-prediction-mlops',
    description='End-to-end MLOps pipeline with validation and deployment'
)
def mlops_pipeline(
    dataset_name: str = 'my-project.customer_data.transactions',
    model_name: str = 'churn-predictor',
    min_accuracy: float = 0.85
):
    """Complete MLOps pipeline"""
    
    # Step 1: Load data
    load_data_task = load_data(dataset_name=dataset_name)
    
    # Step 2: Validate data quality
    validate_task = validate_data(input_dataset=load_data_task.outputs['output_dataset'])
    
    # Step 3: Train model (conditional on data quality)
    with dsl.Condition(
        validate_task.outputs['is_valid'] == True,
        name='data-quality-passed'
    ):
        train_task = train_model(input_dataset=load_data_task.outputs['output_dataset'])
        
        # Step 4: Register model (conditional on accuracy)
        with dsl.Condition(
            train_task.outputs['metrics'].metadata['accuracy'] >= min_accuracy,
            name='accuracy-threshold-met'
        ):
            register_task = register_model(
                model=train_task.outputs['model'],
                accuracy=train_task.outputs['metrics'].metadata['accuracy'],
                model_name=model_name
            )
            
            # Step 5: Deploy model
            deploy_task = deploy_model(
                model_resource_name=register_task.output,
                endpoint_name=f'{model_name}-endpoint'
            )

# Compile pipeline
compiler.Compiler().compile(
    pipeline_func=mlops_pipeline,
    package_path='churn_mlops_pipeline.json'
)

# Run pipeline
job = aiplatform.PipelineJob(
    display_name='churn-mlops-pipeline',
    template_path='churn_mlops_pipeline.json',
    pipeline_root='gs://mlops-staging/pipeline-runs',
    parameter_values={
        'dataset_name': 'my-project.customer_data.transactions',
        'model_name': 'churn-predictor',
        'min_accuracy': 0.85
    },
    enable_caching=True
)

job.run(sync=True)
```

**Automated Retraining with Cloud Scheduler:**

```python
# monitoring_and_retraining.py
from google.cloud import aiplatform, monitoring_v3
import json

def setup_model_monitoring():
    """Configure model monitoring for drift detection"""
    
    # Create monitoring job
    monitoring_job_config = {
        "displayName": "churn-model-monitoring",
        "modelMonitoringObjectiveConfig": {
            "trainingDataset": {
                "bigquerySource": {
                    "inputUri": "bq://my-project.customer_data.training_baseline"
                }
            },
            "trainingPredictionSkewDetectionConfig": {
                "skewThresholds": {
                    "age": {"value": 0.3},
                    "monthly_charges": {"value": 0.3},
                    "tenure_months": {"value": 0.3}
                }
            },
            "predictionDriftDetectionConfig": {
                "driftThresholds": {
                    "age": {"value": 0.3},
                    "monthly_charges": {"value": 0.3}
                }
            }
        },
        "modelMonitoringAlertConfig": {
            "emailAlertConfig": {
                "userEmails": ["ml-team@example.com"]
            },
            "enableLogging": True
        },
        "loggingSamplingStrategy": {
            "randomSampleConfig": {"sampleRate": 0.8}
        },
        "schedule": {
            "cron": "0 */12 * * *"  # Every 12 hours
        }
    }
    
    return monitoring_job_config

def trigger_retraining_on_drift():
    """Cloud Function to trigger retraining on drift detection"""
    
    def retraining_trigger(event, context):
        """Triggered by Pub/Sub message from model monitoring"""
        import base64
        
        # Parse monitoring alert
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        alert_data = json.loads(pubsub_message)
        
        drift_detected = alert_data.get('driftDetected', False)
        drift_score = alert_data.get('driftScore', 0)
        
        if drift_detected and drift_score > 0.3:
            print(f"Drift detected with score {drift_score}, triggering retraining")
            
            # Trigger pipeline
            job = aiplatform.PipelineJob(
                display_name='automated-retraining',
                template_path='gs://mlops-staging/churn_mlops_pipeline.json',
                pipeline_root='gs://mlops-staging/pipeline-runs',
                parameter_values={
                    'dataset_name': 'my-project.customer_data.transactions',
                    'model_name': 'churn-predictor',
                    'min_accuracy': 0.85
                }
            )
            
            job.submit()
            
            return {'status': 'retraining_triggered', 'job_id': job.resource_name}
        
        return {'status': 'no_action_needed'}
    
    return retraining_trigger
```

**Cloud Build CI/CD Pipeline:**

```yaml
# cloudbuild.yaml
steps:
  # Step 1: Run unit tests
  - name: 'python:3.9'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        pip install pytest pandas scikit-learn
        pytest tests/ -v

  # Step 2: Build training container
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - 'gcr.io/$PROJECT_ID/churn-trainer:$SHORT_SHA'
      - '-f'
      - 'Dockerfile.training'
      - '.'

  # Step 3: Push container
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - 'gcr.io/$PROJECT_ID/churn-trainer:$SHORT_SHA'

  # Step 4: Compile pipeline
  - name: 'python:3.9'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        pip install kfp google-cloud-aiplatform
        python compile_pipeline.py

  # Step 5: Deploy to staging
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        gcloud ai custom-jobs create \
          --region=us-central1 \
          --display-name=pipeline-validation-$SHORT_SHA \
          --config=pipeline_config.yaml

  # Step 6: Run integration tests
  - name: 'python:3.9'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        pip install google-cloud-aiplatform requests
        python tests/integration_tests.py --endpoint staging-endpoint

  # Step 7: Deploy to production (on main branch)
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        if [ "$BRANCH_NAME" = "main" ]; then
          python deploy_production.py --traffic-split 10
        fi

options:
  logging: CLOUD_LOGGING_ONLY
  machineType: 'N1_HIGHCPU_8'

timeout: '1800s'
```

**Key Features:**
- Automated data quality validation with Great Expectations
- Conditional pipeline execution based on metrics
- Model versioning and registry integration
- Blue-green deployment with traffic splitting
- Drift detection and automated retraining
- CI/CD with Cloud Build
- Comprehensive monitoring and alerting

---

##### Q. How do you implement AIOps for predictive incident detection on GCP using Cloud Operations?

**Answer:**
AIOps on GCP leverages Cloud Operations Suite (formerly Stackdriver) with machine learning for proactive incident detection and automated remediation.

**Architecture:**
1. **Cloud Logging** - Centralized log aggregation
2. **Cloud Monitoring** - Metrics and alerting
3. **Cloud Trace** - Distributed tracing
4. **Cloud Profiler** - Performance profiling
5. **Error Reporting** - Error tracking
6. **BigQuery** - Log analytics
7. **Vertex AI** - Anomaly detection models

**Implementation:**

```python
# aiops_anomaly_detection.py
from google.cloud import logging_v2, monitoring_v3, bigquery
from google.cloud import aiplatform
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta

class GCPAIOps:
    """AIOps implementation for GCP infrastructure"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.logging_client = logging_v2.Client(project=project_id)
        self.monitoring_client = monitoring_v3.MetricServiceClient()
        self.bq_client = bigquery.Client(project=project_id)
        
    def setup_log_based_metrics(self):
        """Create log-based metrics for anomaly detection"""
        
        # Create metric for error rate
        metric_descriptor = {
            "type": f"logging.googleapis.com/user/error_rate",
            "metric_kind": monitoring_v3.MetricDescriptor.MetricKind.GAUGE,
            "value_type": monitoring_v3.MetricDescriptor.ValueType.DOUBLE,
            "description": "Application error rate per minute",
            "display_name": "Error Rate"
        }
        
        # Create log sink to BigQuery for ML analysis
        sink_name = f"projects/{self.project_id}/sinks/aiops-analysis"
        destination = f"bigquery.googleapis.com/projects/{self.project_id}/datasets/aiops_logs"
        
        log_filter = '''
        severity >= ERROR
        OR resource.type = "gce_instance"
        OR resource.type = "k8s_cluster"
        OR protoPayload.status.code != 0
        '''
        
        sink = self.logging_client.sink(sink_name, filter_=log_filter, destination=destination)
        
        if not sink.exists():
            sink.create()
            print(f"Created log sink: {sink_name}")
        
        return sink
    
    def collect_metrics_for_training(self, days: int = 30):
        """Collect historical metrics for anomaly detection model"""
        
        query = f"""
        SELECT
            TIMESTAMP_TRUNC(timestamp, MINUTE) as time_bucket,
            resource.type as resource_type,
            resource.labels.instance_id as instance_id,
            
            -- CPU metrics
            AVG(IF(metric.type = 'compute.googleapis.com/instance/cpu/utilization',
                metric.value, NULL)) as cpu_utilization,
            
            -- Memory metrics
            AVG(IF(metric.type = 'compute.googleapis.com/instance/memory/used_bytes',
                metric.value, NULL)) as memory_used,
            
            -- Network metrics
            SUM(IF(metric.type = 'compute.googleapis.com/instance/network/received_bytes_count',
                metric.value, NULL)) as network_rx_bytes,
            SUM(IF(metric.type = 'compute.googleapis.com/instance/network/sent_bytes_count',
                metric.value, NULL)) as network_tx_bytes,
            
            -- Disk metrics
            AVG(IF(metric.type = 'compute.googleapis.com/instance/disk/write_ops_count',
                metric.value, NULL)) as disk_write_ops,
            AVG(IF(metric.type = 'compute.googleapis.com/instance/disk/read_ops_count',
                metric.value, NULL)) as disk_read_ops,
            
            -- Error count from logs
            COUNTIF(severity = 'ERROR') as error_count,
            COUNTIF(severity = 'WARNING') as warning_count
            
        FROM `{self.project_id}.aiops_logs.compute_googleapis_com_*`
        WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {days} DAY)
        GROUP BY time_bucket, resource_type, instance_id
        ORDER BY time_bucket DESC
        """
        
        df = self.bq_client.query(query).to_dataframe()
        return df
    
    def train_anomaly_detector(self):
        """Train ML model for anomaly detection"""
        
        # Collect training data
        df = self.collect_metrics_for_training(days=90)
        
        # Feature engineering
        features = [
            'cpu_utilization',
            'memory_used',
            'network_rx_bytes',
            'network_tx_bytes',
            'disk_write_ops',
            'disk_read_ops',
            'error_count',
            'warning_count'
        ]
        
        # Fill missing values
        df[features] = df[features].fillna(0)
        
        # Add temporal features
        df['hour'] = pd.to_datetime(df['time_bucket']).dt.hour
        df['day_of_week'] = pd.to_datetime(df['time_bucket']).dt.dayofweek
        
        features.extend(['hour', 'day_of_week'])
        
        # Train Isolation Forest for anomaly detection
        X = df[features].values
        
        model = IsolationForest(
            contamination=0.1,  # Expect 10% anomalies
            random_state=42,
            n_estimators=100
        )
        model.fit(X)
        
        # Save model to Vertex AI
        import pickle
        with open('anomaly_detector.pkl', 'wb') as f:
            pickle.dump(model, f)
        
        # Upload to Vertex AI Model Registry
        aiplatform.init(project=self.project_id, location='us-central1')
        
        uploaded_model = aiplatform.Model.upload(
            display_name='infrastructure-anomaly-detector',
            artifact_uri='gs://aiops-models/anomaly_detector.pkl',
            serving_container_image_uri='us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.0-24:latest'
        )
        
        return uploaded_model
    
    def predict_anomalies_realtime(self):
        """Real-time anomaly detection on streaming metrics"""
        
        # Get current metrics
        now = datetime.utcnow()
        interval = monitoring_v3.TimeInterval({
            'end_time': {'seconds': int(now.timestamp())},
            'start_time': {'seconds': int((now - timedelta(minutes=5)).timestamp())}
        })
        
        # Query multiple metrics
        results = self.monitoring_client.list_time_series(
            request={
                'name': f'projects/{self.project_id}',
                'filter': 'resource.type = "gce_instance"',
                'interval': interval,
                'view': monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
            }
        )
        
        anomalies = []
        
        for result in results:
            # Extract metrics
            for point in result.points:
                # Call Vertex AI model for prediction
                # If anomaly score high, trigger alert
                
                if self.is_anomalous(point.value):
                    anomalies.append({
                        'resource': result.resource.labels,
                        'metric': result.metric.type,
                        'value': point.value.double_value,
                        'timestamp': point.interval.end_time
                    })
        
        return anomalies
    
    def automated_remediation(self, anomaly):
        """Automated incident remediation"""
        
        from googleapiclient import discovery
        
        compute = discovery.build('compute', 'v1')
        
        resource_type = anomaly['resource'].get('resource_type')
        instance_name = anomaly['resource'].get('instance_id')
        zone = anomaly['resource'].get('zone')
        
        # Determine remediation action
        if anomaly['metric'] == 'cpu_utilization' and anomaly['value'] > 90:
            # High CPU - restart instance
            print(f"High CPU detected on {instance_name}, restarting...")
            
            # Take snapshot first
            snapshot_body = {
                'name': f'{instance_name}-snapshot-{int(datetime.now().timestamp())}',
                'sourceDisk': f'zones/{zone}/disks/{instance_name}'
            }
            
            compute.disks().createSnapshot(
                project=self.project_id,
                zone=zone,
                disk=instance_name,
                body=snapshot_body
            ).execute()
            
            # Restart instance
            compute.instances().reset(
                project=self.project_id,
                zone=zone,
                instance=instance_name
            ).execute()
            
            return {'action': 'instance_restarted', 'instance': instance_name}
        
        elif anomaly['metric'] == 'error_count' and anomaly['value'] > 100:
            # High error rate - scale up
            print(f"High error rate detected, scaling up...")
            
            # Trigger autoscaler
            # This would integrate with GKE or Instance Groups
            
            return {'action': 'scaled_up', 'reason': 'high_error_rate'}
        
        return {'action': 'alert_only', 'reason': 'no_automation_defined'}
    
    def setup_slo_monitoring(self):
        """Configure SLO-based alerting"""
        
        # Create SLO for API availability
        slo_config = {
            "displayName": "API Availability SLO",
            "serviceLevelIndicator": {
                "requestBased": {
                    "goodTotalRatio": {
                        "goodServiceFilter": 'metric.type="loadbalancing.googleapis.com/https/request_count" AND metric.response_code_class="2xx"',
                        "totalServiceFilter": 'metric.type="loadbalancing.googleapis.com/https/request_count"'
                    }
                }
            },
            "goal": 0.995,  # 99.5% availability
            "rollingPeriod": "2592000s"  # 30 days
        }
        
        return slo_config

# Deploy as Cloud Function for continuous monitoring
def aiops_monitor(event, context):
    """Cloud Function triggered every 5 minutes"""
    
    aiops = GCPAIOps(project_id='my-project')
    
    # Detect anomalies
    anomalies = aiops.predict_anomalies_realtime()
    
    # Remediate automatically
    for anomaly in anomalies:
        result = aiops.automated_remediation(anomaly)
        print(f"Remediation result: {result}")
    
    return {'anomalies_detected': len(anomalies)}
```

**Cloud Function for Intelligent Alerting:**

```python
# intelligent_alerting.py
from google.cloud import logging_v2, monitoring_v3
import json

def intelligent_alert_routing(event, context):
    """Route alerts based on ML-predicted severity and context"""
    
    import base64
    alert_data = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    
    # Extract alert details
    incident = alert_data.get('incident', {})
    severity = incident.get('severity', 'UNKNOWN')
    resource = incident.get('resource', {})
    
    # Determine routing based on context
    if severity == 'CRITICAL':
        # Page on-call engineer
        notify_pagerduty(incident)
        
        # Create high-priority ticket
        create_jira_ticket(incident, priority='P1')
        
        # Attempt auto-remediation
        auto_remediate(incident)
        
    elif severity == 'WARNING':
        # Check if part of known pattern
        if is_recurring_pattern(incident):
            # Suppress if already being tracked
            update_existing_incident(incident)
        else:
            # Create normal ticket
            create_jira_ticket(incident, priority='P3')
            send_slack_notification(incident)
    
    return {'status': 'processed'}

def correlation_analysis(alerts):
    """Correlate multiple alerts to identify root cause"""
    
    # Group alerts by time window and resource
    time_window = timedelta(minutes=5)
    
    correlated_groups = []
    
    for alert in alerts:
        # Check if related to existing group
        added_to_group = False
        
        for group in correlated_groups:
            if (alert['timestamp'] - group['start_time'] < time_window and
                alert['resource'] == group['resource']):
                group['alerts'].append(alert)
                added_to_group = True
                break
        
        if not added_to_group:
            correlated_groups.append({
                'start_time': alert['timestamp'],
                'resource': alert['resource'],
                'alerts': [alert]
            })
    
    # Identify root cause
    for group in correlated_groups:
        if len(group['alerts']) > 3:
            # Multiple correlated alerts - likely cascading failure
            root_cause = identify_root_cause(group['alerts'])
            group['root_cause'] = root_cause
    
    return correlated_groups
```

**Terraform for AIOps Infrastructure:**

```hcl
# aiops_infrastructure.tf

# Log sink to BigQuery for ML analysis
resource "google_logging_project_sink" "aiops_logs" {
  name        = "aiops-log-sink"
  destination = "bigquery.googleapis.com/projects/${var.project_id}/datasets/aiops_logs"
  
  filter = <<-EOT
    severity >= ERROR
    OR resource.type = "gce_instance"
    OR resource.type = "k8s_cluster"
  EOT
  
  unique_writer_identity = true
}

# BigQuery dataset for log storage
resource "google_bigquery_dataset" "aiops_logs" {
  dataset_id = "aiops_logs"
  location   = "US"
  
  default_table_expiration_ms = 7776000000  # 90 days
}

# Cloud Function for anomaly detection
resource "google_cloudfunctions_function" "aiops_monitor" {
  name        = "aiops-anomaly-detector"
  runtime     = "python39"
  entry_point = "aiops_monitor"
  
  source_archive_bucket = google_storage_bucket.functions.name
  source_archive_object = google_storage_bucket_object.function_code.name
  
  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.metrics_stream.id
  }
  
  environment_variables = {
    PROJECT_ID = var.project_id
  }
}

# Pub/Sub topic for metrics streaming
resource "google_pubsub_topic" "metrics_stream" {
  name = "aiops-metrics-stream"
}

# Cloud Scheduler for periodic monitoring
resource "google_cloud_scheduler_job" "aiops_check" {
  name     = "aiops-periodic-check"
  schedule = "*/5 * * * *"  # Every 5 minutes
  
  pubsub_target {
    topic_name = google_pubsub_topic.metrics_stream.id
    data       = base64encode("{\"action\": \"check_anomalies\"}")
  }
}

# Alert policy for ML-detected anomalies
resource "google_monitoring_alert_policy" "anomaly_detected" {
  display_name = "ML Anomaly Detection Alert"
  combiner     = "OR"
  
  conditions {
    display_name = "Anomaly Score Threshold"
    
    condition_threshold {
      filter          = "metric.type=\"custom.googleapis.com/aiops/anomaly_score\" AND resource.type=\"global\""
      duration        = "60s"
      comparison      = "COMPARISON_GT"
      threshold_value = 0.8
      
      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_MEAN"
      }
    }
  }
  
  notification_channels = [
    google_monitoring_notification_channel.oncall.id
  ]
  
  alert_strategy {
    auto_close = "604800s"  # 7 days
  }
}
```

---

##### Q. How do you build a secure, serverless data lakehouse on GCP with BigQuery and Dataproc?

**Answer:**
A modern data lakehouse on GCP combines BigQuery's analytics capabilities with Cloud Storage's flexibility, secured with comprehensive access controls.

**Architecture:**
1. **Cloud Storage** - Raw/processed data lake
2. **BigQuery** - Analytics and serving layer
3. **Dataproc Serverless** - Spark processing
4. **Dataflow** - Stream processing
5. **Data Catalog** - Metadata and governance
6. **DLP API** - Data loss prevention
7. **VPC Service Controls** - Security perimeter

**Implementation:**

```bash
# Setup secure data lake infrastructure

# Create data lake buckets with encryption
gcloud storage buckets create gs://data-lake-raw-${PROJECT_ID} \
    --location=us-central1 \
    --uniform-bucket-level-access \
    --encryption-key=projects/${PROJECT_ID}/locations/us-central1/keyRings/data-lake/cryptoKeys/storage-key

gcloud storage buckets create gs://data-lake-processed-${PROJECT_ID} \
    --location=us-central1 \
    --uniform-bucket-level-access \
    --encryption-key=projects/${PROJECT_ID}/locations/us-central1/keyRings/data-lake/cryptoKeys/storage-key

# Set lifecycle policies
cat > lifecycle-config.json <<EOF
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
        "condition": {"age": 30, "matchesPrefix": ["raw/"]}
      },
      {
        "action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},
        "condition": {"age": 90, "matchesPrefix": ["raw/"]}
      },
      {
        "action": {"type": "SetStorageClass", "storageClass": "ARCHIVE"},
        "condition": {"age": 365, "matchesPrefix": ["raw/"]}
      },
      {
        "action": {"type": "Delete"},
        "condition": {"age": 730, "matchesPrefix": ["temp/"]}
      }
    ]
  }
}
EOF

gcloud storage buckets update gs://data-lake-raw-${PROJECT_ID} \
    --lifecycle-file=lifecycle-config.json

# Create BigQuery datasets with encryption
bq mk \
    --dataset \
    --location=us-central1 \
    --default_table_expiration=0 \
    --default_kms_key=projects/${PROJECT_ID}/locations/us-central1/keyRings/data-lake/cryptoKeys/bq-key \
    ${PROJECT_ID}:data_warehouse

bq mk \
    --dataset \
    --location=us-central1 \
    ${PROJECT_ID}:data_staging

# Enable column-level security
bq mk --table \
    --schema=schema.json \
    --time_partitioning_field=event_timestamp \
    --clustering_fields=customer_id,region \
    ${PROJECT_ID}:data_warehouse.customer_transactions
```

**Dataproc Serverless for Data Processing:**

```python
# dataproc_serverless_job.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from google.cloud import storage, dlp_v2

class SecureDataProcessor:
    """Secure data processing with PII detection and masking"""
    
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("SecureDataLakehouse") \
            .config("spark.sql.catalog.bigquery", "com.google.cloud.spark.bigquery.v2.BigQueryConnector") \
            .config("spark.jars.packages", "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.28.0") \
            .getOrCreate()
        
        self.dlp_client = dlp_v2.DlpServiceClient()
        
    def read_from_gcs(self, bucket: str, path: str):
        """Read data from Cloud Storage"""
        
        df = self.spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv(f"gs://{bucket}/{path}")
        
        return df
    
    def detect_and_mask_pii(self, df, column_name: str):
        """Detect and mask PII using Cloud DLP API"""
        
        project_id = self.spark.conf.get("spark.app.id").split('-')[0]
        
        # Define PII detection config
        inspect_config = {
            "info_types": [
                {"name": "EMAIL_ADDRESS"},
                {"name": "PHONE_NUMBER"},
                {"name": "CREDIT_CARD_NUMBER"},
                {"name": "US_SOCIAL_SECURITY_NUMBER"}
            ],
            "min_likelihood": dlp_v2.Likelihood.LIKELY
        }
        
        # Define de-identification config
        deidentify_config = {
            "info_type_transformations": {
                "transformations": [
                    {
                        "primitive_transformation": {
                            "character_mask_config": {
                                "masking_character": "*",
                                "number_to_mask": 0
                            }
                        }
                    }
                ]
            }
        }
        
        # Apply masking UDF
        def mask_pii(value):
            if not value:
                return value
            
            parent = f"projects/{project_id}"
            
            item = {"value": str(value)}
            
            response = self.dlp_client.deidentify_content(
                request={
                    "parent": parent,
                    "deidentify_config": deidentify_config,
                    "inspect_config": inspect_config,
                    "item": item
                }
            )
            
            return response.item.value
        
        mask_pii_udf = udf(mask_pii, StringType())
        
        return df.withColumn(f"{column_name}_masked", mask_pii_udf(col(column_name)))
    
    def apply_data_quality_checks(self, df):
        """Apply data quality validations"""
        
        # Check for nulls in critical columns
        null_checks = df.select([
            count(when(col(c).isNull(), c)).alias(c) 
            for c in df.columns
        ])
        
        # Check for duplicates
        duplicate_count = df.count() - df.dropDuplicates().count()
        
        # Check value ranges
        quality_metrics = {
            'total_records': df.count(),
            'duplicate_records': duplicate_count,
            'null_counts': null_checks.first().asDict()
        }
        
        # Write quality metrics to BigQuery
        quality_df = self.spark.createDataFrame([quality_metrics])
        
        quality_df.write \
            .format("bigquery") \
            .option("table", f"{project_id}:data_warehouse.quality_metrics") \
            .option("temporaryGcsBucket", f"dataproc-temp-{project_id}") \
            .mode("append") \
            .save()
        
        # Fail if quality threshold not met
        if duplicate_count > df.count() * 0.01:  # More than 1% duplicates
            raise ValueError(f"Data quality check failed: {duplicate_count} duplicates found")
        
        return df
    
    def write_to_bigquery_partitioned(self, df, table_name: str, partition_field: str):
        """Write to BigQuery with partitioning and clustering"""
        
        project_id = self.spark.conf.get("spark.app.id").split('-')[0]
        
        df.write \
            .format("bigquery") \
            .option("table", f"{project_id}:data_warehouse.{table_name}") \
            .option("temporaryGcsBucket", f"dataproc-temp-{project_id}") \
            .option("partitionField", partition_field) \
            .option("partitionType", "DAY") \
            .option("clusteredFields", "customer_id,region") \
            .option("allowFieldAddition", "true") \
            .option("allowFieldRelaxation", "true") \
            .mode("append") \
            .save()
    
    def process_incremental_data(self):
        """Process incremental data with CDC pattern"""
        
        # Read new data from GCS
        raw_df = self.read_from_gcs(
            bucket=f"data-lake-raw-{project_id}",
            path="transactions/date=2026-02-24/*.csv"
        )
        
        # Add processing metadata
        processed_df = raw_df \
            .withColumn("processing_timestamp", current_timestamp()) \
            .withColumn("data_source", lit("customer_transactions")) \
            .withColumn("partition_date", to_date(col("event_timestamp")))
        
        # Mask PII columns
        processed_df = self.detect_and_mask_pii(processed_df, "email")
        processed_df = self.detect_and_mask_pii(processed_df, "phone")
        
        # Apply quality checks
        processed_df = self.apply_data_quality_checks(processed_df)
        
        # Write to processed zone
        processed_df.write \
            .mode("append") \
            .partitionBy("partition_date") \
            .parquet(f"gs://data-lake-processed-{project_id}/transactions/")
        
        # Load to BigQuery
        self.write_to_bigquery_partitioned(
            processed_df,
            table_name="customer_transactions",
            partition_field="event_timestamp"
        )
        
        print(f"Processed {processed_df.count()} records")

# Submit Dataproc Serverless job
if __name__ == "__main__":
    processor = SecureDataProcessor()
    processor.process_incremental_data()
```

**Submit job with gcloud:**

```bash
# Submit Dataproc Serverless Spark job
gcloud dataproc batches submit pyspark dataproc_serverless_job.py \
    --region=us-central1 \
    --batch=data-processing-$(date +%Y%m%d-%H%M%S) \
    --deps-bucket=gs://dataproc-deps-${PROJECT_ID} \
    --subnet=projects/${PROJECT_ID}/regions/us-central1/subnetworks/dataproc-subnet \
    --service-account=dataproc-sa@${PROJECT_ID}.iam.gserviceaccount.com \
    --properties=spark.dynamicAllocation.enabled=true,spark.dynamicAllocation.minExecutors=2,spark.dynamicAllocation.maxExecutors=20 \
    --kms-key=projects/${PROJECT_ID}/locations/us-central1/keyRings/data-lake/cryptoKeys/compute-key
```

**BigQuery Security and Governance:**

```sql
-- Row-level security for multi-tenant data
CREATE ROW ACCESS POLICY tenant_filter
ON data_warehouse.customer_transactions
GRANT TO ('user:analyst@example.com')
FILTER USING (tenant_id = SESSION_USER());

-- Column-level security with policy tags
CREATE TAXONOMY pii_taxonomy
  OPTIONS(
    display_name="PII Data Classification",
    description="Data sensitivity classification"
  );

CREATE POLICY TAG pii_taxonomy.highly_sensitive
  OPTIONS(
    display_name="Highly Sensitive PII",
    description="Contains sensitive personal information"
  );

-- Apply policy tag to columns
ALTER TABLE data_warehouse.customer_transactions
  ALTER COLUMN email SET OPTIONS (
    policy_tags=('projects/${PROJECT_ID}/locations/us-central1/taxonomies/pii_taxonomy/policyTags/highly_sensitive')
  );

-- Data masking with authorized views
CREATE VIEW `data_warehouse.customer_transactions_masked` AS
SELECT
  transaction_id,
  customer_id,
  CASE 
    WHEN SESSION_USER() IN ('user:admin@example.com') THEN email
    ELSE CONCAT('***', SUBSTR(email, INSTR(email, '@'), LENGTH(email)))
  END AS email,
  transaction_amount,
  event_timestamp
FROM `data_warehouse.customer_transactions`;

-- Grant access to masked view
GRANT `roles/bigquery.dataViewer`
ON VIEW `data_warehouse.customer_transactions_masked`
TO 'group:analysts@example.com';
```

**Data Catalog for Discovery and Lineage:**

```python
# setup_data_catalog.py
from google.cloud import datacatalog_v1

def tag_bigquery_tables():
    """Tag BigQuery tables with metadata"""
    
    datacatalog_client = datacatalog_v1.DataCatalogClient()
    
    # Create tag template
    tag_template = datacatalog_v1.TagTemplate()
    tag_template.display_name = "Data Quality Metrics"
    
    tag_template.fields["data_owner"] = datacatalog_v1.TagTemplateField()
    tag_template.fields["data_owner"].display_name = "Data Owner"
    tag_template.fields["data_owner"].type_.primitive_type = datacatalog_v1.FieldType.PrimitiveType.STRING
    
    tag_template.fields["quality_score"] = datacatalog_v1.TagTemplateField()
    tag_template.fields["quality_score"].display_name = "Quality Score"
    tag_template.fields["quality_score"].type_.primitive_type = datacatalog_v1.FieldType.PrimitiveType.DOUBLE
    
    tag_template.fields["contains_pii"] = datacatalog_v1.TagTemplateField()
    tag_template.fields["contains_pii"].display_name = "Contains PII"
    tag_template.fields["contains_pii"].type_.primitive_type = datacatalog_v1.FieldType.PrimitiveType.BOOL
    
    # Create template
    parent = f"projects/{project_id}/locations/us-central1"
    
    created_template = datacatalog_client.create_tag_template(
        parent=parent,
        tag_template_id="data_quality_template",
        tag_template=tag_template
    )
    
    # Tag tables
    table_resource = f"//bigquery.googleapis.com/projects/{project_id}/datasets/data_warehouse/tables/customer_transactions"
    
    entry = datacatalog_client.lookup_entry(
        request={"linked_resource": table_resource}
    )
    
    tag = datacatalog_v1.Tag()
    tag.template = created_template.name
    tag.fields["data_owner"].string_value = "data-engineering-team@example.com"
    tag.fields["quality_score"].double_value = 0.98
    tag.fields["contains_pii"].bool_value = True
    
    datacatalog_client.create_tag(parent=entry.name, tag=tag)
    
    print(f"Tagged table: {table_resource}")
```

**VPC Service Controls for Data Perimeter:**

```bash
# Create service perimeter for data lakehouse
gcloud access-context-manager perimeters create data_lakehouse_perimeter \
    --title="Data Lakehouse Security Perimeter" \
    --resources=projects/${PROJECT_NUMBER} \
    --restricted-services=bigquery.googleapis.com,storage.googleapis.com,dataproc.googleapis.com \
    --policy=${POLICY_NAME} \
    --perimeter-type=regular \
    --enable-vpc-accessible-services \
    --vpc-allowed-services=bigquery.googleapis.com,storage.googleapis.com

# Add ingress rule for trusted sources
cat > ingress-policy.yaml <<EOF
- ingressFrom:
    sources:
      - accessLevel: accessPolicies/${POLICY_NAME}/accessLevels/trusted_networks
    identities:
      - serviceAccount:dataproc-sa@${PROJECT_ID}.iam.gserviceaccount.com
  ingressTo:
    resources:
      - projects/${PROJECT_NUMBER}
    operations:
      - serviceName: bigquery.googleapis.com
        methodSelectors:
          - method: "*"
      - serviceName: storage.googleapis.com
        methodSelectors:
          - method: "storage.objects.get"
          - method: "storage.objects.create"
EOF

gcloud access-context-manager perimeters update data_lakehouse_perimeter \
    --set-ingress-policies=ingress-policy.yaml \
    --policy=${POLICY_NAME}
```

---

##### Q. How do you implement cost optimization and FinOps for GCP data platforms?

**Answer:**
FinOps on GCP requires continuous monitoring, rightsizing, and intelligent resource management.

**Cost Monitoring and Budgets:**

```bash
# Create budget with alerts
gcloud billing budgets create \
    --billing-account=${BILLING_ACCOUNT_ID} \
    --display-name="Data Platform Monthly Budget" \
    --budget-amount=50000USD \
    --threshold-rule=percent=50 \
    --threshold-rule=percent=90 \
    --threshold-rule=percent=100 \
    --all-updates-rule-pubsub-topic=projects/${PROJECT_ID}/topics/budget-alerts

# Export billing data to BigQuery
gcloud beta billing accounts describe ${BILLING_ACCOUNT_ID} \
    --format="value(billingAccountId)"

# Configure export
gcloud beta billing accounts update ${BILLING_ACCOUNT_ID} \
    --billing-data-export-project=${PROJECT_ID} \
    --billing-data-export-dataset-id=billing_export
```

**Automated Cost Optimization:**

```python
# cost_optimizer.py
from google.cloud import bigquery, compute_v1, recommender_v1
from google.cloud import billing_v1
import pandas as pd
from datetime import datetime, timedelta

class GCPCostOptimizer:
    """Automated cost optimization for GCP"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.bq_client = bigquery.Client(project=project_id)
        self.compute_client = compute_v1.InstancesClient()
        self.recommender_client = recommender_v1.RecommenderClient()
        
    def analyze_bigquery_costs(self, days: int = 30):
        """Analyze BigQuery costs and identify savings opportunities"""
        
        query = f"""
        SELECT
            DATE(usage_start_time) as usage_date,
            service.description as service,
            sku.description as sku,
            project.id as project_id,
            SUM(cost) as total_cost,
            SUM(usage.amount) as usage_amount,
            usage.unit as usage_unit,
            location.region as region
        FROM `{self.project_id}.billing_export.gcp_billing_export_*`
        WHERE service.description = 'BigQuery'
            AND DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL {days} DAY)
        GROUP BY usage_date, service, sku, project_id, usage_unit, region
        ORDER BY total_cost DESC
        """
        
        df = self.bq_client.query(query).to_dataframe()
        
        # Identify expensive queries
        expensive_queries = df[df['sku'].str.contains('Analysis|Streaming')]
        
        recommendations = []
        
        # Check for partition pruning opportunities
        if expensive_queries['total_cost'].sum() > 1000:
            recommendations.append({
                'category': 'BigQuery',
                'issue': 'High query analysis costs',
                'recommendation': 'Implement partition pruning and clustering',
                'potential_savings': expensive_queries['total_cost'].sum() * 0.4
            })
        
        # Check for storage optimization
        storage_costs = df[df['sku'].str.contains('Storage')]
        
        if storage_costs['total_cost'].sum() > 500:
            recommendations.append({
                'category': 'BigQuery',
                'issue': 'High storage costs',
                'recommendation': 'Implement table expiration and archive old data',
                'potential_savings': storage_costs['total_cost'].sum() * 0.3
            })
        
        return recommendations
    
    def optimize_compute_instances(self):
        """Rightsize and schedule compute instances"""
        
        # Get all instances
        instances = self.compute_client.aggregated_list(project=self.project_id)
        
        recommendations = []
        
        for zone, instance_list in instances:
            if not instance_list.instances:
                continue
            
            for instance in instance_list.instances:
                # Get CPU utilization metrics
                utilization = self.get_instance_utilization(instance.name, zone)
                
                if utilization['avg_cpu'] < 20:  # Underutilized
                    current_machine = instance.machine_type.split('/')[-1]
                    recommended_machine = self.recommend_smaller_machine(current_machine)
                    
                    recommendations.append({
                        'category': 'Compute Engine',
                        'instance': instance.name,
                        'current': current_machine,
                        'recommended': recommended_machine,
                        'potential_savings': self.calculate_savings(current_machine, recommended_machine)
                    })
                
                # Check for idle instances
                if utilization['avg_cpu'] < 5 and utilization['network_bytes'] < 1000000:
                    recommendations.append({
                        'category': 'Compute Engine',
                        'instance': instance.name,
                        'issue': 'Idle instance detected',
                        'recommendation': 'Delete or stop instance',
                        'potential_savings': self.get_instance_monthly_cost(instance.machine_type)
                    })
        
        return recommendations
    
    def optimize_storage_lifecycle(self):
        """Implement intelligent storage tiering"""
        
        from google.cloud import storage
        
        storage_client = storage.Client()
        
        recommendations = []
        
        for bucket in storage_client.list_buckets():
            # Analyze blob access patterns
            blobs = list(bucket.list_blobs())
            
            old_blobs = [
                b for b in blobs 
                if (datetime.now() - b.time_created).days > 30
            ]
            
            if old_blobs:
                # Calculate potential savings by moving to Nearline/Coldline
                total_size_gb = sum([b.size for b in old_blobs]) / (1024**3)
                
                # Standard: $0.020/GB, Nearline: $0.010/GB, Coldline: $0.004/GB
                current_cost = total_size_gb * 0.020
                nearline_cost = total_size_gb * 0.010
                
                recommendations.append({
                    'category': 'Cloud Storage',
                    'bucket': bucket.name,
                    'issue': f'{len(old_blobs)} objects older than 30 days in Standard storage',
                    'recommendation': 'Move to Nearline or Coldline storage',
                    'potential_savings': current_cost - nearline_cost
                })
                
                # Auto-apply lifecycle policy
                self.apply_lifecycle_policy(bucket.name)
        
        return recommendations
    
    def apply_lifecycle_policy(self, bucket_name: str):
        """Apply lifecycle management to bucket"""
        
        from google.cloud import storage
        
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        
        rule = storage.lifecycle.LifecycleRule(
            action=storage.lifecycle.SetStorageClass("NEARLINE"),
            condition=storage.lifecycle.Age(30)
        )
        
        rule2 = storage.lifecycle.LifecycleRule(
            action=storage.lifecycle.SetStorageClass("COLDLINE"),
            condition=storage.lifecycle.Age(90)
        )
        
        rule3 = storage.lifecycle.LifecycleRule(
            action=storage.lifecycle.Delete(),
            condition=storage.lifecycle.Age(365)
        )
        
        bucket.lifecycle_rules = [rule, rule2, rule3]
        bucket.patch()
        
        print(f"Applied lifecycle policy to {bucket_name}")
    
    def get_recommender_insights(self):
        """Get Google Cloud Recommender suggestions"""
        
        parent = f"projects/{self.project_id}/locations/global/recommenders/google.compute.instance.MachineTypeRecommender"
        
        recommendations = []
        
        for recommendation in self.recommender_client.list_recommendations(parent=parent):
            recommendations.append({
                'name': recommendation.name,
                'description': recommendation.description,
                'primary_impact': recommendation.primary_impact,
                'state': recommendation.state
            })
        
        return recommendations
    
    def generate_cost_report(self):
        """Generate comprehensive cost optimization report"""
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'project_id': self.project_id,
            'recommendations': []
        }
        
        # Collect all recommendations
        report['recommendations'].extend(self.analyze_bigquery_costs())
        report['recommendations'].extend(self.optimize_compute_instances())
        report['recommendations'].extend(self.optimize_storage_lifecycle())
        report['recommendations'].extend(self.get_recommender_insights())
        
        # Calculate total potential savings
        total_savings = sum([
            r.get('potential_savings', 0) 
            for r in report['recommendations']
        ])
        
        report['total_potential_monthly_savings'] = total_savings
        
        # Write report to BigQuery
        df = pd.DataFrame(report['recommendations'])
        
        df.to_gbq(
            destination_table=f'{self.project_id}.cost_optimization.recommendations',
            project_id=self.project_id,
            if_exists='append'
        )
        
        return report

# Usage
optimizer = GCPCostOptimizer(project_id='my-project')
report = optimizer.generate_cost_report()

print(f"Total potential monthly savings: ${report['total_potential_monthly_savings']:.2f}")
```

**BigQuery Cost Controls:**

```sql
-- Set max bytes billed for queries
CREATE OR REPLACE PROCEDURE enforce_query_limits()
BEGIN
  -- Set project-level quota
  ALTER PROJECT `my-project`
  SET OPTIONS (
    max_bytes_billed = 1099511627776  -- 1 TB
  );
END;

-- Create materialized view for frequently queried data
CREATE MATERIALIZED VIEW data_warehouse.customer_summary
PARTITION BY DATE(last_updated)
CLUSTER BY customer_id
AS
SELECT
  customer_id,
  COUNT(*) as transaction_count,
  SUM(transaction_amount) as total_spent,
  AVG(transaction_amount) as avg_transaction,
  MAX(transaction_date) as last_transaction_date,
  CURRENT_TIMESTAMP() as last_updated
FROM data_warehouse.customer_transactions
GROUP BY customer_id;

-- Use partitioned and clustered tables to reduce costs
CREATE OR REPLACE TABLE data_warehouse.transactions
PARTITION BY DATE(transaction_date)
CLUSTER BY customer_id, region
OPTIONS(
  partition_expiration_days=90,
  require_partition_filter=true
) AS
SELECT * FROM data_warehouse.raw_transactions;

-- Cost monitoring query
SELECT
  user_email,
  query,
  ROUND(total_bytes_billed / 1024 / 1024 / 1024, 2) as gb_billed,
  ROUND(total_slot_ms / 1000 / 60 / 60, 2) as slot_hours,
  ROUND(total_bytes_billed / 1024 / 1024 / 1024 * 5 / 1000, 2) as estimated_cost_usd,
  creation_time
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  AND state = 'DONE'
  AND total_bytes_billed > 0
ORDER BY total_bytes_billed DESC
LIMIT 100;
```

**Committed Use Discounts and Reservations:**

```bash
# Purchase committed use discount for BigQuery
gcloud beta compute commitments create bigquery-commitment \
    --region=us-central1 \
    --plan=12-month \
    --resources=slots=500 \
    --auto-renew

# Purchase committed use for Compute Engine
gcloud compute commitments create compute-commitment \
    --region=us-central1 \
    --resources=vcpu=100,memory=400GB \
    --plan=12-month

# Create BigQuery reservation
bq mk \
    --project_id=${PROJECT_ID} \
    --location=us-central1 \
    --reservation \
    --slots=500 \
    --ignore_idle_slots=false \
    prod-reservation

# Assign reservation to project
bq mk \
    --project_id=${PROJECT_ID} \
    --location=us-central1 \
    --reservation_assignment \
    --reservation_id=projects/${PROJECT_ID}/locations/us-central1/reservations/prod-reservation \
    --job_type=QUERY \
    --assignee_type=PROJECT \
    --assignee_id=${PROJECT_ID}
```

---

