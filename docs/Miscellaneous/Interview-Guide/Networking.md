## Networking

### Network Configuration & Security

##### Q. Service Endpoint vs Private Endpoint?

**Azure Private Link (Private Endpoint):**
- Access PaaS over private IP within VNet
- Gets new private IP on VNet
- Traffic stays within VNet
- Inbuilt data protection
- Extensible for on-premises via ExpressRoute/VPN
- Additional resource to manage
- Cost based on traffic and runtime
- Blocks all internet traffic to resource

**Azure Service Endpoint:**
- Secure connectivity over Azure backbone
- Traffic leaves VNet to public endpoint
- Publicly routable IP remains
- Not easily restricted for on-premises
- Simpler implementation
- No additional cost
- Only secures to Azure VNet

##### Q. Public vs Private networking?

**Public Networking:**
- Internet-accessible
- Public IP addresses
- Less secure (requires firewalls, encryption)

**Private Networking:**
- Organization/group restricted
- Private IP addresses
- Not directly internet-accessible
- More secure (internal security, controlled access)

##### Q. Connect bastion host to private network?

1. **Deploy Bastion Host:**
   - Place in public subnet
   - Configure security groups (SSH/RDP from trusted IPs)

2. **Access Private Resources:**
   - Place resources in private subnets
   - Configure security groups allowing bastion traffic

3. **SSH/RDP into Bastion:**
   - Connect from local machine to bastion

4. **Access Private Instances:**
   - SSH tunnel through bastion to private IPs

##### Q. What is VPC?
Logically isolated network in cloud with:
- Custom IP address ranges
- Subnets (public/private)
- Internet Gateway (IGW)
- NAT Gateway/Instance
- Route Tables
- Security Groups
- Network ACLs

##### Q. What is VPC Peering?
Enables communication between two VPCs using private IPs:
1. Create peering connection
2. Update route tables in both VPCs
3. Configure security groups/NACLs
4. Private communication without public IPs

##### Q. What is load balancer?
Distributes incoming traffic across multiple servers for:
- Increased availability
- Scalability
- Improved performance
- Health monitoring
- Fault tolerance
- SSL termination
- Geographic distribution

##### Q. What is Cloud NAT?
Managed service enabling private instances to access internet without exposing private IPs:
- Managed by cloud provider
- Security (prevents inbound connections)
- Automatic scaling
- Cost-efficient
- High availability

##### Q. Load Balancer vs Cloud NAT Gateway?

**Load Balancer:**
- Distributes incoming traffic
- Layer 4 (TCP/UDP)
- Health monitoring
- Scalability and fault tolerance
- SSL termination
- Session persistence

**Cloud NAT Gateway:**
- Handles outbound traffic
- Private IP masking
- Managed service
- Security (no inbound access)
- Automatic scaling
- High availability

##### Q. Secure way to manage sensitive information?
1. Use Secrets Manager
2. Encrypt data (rest and transit)
3. Implement access controls
4. Automate secret rotation
5. Audit and monitor access
6. Use environment variables
7. Secure backup/recovery
8. Regular security assessments

##### Q. What is secrets manager?
Tool for securely storing, managing, and accessing:
- Passwords
- API keys
- Encryption keys
- Confidential data

**Features:**
- Secure encrypted storage
- Access control
- Automated rotation
- Audit and monitoring

##### Q. Networking setup rules?

**1. Network Segmentation:**
- VPCs and subnets
- Network ACLs and security groups

**2. Access Control:**
- Least privilege principle
- Private connectivity

**3. Performance:**
- Load balancers
- DNS configuration

**4. High Availability:**
- Multi-AZ deployments
- Failover mechanisms

**5. Monitoring:**
- Network monitoring tools
- Traffic logging

**6. Compliance:**
- Industry standards
- Regular patching

**7. Scalability:**
- Auto-scaling
- Elastic IPs

##### Q. Deny traffic from specific IP for AKS pod?
Using NACL deny rule.

##### Q. Create private or public subnet?
- **Private:** Routing table without internet gateway
- **Public:** Routing table with internet gateway

##### Q. SGID, SUID, Sticky Bit, ACL commands?

**SUID (Set User ID):**
- Run programs as file owner
- Value: 4 or u+s
```bash
chmod 4775 um.sh
chmod u+s um.sh
```

**SGID (Set Group ID):**
- Inherit group ownership
- Value: 2 or g+s
```bash
chmod 2775 /data
chmod g+s /data
```

**Sticky Bit:**
- Only owner can delete file
- Value: 1 or +t
```bash
chmod 1775 /tmp
chmod +t /tmp
```

**ACL (Access Control List):**
```bash
# Check ACL
getfacl

# Set ACL
setfacl -R -m d:g:marketing:rw acl/
setfacl -R -m user:geeko:rwx,group:mascots:rwx mydir/
```

---



### Security & Troubleshooting

##### Q. Production app works fine for internal users but fails for external ones (403 error). How will you isolate the issue?
**Answer:**
An HTTP 403 Forbidden indicates an authentication, authorization, or strict firewall block issue.
1. **Network Topology:** External users typically traverse through a CDN, Web Application Firewall (WAF), or Internet-facing Ingress, whereas internal users on a corporate VPN might traverse an ExpressRoute or internal Load Balancer, completely bypassing external security rules.
2. **Check Logs:** Check the WAF (e.g., Azure Front Door or App Gateway WAF) log diagnostics for matched rule IDs blocking the request (e.g., Geo-blocking, suspected SQLi bots). 
3. **CORS & NSGs:** Verify if CORS (Cross-Origin Resource Sharing) is configured incorrectly on the API Gateway, or if Network Security Groups (NSGs) / Conditional Access Policies are explicitly explicitly whitelisting corporate IP address ranges while denying the public internet.
