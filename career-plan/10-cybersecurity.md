# 🔒 Cybersecurity — Baby Style (8 weeks)

**For:** Zero experience. Like puzzles and security. Want a growing field.

**Time:** 3 hrs/day | **Goal:** Junior Security Analyst / SOC Analyst

**Pay:** $65-95k | **Difficulty:** Medium

---

## What is Cybersecurity?

- Protect companies from hackers
- Monitor systems for attacks
- Find vulnerabilities before bad guys do
- Huge demand. Not enough workers. Entry level jobs exist with certs.

---

## 🗓️ Week 1 — Security Basics

### Day 1: What is cybersecurity?
- Confidentiality (only authorized people see data)
- Integrity (data isn't modified)
- Availability (systems are up)
- CIA triad = foundation of security

**Do:** For each app you use today (email, bank, social media), think: how does it protect CIA?

### Day 2: Common threats
- Malware = viruses, ransomware, trojans
- Phishing = fake emails that steal passwords
- DDoS = overload server to take it down
- Social engineering = trick people into giving access

**Do:** Look at your spam folder. Identify phishing emails. What gives them away?

### Day 3: Networking for security
- IP addresses, ports, protocols (TCP/UDP)
- Firewalls block bad traffic
- VPNs encrypt traffic

**Do:** Use Wireshark to capture network traffic. See what your computer is sending.

### Day 4: Operating system security
- Windows: User Account Control, Windows Defender, BitLocker
- Linux: sudo, file permissions, AppArmor

**Do:** Check your Windows security settings. Enable Defender. Run a scan.

### Day 5: Password security
- Strong passwords: 12+ chars, mixed, unique
- Password managers (Bitwarden, 1Password)
- MFA (multi-factor authentication)

**Do:** Install a password manager. Change your important passwords. Enable MFA everywhere.

### Day 6-7: Practice
- TryHackMe free rooms (search "tryhackme beginner")
- Complete 3 beginner rooms

---

## 🗓️ Week 2 — Tools of the Trade

### Day 1: Linux for security
- `grep`, `awk`, `sed`, `find` — search through files
- `journalctl`, `syslog` — check logs
- `netstat`, `ss` — see network connections

**Do:** Search log files for "failed password" or "error".

### Day 2: Wireshark (network analysis)
- Capture network traffic
- Filter: HTTP, DNS, specific IPs
- Follow TCP streams (see what data was sent)

**Do:** Capture your own traffic. Find an HTTP request. See the data inside.

### Day 3: Nmap (network scanning)
- `nmap 192.168.1.1` — scan a device for open ports
- Find what services are running

**Do:** Scan your home network. Find all connected devices and their open ports.

### Day 4: Burp Suite (web security)
- Intercept web traffic between browser and server
- Modify requests, test for vulnerabilities

**Do:** Install Burp Suite (Community Edition). Intercept a login request. See the password in plain text.

### Day 5: Metasploit (exploitation)
- Framework for running exploits
- You DON'T use this on real systems without permission

**Do:** Set up a vulnerable VM (Metasploitable). Scan it. Find vulnerabilities.

### Day 6-7: Practice
- TryHackMe rooms: Nmap, Wireshark, Burp Suite
- Complete 5 rooms this week

---

## 🗓️ Week 3 — Web Security

### Day 1: OWASP Top 10
- The 10 most common web vulnerabilities
- #1: Broken access control
- #2: Cryptographic failures
- #3: Injection (SQL, XSS)

**Do:** Read about OWASP Top 10 (just the first 5). Understand each.

### Day 2: SQL injection
- Attacker puts SQL code in input fields
- `' OR 1=1 --` can bypass login
- Fix: use parameterized queries

**Do:** Try SQL injection on a practice site (DVWA or bWAPP).

### Day 3: XSS (Cross-Site Scripting)
- Attacker puts JavaScript in a website
- Steals cookies, redirects users, defaces pages

**Do:** Try XSS on a practice site. `<script>alert('XSS')</script>`

### Day 4: Broken authentication
- Weak passwords, no MFA, session hijacking
- Fix: enforce strong passwords, MFA, secure sessions

**Do:** Audit a website's authentication. What's wrong with it?

### Day 5: Security headers
- HTTPS (SSL/TLS)
- Content Security Policy (CSP)
- HTTP Strict Transport Security (HSTS)

**Do:** Use securityheaders.com to check a website's security headers.

### Day 6-7: Practice
- PortSwigger Web Security Academy (free labs)
- Complete 5 labs (SQL injection + XSS)

---

## 🗓️ Week 4 — SOC Analyst Skills

### Day 1: What is a SOC?
- SOC = Security Operations Center
- Analysts monitor alerts 24/7
- Triage: is this a real threat or false alarm?

**Do:** Watch "Day in the life of a SOC Analyst" on YouTube.

### Day 2: SIEM (Security Information and Event Management)
- Splunk, ELK, or Wazuh
- Central place to see all security events

**Do:** Install Wazuh (free SIEM). See security events from your computer.

### Day 3: Log analysis
- Windows Event Viewer: security logs, application logs
- Linux: /var/log/auth.log, syslog
- Look for: failed logins, unusual times, unknown IPs

**Do:** Check your Windows event logs. Find failed login attempts.

### Day 4: Phishing analysis
- Check email headers (see real sender)
- Check links without clicking (hover, inspect)
- Report and delete

**Do:** Analyze a phishing email. Extract the real sender IP. Check the link destination.

### Day 5: Incident response
- Steps: Identify → Contain → Eradicate → Recover → Lessons Learned
- Don't panic. Follow the process.

**Do:** Write an incident response plan for a ransomware attack.

### Day 6-7: Practice
- Blue Team Labs Online (free)
- Complete 3 SOC analyst challenges

---

## 🗓️ Week 5 — Certifications

### Day 1-2: CompTIA Security+
- Entry level security cert. Very recognized.
- Covers: threats, vulnerabilities, cryptography, identity management
- Costs ~$250

**Do:** Buy a practice exam. Take it. Identify weak areas.

### Day 3-4: Study
- Professor Messer Security+ videos (free on YouTube)
- Focus on weak areas from practice test

### Day 5-6: More practice tests
- Score 80%+ on practice tests? Schedule the real exam.

### Day 7: Take exam (or schedule it)

**Alternative certs:**
- Google Cybersecurity Certificate ($50/month on Coursera)
- CompTIA Security+ (most recognized)
- Certified Ethical Hacker (CEH) — more advanced

---

## 🗓️ Week 6 — Portfolio + Resume

### Day 1-2: Portfolio
- TryHackMe profile with badges
- GitHub with security scripts (log analyzer, port scanner, phishing detector)

### Day 3-4: Resume
- 1 page. Keywords: Security+, SIEM, log analysis, vulnerability assessment, Wireshark, Nmap, OWASP, incident response

### Day 5-6: LinkedIn
- Headline: "Cybersecurity Analyst" or "Junior Security Analyst"
- Add TryHackMe badges
- Set Open to Work

### Day 7: Apply
- Roles: SOC Analyst, Junior Security Analyst, Cybersecurity Analyst, Information Security Analyst
- LinkedIn, Indeed — 10 apps/day

---

## 🗓️ Week 7-8 — Interview prep + Apply

### Days 1-14:
- "What's the difference between a vulnerability and a threat?"
- "Explain the CIA triad"
- "How would you handle a phishing attack?"
- "Walk me through incident response"

**Keep applying 10/day. First job takes 2-8 weeks of searching.**

---

> ✅ **Cybersecurity = growing field, good pay, meaningful work.** Certs help a lot for entry. After 1-2 years, you can specialize in penetration testing ($100k+), cloud security ($120k+), or management.
