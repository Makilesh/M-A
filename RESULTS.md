# E2E RAG Pipeline Validation Results

This document contains the actual execution results of the M&A Due Diligence Intelligence Engine run against the real **golden QA set**.

## Run Summary
- **Timestamp**: 2026-06-22 00:26:48
- **Deal ID**: `aurora_vertex_2024`
- **Total Queries Evaluated**: 19
- **Successfully Completed**: 14/19
- **Average E2E Latency**: 59113.53 ms
- **Average Grounding Fact Recall**: 32.9%
- **Citations Grounding Match**: 5/14 (35.7% of successful runs)

## Metrics by Query Type

| Query Type | Count | Success | Avg Recall | Avg Latency (ms) |
| --- | --- | --- | --- | --- |
| Financial | 5 | 5/5 | 72.0% | 84940.60 |
| Legal | 5 | 4/5 | 25.0% | 50600.00 |
| Comparative | 3 | 2/3 | 0.0% | 45797.00 |
| Summary | 2 | 1/2 | 0.0% | 34156.50 |
| Multi_hop | 4 | 2/4 | 0.0% | 59937.50 |

## Detailed Query Output Reports

### fin_01 (Financial)
**Query**: What was Aurora's total revenue in FY2023 and how does it compare to FY2022?

- **Status**: ✅ PASS
- **Confidence Score**: 1.00
- **Validation Status**: passed
- **Facts Recalled**: 4/4 (100.0%)
  - *Recalled*: ['$452.8', '$387.1', '17.0%', 'growth']
- **Citations Match**: ✅ Yes
- **Total Latency**: 67688.00 ms
- **Answer**:
```
### 1. Direct Answer

* **FY2023 Total Revenue:** $452.8 million USD
* **FY2022 Total Revenue:** $387.1 million USD
* **Year-over-Year (YoY) Variance:** 
  * **Absolute Variance:** Increase of $65.7 million USD *(computed)*
  * **Percentage Variance:** 17.0% increase (16.97% computed)

---

### 2. Supporting Evidence with Citations

* **FY2023 and FY2022 Revenue Figures:** 
  * In FY2023, Aurora Technologies Inc. recorded total revenue of **$452.8 million USD**, up from **$387.1 million USD** in FY2022 [📄 aurora_financials_fy2023.txt | FY2023 | p.1 | Section: AURORA TECHNOLOGIES INC.].
  * The revenue breakdown for both years is as follows [📄 aurora_financials_fy2023.txt | FY2023 | p.1 | Section: AURORA TECHNOLOGIES INC.]:
    * *Software Licenses:* $198.4 million (FY2023) vs. $172.3 million (FY2022)
    * *SaaS Subscriptions:* $189.6 million (FY2023) vs. $148.2 million (FY2022)
    * *Professional Services:* $64.8 million (FY2023) vs. $66.6 million (FY2022)

* **Year-over-Year Variance:**
  * **Absolute Increase:** $65.7 million USD [📄 aurora_financials_fy2023.txt | FY2023 | p.1 | Section: AURORA TECHNOLOGIES INC. | COMPUTED: FY2023 Revenue ($452.8M) - FY2022 Revenue ($387.1M)].
  * **Percentage Growth:** The company reports a YoY Revenue Growth of **17.0%** [📄 aurora_financials_fy2023.txt | FY2023 | p.3 | Section: Revenue Growth: 17.0% YoY]. *(Note: The exact calculated growth rate is 16.97% [📄 aurora_financials_fy2023.txt | FY2023 | p.1 | COMPUTED: ($65.7M / $387.1M) * 100]).*

---

### 3. Caveats, Inconsistencies, or Missing Information

* **Rounding:** The percentage growth rate of 17.0% stated in the "Key Financial Metrics" section [📄 aurora_financials_fy2023.txt | FY2023 | p.3 | Section: Revenue Growth: 17.0% YoY] is a rounded figure. The precise mathematical variance based on the income statement figures is 16.97%.
* No other inconsistencies or missing data points were identified in the provided financial statements.

---

### 4. Normalized Financial Values (Scale Context)

All values are presented in millions of USD:
* **FY2022 Revenue:** $387,100,000 USD ($387.1M)
* **FY2023 Revenue:** $452,800,000 USD ($452.8M)
* **YoY Revenue Variance:** +$65,700,000 USD (+$65.7M)
```
- **Agent Trace Summary**:
  - **query_intelligence**:  ()
  - **retrieval_executor**:  ()
  - **financial_verifier**:  ()
  - **quality_assessor**:  ()
  - **answer_synthesizer**:  ()

