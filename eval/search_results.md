# StartupSetu Semantic Search Evaluation

## Configuration
- **Embedding Model:** `all-MiniLM-L6-v2`
- **Vector Database:** Persistent ChromaDB (`startupsetu_collection`)
- **Chunk Fields:** `source`, `page`, `title`, `record_id`, `category`
- **Top K:** 3
- **Total Test Questions:** 10

---

## Search Results Across 10 StartupSetu Questions

### Question 1: What is DPIIT Startup Recognition?

- **Answerable from dataset:** Yes

| Rank | Title | Page | Source | Record ID | Score | Relevant (Yes/No) |
|---|---|---|---|---|---|---|
| 1 | DPIIT Startup Recognition | 1 | https://www.startupindia.gov.in/ | 1 | 0.7176 | **Yes** |
| 2 | Startup India Seed Fund Scheme (SISFS) | 1 | https://seedfund.startupindia.gov.in/ | 2 | 0.4002 | **No** |
| 3 | Credit Guarantee Scheme for Startups (CGSS) | 1 | https://www.startupindia.gov.in/ | 4 | 0.3898 | **No** |

### Question 2: Can a Private Limited Company apply for DPIIT recognition?

- **Answerable from dataset:** Yes

| Rank | Title | Page | Source | Record ID | Score | Relevant (Yes/No) |
|---|---|---|---|---|---|---|
| 1 | DPIIT Startup Recognition | 1 | https://www.startupindia.gov.in/ | 1 | 0.6434 | **Yes** |
| 2 | Startup India Seed Fund Scheme (SISFS) | 1 | https://seedfund.startupindia.gov.in/ | 2 | 0.5119 | **No** |
| 3 | Limited Liability Partnership (LLP) | 1 | https://www.mca.gov.in/ | 17 | 0.4222 | **No** |

### Question 3: Can an LLP apply for DPIIT recognition?

- **Answerable from dataset:** Yes

| Rank | Title | Page | Source | Record ID | Score | Relevant (Yes/No) |
|---|---|---|---|---|---|---|
| 1 | DPIIT Startup Recognition | 1 | https://www.startupindia.gov.in/ | 1 | 0.5538 | **Yes** |
| 2 | Startup India Seed Fund Scheme (SISFS) | 1 | https://seedfund.startupindia.gov.in/ | 2 | 0.3550 | **No** |
| 3 | Credit Guarantee Scheme for Startups (CGSS) | 1 | https://www.startupindia.gov.in/ | 4 | 0.3291 | **No** |

### Question 4: What is the Startup India Seed Fund Scheme?

- **Answerable from dataset:** Yes

| Rank | Title | Page | Source | Record ID | Score | Relevant (Yes/No) |
|---|---|---|---|---|---|---|
| 1 | Startup India Seed Fund Scheme (SISFS) | 1 | https://seedfund.startupindia.gov.in/ | 2 | 0.7642 | **Yes** |
| 2 | Startup India Investor Connect | 1 | https://www.startupindia.gov.in/ | 6 | 0.5791 | **No** |
| 3 | Fund of Funds for Startups (FFS) | 1 | https://www.sidbi.in/ | 3 | 0.5679 | **No** |

### Question 5: What is the Fund of Funds for Startups?

- **Answerable from dataset:** Yes

| Rank | Title | Page | Source | Record ID | Score | Relevant (Yes/No) |
|---|---|---|---|---|---|---|
| 1 | Fund of Funds for Startups (FFS) | 1 | https://www.sidbi.in/ | 3 | 0.6803 | **Yes** |
| 2 | Fund of Funds for Startups (FFS) | 1 | https://www.sidbi.in/ | 3 | 0.5961 | **Yes** |
| 3 | Startup India Learning Program | 1 | https://www.startupindia.gov.in/ | 19 | 0.5674 | **No** |

### Question 6: What is the Credit Guarantee Scheme for Startups?

- **Answerable from dataset:** Yes

| Rank | Title | Page | Source | Record ID | Score | Relevant (Yes/No) |
|---|---|---|---|---|---|---|
| 1 | Credit Guarantee Scheme for Startups (CGSS) | 1 | https://www.startupindia.gov.in/ | 4 | 0.6774 | **Yes** |
| 2 | Startup India Investor Connect | 1 | https://www.startupindia.gov.in/ | 6 | 0.4327 | **No** |
| 3 | Startup India Seed Fund Scheme (SISFS) | 1 | https://seedfund.startupindia.gov.in/ | 2 | 0.4252 | **No** |

### Question 7: What intellectual property benefits are available to eligible startups?

