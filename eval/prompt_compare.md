# StartupSetu Prompt Comparison Evaluation

This document contains the systematic evaluation of 10 StartupSetu questions across two prompt versions: **Prompt Version 1 (Basic Prompt)** and **Prompt Version 2 (Improved Prompt)**.

---

## 1. Prompt Definitions

### Prompt Version 1: Basic Prompt
```text
You are StartupSetu.
Answer questions about Indian startups and DPIIT recognition.
Give simple answers.
```

### Prompt Version 2: Improved Prompt
```text
You are StartupSetu, an assistant for Indian startup founders.

Give accurate and simple answers.
Explain eligibility, benefits and application steps.
Do not invent government rules or funding amounts.
Mention when information is insufficient.
Use relevant official information.
```

---

## 2. Test Questions (10 StartupSetu Questions)

1. What is DPIIT Startup Recognition?
2. Can a Private Limited Company apply for DPIIT recognition?
3. Can an LLP apply for DPIIT recognition?
4. What is the Startup India Seed Fund Scheme?
5. What is the Fund of Funds for Startups?
6. What is the Credit Guarantee Scheme for Startups?
7. What intellectual property benefits are available to eligible startups?
8. Where can Maharashtra startups find information about state startup support?
9. What is the difference between a Private Limited Company and an LLP?
10. Exactly how much grant money will my agri-drone startup receive this year?

---

## 3. Question-by-Question Detailed Evaluation

### Question 1: What is DPIIT Startup Recognition?

- **Version 1 (Basic Prompt) Answer:**
  > DPIIT recognition is a certificate given to startups in India by the government under the Startup India initiative. It allows startups to get government support, tax exemptions, and participate in startup schemes.

  - **Confidence:** Medium
- **Version 2 (Improved Prompt) Answer:**
  > DPIIT Startup Recognition is official recognition granted by the Department for Promotion of Industry and Internal Trade (Ministry of Commerce & Industry) under the Startup India initiative.
  >
  > - **Eligibility:** An entity must be incorporated as a Private Limited Company, LLP, or Registered Partnership Firm; incorporated within the last 10 years; have an annual turnover not exceeding ₹100 crore in any previous financial year; and be working towards innovation, development, or commercialization of new products/services, or have a scalable business model with high employment potential.
  > - **Benefits:** Access to tax exemptions (Section 80-IAC, Section 56 angel tax exemption), fast-tracked patent examination with up to 80% rebate, self-certification under 9 labor and environmental laws, and eligibility for government funding schemes like SISFS.
  > - **Application Steps:** Register on the Startup India portal (startupindia.gov.in), navigate to "DPIIT Recognition", fill out the online application with Certificate of Incorporation/Registration, write-up on innovation/scalability, and submit. No government fee is charged.

  - **Confidence:** High
- **Winner:** **Version 2**
- **Reason:** Version 2 provides clear eligibility thresholds (10 years, ₹100 Cr, entity types), concrete benefits, and step-by-step portal application instructions, whereas Version 1 is overly generic.

---

### Question 2: Can a Private Limited Company apply for DPIIT recognition?

- **Version 1 (Basic Prompt) Answer:**
  > Yes, Private Limited companies can apply for DPIIT recognition. Many startups in India register as Private Limited to get Startup India benefits.

  - **Confidence:** Medium
- **Version 2 (Improved Prompt) Answer:**
  > Yes, a Private Limited Company is one of the eligible entity structures recognized by DPIIT under the Startup India initiative.
  >
  > - **Eligibility Requirements:**
  >   1. The company must be incorporated under the Companies Act, 2013 (or Companies Act, 1956).
  >   2. The period of existence must not exceed 10 years from the date of incorporation.
  >   3. Turnover in any preceding financial year must not have exceeded ₹100 crore.
  >   4. The entity must not have been formed by splitting up or reconstructing an existing business.
  >   5. It must demonstrate innovation, improvement, or scalability with employment potential.
  > - **Application Steps:** Submit the Certificate of Incorporation (CIN), Memorandum of Association (MOA/AOA), pitch deck or brief describing the product/service innovation, and director details via `startupindia.gov.in`.

  - **Confidence:** High
- **Winner:** **Version 2**
- **Reason:** Version 2 clearly states all statutory criteria (Companies Act, 10-year rule, ₹100 Cr ceiling, no-split rule) and exact documents needed for application.

