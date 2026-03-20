#!/bin/bash
# Quota check hook script
# Reads from OMC HUD usage cache (api.anthropic.com/api/oauth/usage)
# Cache: ~/.claude/plugins/oh-my-claudecode/.usage-cache.json (30s TTL)
# Tracks burn rate via snapshots in /tmp/claude-quota-snapshots.csv

CACHE="$HOME/.claude/plugins/oh-my-claudecode/.usage-cache.json"
LOG="/tmp/claude-quota-snapshots.csv"

if [ ! -f "$CACHE" ]; then exit 0; fi

# Read from cache
data=$(jq -r '.data // empty' "$CACHE" 2>/dev/null)
if [ -z "$data" ]; then exit 0; fi

pct_5h=$(echo "$data" | jq -r '.fiveHourPercent // 0')
pct_wk=$(echo "$data" | jq -r '.weeklyPercent // 0')
resets_at=$(echo "$data" | jq -r '.fiveHourResetsAt // empty')

now=$(date +%s)

# Calculate minutes until 5h window reset
reset_mins=300
if [ -n "$resets_at" ]; then
  reset_epoch=$(date -d "$resets_at" +%s 2>/dev/null)
  if [ -n "$reset_epoch" ]; then
    reset_mins=$(( (reset_epoch - now) / 60 ))
    if [ "$reset_mins" -lt 0 ]; then reset_mins=0; fi
  fi
fi

# Track snapshots for burn rate
touch "$LOG"
echo "${now},${pct_5h},${pct_wk}" >> "$LOG"
tail -100 "$LOG" > "${LOG}.tmp" && mv "${LOG}.tmp" "$LOG"

# Calculate burn rate from snapshot ~5min ago
burn_msg=""
five_min_ago=$((now - 300))
prev_entry=$(awk -F, -v cutoff="$five_min_ago" '$1 >= cutoff { print; exit }' "$LOG")

if [ -n "$prev_entry" ]; then
  prev_time=$(echo "$prev_entry" | cut -d, -f1)
  prev_pct=$(echo "$prev_entry" | cut -d, -f2)
  time_delta_sec=$((now - prev_time))
  pct_delta=$((pct_5h - prev_pct))

  if [ "$time_delta_sec" -gt 30 ] && [ "$pct_delta" -gt 0 ]; then
    time_delta_min=$((time_delta_sec / 60))
    [ "$time_delta_min" -eq 0 ] && time_delta_min=1

    burn_rate_x10=$((pct_delta * 10 / time_delta_min))
    burn_per_min="$((burn_rate_x10 / 10)).$((burn_rate_x10 % 10))"

    remaining_pct=$((100 - pct_5h))
    if [ "$burn_rate_x10" -gt 0 ]; then
      mins_to_full=$((remaining_pct * 10 / burn_rate_x10))
    else
      mins_to_full=999
    fi

    # How long to rest: stop now, window resets in reset_mins, then you have 100% budget
    # If you need W mins of work at R%/min, you need W*R% budget
    # Assume ~30min work session needed → need 30*R% budget
    work_needed=$((30 * burn_rate_x10 / 10))
    if [ "$remaining_pct" -lt "$work_needed" ]; then
      # Not enough budget for 30min work → rest until reset
      rest_mins=$reset_mins
    else
      rest_mins=0
    fi

    burn_msg="소모율:~${burn_per_min}%/분, 현재속도로 ${mins_to_full}분 후 한도도달."
  fi
fi

# Format reset time
if [ "$reset_mins" -gt 60 ]; then
  reset_h=$((reset_mins / 60))
  reset_m=$((reset_mins % 60))
  reset_str="${reset_h}시간${reset_m}분"
else
  reset_str="${reset_mins}분"
fi

# Decision
if [ "$pct_5h" -ge 80 ]; then
  msg="🔴 QUOTA CRITICAL: 5h:${pct_5h}% wk:${pct_wk}%. ${burn_msg} 윈도우 리셋까지 ${reset_str}. 지금 중단하고 리셋 후 재개 권장. 꼭 필요한 작업만."
elif [ "$pct_5h" -ge 50 ]; then
  if [ -n "$burn_msg" ] && [ "${rest_mins:-0}" -gt 0 ]; then
    msg="🟡 QUOTA WARNING: 5h:${pct_5h}% wk:${pct_wk}%. ${burn_msg} 30분 작업하려면 지금 ${rest_str:-${reset_str}} 쉬고 재개해야 끊기지 않음. 또는 Sonnet 위임으로 절약."
  else
    msg="🟡 QUOTA WARNING: 5h:${pct_5h}% wk:${pct_wk}%. ${burn_msg} 리셋까지 ${reset_str}. 대형 작업 자제, Sonnet 위임 권장."
  fi
elif [ "$pct_5h" -ge 30 ]; then
  msg="🟢 QUOTA OK: 5h:${pct_5h}% wk:${pct_wk}%. ${burn_msg} 리셋까지 ${reset_str}. 여유있지만 Sonnet 위임이 효율적."
else
  # Under 30% - no message needed
  exit 0
fi

printf '{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"%s"}}\n' "$msg"