---

### fin_02 (Financial)
**Query**: What is the EBITDA and Adjusted EBITDA for FY2023?

- **Status**: ✅ PASS
- **Confidence Score**: 1.00
- **Validation Status**: passed
- **Facts Recalled**: 4/4 (100.0%)
  - *Recalled*: ['$92.8', '$97.3', 'restructuring', '$4.5']
- **Citations Match**: ✅ Yes
- **Total Latency**: 135562.00 ms
- **Answer**:
```
### 1. Direct Answer

For the fiscal year ended December 31, 2023 (FY2023), Aurora Technologies Inc. reported the following financial metrics:
*   **EBITDA**: **$92.8 million USD** [📄 aurora_financials_fy2023.txt | p. 2 | KEY FINANCIAL METRICS AND NOTES]
*   **Adjusted EBITDA**: **$97.3 million USD** (excluding restructuring charges) [📄 aurora_financials_fy2023.txt | p. 2 | KEY FINANCIAL METRICS AND NOTES]

---

### 2. Supporting Evidence & Reconciliation

The figures are reconciled in the financial statements as follows:

#### **EBITDA Reconciliation (FY2023)**
*   **Operating Income (EBIT)**: $68.0 million [📄 aurora_financials_fy2023.txt | p. 2 | KEY FINANCIAL METRICS AND NOTES]
*   **(+) Depreciation & Amortization**: $24.8 million [📄 aurora_financials_fy2023.txt | p. 2 | KEY FINANCIAL METRICS AND NOTES]
*   **EBITDA**: **$92.8 million** (representing a **20.5% EBITDA Margin**) [📄 aurora_financials_fy2023.txt | p. 2 | KEY FINANCIAL METRICS AND NOTES]

#### **Adjusted EBITDA Reconciliation (FY2023)**
*   **EBITDA**: $92.8 million [📄 aurora_financials_fy2023.txt | p. 2 | KEY FINANCIAL METRICS AND NOTES]
*   **(+) Restructuring Charges**: $4.5 million [📄 aurora_financials_fy2023.txt | p. 2 | KEY FINANCIAL METRICS AND NOTES]
*   **Adjusted EBITDA**: **$97.3 million** (representing a **21.5% Adjusted EBITDA Margin**) [📄 aurora_financials_fy2023.txt | p. 2 | KEY FINANCIAL METRICS AND NOTES]

---

### 3. Caveats, Inconsistencies, and Tool Discrepancies

*   **Verification Tool Error**: The automated *Financial Verification Results* provided in the context metadata contain an error. The tool incorrectly flags **$68.0 million** (FY2023) and **$51.4 million** (FY2022) as "EBITDA" values. However, the source document clearly identifies these figures as **Operating Income (EBIT)** [📄 aurora_financials_fy2023.txt | p. 1 | Operating Income (EBIT) $68.0 $51.4] and [📄 aurora_financials_fy2023.txt | p. 2 | KEY FINANCIAL METRICS AND NOTES]. The actual EBITDA values are $92.8 million (FY2023) and $74.0 million (FY2022).
*   **Restructuring Charges**: Adjusted EBITDA adds back $4.5 million in restructuring charges, which are also listed under Operating Expenses on the Consolidated Income Statement [📄 aurora_financials_fy2023.txt | p. 1 | AURORA TECHNOLOGIES INC.].

---

### 4. Normalized Values (Scale Context)

All financial statement figures are reported in **millions of USD** [📄 aurora_financials_fy2023.txt | p. 1 | AURORA TECHNOLOGIES INC.]. 

*   **EBITDA (FY2023)**: $92,800,000 USD
*   **Adjusted EBITDA (FY2023)**: $97,300,000 USD
```
- **Agent Trace Summary**:
  - **query_intelligence**:  ()
  - **retrieval_executor**:  ()
  - **financial_verifier**:  ()
  - **quality_assessor**:  ()
  - **query_rewriter**:  ()

---

### fin_03 (Financial)
**Query**: What is the company's free cash flow for FY2023 and what were the components?

- **Status**: ✅ PASS
- **Confidence Score**: 0.85
- **Validation Status**: warning
- **Facts Recalled**: 5/5 (100.0%)
  - *Recalled*: ['$64.2', '$78.4', 'operations', '$14.2', 'capital expenditures']
