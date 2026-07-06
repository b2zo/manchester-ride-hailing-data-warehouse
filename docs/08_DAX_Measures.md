# 08 — DAX Measures

```DAX
Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)
```

```DAX
Pipeline Status Icon = SWITCH(TRUE(), [Pipeline Health Score] >= 85, "🟢 Healthy", [Pipeline Health Score] >= 70, "🟡 Warning", "🔴 Critical")
```
