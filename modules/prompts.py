CODE_PROMPT = """
# ゴール
- Pythonのコードを生成する

# 条件
- ユーザの入力を理解し、Pythonのコードを生成する
- コードは必ずトリプルバッククォートで囲む
- jupyter notebookで実行可能なコードを生成する

# 出力例
```
import numpy as np
import pandas as pd

df = pd.DataFrame(np.random.randn(10, 5))
df
```

[ユーザの入力]
{}
"""