- **Citations Match**: ✅ Yes
- **Total Latency**: 53969.00 ms
- **Answer**:
```
### 1. Direct Answer

The total Free Cash Flow (FCF) for Aurora Technologies Inc. in **FY2023** is **$64.2 million USD** [📄 aurora_financials_fy2023.txt | Page: 2 | Section: ================================================================================].

---

### 2. Detailed Breakdown of Components

The Free Cash Flow is calculated by subtracting Capital Expenditures from Cash from Operations. The detailed breakdown for FY2023 is as follows:

*   **Cash from Operations:** $78.4 million USD [📄 aurora_financials_fy2023.txt | Page: 2 | Section: ================================================================================]
*   **Capital Expenditures:** ($14.2) million USD [📄 aurora_financials_fy2023.txt | Page: 2 | Section: ================================================================================]
*   **Total Free Cash Flow:** **$64.2 million USD** (calculated as $78.4M - $14.2M) [📄 aurora_financials_fy2023.txt | Page: 2 | Section: ================================================================================]

*(Note: All financial figures are reported in millions of USD [📄 aurora_financials_fy2023.txt | Page: 1 | Section: AURORA TECHNOLOGIES INC.]).*

---

### 3. Caveats, Inconsistencies, or Missing Information

*   **No Inconsistencies Found:** The Free Cash Flow calculation is mathematically consistent with the provided financial statements. 
*   **Detailed Cash Flow Statement Missing:** While the summary figures for "Cash from Operations" and "Capital Expenditures" are provided, a full Consolidated Statement of Cash Flows (detailing the specific operating cash adjustments such as working capital changes or stock-based compensation) was not included in the provided context.
```
- **Agent Trace Summary**:
  - **query_intelligence**:  ()
  - **retrieval_executor**:  ()
  - **financial_verifier**:  ()
  - **quality_assessor**:  ()
  - **answer_synthesizer**:  ()

---

### fin_04 (Financial)
**Query**: What is the Net Debt/EBITDA leverage ratio and how has it changed?

- **Status**: ✅ PASS
- **Confidence Score**: 0.75
- **Validation Status**: warning
- **Facts Recalled**: 3/5 (60.0%)
  - *Recalled*: ['0.2x', '0.7x', '$20.6']
  - *Missing*: ['improved', 'deleveraged']
