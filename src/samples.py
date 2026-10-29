"""Clearly labelled SYNTHETIC inquiries for demo and testing. Not real customer data."""

SAMPLES = [
    {
        "name": "Hot: AI support chatbot (clear brief)",
        "expected_category": "Chatbot / AI Agent",
        "text": (
            "Hi, I'm Rohan Mehta, CEO of Brightcart Retail. We need an AI chatbot for our website "
            "and WhatsApp that answers order-status questions and escalates to humans.\n"
            "- Integrate with our Shopify store and Zendesk\n"
            "- Support English and Hindi\n"
            "- Weekly analytics dashboard\n"
            "Our budget is around INR 3 lakh and we want to launch within 8 weeks. "
            "Reach me at rohan@brightcart.example"
        ),
    },
    {
        "name": "Warm: invoice extraction (no budget)",
        "expected_category": "Document Processing",
        "text": (
            "Hello, this is Priya Nair from Medline Distributors. We receive 400 scanned invoices a month "
            "and want to extract vendor, amount and date into our accounting system automatically. "
            "We would like it done in 3 months. priya@medline.example"
        ),
    },
    {
        "name": "Cold: vague inquiry",
        "expected_category": "Other",
        "text": "hey do u guys make apps? just exploring, no rush. let me know",
    },
    {
        "name": "Hot: urgent CRM automation",
        "expected_category": "CRM / Workflow Automation",
        "text": (
            "URGENT: I'm Aman Verma, founder of Growthly Agency. Our CRM follow-up process is manual and "
            "we are losing leads. We need workflow automation that sends follow-ups and updates the pipeline.\n"
            "1. Connect to HubSpot\n2. Auto-assign leads to sales reps\n3. Daily summary report\n"
            "Budget $4,000, need it in 3 weeks. aman@growthly.example"
        ),
    },
    {
        "name": "Warm: SaaS dashboard",
        "expected_category": "Web / SaaS Development",
        "text": (
            "We are a logistics startup building a SaaS dashboard for fleet owners to track deliveries. "
            "We need user login, live map view and billing. Timeline is about 5 months. "
            "Contact: ops@fleetly.example"
        ),
    },
]