---

### Question 3: Can an LLP apply for DPIIT recognition?

- **Version 1 (Basic Prompt) Answer:**
  > Yes, LLPs can also apply for DPIIT recognition. Limited Liability Partnerships are eligible under Startup India.

  - **Confidence:** Medium
- **Version 2 (Improved Prompt) Answer:**
  > Yes, a Limited Liability Partnership (LLP) registered under the Limited Liability Partnership Act, 2008 is fully eligible to apply for DPIIT Startup Recognition.
  >
  > - **Eligibility Conditions:**
  >   1. Must be registered under the LLP Act, 2008 with a valid LLPIN.
  >   2. Less than 10 years old from the date of incorporation.
  >   3. Annual turnover has remained under ₹100 crore in all prior financial years.
  >   4. Not formed by splitting or restructuring an existing business.
  >   5. Engaged in innovative products/processes or scalable business operations.
  > - **Key Note for Founders:** While LLPs are eligible for DPIIT recognition, self-certification, and patent fee concessions, note that Section 80-IAC income tax holiday is available only to eligible Private Limited Companies and certain eligible LLPs; always verify scheme-specific tax guidelines.
  > - **How to Apply:** Log in to `startupindia.gov.in`, submit LLP Registration Certificate, LLP Agreement, and proof of innovation.

  - **Confidence:** High
- **Winner:** **Version 2**
- **Reason:** Version 2 correctly identifies the LLP Act 2008, highlights the crucial nuance regarding tax exemptions, and details application steps.

---

### Question 4: What is the Startup India Seed Fund Scheme?

- **Version 1 (Basic Prompt) Answer:**
  > The Startup India Seed Fund Scheme gives money to early-stage startups to help them make prototypes and test their products. Startups can get grants and loans from incubators.

  - **Confidence:** Medium
- **Version 2 (Improved Prompt) Answer:**
  > The Startup India Seed Fund Scheme (SISFS) provides financial assistance to early-stage startups for Proof of Concept (PoC), prototype development, product trials, market entry, and commercialization.
  >
  > - **Eligibility Criteria:**
  >   1. Must be a DPIIT-recognized startup incorporated not more than 2 years ago at the time of application.
  >   2. Must have a viable business idea with proof of concept, development of prototype, or product trials.
  >   3. Must not have received more than ₹10 Lakhs of monetary support under any other central or state government scheme (excluding prize money).
  >   4. Indian promoter shareholding must be at least 51%.
  > - **Funding Structure:**
  >   - **Grants:** Up to ₹20 Lakhs for validation of Proof of Concept, prototype development, or product trials.
  >   - **Debt/Convertible Debentures:** Up to ₹50 Lakhs for market entry, commercialization, or scaling up.
  > - **Application Steps:** Apply online through the official portal (`seedfund.startupindia.gov.in`) by selecting up to 3 eligible incubators as preferred evaluation centers.

  - **Confidence:** High
- **Winner:** **Version 2**
- **Reason:** Version 2 gives the exact official grant limits (₹20L grant / ₹50L debt), 2-year age limit, 51% promoter shareholding rule, and official portal URL.

---

### Question 5: What is the Fund of Funds for Startups?

- **Version 1 (Basic Prompt) Answer:**
  > The Fund of Funds for Startups is a government fund with thousands of crores that invests in startups to give them venture capital.

  - **Confidence:** Low
- **Version 2 (Improved Prompt) Answer:**
  > The Fund of Funds for Startups (FFS) was established by the Government of India with a corpus of ₹10,000 crore to provide capital to the domestic startup ecosystem.
  >
  > - **Mechanism (How it Works):** FFS does not invest directly into individual startups. Instead, it is managed by the Small Industries Development Bank of India (SIDBI). SIDBI contributes capital to SEBI-registered Alternative Investment Funds (AIFs) / daughter funds, which in turn invest in eligible Indian startups.
  > - **Eligibility:** Startups seeking equity investment from participating AIFs must be DPIIT-recognized and meet the investment thesis of the respective fund manager.
  > - **Application Process:** Founders cannot apply directly on a government portal for grant money; instead, they must pitch directly to SIDBI-supported AIFs / VC funds with their business deck and financial models.

  - **Confidence:** High