- **Citations Match**: ✅ Yes
- **Total Latency**: 129078.00 ms
- **Answer**:
```
### 1. Direct Answer

For the current period (**FY2023**), the reported **Net Debt/EBITDA leverage ratio is 0.2x** (computed precisely as **0.22x**). 

Compared to the historical period (**FY2022**), where the reported **Net Debt/EBITDA leverage ratio was 0.7x** (computed precisely as **0.67x**), the leverage ratio has **decreased by 0.5x** (or **0.45x** using precise figures). 

This indicates a **strong deleveraging trend** driven by a combination of:
1. A significant reduction in Net Debt (down **58.7%** from $49.9M to $20.6M).
2. Strong growth in EBITDA (up **25.4%** from $74.0M to $92.8M).

The company remains well in compliance with its senior secured revolving credit facility covenant, which requires a Net Debt/EBITDA ratio of $\le$ 3.5x.

---

### 2. Supporting Evidence & Calculations

All financial values are in millions of USD ($M).

#### **A. Net Debt Components**
* **FY2023 (Current Period):**
  * Total Debt (Current + Non-Current): **$110.0M** [📄 aurora_financials_fy2023.txt | Page 3 | Net Debt:]
    * *Derived from: Current Portion of Long-Term Debt ($12.0M) [📄 aurora_financials_fy2023.txt | Page 2 | LIABILITIES AND STOCKHOLDERS' EQUITY] + Long-Term Debt ($98.0M) [📄 aurora_financials_fy2023.txt | Page 2 | Non-Current Liabilities:]*
  * Less: Cash and Cash Equivalents: **($89.4M)** [📄 aurora_financials_fy2023.txt | Page 3 | Net Debt:]
  * **Net Debt:** **$20.6M** [📄 aurora_financials_fy2023.txt | Page 3 | Net Debt:]
* **FY2022 (Historical Period):**
  * Total Debt (Current + Non-Current): **$122.0M** [📄 aurora_financials_fy2023.txt | Page 3 | Net Debt:]
    * *Derived from: Current Portion of Long-Term Debt ($12.0M) [📄 aurora_financials_fy2023.txt | Page 2 | LIABILITIES AND STOCKHOLDERS' EQUITY] + Long-Term Debt ($110.0M) [📄 aurora_financials_fy2023.txt | Page 2 | Non-Current Liabilities:]*
  * Less: Cash and Cash Equivalents: **($72.1M)** [📄 aurora_financials_fy2023.txt | Page 3 | Net Debt:]
  * **Net Debt:** **$49.9M** [📄 aurora_financials_fy2023.txt | Page 3 | Net Debt:]

#### **B. EBITDA Reconciliation**
* **FY2023 (Current Period):**
  * Operating Income (EBIT): **$68.0M** [📄 aurora_financials_fy2023.txt | Page 2 | KEY FINANCIAL METRICS AND NOTES]
  * Depreciation & Amortization: **$24.8M** [📄 aurora_financials_fy2023.txt | Page 2 | KEY FINANCIAL METRICS AND NOTES]
  * **EBITDA:** **$92.8M** [📄 aurora_financials_fy2023.txt | Page 2 | KEY FINANCIAL METRICS AND NOTES]
  * **Adjusted EBITDA** (adding back $4.5M restructuring): **$97.3M** [📄 aurora_financials_fy2023.txt | Page 2 | KEY FINANCIAL METRICS AND NOTES]
* **FY2022 (Historical Period):**
  * Operating Income (EBIT): **$51.4M** [📄 aurora_financials_fy2023.txt | Page 2 | KEY FINANCIAL METRICS AND NOTES]
  * Depreciation & Amortization: **$22.6M** [📄 aurora_financials_fy2023.txt | Page 2 | KEY FINANCIAL METRICS AND NOTES]
  * **EBITDA:** **$74.0M** [📄 aurora_financials_fy2023.txt | Page 2 | KEY FINANCIAL METRICS AND NOTES]
  * **Adjusted EBITDA:** **$74.0M** [📄 aurora_financials_fy2023.txt | Page 2 | KEY FINANCIAL METRICS AND NOTES]

#### **C. Leverage Ratio Calculations**
* **FY2023 (Current Period):**
  * Reported Net Debt/EBITDA: **0.2x** [📄 aurora_financials_fy2023.txt | Page 3 | Net Debt:]
  * Computed Net Debt/EBITDA: $\frac{\$20.6M}{\$92.8M} =$ **0.22x** [COMPUTED: Net Debt/EBITDA FY2023]
  * Computed Net Debt/Adjusted EBITDA: $\frac{\$20.6M}{\$97.3M} =$ **0.21x** [COMP
```
- **Agent Trace Summary**:
  - **query_intelligence**:  ()
  - **retrieval_executor**:  ()
  - **financial_verifier**:  ()
  - **quality_assessor**:  ()
  - **answer_synthesizer**:  ()

---

### fin_05 (Financial)
**Query**: What are the terms of the company's revolving credit facility?

- **Status**: ✅ PASS
- **Confidence Score**: 0.00
- **Validation Status**: passed
- **Facts Recalled**: 0/6 (0.0%)
  - *Recalled*: []
  - *Missing*: ['$150', 'JPMorgan', 'SOFR', '225', 'June 30, 2026', '3.5x']
- **Citations Match**: ❌ No
- **Total Latency**: 38406.00 ms
- **Answer**:
```
I was unable to find sufficient relevant information in the data room to answer this question, even after refining the search. This may mean the relevant documents haven't been uploaded yet, or the question falls outside the scope of the available materials.

Search attempts: 3
Best quality score achieved: 0.00
```
- **Agent Trace Summary**:
  - **query_intelligence**:  ()
  - **retrieval_executor**:  ()
  - **quality_assessor**:  ()
  - **query_rewriter**:  ()
  - **retrieval_executor**:  ()

---

### legal_01 (Legal)
**Query**: What is the per share merger consideration and what premium does it represent?

- **Status**: ✅ PASS
- **Confidence Score**: 0.00
- **Validation Status**: passed
- **Facts Recalled**: 0/4 (0.0%)
  - *Recalled*: []
  - *Missing*: ['$58.00', '42%', '$40.85', '90-day']
- **Citations Match**: ❌ No
- **Total Latency**: 61610.00 ms
- **Answer**:
```
I was unable to find sufficient relevant information in the data room to answer this question, even after refining the search. This may mean the relevant documents haven't been uploaded yet, or the question falls outside the scope of the available materials.

Search attempts: 3
Best quality score achieved: 0.03
```
- **Agent Trace Summary**:
  - **query_intelligence**:  ()
  - **retrieval_executor**:  ()
  - **financial_verifier**:  ()
  - **quality_assessor**:  ()
  - **query_rewriter**:  ()

