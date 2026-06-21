# E2E RAG Pipeline Validation Results

This document contains the actual execution results of the M&A Due Diligence Intelligence Engine run against the real **golden QA set**.

## Run Summary
- **Timestamp**: 2026-06-21 19:15:06
- **Deal ID**: `aurora_vertex_2024`
- **Total Queries Evaluated**: 19
- **Successfully Completed**: 19/19
- **Average E2E Latency**: 4572.37 ms
- **Average Grounding Fact Recall**: 0.0%
- **Citations Grounding Match**: 0/19 (0.0% of successful runs)

## Metrics by Query Type

| Query Type | Count | Success | Avg Recall | Avg Latency (ms) |
| --- | --- | --- | --- | --- |
| Financial | 5 | 5/5 | 0.0% | 4287.60 |
| Legal | 5 | 5/5 | 0.0% | 2209.40 |
| Comparative | 3 | 3/3 | 0.0% | 7510.33 |
| Summary | 2 | 2/2 | 0.0% | 8398.50 |
| Multi_hop | 4 | 4/4 | 0.0% | 3765.50 |

## Detailed Query Output Reports

### fin_01 (Financial)
**Query**: What was Aurora's total revenue in FY2023 and how does it compare to FY2022?

- **Status**: ✅ PASS
- **Confidence Score**: 0.00
- **Validation Status**: passed
- **Facts Recalled**: 0/4 (0.0%)
  - *Recalled*: []
  - *Missing*: ['$452.8', '$387.1', '17.0%', 'growth']
- **Citations Match**: ❌ No
- **Total Latency**: 3204.00 ms
- **Answer**:
```

```

---

### fin_02 (Financial)
**Query**: What is the EBITDA and Adjusted EBITDA for FY2023?

- **Status**: ✅ PASS
- **Confidence Score**: 0.00
- **Validation Status**: passed
- **Facts Recalled**: 0/4 (0.0%)
  - *Recalled*: []
  - *Missing*: ['$92.8', '$97.3', 'restructuring', '$4.5']
- **Citations Match**: ❌ No
- **Total Latency**: 2484.00 ms
- **Answer**:
```

```

---

### fin_03 (Financial)
**Query**: What is the company's free cash flow for FY2023 and what were the components?

- **Status**: ✅ PASS
- **Confidence Score**: 0.00
- **Validation Status**: passed
- **Facts Recalled**: 0/5 (0.0%)
  - *Recalled*: []
  - *Missing*: ['$64.2', '$78.4', 'operations', '$14.2', 'capital expenditures']
- **Citations Match**: ❌ No
- **Total Latency**: 4891.00 ms
- **Answer**:
```

```

---

### fin_04 (Financial)
**Query**: What is the Net Debt/EBITDA leverage ratio and how has it changed?

- **Status**: ✅ PASS
- **Confidence Score**: 0.00
- **Validation Status**: passed
- **Facts Recalled**: 0/5 (0.0%)
  - *Recalled*: []
  - *Missing*: ['0.2x', '0.7x', '$20.6', 'improved', 'deleveraged']
- **Citations Match**: ❌ No
- **Total Latency**: 8812.00 ms
- **Answer**:
```

```

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
- **Total Latency**: 2047.00 ms
- **Answer**:
```

```

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
- **Total Latency**: 2359.00 ms
- **Answer**:
```

```

---

### legal_02 (Legal)
**Query**: What are the termination fee provisions?

- **Status**: ✅ PASS
- **Confidence Score**: 0.00
- **Validation Status**: passed
- **Facts Recalled**: 0/6 (0.0%)
  - *Recalled*: []
  - *Missing*: ['$20.88', '3.0%', '$13.92', '2.0%', 'Superior Proposal', 'Company Breach']
- **Citations Match**: ❌ No
- **Total Latency**: 2360.00 ms
- **Answer**:
```

```

---

### legal_03 (Legal)
**Query**: What are the indemnification caps and deductible?

- **Status**: ✅ PASS
- **Confidence Score**: 0.00
- **Validation Status**: passed
- **Facts Recalled**: 0/7 (0.0%)
  - *Recalled*: []
  - *Missing*: ['$69.6', '10%', '$174.0', '25%', '$3.48', '0.5%', 'Fundamental']
- **Citations Match**: ❌ No
- **Total Latency**: 2203.00 ms
- **Answer**:
```

```

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
- **Total Latency**: 2265.00 ms
- **Answer**:
```

```

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
- **Total Latency**: 1860.00 ms
- **Answer**:
```

```

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
- **Total Latency**: 5125.00 ms
- **Answer**:
```

```

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
- **Total Latency**: 2187.00 ms
- **Answer**:
```

```

---

### comp_03 (Comparative)
**Query**: Compare Aurora's gross margin and operating margin between FY2022 and FY2023.

- **Status**: ✅ PASS
- **Confidence Score**: 0.00
- **Validation Status**: passed
- **Facts Recalled**: 0/5 (0.0%)
  - *Recalled*: []
  - *Missing*: ['60.0%', '59.1%', '15.0%', '13.3%', 'improved']
- **Citations Match**: ❌ No
- **Total Latency**: 15219.00 ms
- **Answer**:
```

```

---

### sum_01 (Summary)
**Query**: Summarize the board's recommendation regarding the strategic alternatives.

- **Status**: ✅ PASS
- **Confidence Score**: 0.00
- **Validation Status**: passed
- **Facts Recalled**: 0/9 (0.0%)
  - *Recalled*: []
  - *Missing*: ['Vertex Capital', 'preferred bidder', 'all-cash', 'Meridian', 'backup', 'Atlas', 'decline', 'unanimous', '7-0']
- **Citations Match**: ❌ No
- **Total Latency**: 14750.00 ms
- **Answer**:
```

```

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
- **Total Latency**: 2047.00 ms
- **Answer**:
```

```

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
- **Total Latency**: 4828.00 ms
- **Answer**:
```

```

---

### mh_02 (Multi_hop)
**Query**: What indemnification exposure is tied to the financial statement representations, and how long do those representations survive?

- **Status**: ✅ PASS
- **Confidence Score**: 0.00
- **Validation Status**: passed
- **Facts Recalled**: 0/6 (0.0%)
  - *Recalled*: []
  - *Missing*: ['$174.0', '25%', 'Fundamental Representations', 'Section 3.5', 'thirty-six', '36 months']
- **Citations Match**: ❌ No
- **Total Latency**: 4813.00 ms
- **Answer**:
```

```

---

### mh_03 (Multi_hop)
**Query**: How does the DataFlow litigation exposure compare to the merger's indemnification deductible?

- **Status**: ✅ PASS
- **Confidence Score**: 0.00
- **Validation Status**: passed
- **Facts Recalled**: 0/6 (0.0%)
  - *Recalled*: []
  - *Missing*: ['$3.5', '$8.0', 'DataFlow', '$3.48', 'deductible', 'exceeds']
- **Citations Match**: ❌ No
- **Total Latency**: 2265.00 ms
- **Answer**:
```

```

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
- **Total Latency**: 3156.00 ms
- **Answer**:
```

```

---