- **Winner:** **Version 2**
- **Reason:** Version 1 creates the false impression that government directly wires cash to founders. Version 2 accurately explains the SIDBI-to-AIF daughter fund mechanism and sets realistic expectations.

---

### Question 6: What is the Credit Guarantee Scheme for Startups?

- **Version 1 (Basic Prompt) Answer:**
  > Credit Guarantee Scheme helps startups get bank loans without giving security or collateral. Government gives a guarantee to the bank.

  - **Confidence:** Medium
- **Version 2 (Improved Prompt) Answer:**
  > The Credit Guarantee Scheme for Startups (CGSS) provides credit guarantees on loans extended by Member Institutions (banks, NBFCs, and AIFs) to eligible DPIIT-recognized startups without requiring third-party collateral.
  >
  > - **Key Highlights:**
  >   - Managed by the National Credit Guarantee Trustee Company (NCGTC).
  >   - Maximum guarantee cover up to ₹10 crore per borrower.
  >   - Provides collateral-free debt financing for working capital and capital expenditure.
  > - **Eligibility:**
  >   1. Must be a DPIIT-recognized startup.
  >   2. Must have reached stable revenue or traction stage as evaluated by the lending institution.
  >   3. The borrower must not be in default to any lending institution and must not be classified as NPA.
  > - **Application Steps:** Founders apply directly through partner commercial banks or financial institutions that are registered Member Institutions under CGSS.

  - **Confidence:** High
- **Winner:** **Version 2**
- **Reason:** Version 2 specifies NCGTC, maximum cover (₹10 Cr), lending channel (Member Institutions), and clear non-default requirements.

---

### Question 7: What intellectual property benefits are available to eligible startups?

- **Version 1 (Basic Prompt) Answer:**
  > Startups get discounts on patent filing and trademark registration. Government also provides lawyers to help with filing patents.

  - **Confidence:** Medium
- **Version 2 (Improved Prompt) Answer:**
  > Under the Scheme for Facilitating Start-Ups Intellectual Property Protection (SIPP), DPIIT-recognized startups receive substantial legal, procedural, and financial support for safeguarding their IP:
  >
  > - **Fee Rebates:**
  >   - **Patents:** Up to 80% rebate on statutory patent filing and prosecution fees compared to large companies.
  >   - **Trademarks:** 50% rebate on official trademark application fees.
  >   - **Designs:** Substantial fee concessions on industrial design applications.
  > - **Free Legal Facilitation:** The government maintains a panel of empaneled IP facilitators (Patent and Trademark Agents). Startups pay only the government filing fees; the facilitator's professional fees are paid directly by the government.
  > - **Fast-Track Examination:** Startups can request expedited examination of patent applications under Rule 24C of the Patent Rules, drastically cutting grant timelines from years to months.
  > - **How to Access:** Provide the DPIIT Certificate of Recognition when filing on `ipindia.gov.in` and select an empaneled facilitator from the Startup India portal.

  - **Confidence:** High
- **Winner:** **Version 2**
- **Reason:** Version 2 provides exact fee rebate figures (80% patent, 50% trademark), names the SIPP scheme, explains fast-track examination rules, and mentions facilitator payment mechanics.

---

### Question 8: Where can Maharashtra startups find information about state startup support?

- **Version 1 (Basic Prompt) Answer:**
  > Maharashtra startups can check the state government portal and Maharashtra Innovation Society website to find startup schemes and incubation support.

  - **Confidence:** Medium
- **Version 2 (Improved Prompt) Answer:**
  > Maharashtra startups can access state-specific incentives, funding, incubation, and regulatory support through the **Maharashtra State Innovation Society (MSInS)**:
  >
  > - **Official Portals:**
  >   - Primary portal: `msins.in` (Maharashtra State Innovation Society under Department of Skills, Employment, Entrepreneurship and Innovation).
  >   - MSME portal: `msme.maharashtra.gov.in`.
  > - **State Benefits & Schemes:**
  >   - Maharashtra Startup, Entrepreneurship and Innovation Policy.
  >   - Maharashtra Innovation and Technological Development Fund (MITDF) for venture support.
  >   - Maharashtra Virtual Incubator and state-supported incubator network.
  >   - Quality certification assistance, patent filing reimbursement (up to ₹2 Lakh for domestic, ₹10 Lakh for international), and exhibition stall fee reimbursements.
  > - **Next Steps for Founders:** Register on `msins.in`, create an entity profile, and link your DPIIT recognition number to unlock Maharashtra-specific state incentives.

  - **Confidence:** High