---

### legal_02 (Legal)
**Query**: What are the termination fee provisions?

- **Status**: ✅ PASS
- **Confidence Score**: 1.00
- **Validation Status**: passed
- **Facts Recalled**: 6/6 (100.0%)
  - *Recalled*: ['$20.88', '3.0%', '$13.92', '2.0%', 'Superior Proposal', 'Company Breach']
- **Citations Match**: ✅ Yes
- **Total Latency**: 78953.00 ms
- **Answer**:
```
Based on the provided merger agreement for the **aurora_vertex_2024** deal, the termination fee provisions are structured as follows:

### 1. Direct Answer
There are two specific termination fee provisions outlined in the agreement, both of which require the **Company** (Aurora Technologies Inc.) to make payments to the **Buyer** (Vertex Capital Partners LLC):
*   **Termination Fee:** **$20.88 million** (3.0% of the aggregate Merger Consideration).
*   **Reverse Termination Fee:** **$13.92 million** (2.0% of the aggregate Merger Consideration).

---

### 2. Supporting Evidence & Triggering Conditions

*   **Termination Fee ($20.88 million)**
    *   **Triggering Condition:** This fee is triggered if the Agreement is terminated by the Company pursuant to Section 7.1(d) in order to accept a "Superior Proposal" [📄 merger_agreement_v2_final.txt | Page 3 | Section 7.2 — Termination Fee]. 
    *   **Context:** Section 7.1(d) permits termination by the Company to accept a Superior Proposal, subject to the payment of this fee [📄 merger_agreement_v2_final.txt | Page 3 | Section: (a) by mutual written consent of Buyer and the Company;].
    *   **Scale/Value:** Represents exactly 3.0% of the aggregate Merger Consideration [📄 merger_agreement_v2_final.txt | Page 3 | Section 7.2 — Termination Fee].

*   **Reverse Termination Fee ($13.92 million)**
    *   **Triggering Condition:** This fee is triggered if the Agreement is terminated by the Buyer pursuant to Section 7.1(c) due to an uncured breach by the Company of any representation, warranty, or covenant [📄 merger_agreement_v2_final.txt | Page 3 | Section 7.2 — Termination Fee] [📄 merger_agreement_v2_final.txt | Page 3 | Section: (a) by mutual written consent of Buyer and the Company;].
    *   **Scale/Value:** Represents exactly 2.0% of the aggregate Merger Consideration [📄 merger_agreement_v2_final.txt | Page 3 | Section 7.2 — Termination Fee].

---

### 3. Caveats and Observations
*   **Drafting Inconsistency / Anomaly:** In standard M&A transactions, a "reverse termination fee" is typically paid by the *Buyer* to the *Company* (Target) if the Buyer breaches or fails to close. However, Section 7.2 explicitly dictates that the **Company** shall pay the **Buyer** this "reverse termination fee" of $13.92 million upon a Company breach [📄 merger_agreement_v2_final.txt | Page 3 | Section 7.2 — Termination Fee].
*   **Other Termination Scenarios:** No termination fees are specified if the agreement is terminated by mutual written consent (Section 7.1(a)) or if the merger is not consummated by the Outside Date of September 15, 2024 (Section 7.1(b)) [📄 merger_agreement_v2_final.txt | Page 3 | Section: (a) by mutual written consent of Buyer and the Company;].
```
- **Agent Trace Summary**:
  - **query_intelligence**:  ()
  - **retrieval_executor**:  ()
  - **financial_verifier**:  ()
  - **quality_assessor**:  ()
  - **answer_synthesizer**:  ()

---

### legal_03 (Legal)
**Query**: What are the indemnification caps and deductible?

- **Status**: ❌ FAIL
- **Error**: `{"detail":"Query pipeline error: litellm.RateLimitError: litellm.RateLimitError: geminiException - {\n  \"error\": {\n    \"code\": 429,\n    \"message\": \"You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-3.5-flash\\nPlease retry in 57.959078232s.\",\n    \"status\": \"RESOURCE_EXHAUSTED\",\n    \"details\": [\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.Help\",\n        \"links\": [\n          {\n            \"description\": \"Learn more about Gemini API quotas\",\n            \"url\": \"https://ai.google.dev/gemini-api/docs/rate-limits\"\n          }\n        ]\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.QuotaFailure\",\n        \"violations\": [\n          {\n            \"quotaMetric\": \"generativelanguage.googleapis.com/generate_content_free_tier_requests\",\n            \"quotaId\": \"GenerateRequestsPerDayPerProjectPerModel-FreeTier\",\n            \"quotaDimensions\": {\n              \"model\": \"gemini-3.5-flash\",\n              \"location\": \"global\"\n            },\n            \"quotaValue\": \"20\"\n          }\n        ]\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.RetryInfo\",\n        \"retryDelay\": \"57s\"\n      }\n    ]\n  }\n}\n"}`
- **Latency**: 31437.00 ms

