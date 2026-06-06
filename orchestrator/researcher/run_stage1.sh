#!/usr/bin/env bash
# Stage 1 batch driver — runs extractor per researcher, smallest first.
# Resumable: each researcher script call skips already-extracted papers.
# Logs to logs/<slug>.log. Exit non-zero only on python import errors etc.

set -u
cd "$(dirname "$0")"

# Researchers ordered by ascending paper count (smaller batches first so we
# get breadth/coverage quickly; biggest batch yunhao_liu_674 runs last).
SLUGS=(
  mingyi_liu        # 1
  yuan_wang         # 1
  hailong_sun       # 2 (already done in smoke test)
  honggui_han       # 3
  xiaoping_li       # 4
  yang_song         # 4
  xuanhua_shi       # 7
  lei_ren           # 11
  hailiang_zhao     # 13
  gang_xiong        # 14
  yutao_ma          # 15
  zhongjie_wang     # 18
  li_kuang          # 24
  xiaofei_xu        # 26
  ge_li             # 44
  xuanzhe_liu       # 62
  shangguang_wang   # 69
  xinpeng_zhao      # 76
  xiaocheng_feng    # 82
  shuiguang_deng    # 84
  jianwei_yin       # 85
  zhi_jin           # 134
  yunhao_liu        # 674
)

CONCURRENCY="${CONCURRENCY:-6}"

for slug in "${SLUGS[@]}"; do
  log="logs/${slug}.log"
  echo "[$(date '+%H:%M:%S')] === ${slug} === (log: ${log})"
  python3 extract_papers.py --concurrency "${CONCURRENCY}" "${slug}" \
      >> "${log}" 2>&1
  tail -1 "${log}"
done

echo "[$(date '+%H:%M:%S')] STAGE 1 COMPLETE"