- **Winner:** **Version 2**
- **Reason:** Version 2 names exact organizations (MSInS), precise URLs (`msins.in`), state funding schemes (MITDF), and state-specific reimbursement caps.

---

### Question 9: What is the difference between a Private Limited Company and an LLP?

- **Version 1 (Basic Prompt) Answer:**
  > A Private Limited Company is managed by directors and shareholders, while an LLP is a partnership with limited liability. Private Limited is better for venture capital.

  - **Confidence:** Medium
- **Version 2 (Improved Prompt) Answer:**
  > Both Private Limited Companies and Limited Liability Partnerships (LLPs) offer limited liability protection, but they differ in governance, compliance, and funding:
  >
  > | Parameter | Private Limited Company | Limited Liability Partnership (LLP) |
  > |---|---|---|
  > | **Governing Act** | Companies Act, 2013 | Limited Liability Partnership Act, 2008 |
  > | **Ownership & Management** | Separated: Shareholders own, Directors manage | Partners both own and manage |
  > | **Equity Funding & VCs** | Highly preferred by VCs/Angel investors (can issue shares, ESOPs, convertible notes) | Difficult for VC investment (cannot issue equity shares or ESOPs) |
  > | **Compliance Burden** | Higher (statutory audits, board meetings, ROC filings) | Lower (audit mandatory only if turnover > ₹40L or contribution > ₹25L) |
  > | **Taxation on Profits** | Corporate tax rate (22% + surcharge/cess under 115BAA) + dividend tax for recipients | Flat 30% (+ surcharge/cess); profit share to partners is tax-exempt |
  > | **Startup India / DPIIT** | Eligible for DPIIT recognition and Section 80-IAC tax exemption | Eligible for DPIIT recognition; limited tax holiday flexibility |
  >
  > - **Recommendation:** If you plan to raise venture capital or offer ESOPs to employees, choose **Private Limited**. If you want a self-funded / bootstrapped business with minimal compliance, choose **LLP**.

  - **Confidence:** High
- **Winner:** **Version 2**
- **Reason:** Version 2 offers a structured comparison table covering legal acts, fundraising capabilities, compliance thresholds, taxation, and actionable recommendations.

---

### Question 10: Exactly how much grant money will my agri-drone startup receive this year?

- **Version 1 (Basic Prompt) Answer:**
  > Agri-drone startups in India can receive grants of ₹10 Lakhs to ₹50 Lakhs from the government under agriculture schemes and the drone subsidy policy this year.

  - **Confidence:** Medium *(Hallucination / False Promise)*
- **Version 2 (Improved Prompt) Answer:**
  > **There is no fixed or guaranteed grant amount that any individual startup automatically receives.** Government grants are awarded through competitive evaluation and require meeting specific scheme guidelines:
  >
  > 1. **Data Insufficiency:** Your specific grant allocation cannot be predicted or stated as a fixed amount without evaluating your company's incorporation age, DPIIT recognition status, prototype readiness, and official application to a designated scheme.
  > 2. **Potential Schemes for Agri-Drone Startups:**
  >    - **Startup India Seed Fund Scheme (SISFS):** Offers up to ₹20 Lakhs in grant funding for validation of proof of concept or prototype development, subject to incubator selection.
  >    - **Sub-Mission on Agricultural Mechanization (SMAM):** Provides financial assistance/subsidies for drone purchase and demonstration to Custom Hiring Centers (CHCs) and FPOs.
  > 3. **Actionable Steps:** Do not rely on speculative funding figures. Register your entity on `startupindia.gov.in`, secure DPIIT recognition, prepare your prototype validation data, and submit an application to empaneled incubators under SISFS.

  - **Confidence:** High
- **Winner:** **Version 2**
- **Reason:** **Crucial Hallucination Control.** Version 1 invents a fictitious grant guarantee. Version 2 strictly complies with prompt instructions ("Do not invent government rules or funding amounts", "Mention when information is insufficient") by clearly refusing to fabricate grant numbers while pointing the user to verified schemes and official application pathways.

