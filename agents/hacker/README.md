# Hacker Agent - Elite Offensive Security Specialist

## Overview

The Hacker Agent is a comprehensive offensive security specialist designed for authorized penetration testing, vulnerability assessment, and red team operations. This agent operates with professional-grade capabilities while maintaining strict ethical standards and legal compliance.

**🧠 Persistent Memory**: The agent remembers all engagements, findings, credentials, and techniques across sessions, ensuring continuity and efficiency in security operations.

## Quick Start

### Activating the Hacker Agent

```json
{
    "tool_name": "call_subordinate",
    "tool_args": {
        "profile": "hacker",
        "message": "Your security testing request here...",
        "reset": "true"
    }
}
```

### Example Use Cases

**1. Web Application Penetration Test**
```
"Perform a comprehensive security assessment of https://example.com. 
Focus on OWASP Top 10 vulnerabilities including SQLi, XSS, and authentication flaws.
Authorization: Engagement #2024-001"
```

**2. Network Penetration Test**
```
"Conduct internal network penetration testing for 192.168.1.0/24.
Identify vulnerabilities, attempt lateral movement, and document privilege escalation paths.
Authorization: SOW dated 2024-01-15"
```

**3. Cloud Security Assessment**
```
"Audit AWS infrastructure for security misconfigurations.
Review IAM policies, S3 bucket permissions, and security group rules.
Authorization: Client approval email 2024-01-20"
```

## Persistent Memory System

The Hacker Agent maintains **persistent memory across all sessions**, providing:

### What Gets Remembered
- ✅ **Engagement Details**: Authorization, scope, Rules of Engagement
- ✅ **Target Intelligence**: Network maps, discovered hosts, services
- ✅ **Vulnerability Database**: All findings with severity and status
- ✅ **Compromised Credentials**: Securely stored access credentials
- ✅ **Exploitation Techniques**: Successful attack vectors and payloads
- ✅ **Tool Configurations**: Custom scripts and wordlists
- ✅ **Lessons Learned**: What worked, what didn't, OPSEC notes

### Memory Workflow Example

**First Session - Initial Reconnaissance**:
```
User: "Scan example.com for vulnerabilities"
Agent:
1. Checks memory for existing data on example.com
2. Performs reconnaissance (Nmap, subdomain enum)
3. Saves discovered hosts and services to memory
4. Documents findings in persistent vulnerability database
```

**Later Session - Exploitation**:
```
User: "Exploit the SQL injection we found on example.com"
Agent:
1. Loads vulnerability database from memory
2. Recalls VULN-001: SQL Injection in /login
3. Retrieves saved payload and exploitation notes
4. Executes attack using remembered technique
5. Updates memory with new credentials obtained
```

**Future Session - Reporting**:
```
User: "Generate report for example.com engagement"
Agent:
1. Loads complete engagement history from memory
2. Retrieves all vulnerabilities, credentials, and findings
3. Compiles comprehensive report with evidence
4. No need to re-scan or re-discover anything
```

### Benefits
- 🚀 **Faster Assessments**: No repeated reconnaissance
- 🎯 **Continuity**: Pick up exactly where you left off
- 📚 **Knowledge Base**: Builds expertise from past engagements
- 🔐 **Credential Tracking**: Maintains access across sessions
- 📊 **Historical Context**: Understands target evolution over time

## Capabilities

### Penetration Testing Methodologies
- ✅ OWASP Testing Guide
- ✅ PTES (Penetration Testing Execution Standard)
- ✅ NIST Cybersecurity Framework
- ✅ MITRE ATT&CK Framework
- ✅ Cyber Kill Chain

### Technical Domains
- 🌐 **Web Application Security**: SQLi, XSS, CSRF, SSRF, XXE, API testing
- 🔌 **Network Penetration**: Internal/external network testing, lateral movement
- 📡 **Wireless Security**: WiFi assessment, WPA/WPA2 attacks
- 🎭 **Social Engineering**: Phishing, pretexting, physical security
- ☁️ **Cloud Security**: AWS, Azure, GCP security auditing
- 🐳 **Container Security**: Docker, Kubernetes penetration testing
- 🏢 **Active Directory**: AD enumeration, Kerberos attacks, privilege escalation
- 🔐 **Password Attacks**: Hash cracking, credential stuffing, brute-forcing

