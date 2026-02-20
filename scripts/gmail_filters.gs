/**
 * Gmail Auto-Filter Setup for Andy McAteer
 * andy.mcateer@corvallis.k12.or.us
 *
 * HOW TO USE:
 * 1. Go to https://script.google.com
 * 2. Click "New project"
 * 3. Paste this entire script
 * 4. Click Run → select "createAllFilters"
 * 5. Authorize when prompted (grant Gmail access)
 * 6. Check the Execution Log for results
 *
 * WHAT IT DOES:
 * - Creates 7 Gmail filters that auto-label incoming mail
 * - Applies labels to ALL existing matching emails retroactively
 * - Some filters skip the inbox (archive), others just label
 *
 * SAFE TO RE-RUN: Won't create duplicate filters
 */

function createAllFilters() {
  const filters = [
    // ── Filter 1: School/Admin ──
    // Already created via Gmail UI. Included here for completeness.
    {
      from: "spreadbury OR parentsquare",
      label: "School/Admin",
      skipInbox: true,
      neverSpam: true,
      description: "Admin broadcasts from Spreadbury & ParentSquare"
    },

    // ── Filter 2: School/Grades ──
    {
      from: "chappy.swearingen OR sherry.dickerson OR csd509j.instructure",
      label: "School/Grades",
      skipInbox: false,
      neverSpam: false,
      description: "Canvas/Synergy grade notifications & Chappy/Dickerson"
    },

    // ── Filter 3: School/SPED ──
    {
      from: "panknin OR lisa.mathews OR viramontes OR godsey",
      label: "School/SPED",
      skipInbox: false,
      neverSpam: false,
      description: "SPED team communications"
    },

    // ── Filter 4: Students/Submissions ──
    {
      from: "student.csd509j.net OR onshape.com",
      label: "Students/Submissions",
      skipInbox: true,
      neverSpam: false,
      description: "Student emails & Onshape notifications (auto-archive)"
    },

    // ── Filter 5: CTE ──
    {
      from: "fortd@linnbenton.edu OR nikki.mcfarland",
      label: "CTE",
      skipInbox: false,
      neverSpam: false,
      description: "CTE network — Deron Fort & Nikki McFarland"
    },

    // ── Filter 6: Drift-Trike ──
    {
      from: "colton.hankey@student.csd509j.net",
      label: "Drift-Trike",
      skipInbox: false,
      neverSpam: false,
      description: "Colton's drift trike project emails"
    },

    // ── Filter 7: Purchasing/Orders ──
    {
      from: "robert.parrott",
      hasWords: "order OR purchase OR invoice OR requisition",
      label: "Purchasing/Orders",
      skipInbox: false,
      neverSpam: false,
      description: "Purchase orders from Robert Parrott"
    }
  ];

  Logger.log("═══════════════════════════════════════");
  Logger.log("  Gmail Filter Setup — Andy McAteer");
  Logger.log("═══════════════════════════════════════\n");

  for (const filter of filters) {
    try {
      createFilterAndLabel(filter);
      Logger.log(`✅ ${filter.label}: ${filter.description}`);
    } catch (e) {
      Logger.log(`❌ ${filter.label}: ${e.message}`);
    }
  }

  Logger.log("\n═══════════════════════════════════════");
  Logger.log("  Done! Now retroactively labeling...");
  Logger.log("═══════════════════════════════════════\n");

  // Retroactively label existing emails
  for (const filter of filters) {
    try {
      retroactivelyLabel(filter);
    } catch (e) {
      Logger.log(`⚠️  Retroactive labeling failed for ${filter.label}: ${e.message}`);
    }
  }

  Logger.log("\n🎉 All filters created and existing emails labeled!");
}


/**
 * Creates a Gmail filter using the Gmail API (Advanced Service)
 * Falls back to GmailApp if Advanced Service isn't enabled
 */
function createFilterAndLabel(config) {
  // Ensure the label exists
  let label = GmailApp.getUserLabelByName(config.label);
  if (!label) {
    label = GmailApp.createLabel(config.label);
    Logger.log(`   Created label: ${config.label}`);
  }

  // Build the filter using Gmail Advanced Service
  // NOTE: If Gmail API isn't enabled, we'll just do retroactive labeling
  try {
    const labelId = getLabelId_(config.label);

    const filterResource = {
      criteria: {
        from: config.from
      },
      action: {
        addLabelIds: [labelId],
        removeLabelIds: []
      }
    };

    // Add "has words" criteria if specified
    if (config.hasWords) {
      filterResource.criteria.query = config.hasWords;
    }

    // Skip inbox = remove INBOX label
    if (config.skipInbox) {
      filterResource.action.removeLabelIds.push("INBOX");
    }

    // Never spam = remove SPAM label
    if (config.neverSpam) {
      filterResource.action.removeLabelIds.push("SPAM");
    }

    Gmail.Users.Settings.Filters.create(filterResource, "me");

  } catch (e) {
    if (e.message.includes("is not available")) {
      Logger.log(`   ⚠️  Gmail Advanced Service not enabled. Filter for "${config.label}" will only apply retroactively.`);
      Logger.log(`   → To enable: Extensions > Services > Gmail API > Enable`);
    } else if (e.message.includes("Filter already exists")) {
      Logger.log(`   ℹ️  Filter for "${config.label}" already exists, skipping.`);
    } else {
      throw e;
    }
  }
}