---

### legal_04 (Legal)
**Query**: What pending litigation does the company face?

- **Status**: ✅ PASS
- **Confidence Score**: 0.00
- **Validation Status**: passed
- **Facts Recalled**: 0/5 (0.0%)
  - *Recalled*: []
  - *Missing*: ['DataFlow Systems', 'patent infringement', '$3.5 million', '$8.0 million', 'Northern District of California']
- **Citations Match**: ❌ No
- **Total Latency**: 29079.00 ms
- **Answer**:
```
I was unable to find sufficient relevant information in the data room to answer this question, even after refining the search. This may mean the relevant documents haven't been uploaded yet, or the question falls outside the scope of the available materials.

Search attempts: 3
Best quality score achieved: 0.01
```
- **Agent Trace Summary**:
  - **query_intelligence**:  ()
  - **retrieval_executor**:  ()
  - **quality_assessor**:  ()
  - **query_rewriter**:  ()
  - **retrieval_executor**:  ()

---

### legal_05 (Legal)
**Query**: What change of control provisions exist in the company's material contracts?

- **Status**: ✅ PASS
- **Confidence Score**: 0.00
- **Validation Status**: passed
- **Facts Recalled**: 0/7 (0.0%)
  - *Recalled*: []
  - *Missing*: ['Northstar Defense', '$12.4M', '60-day', 'Pacific Data', '$8.7M', 'terminate', '90 days']
- **Citations Match**: ❌ No
- **Total Latency**: 51921.00 ms
- **Answer**:
```
I was unable to find sufficient relevant information in the data room to answer this question, even after refining the search. This may mean the relevant documents haven't been uploaded yet, or the question falls outside the scope of the available materials.

Search attempts: 3
Best quality score achieved: 0.30
```
- **Agent Trace Summary**:
  - **query_intelligence**:  ()
  - **retrieval_executor**:  ()
  - **quality_assessor**:  ()
  - **query_rewriter**:  ()
  - **retrieval_executor**:  ()

---

### comp_01 (Comparative)
**Query**: Compare the three bidders — what were their offer ranges and certainty levels?

- **Status**: ✅ PASS
- **Confidence Score**: 0.00
- **Validation Status**: passed
- **Facts Recalled**: 0/12 (0.0%)
  - *Recalled*: []
  - *Missing*: ['Vertex', '$55', '$60', 'HIGH', 'Meridian', '$50', '$54', 'MEDIUM', 'Atlas', '$48', '$52', 'LOW']
- **Citations Match**: ❌ No
- **Total Latency**: 47250.00 ms
- **Answer**:
```
I was unable to find sufficient relevant information in the data room to answer this question, even after refining the search. This may mean the relevant documents haven't been uploaded yet, or the question falls outside the scope of the available materials.

Search attempts: 3
Best quality score achieved: 0.04
```
- **Agent Trace Summary**:
  - **query_intelligence**:  ()
  - **retrieval_executor**:  ()
  - **financial_verifier**:  ()
  - **quality_assessor**:  ()
  - **query_rewriter**:  ()

---

### comp_02 (Comparative)
**Query**: How do the different valuation methodologies compare?

- **Status**: ✅ PASS
- **Confidence Score**: 0.00
- **Validation Status**: passed
- **Facts Recalled**: 0/10 (0.0%)
  - *Recalled*: []
  - *Missing*: ['DCF', '$47', '$63', 'Precedent', '$46', '$62', 'LBO', '$50', '$61', 'Comparable']
- **Citations Match**: ❌ No
- **Total Latency**: 50375.00 ms
- **Answer**:
```
I was unable to find sufficient relevant information in the data room to answer this question, even after refining the search. This may mean the relevant documents haven't been uploaded yet, or the question falls outside the scope of the available materials.

Search attempts: 3
Best quality score achieved: 0.10
```
- **Agent Trace Summary**:
  - **query_intelligence**:  ()
  - **retrieval_executor**:  ()
  - **quality_assessor**:  ()
  - **query_rewriter**:  ()
  - **retrieval_executor**:  ()

