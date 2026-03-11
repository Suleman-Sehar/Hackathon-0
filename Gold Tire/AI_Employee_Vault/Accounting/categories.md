# Accounting Categories

**Version:** 0.3 Gold Tier - Phase 4
**Last Updated:** 2026-03-04

---

## Category Rules

### Revenue
**Keywords:** "invoice", "paid", "payment received", "freelance", "sale", "client"

**Examples:**
- Client B Invoice Paid → Revenue
- Freelance Gig → Revenue
- Product Sale → Revenue
- Payment Received → Revenue

### Expense
**Keywords:** "subscription", "fee", "tool", "marketing", "service", "cloud", "supplies"

**Examples:**
- Adobe Subscription → Expense
- Marketing Tools → Expense
- Bank Fee → Expense
- AWS Cloud Services → Expense
- Office Supplies → Expense

---

## Flag for Review

**Automatic flagging conditions:**

1. **High Amount:** Any transaction with |amount| > 10,000 PKR
2. **Pending Status:** Any transaction with status = "pending"
3. **Unusual Category:** Transactions that don't match keywords

---

## Review Process

```
1. Weekly audit reads transactions.csv
2. Flag transactions meeting review conditions
3. Include flagged items in CEO Briefing
4. Move to Approved/ after CEO review
```

---

## Domain Separation

| Domain | Folder | Briefing Section |
|--------|--------|------------------|
| Business | /Business/ | Business Financial Summary |
| Personal | /Personal/ | Personal Finance Summary |

---

**Status:** ✅ Active  
**Audit Schedule:** Every Sunday 11 PM PKT