/**
 * Get the Gmail label ID from label name (needed for API calls)
 */
function getLabelId_(labelName) {
  const labels = Gmail.Users.Labels.list("me").labels;
  for (const label of labels) {
    if (label.name === labelName) {
      return label.id;
    }
  }
  throw new Error(`Label "${labelName}" not found`);
}


/**
 * Retroactively applies labels to all existing matching emails
 * This works even without the Gmail Advanced Service
 */
function retroactivelyLabel(config) {
  const label = GmailApp.getUserLabelByName(config.label);
  if (!label) {
    Logger.log(`   ⚠️  Label "${config.label}" not found, skipping retroactive labeling`);
    return;
  }

  // Build search query
  let query = `from:(${config.from})`;
  if (config.hasWords) {
    query += ` {${config.hasWords}}`;
  }

  // Search for matching threads
  const threads = GmailApp.search(query, 0, 500);

  if (threads.length === 0) {
    Logger.log(`   ${config.label}: No matching emails found`);
    return;
  }

  // Apply label to all matching threads
  label.addToThreads(threads);

  // Archive if skipInbox
  if (config.skipInbox) {
    for (const thread of threads) {
      if (thread.isInInbox()) {
        thread.moveToArchive();
      }
    }
    Logger.log(`   ${config.label}: Labeled + archived ${threads.length} threads`);
  } else {
    Logger.log(`   ${config.label}: Labeled ${threads.length} threads`);
  }
}


/**
 * BONUS: Run this separately to label + archive inbox emails by category
 * (This handles emails that don't match any filter above)
 */
function labelRemainingInbox() {
  Logger.log("Scanning inbox for uncategorized emails...\n");

  const additionalRules = [
    { query: 'from:parentsquare', label: 'School/Admin', archive: true },
    { query: 'from:noreply@google.com', label: 'Resources', archive: true },
    { query: 'from:notifications@onshape.com', label: 'Students/Submissions', archive: true },
    { query: 'subject:"staff meeting" OR subject:"professional development"', label: 'School/Events', archive: false },
  ];

  for (const rule of additionalRules) {
    const label = GmailApp.getUserLabelByName(rule.label);
    if (!label) continue;

    const threads = GmailApp.search(`in:inbox ${rule.query}`, 0, 200);
    if (threads.length > 0) {
      label.addToThreads(threads);
      if (rule.archive) {
        GmailApp.moveThreadsToArchive(threads);
      }
      Logger.log(`${rule.label}: ${threads.length} threads labeled${rule.archive ? ' + archived' : ''}`);
    }
  }

  Logger.log("\n✅ Done categorizing remaining inbox emails!");
}


/**
 * Utility: List all current filters (for debugging)
 */
function listExistingFilters() {
  try {
    const filters = Gmail.Users.Settings.Filters.list("me").filter;
    if (!filters || filters.length === 0) {
      Logger.log("No filters found.");
      return;
    }
    Logger.log(`Found ${filters.length} filters:\n`);
    for (const f of filters) {
      const from = f.criteria?.from || "(any)";
      const query = f.criteria?.query || "";
      const labels = f.action?.addLabelIds?.join(", ") || "(none)";
      const removes = f.action?.removeLabelIds?.join(", ") || "(none)";
      Logger.log(`  From: ${from} ${query ? '| Query: ' + query : ''}`);
      Logger.log(`  → Add: ${labels} | Remove: ${removes}\n`);
    }
  } catch (e) {
    Logger.log("Gmail Advanced Service not enabled. Enable it at: Extensions > Services > Gmail API");
  }
}


/**
 * Utility: Delete ALL filters (nuclear option — use carefully)
 */
function deleteAllFilters() {
  try {
    const filters = Gmail.Users.Settings.Filters.list("me").filter;
    if (!filters) {
      Logger.log("No filters to delete.");
      return;
    }
    for (const f of filters) {
      Gmail.Users.Settings.Filters.remove("me", f.id);
    }
    Logger.log(`Deleted ${filters.length} filters.`);
  } catch (e) {
    Logger.log("Error: " + e.message);
  }
}
