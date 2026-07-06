# ☁️ Salesforce — Baby Style (5-6 weeks)

**For:** No coding experience. Want high salary fast. Like organized systems.

**Time:** 3 hrs/day | **Goal:** Salesforce Admin or Developer

**Pay:** $70-100k | **Difficulty:** Medium (but well-paid)

---

## What is Salesforce?

- Salesforce = software companies use to track customers, sales, support
- Huge demand. Not enough people who know it.
- You DON'T need a degree. Certifications matter more.
- Certs cost $200-400. Worth it. Unlock $70k+ jobs.

---

## 🗓️ Week 1 — Admin Basics (no code)

### Day 1: What is Salesforce?
- A CRM (Customer Relationship Management)
- Tracks: leads, contacts, accounts, opportunities, cases
- Companies customize it for their needs

**Do:** Sign up for a FREE Salesforce Developer Edition. Log in. Look around.

### Day 2: Objects + Records
- Object = table (like "Contact" or "Account")
- Record = one row in that table (like "John Smith")
- Standard objects: Account, Contact, Lead, Opportunity, Case

**Do:** Create 3 contacts and 2 accounts in your org.

### Day 3: Fields + Relationships
- Field = column (Name, Phone, Email)
- Lookup = link one object to another (Contact → Account)
- Master-Detail = tighter relationship (if parent deleted, child deleted)

**Do:** Add custom fields to Contact (like "Birthday" or "Twitter handle").

### Day 4: Security
- Profiles = what a user can see/do
- Permission sets = extra permissions
- Roles = who reports to whom
- Sharing rules = share records with groups

**Do:** Create a profile that can only read contacts (not edit).

### Day 5: Automation basics
- Workflow Rule = if X happens, do Y (send email, update field)
- Process Builder = visual automation (drag and drop)

**Do:** Create a workflow that sends an email when a new lead comes in.

### Day 6-7: Reports + Dashboards
- Reports = list of data (filtered, grouped)
- Dashboards = charts from reports

**Do:** Create a report of all contacts. Turn it into a dashboard with a chart.

---

## 🗓️ Week 2 — Admin Certification Prep

### Study for Salesforce Admin (ADM 201) exam

**Topics to cover:**
- Security: profiles, permission sets, sharing rules
- Objects: standard + custom, fields, relationships
- Automation: workflow rules, process builder, flows
- Data: import wizard, data loader
- Reports + dashboards
- AppExchange (App Store for Salesforce)

**Resources:**
- Trailhead.salesforce.com (free — official)
- focusonforce.com practice exams ($20)
- Quizlet flashcards

**Do:** Take practice exams. Score 70%+ consistently. Then schedule the real exam ($200).

> Note: You can get a Salesforce Admin job with JUST the cert ($60-85k). But adding dev skills pays more.

---

## 🗓️ Week 3 — Apex (Salesforce coding)

### Day 1: What is Apex?
- Apex = Salesforce's programming language (like Java)
- Runs on Salesforce servers
- Used for complex automation

**Do:** Open Developer Console in Salesforce. Write `System.debug('Hello World');`

### Day 2: Variables + SOQL
- SOQL = Salesforce's version of SQL
- `List<Contact> contacts = [SELECT Id, Name FROM Contact];`

**Do:** Write a SOQL query to get all contacts. Print their names.

### Day 3: DML (Data Manipulation)
- `insert`, `update`, `upsert`, `delete`
- `insert new Contact(FirstName='John', LastName='Doe');`

**Do:** Write Apex that creates a new contact. Then updates their phone.

### Day 4: Triggers
- Trigger = code that runs when data changes
- "After insert" = after a record is created
- Used for: validation, auto-updates, integrations

**Do:** Write a trigger that auto-assigns new leads to a specific user.

### Day 5: Test classes
- Salesforce REQUIRES 75% code coverage to deploy
- `@isTest` class + `Test.startTest()` / `Test.stopTest()`

**Do:** Write a test class for your trigger. Get 75%+ coverage.

### Day 6-7: Practice
- Write 2 triggers with test classes
- Push to a sandbox

---

## 🗓️ Week 4 — Lightning Web Components (modern UI)

### Day 1: What is LWC?
- LWC = modern way to build Salesforce UI
- Uses JavaScript + HTML + CSS
- Replaces old Visualforce pages

**Do:** Create a simple LWC that shows "Hello World".

### Day 2: LWC basics
- `@api` = property that can be set from outside
- `@track` = property that triggers re-render (old) / just use regular vars (new)
- `@wire` = get data from Salesforce

**Do:** Make a component that accepts a name (@api) and displays it.

### Day 3: Call Apex from LWC
- `@AuraEnabled(cacheable=true)` in Apex
- `import getContacts from '@salesforce/apex/ContactController.getContacts'`

**Do:** Display a list of contacts in your LWC component.

### Day 4: LWC forms
- Input fields → save button → insert to Salesforce

**Do:** Build a contact form component. Fill it → creates contact in Salesforce.

### Day 5: LWC project
- Dashboard component: show contacts, accounts, opportunities in cards

### Day 6-7: LWC polish
- Styling (Salesforce Design System / SLDS)
- Error handling
- Loading spinners

---

## 🗓️ Week 5 — Cert + Portfolio

### Day 1-2: Platform App Builder cert
- Covers: custom objects, automation, security, mobile
- Another cert for your resume

**Do:** Take practice tests. Schedule exam ($200).

### Day 3-4: Portfolio
- GitHub with your Apex classes + LWC components
- Trailhead badges (show on LinkedIn)
- Write a README explaining what you built

### Day 5-6: Resume + LinkedIn
- Keywords: Salesforce, Apex, LWC, SOQL, Triggers, Admin, App Builder
- Headline: "Salesforce Developer" or "Salesforce Admin"

### Day 7: Apply
- Roles: Salesforce Developer, Admin, Associate, Jr. Salesforce Dev
- LinkedIn, masonfrank.com (Salesforce jobs), salesforceben.com/jobs
- Contract work pays $50-80/hr for entry

---

## 🗓️ Week 6 — Interview + Keep going

- "What's the difference between a trigger and a workflow?"
- "How do you ensure 75% code coverage?"
- "Explain SOQL vs SOSL"
- "What are governor limits?"

> ✅ **Salesforce = high pay, lots of jobs, less competition than web dev.** Certs cost $ but the ROI is fast.
