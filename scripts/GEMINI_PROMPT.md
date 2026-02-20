# Gemini Apps Script Prompt — Gmail Organization

Copy and paste this entire prompt into Gemini (in the Apps Script editor, or at gemini.google.com) to have it build and run the full automation.

---

## THE PROMPT:

I need you to write a Google Apps Script that automates organizing my Gmail inbox. Here's the full context:

**Account:** andy.mcateer@corvallis.k12.or.us (Google Workspace / Edu)
**Role:** CTE teacher at Crescent Valley High School, Corvallis OR

### TASK 1: Create Gmail Filters (7 filters)

Create these Gmail filters using the Gmail Advanced Service API (`Gmail.Users.Settings.Filters.create`). Each filter should also retroactively apply to all existing matching emails using `GmailApp.search()` + `label.addToThreads()`.

| # | From criteria | Has words | Label | Skip Inbox? | Never Spam? |
|---|---|---|---|---|---|
| 1 | `spreadbury OR parentsquare` | | School/Admin | YES | YES |
| 2 | `chappy.swearingen OR sherry.dickerson OR csd509j.instructure` | | School/Grades | no | no |
| 3 | `panknin OR lisa.mathews OR viramontes OR godsey` | | School/SPED | no | no |
| 4 | `student.csd509j.net OR onshape.com` | | Students/Submissions | YES | no |
| 5 | `fortd@linnbenton.edu OR nikki.mcfarland` | | CTE | no | no |
| 6 | `colton.hankey@student.csd509j.net` | | Drift-Trike | no | no |
| 7 | `robert.parrott` | `order OR purchase OR invoice OR requisition` | Purchasing/Orders | no | no |

**Important:** All 14 labels already exist in Gmail. The script should use `GmailApp.getUserLabelByName()` to find them (don't create new ones unless missing). One filter (#1 School/Admin) already exists in Gmail — skip it if duplicate error.

### TASK 2: Retroactively Label + Archive Existing Inbox Emails

After creating filters, search for and label ALL existing matching emails. For filters with "Skip Inbox = YES", also archive those threads (`thread.moveToArchive()`).

Additionally, apply these catch-all rules to remaining inbox emails:

- `from:parentsquare` → label "School/Admin", archive
- `from:noreply@google.com` → label "Resources", archive
- `from:notifications@onshape.com` → label "Students/Submissions", archive
- `subject:"staff meeting" OR subject:"professional development"` → label "School/Events"

### TASK 3: Clean Up Drafts

I have 109 drafts. The script should:
1. Get all drafts via `GmailApp.getDrafts()`
2. Delete any draft where the body is empty or only whitespace (these are blank/accidental drafts)
3. Log how many were deleted vs kept
4. Do NOT delete drafts that have actual content

### TASK 4: Create 7 Draft Email Replies

Create these draft replies in Gmail using `GmailApp.createDraft()`. Each should be a reply to the most recent email from that sender. If the original thread can't be found, create a new compose draft to the email address instead.

**Draft 1 — Tori Melanson (tori.melanson@corvallis.k12.or.us)**
Subject: Re: [whatever her last email was]
Body:
```
Hi Tori,

Thanks for reaching out. I'd be happy to help with the PowerSchool/Canvas sync issue. Let me know a good time to connect this week and we can get it sorted out.

Best,
Andy
```

**Draft 2 — Robert Parrott (robert.parrott@corvallis.k12.or.us)**
Subject: Re: Purchase order
Body:
```
Hi Robert,

Following up on the purchase order for the drift trike project materials. Just want to confirm everything is still on track. Let me know if you need any additional documentation from my end.

Thanks,
Andy
```

**Draft 3 — Oliver Norris (oliver.norris@student.csd509j.net)**
Subject: Re: [his last email]
Body:
```
Hi Oliver,

Got your message. Let's plan to connect during class this week to go over your project progress. Keep up the good work.

Mr. McAteer
```

**Draft 4 — Zeph Cazé (zeph.caze@student.csd509j.net)**
Subject: Re: [his last email]
Body:
```
Hi Zeph,

Thanks for the update. Let's touch base during class to make sure you're on track with the project timeline.

Mr. McAteer
```

**Draft 5 — Matt Gough (matt.gough@corvallis.k12.or.us)**
Subject: Re: [his last email]
Body:
```
Hi Matt,

Thanks for the heads up. I'll review the info and get back to you by end of week. Let me know if anything changes in the meantime.

Best,
Andy
```

**Draft 6 — Nikki McFarland (nikki.mcfarland@corvallis.k12.or.us)**
Subject: Re: CTE
Body:
```
Hi Nikki,

Thanks for the update on CTE coordination. I'm on board and happy to help however needed. Just let me know the next steps and any deadlines I should be aware of.

Best,
Andy
```

**Draft 7 — Deron Fort (fortd@linnbenton.edu)** ← HIGH PRIORITY
Subject: Re: Career Fair
Body:
```
Hi Deron,

Thanks for organizing the career fair. I'm confirmed and planning to attend. Please send over any logistics details (time, setup, what to bring) when you have them.

Looking forward to it,
Andy McAteer
Crescent Valley High School
```

### TECHNICAL REQUIREMENTS:

1. **Enable Gmail Advanced Service** — the script uses `Gmail.Users.Settings.Filters.create()` which requires the Gmail API advanced service. Add it via Services > Gmail API > v1.
2. **Use V8 runtime** (already enabled)
3. **Main function** should be called `runFullOrganization()` and execute Tasks 1-4 in order
4. **Logging** — use `Logger.log()` throughout so I can see progress in the Execution Log
5. **Error handling** — wrap each task in try/catch so one failure doesn't stop everything
6. **Batch operations** — use `label.addToThreads(threads)` instead of looping one-by-one where possible
7. **Rate limiting** — add `Utilities.sleep(1000)` between major operations to avoid hitting Gmail API rate limits

### EXISTING LABELS (all 14):
_Action, _Waiting, CTE, Drift-Trike, Personal, Purchasing/Invoices, Purchasing/Orders, Resources, School/Admin, School/Events, School/Grades, School/SPED, Students/Communication, Students/Submissions

### WHAT SUCCESS LOOKS LIKE:
- 7 Gmail filters created (future emails auto-labeled)
- All existing emails labeled by category
- School/Admin and Students/Submissions emails archived out of inbox
- Blank drafts deleted
- 7 draft replies ready to review and send
- Execution log shows progress for every step