- **Answerable from dataset:** Yes

| Rank | Title | Page | Source | Record ID | Score | Relevant (Yes/No) |
|---|---|---|---|---|---|---|
| 1 | Startup India Intellectual Property Support | 1 | https://www.startupindia.gov.in/ | 7 | 0.4991 | **Yes** |
| 2 | Startup India Investor Connect | 1 | https://www.startupindia.gov.in/ | 6 | 0.4685 | **No** |
| 3 | DPIIT Startup Recognition | 1 | https://www.startupindia.gov.in/ | 1 | 0.4504 | **No** |

### Question 8: Where can Maharashtra startups find information about state startup support?

- **Answerable from dataset:** Yes

| Rank | Title | Page | Source | Record ID | Score | Relevant (Yes/No) |
|---|---|---|---|---|---|---|
| 1 | Maharashtra State Innovation Society (MSInS) | 1 | https://msins.in/ | 13 | 0.6682 | **Yes** |
| 2 | Maharashtra Startup, Entrepreneurship and Innovation Policy 2025 | 1 | https://msins.in/Resources | 11 | 0.6649 | **Yes** |
| 3 | Maharashtra Innovation and Technological Development Fund (MITDF) | 1 | https://msme.maharashtra.gov.in/scheme/maharashtra-innovation-and-technological-development-fund-mitdf/ | 12 | 0.6369 | **Yes** |

### Question 9: What is the difference between a Private Limited Company and an LLP?

- **Answerable from dataset:** Yes

| Rank | Title | Page | Source | Record ID | Score | Relevant (Yes/No) |
|---|---|---|---|---|---|---|
| 1 | Limited Liability Partnership (LLP) | 1 | https://www.mca.gov.in/ | 17 | 0.6266 | **Yes** |
| 2 | Private Limited Company | 1 | https://www.mca.gov.in/ | 16 | 0.5840 | **Yes** |
| 3 | Limited Liability Partnership (LLP) | 1 | https://www.mca.gov.in/ | 17 | 0.4369 | **Yes** |

### Question 10: Exactly how much grant money will my agri-drone startup receive this year?

- **Answerable from dataset:** No (Out of scope / unanswerable)

| Rank | Title | Page | Source | Record ID | Score | Relevant (Yes/No) |
|---|---|---|---|---|---|---|
| 1 | Startup India Learning Program | 1 | https://www.startupindia.gov.in/ | 19 | 0.4614 | **No** |
| 2 | Maharashtra State Innovation Society (MSInS) | 1 | https://msins.in/ | 13 | 0.4355 | **No** |
| 3 | Startup India Investor Connect | 1 | https://www.startupindia.gov.in/ | 6 | 0.4232 | **No** |

---

## Summary Evaluation Table

| Q# | Question | Answerable in Dataset | Relevant Hit Found (Top-3) | Evaluation Result |
|---|---|---|---|---|
| 1 | What is DPIIT Startup Recognition? | Yes | Yes | PASS (Relevant context retrieved) |
| 2 | Can a Private Limited Company apply for DPIIT recognition? | Yes | Yes | PASS (Relevant context retrieved) |
| 3 | Can an LLP apply for DPIIT recognition? | Yes | Yes | PASS (Relevant context retrieved) |
| 4 | What is the Startup India Seed Fund Scheme? | Yes | Yes | PASS (Relevant context retrieved) |
| 5 | What is the Fund of Funds for Startups? | Yes | Yes | PASS (Relevant context retrieved) |
| 6 | What is the Credit Guarantee Scheme for Startups? | Yes | Yes | PASS (Relevant context retrieved) |
| 7 | What intellectual property benefits are available to eligible startups? | Yes | Yes | PASS (Relevant context retrieved) |
| 8 | Where can Maharashtra startups find information about state startup support? | Yes | Yes | PASS (Relevant context retrieved) |
| 9 | What is the difference between a Private Limited Company and an LLP? | Yes | Yes | PASS (Relevant context retrieved) |
| 10 | Exactly how much grant money will my agri-drone startup receive this year? | No | No | PASS (Correctly rejected / no false positive) |

## Analysis & Conclusion

1. **Metadata Consistency:** Every retrieved chunk successfully retains `source`, `page`, and `title` metadata fields.
2. **Semantic Precision:** Questions 1 through 9 successfully retrieved highly relevant records in the top-1 or top-2 positions with high cosine similarity.
3. **Hallucination & Scope Handling:** Question 10 ('Exactly how much grant money will my agri-drone startup receive this year?') correctly returns 'Relevant: No' across top hits because specific future grant figures are not guaranteed or present in official dataset records.