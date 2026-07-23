QUESTIONNAIRE_CONFIG = {
    "Website Development": [
        {
            "id": "website_purpose",
            "label": "What is the primary purpose of your website?",
            "type": "textarea",
            "required": True
        },
        {
            "id": "website_pages",
            "label": "Approximately how many pages do you need?",
            "type": "select",
            "options": ["1-5", "6-10", "11-20", "20+"],
            "required": False
        },
        {
            "id": "website_features",
            "label": "Do you have any reference websites you like?",
            "type": "url",
            "required": False
        }
    ],

    "Branding": [
        {
            "id": "brand_existing",
            "label": "Do you have an existing brand identity (logo, colors, fonts)?",
            "type": "select",
            "options": ["Yes, fully established", "Yes, partially", "No, need full branding"],
            "required": True
        },
        {
            "id": "brand_tone",
            "label": "Describe the tone and personality of your brand.",
            "type": "textarea",
            "required": True
        },
        {
            "id": "brand_competitors",
            "label": "Who are your main competitors? (Optional)",
            "type": "textarea",
            "required": False
        },
        {
            "id": "brand_deliverables",
            "label": "What specific branding deliverables do you need?",
            "type": "select",
            "options": ["Logo only", "Logo + Stationery", "Full Brand Identity (Logo, Colors, Fonts, Guidelines)", "Complete Branding Package"],
            "required": True
        }
    ],

    "E-Commerce Solution": [
        {
            "id": "ecommerce_products",
            "label": "How many products do you plan to sell initially?",
            "type": "select",
            "options": ["Less than 50", "50-200", "200-1000", "1000+"],
            "required": True
        },
        {
            "id": "ecommerce_payment",
            "label": "What payment gateways do you need?",
            "type": "checkbox",
            "options": ["M-Pesa", "PayPal", "Credit/Debit Card", "Bank Transfer"],
            "required": True
        },
        {
            "id": "ecommerce_shipping",
            "label": "Do you need shipping/delivery integration?",
            "type": "select",
            "options": ["Yes", "No", "Not sure yet"],
            "required": True
        },
        {
            "id": "ecommerce_existing",
            "label": "Do you have an existing e-commerce platform you want to migrate from?",
            "type": "textarea",
            "required": False
        }
    ],

    "SaaS Dashboard": [
        {
            "id": "saas_users",
            "label": "How many users do you expect initially?",
            "type": "select",
            "options": ["Less than 50", "50-200", "200-1000", "1000+"],
            "required": True
        },
        {
            "id": "saas_features",
            "label": "What core features does your SaaS need?",
            "type": "textarea",
            "required": True
        },
        {
            "id": "saas_integrations",
            "labels": "What third-party integrations do you need? (e.g., payment, email, analytics)",
            "type": "textarea",
            "required": False
        },
        {
            "id": "saas_existing",
            "label": "Do you have an existing platform you want to replace or integrate with?",
            "type": "textarea",
            "required": False
        }
    ],

    "Custom CMS": [
        {
            "id": "cms_content_types",
            "label": "What types of content will you manage? (e.g., blog, products, portfolio)",
            "type": "textarea",
            "required": True
        },
        {
            "id": "cms_users",
            "label": "How many content editors will use the CMS?",
            "type": "select",
            "options": ["1-5", "6-20", "21-50", "50+"],
            "required": True
        },
        {
            "id": "cms_features",
            "label": "What specific CMS features do you need?",
            "type": "textarea",
            "required": True
        }
    ],
    "Mobile App": [
        {
            "id": "app_platform",
            "label": "Which platforms do you need?",
            "type": "checkbox",
            "options": ["iOS", "Android", "Both"],
            "required": True
        },
        {
            "id": "app_features",
            "label": "What are the core features of your app?",
            "type": "textarea",
            "required": True
        },
        {
            "id": "app_users",
            "label": "How many users do you expect initially?",
            "type": "select",
            "options": ["Less than 1000", "1000-5000", "5000-20000", "20000+"],
            "required": True
        },
        {
            "id": "app_existing",
            "label": "Do you have an existing app or designs?",
            "type": "textarea",
            "required": False
        }
    ]
}
