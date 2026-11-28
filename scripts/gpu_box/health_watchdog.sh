#!/bin/bash
# Box health watchdog (owner Sat Nov 28 2026 ~12:30 AM PST, after a full disk killed nine trainings unnoticed for 1.5 h).
# Every INTERVAL s: one line in /root/health.log (GPU util, GPU memory, free disk, queue position, running jobs);
# any problem also goes to /root/health_alerts.log, which the session's 15-minute report reads and acts on.
#   Alerts: free disk under DISK_MIN_GB; a job that exited non-zero; GPU under 5% for 2 checks while jobs run or wait;
#   no job log written for STALL_MIN minutes while jobs run. The watchdog's own heartbeat is health.log's last line time.
# Start on the box:  tmux new -d -s watchdog "bash /root/health_watchdog.sh"
set -u
INTERVAL=${INTERVAL:-300}
DISK_MIN_GB=${DISK_MIN_GB:-15}
STALL_MIN=${STALL_MIN:-20}
LOG_DIRS="/root/cita_train/logs /root/cita_ecliptica/logs"
seen=$(wc -l < /root/jobs_done.txt)
idle=0
while true; do
    now=$(date -u +%Y-%m-%dT%H:%MZ)
    util=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits | head -1)
    mem=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -1)
    disk=$(df --output=avail -BG / | tail -1 | tr -dc 0-9)
    jobs=$(tmux ls -F '#{session_name}' 2>/dev/null | grep -vE '^(queue|ssh_tmux|watchdog)$' | tr '\n' ' ')
    pos=$(cat /root/queue_pos)
    total=$(wc -l < /root/jobs.txt)
    alerts=""
    if [ "$disk" -lt "$DISK_MIN_GB" ]; then alerts+="DISK ${disk} GB free (< ${DISK_MIN_GB}); "; fi
    n=$(wc -l < /root/jobs_done.txt)
    if [ "$n" -gt "$seen" ]; then
        fails=$(tail -n $((n - seen)) /root/jobs_done.txt | grep -v '^EXIT 0 ' | tr '\n' ';')
        if [ -n "$fails" ]; then alerts+="FAILED ${fails} "; fi
        seen=$n
    fi
    if [ "$util" -lt 5 ]; then idle=$((idle + 1)); else idle=0; fi
    if [ "$idle" -ge 2 ] && { [ -n "$jobs" ] || [ "$pos" -lt "$total" ]; }; then
        alerts+="GPU IDLE for ${idle} checks with jobs running or queued; "
    fi
    if [ -n "$jobs" ] && [ -z "$(find $LOG_DIRS -name '*.log' -mmin -"$STALL_MIN" | head -1)" ]; then
        alerts+="STALL no log written in ${STALL_MIN} min; "
    fi
    echo "$now gpu ${util}% mem ${mem} MiB disk_free ${disk} GB queue ${pos}/${total} running [${jobs}] ${alerts:+ALERT ${alerts}}" >> /root/health.log
    if [ -n "$alerts" ]; then echo "$now $alerts" >> /root/health_alerts.log; fi
    sleep "$INTERVAL"
done