### Tool Arsenal (50+ Tools)
- **Reconnaissance**: Nmap, Masscan, Recon-ng, Shodan, theHarvester
- **Web Testing**: Burp Suite, OWASP ZAP, SQLMap, XSStrike, Nikto
- **Network**: Metasploit, Impacket, CrackMapExec, BloodHound
- **Wireless**: Aircrack-ng, Wifite, Kismet, Reaver
- **Password**: Hashcat, John the Ripper, Hydra
- **Post-Exploitation**: Mimikatz, PowerSploit, LinPEAS, WinPEAS
- **Cloud**: ScoutSuite, Prowler, Pacu
- **Container**: kube-hunter, kube-bench, Docker security tools

## Authorization Requirements

⚠️ **CRITICAL**: The Hacker Agent will **NEVER** perform security testing without:

1. ✅ **Written Authorization** - Signed SOW, contract, or authorization letter
2. ✅ **Defined Scope** - Specific IP ranges, domains, or systems
3. ✅ **Rules of Engagement** - Testing constraints and limitations
4. ✅ **Testing Window** - Approved dates and times
5. ✅ **Emergency Contact** - Client point of contact for issues

### Authorization Verification

The agent will request authorization before any testing:

```
⚠️ AUTHORIZATION REQUIRED

Before proceeding with penetration testing, I need:
1. Written authorization documentation
2. Defined scope (IP ranges, domains, systems)
3. Rules of Engagement (RoE)
4. Testing window and constraints
5. Emergency contact information

Please provide authorization documentation.
```

## Reporting Format

The agent provides structured vulnerability reports:

```
## [CRITICAL] SQL Injection in Login Form

**Affected System**: https://example.com/login
**CVSS Score**: 9.8 (Critical)
**Discovery Date**: 2024-01-29 14:30 UTC

### Description
The login form is vulnerable to SQL injection via the username parameter...

### Attack Vector
1. Navigate to https://example.com/login
2. Enter payload: admin' OR '1'='1'-- 
3. Observe authentication bypass

### Proof of Concept
[Screenshot and command output]

### Impact Analysis
**Technical Impact**: Complete database compromise, authentication bypass
**Business Impact**: Data breach, regulatory fines, reputational damage

### Remediation
**Immediate**: Disable login form, implement WAF rules
**Long-term**: Use parameterized queries, input validation, prepared statements

### References
- CWE-89: SQL Injection
- OWASP A03:2021 - Injection
```

## Ethical Standards

The Hacker Agent operates under strict ethical guidelines:

- ✅ **Legal Compliance**: All activities within applicable laws
- ✅ **Authorization First**: Never test without permission
- ✅ **Scope Adherence**: Stay within defined boundaries
- ✅ **Responsible Disclosure**: Report vulnerabilities ethically
- ✅ **Data Protection**: Respect privacy and confidentiality
- ✅ **Professional Ethics**: Follow CEH and SANS GIAC codes

## Operational Security (OPSEC)

The agent maintains operational security through:

- 🔒 **Stealth Techniques**: Minimize detection signatures
- 🧹 **Artifact Cleanup**: Remove tools and backdoors post-testing
- 📝 **Comprehensive Logging**: Document all actions with timestamps
- 🔐 **Secure Communication**: Encrypted channels for sensitive data
- 🎯 **Precision Targeting**: Avoid collateral damage

## File Structure

```
agents/hacker/
├── _context.md                                    # Agent overview
├── README.md                                      # This file
└── prompts/
    ├── agent.system.main.role.md                 # Role definition (273 lines)
    ├── agent.system.main.communication.md        # Communication style (231 lines)
    └── agent.system.main.environment.md          # Environment setup
```

## Best Practices

### Before Engagement
1. Verify authorization documentation
2. Confirm scope and constraints
3. Set up secure testing environment
4. Establish communication protocols

### During Engagement
1. Follow systematic methodology (PTES)
2. Document every action with evidence
3. Report critical findings immediately
4. Maintain stealth when required
5. Respect testing windows

### After Engagement
1. Clean up all artifacts
2. Remove persistence mechanisms
3. Compile comprehensive report
4. Provide remediation guidance
5. Securely archive evidence

## Support

For questions or issues with the Hacker Agent:
- Review the role definition: `agents/hacker/prompts/agent.system.main.role.md`
- Check communication guidelines: `agents/hacker/prompts/agent.system.main.communication.md`
- Consult the context file: `agents/hacker/_context.md`

---

**Remember**: This agent is a powerful tool for authorized security testing. Always operate ethically, legally, and with proper authorization. 🔒

