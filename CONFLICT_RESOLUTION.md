# Merge Conflict Resolution Guide

## 🔧 **Conflict Resolution for jumia_elt_dag.py**

If you see this conflict during merge:

```
<<<<<<< cicd-pipeline-implementation
# Add src directory to Python path for imports
sys.path.append("/opt/airflow/src")
=======
from datetime import datetime, timedelta
import sys
>>>>>>> main
```

**✅ RESOLUTION:** Use this corrected import section:

```python
"""
Jumia ELT Pipeline DAG
Orchestrates the extraction, loading, and transformation of Jumia laptop data
"""

from datetime import datetime, timedelta
import sys
import os
from airflow import DAG
from airflow.operators.python import PythonOperator

# Add src directory to Python path for imports
sys.path.append('/opt/airflow/src')

from jumia_pipeline import (
    scrape_laptop_data,
    load_to_bronze,
    run_silver_layer_procedure,
    run_gold_layer_procedure
)
```

## 🚀 **Steps to Resolve:**

1. **Edit the file** to remove conflict markers
2. **Use the resolution above** 
3. **Save the file**
4. **Run:** `git add airflow/dags/jumia_elt_dag.py`
5. **Run:** `git commit -m "fix: resolve merge conflict in DAG imports"`

## ✅ **Why This Works:**

- ✅ Proper import order (standard library first)
- ✅ Maintains sys.path.append for module loading
- ✅ Compatible with both branch requirements
- ✅ Follows Python import conventions

---
*This conflict has been pre-resolved in the current branch* 🎉