---

### comp_03 (Comparative)
**Query**: Compare Aurora's gross margin and operating margin between FY2022 and FY2023.

- **Status**: ❌ FAIL
- **Error**: `{"detail":"Query pipeline error: litellm.RateLimitError: litellm.RateLimitError: geminiException - {\n  \"error\": {\n    \"code\": 429,\n    \"message\": \"You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-3.5-flash\\nPlease retry in 19.621456643s.\",\n    \"status\": \"RESOURCE_EXHAUSTED\",\n    \"details\": [\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.Help\",\n        \"links\": [\n          {\n            \"description\": \"Learn more about Gemini API quotas\",\n            \"url\": \"https://ai.google.dev/gemini-api/docs/rate-limits\"\n          }\n        ]\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.QuotaFailure\",\n        \"violations\": [\n          {\n            \"quotaMetric\": \"generativelanguage.googleapis.com/generate_content_free_tier_requests\",\n            \"quotaId\": \"GenerateRequestsPerDayPerProjectPerModel-FreeTier\",\n            \"quotaDimensions\": {\n              \"model\": \"gemini-3.5-flash\",\n              \"location\": \"global\"\n            },\n            \"quotaValue\": \"20\"\n          }\n        ]\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.RetryInfo\",\n        \"retryDelay\": \"19s\"\n      }\n    ]\n  }\n}\n"}`
- **Latency**: 39766.00 ms

---

### sum_01 (Summary)
**Query**: Summarize the board's recommendation regarding the strategic alternatives.

- **Status**: ❌ FAIL
- **Error**: `{"detail":"Query pipeline error: litellm.RateLimitError: litellm.RateLimitError: geminiException - {\n  \"error\": {\n    \"code\": 429,\n    \"message\": \"You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-3.5-flash\\nPlease retry in 570.88356ms.\",\n    \"status\": \"RESOURCE_EXHAUSTED\",\n    \"details\": [\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.Help\",\n        \"links\": [\n          {\n            \"description\": \"Learn more about Gemini API quotas\",\n            \"url\": \"https://ai.google.dev/gemini-api/docs/rate-limits\"\n          }\n        ]\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.QuotaFailure\",\n        \"violations\": [\n          {\n            \"quotaMetric\": \"generativelanguage.googleapis.com/generate_content_free_tier_requests\",\n            \"quotaId\": \"GenerateRequestsPerDayPerProjectPerModel-FreeTier\",\n            \"quotaDimensions\": {\n              \"location\": \"global\",\n              \"model\": \"gemini-3.5-flash\"\n            },\n            \"quotaValue\": \"20\"\n          }\n        ]\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.RetryInfo\",\n        \"retryDelay\": \"0s\"\n      }\n    ]\n  }\n}\n"}`
- **Latency**: 18969.00 ms

---

### sum_02 (Summary)
**Query**: What are the key risk factors identified for this transaction?

- **Status**: ✅ PASS
- **Confidence Score**: 0.00
- **Validation Status**: passed
- **Facts Recalled**: 0/9 (0.0%)
  - *Recalled*: []
  - *Missing*: ['DataFlow', 'patent litigation', 'customer consent', 'Northstar', 'Pacific Data', 'key employee', 'CTO', '$4.5M', 'HSR']
- **Citations Match**: ❌ No
- **Total Latency**: 49344.00 ms
- **Answer**:
```
I was unable to find sufficient relevant information in the data room to answer this question, even after refining the search. This may mean the relevant documents haven't been uploaded yet, or the question falls outside the scope of the available materials.

Search attempts: 3
Best quality score achieved: 0.40
```
- **Agent Trace Summary**:
  - **query_intelligence**:  ()
  - **retrieval_executor**:  ()
  - **quality_assessor**:  ()
  - **query_rewriter**:  ()
  - **retrieval_executor**:  ()

---

### mh_01 (Multi_hop)
**Query**: What is the relationship between the FY2023 restructuring charge and the Adjusted EBITDA? Where did the restructuring charge come from?

- **Status**: ✅ PASS
- **Confidence Score**: 0.00
- **Validation Status**: passed
- **Facts Recalled**: 0/7 (0.0%)
  - *Recalled*: []
  - *Missing*: ['$4.5', 'restructuring', 'Austin development center', '32 employees', '$92.8', '$97.3', 'add back']
