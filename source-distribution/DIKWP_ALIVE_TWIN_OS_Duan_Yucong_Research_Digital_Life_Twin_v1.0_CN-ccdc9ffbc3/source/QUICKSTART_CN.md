# DIKWP-ALIVE TWIN OS 快速启动

## 1. 离线驾驶舱

双击 `prototype/index.html`。页面内置本次公开语料样例，可查看证据指标、全局工作空间、矛盾账本、假设、实验和主动更新路线，并下载本地 JSON。

## 2. 运行参考内核

```bash
python runtime/alive_twin_runtime.py demo
```

输出写入 `examples/demo_result.json`，并打印确定性结果哈希。

## 3. 运行测试

```bash
python -m unittest discover -s tests -v
```

## 4. 替换为真实语料

编辑 `data/sample_corpus.json`：

1. 为每个工件创建 ArtifactCard；
2. 为每条可争论陈述创建 ClaimGene；
3. 不同日期或计数口径不得覆盖，必须并存；
4. 私有材料必须先更新 PurposeContract 和同意记录；
5. 运行时不会自动联网，也不会自动发布。

## 5. 生产化建议

- 元数据：Crossref、ORCID、GitHub API、专利和标准官方数据源；
- 存储：事件溯源数据库 + 图数据库 + 对象存储；
- 检索：混合检索、知识图谱、引用对齐；
- 安全：真实数字签名、密钥管理、最小权限、审计日志；
- 治理：本人/机构签名、外部 Critic Council、撤回与申诉；
- 发布：GitHub Release、DOI/Zenodo、CITATION.cff、RO-Crate、SPDX。