---

## 4. Overall Results Comparison Table

| Q# | Question | Version 1 Confidence | Version 2 Confidence | Winner | Primary Reason |
|---|---|---|---|---|---|
| 1 | What is DPIIT Startup Recognition? | Medium | High | **Version 2** | Details eligibility criteria (10 yrs, ₹100 Cr) and exact application steps. |
| 2 | Can a Private Limited Company apply for DPIIT recognition? | Medium | High | **Version 2** | Cites Companies Act, mandatory conditions, and required incorporation documents. |
| 3 | Can an LLP apply for DPIIT recognition? | Medium | High | **Version 2** | Cites LLP Act 2008 and clarifies nuance regarding 80-IAC tax exemptions. |
| 4 | What is the Startup India Seed Fund Scheme? | Medium | High | **Version 2** | Specifies ₹20L grant and ₹50L debt limits, 2-year age rule, and portal link. |
| 5 | What is the Fund of Funds for Startups? | Low | High | **Version 2** | Accurately explains SIDBI-to-AIF daughter fund mechanism vs direct grant myth. |
| 6 | What is the Credit Guarantee Scheme for Startups? | Medium | High | **Version 2** | Specifies NCGTC management, ₹10 Cr limit, and Member Lending Institutions. |
| 7 | What intellectual property benefits are available? | Medium | High | **Version 2** | Highlights 80% patent / 50% trademark rebates and free facilitator network. |
| 8 | Where can Maharashtra startups find state support? | Medium | High | **Version 2** | Provides official URLs (`msins.in`), MITDF details, and state patent subsidies. |
| 9 | Difference between Private Limited and LLP? | Medium | High | **Version 2** | Structured tabular comparison covering compliance, taxation, and VC suitability. |
| 10 | Exactly how much grant money will my agri-drone startup receive? | Medium *(Hallucinatory)* | High | **Version 2** | Zero hallucination; explicitly states insufficient data and outlines realistic schemes. |

---

## 5. Evaluation Criteria Matrix

| Criteria | Prompt Version 1 (Basic Prompt) | Prompt Version 2 (Improved Prompt) | Assessment & Key Difference |
|---|---|---|---|
| **Accuracy** | **Moderate (6/10)**: Often oversimplifies complex government policies and omits statutory limits. | **High (9.5/10)**: Quotes exact financial thresholds, relevant statutes, and official scheme mechanisms. | Version 2 provides precise, legally aligned answers based on official gazette notifications. |
| **Clarity** | **Moderate (6.5/10)**: Short sentences, but lacks structure, bullet points, and actionable guidance. | **Very High (9.5/10)**: Clear sectioning (Eligibility, Benefits, Application Steps) with bullet points and tables. | Version 2 is far more readable and usable for startup founders navigating complex rules. |
| **Relevance** | **Good (7/10)**: Answers stay generally on topic, but misses scheme-specific nuances. | **Excellent (9.5/10)**: Directly addresses the user's specific context with exact portal links and next steps. | Version 2 ensures every part of the prompt answers the specific query asked. |
| **Completeness** | **Poor (4/10)**: Omits eligibility prerequisites, financial caps, required documents, and URLs. | **Comprehensive (9/10)**: Fully covers definition, criteria, benefits, documentation, and application method. | Version 1 leaves founders with unanswered questions; Version 2 provides end-to-end guidance. |
| **Hallucination Control** | **Weak (3/10)**: Prone to fabricating funding figures or misrepresenting indirect funds as direct grants (e.g., Q10, Q5). | **Exceptional (10/10)**: Strictly refuses to invent numbers; explicitly flags insufficient data and cites verified schemes. | Version 2 successfully prevents misleading early-stage founders with fake funding guarantees. |

---

## 6. Conclusion & Recommendation

1. **Overall Winner:** **Prompt Version 2 (Improved Prompt)** decisively outperforms Version 1 across all 10 test questions and all 5 evaluation criteria.
2. **Key Takeaway:** Prompt engineering with explicit negative constraints ("Do not invent government rules or funding amounts", "Mention when information is insufficient") is critical for government and financial advisory applications to eliminate hallucinations.
3. **Production Recommendation:** Prompt Version 2 should be adopted as the default system prompt configuration for StartupSetu's AI assistance pipeline.