- **Citations Match**: ❌ No
- **Total Latency**: 75437.00 ms
- **Answer**:
```
I was unable to find sufficient relevant information in the data room to answer this question, even after refining the search. This may mean the relevant documents haven't been uploaded yet, or the question falls outside the scope of the available materials.

Search attempts: 3
Best quality score achieved: 0.40
```
- **Agent Trace Summary**:
  - **query_intelligence**:  ()
  - **retrieval_executor**:  ()
  - **financial_verifier**:  ()
  - **quality_assessor**:  ()
  - **query_rewriter**:  ()

---

### mh_02 (Multi_hop)
**Query**: What indemnification exposure is tied to the financial statement representations, and how long do those representations survive?

- **Status**: ❌ FAIL
- **Error**: `{"detail":"Query pipeline error: litellm.RateLimitError: litellm.RateLimitError: geminiException - {\n  \"error\": {\n    \"code\": 429,\n    \"message\": \"You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-3.5-flash\\nPlease retry in 14.795958408s.\",\n    \"status\": \"RESOURCE_EXHAUSTED\",\n    \"details\": [\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.Help\",\n        \"links\": [\n          {\n            \"description\": \"Learn more about Gemini API quotas\",\n            \"url\": \"https://ai.google.dev/gemini-api/docs/rate-limits\"\n          }\n        ]\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.QuotaFailure\",\n        \"violations\": [\n          {\n            \"quotaMetric\": \"generativelanguage.googleapis.com/generate_content_free_tier_requests\",\n            \"quotaId\": \"GenerateRequestsPerDayPerProjectPerModel-FreeTier\",\n            \"quotaDimensions\": {\n              \"model\": \"gemini-3.5-flash\",\n              \"location\": \"global\"\n            },\n            \"quotaValue\": \"20\"\n          }\n        ]\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.RetryInfo\",\n        \"retryDelay\": \"14s\"\n      }\n    ]\n  }\n}\n"}`
- **Latency**: 41000.00 ms

---

### mh_03 (Multi_hop)
**Query**: How does the DataFlow litigation exposure compare to the merger's indemnification deductible?

- **Status**: ❌ FAIL
- **Error**: `{"detail":"Query pipeline error: litellm.RateLimitError: litellm.RateLimitError: geminiException - {\n  \"error\": {\n    \"code\": 429,\n    \"message\": \"You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-3.5-flash\\nPlease retry in 52.505676396s.\",\n    \"status\": \"RESOURCE_EXHAUSTED\",\n    \"details\": [\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.Help\",\n        \"links\": [\n          {\n            \"description\": \"Learn more about Gemini API quotas\",\n            \"url\": \"https://ai.google.dev/gemini-api/docs/rate-limits\"\n          }\n        ]\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.QuotaFailure\",\n        \"violations\": [\n          {\n            \"quotaMetric\": \"generativelanguage.googleapis.com/generate_content_free_tier_requests\",\n            \"quotaId\": \"GenerateRequestsPerDayPerProjectPerModel-FreeTier\",\n            \"quotaDimensions\": {\n              \"location\": \"global\",\n              \"model\": \"gemini-3.5-flash\"\n            },\n            \"quotaValue\": \"20\"\n          }\n        ]\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.RetryInfo\",\n        \"retryDelay\": \"52s\"\n      }\n    ]\n  }\n}\n"}`
- **Latency**: 22297.00 ms

---

### mh_04 (Multi_hop)
**Query**: What is the implied EV/EBITDA multiple of the Vertex deal based on the agreed price and Aurora's FY2023 EBITDA?

- **Status**: ✅ PASS
- **Confidence Score**: 0.00
- **Validation Status**: passed
- **Facts Recalled**: 0/3 (0.0%)
  - *Recalled*: []
  - *Missing*: ['$696', '$92.8', '7.5x']
- **Citations Match**: ❌ No
- **Total Latency**: 101016.00 ms
- **Answer**:
```
I was unable to find sufficient relevant information in the data room to answer this question, even after refining the search. This may mean the relevant documents haven't been uploaded yet, or the question falls outside the scope of the available materials.

Search attempts: 3
Best quality score achieved: 0.58
```
- **Agent Trace Summary**:
  - **query_intelligence**:  ()
  - **retrieval_executor**:  ()
  - **financial_verifier**:  ()
  - **quality_assessor**:  ()
  - **query_rewriter**:  ()

---

