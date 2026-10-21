#!/bin/bash
: '
=============================================================================
git_push.sh: two push lanes for the dataset-bench lab (CODE PUSH ONLY)
=============================================================================

Lane 1, the PRIVATE umbrella (this folder): commit everything and push main to
    https://github.com/<owner>/dataset-bench-lab   (created private on first run)

Lane 2, one repo per paper: export the paper with paperkit, commit the export
in exports/<public-name>/ (gitignored here, its own .git) and push it to
    https://github.com/<owner>/<public-name>       (created PRIVATE on first run; an existing repo keeps its
                                                   visibility, so spatialgym stays public until switched by hand)

Every repo is owned by OWNER (kapilw25) and pushed with the owner token. The account prompt only
sets the commit author (Kapil or Gaytri); it never changes where anything goes. Repos are created only
on a first --paper publish; the umbrella and --all never create anything.
Credentials come from the gitignored .env (GITHUB_TOKEN_KAPIL / GITHUB_TOKEN_GAYTRI);
nothing is hardcoded here and tokens are never printed. HuggingFace is never touched.

Usage:
    bash git_push.sh "message"                                   # lane 1: umbrella, asks which account
    bash git_push.sh --account kapil "message"                   # lane 1 without the prompt
    bash git_push.sh --paper p01-spatial-vqa --name spatialgym "SpatialGym v0"   # lane 2
    bash git_push.sh --paper p01-spatial-vqa --name spatialgym --dry-run "x"     # export + show, no git, no API
    bash git_push.sh --repo other-name "message"                 # lane 1 with another umbrella repo name
    bash git_push.sh --all "message"                             # lane 1, then lane 2 for every paper in public_papers.txt, then lane 3
    bash git_push.sh --hub "message"                             # lane 3 only: the public docs hub
    bash git_push.sh --with-hub "message"                        # lane 1, then lane 3: umbrella code + public pages in one run
    bash git_push.sh --hub --dry-run "x"                         # build the hub and show the change, no git, no API

Lane 3, the public docs hub (decided 2026-09-30): paperkit.hub builds papers/docs/ (gitignored here, its own .git) from
hub_papers.txt, one folder of pages per paper plus redirects from old names, and pushes it to
    https://github.com/<owner>/<owner>.github.io                  (created PUBLIC on first run: pages only, no code or data)
served at https://<owner>.github.io/dataset-bench-lab/ (the site root redirects there),
so every paper repo can stay private while its pages stay online.

public_papers.txt lists the papers that are already public ("<paper-folder> <public-name>" per line); a paper is
added to it the first time lane 2 pushes it, so --all never makes a private paper public.

Every run is appended to logs/git_push.log.
=============================================================================
'
set -o pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
OWNER="kapilw25"; OWNER_TOKEN_VAR="GITHUB_TOKEN_KAPIL"
UMBRELLA="dataset-bench-lab"
PAPER=""; PUBNAME=""; ACCOUNT_FLAG=""; DRY=0; ALL=0; HUB=0; WITHHUB=0; MESSAGE=""
REGISTRY="$HERE/public_papers.txt"

while [ $# -gt 0 ]; do
    case "$1" in
        --paper)   PAPER="$2"; shift 2 ;;
        --name)    PUBNAME="$2"; shift 2 ;;
        --repo)    UMBRELLA="$2"; shift 2 ;;
        --account) ACCOUNT_FLAG="$2"; shift 2 ;;
        --dry-run) DRY=1; shift ;;
        --all)     ALL=1; shift ;;
        --hub)     HUB=1; shift ;;
        --with-hub) WITHHUB=1; shift ;;
        -h|--help) sed -n '2,40p' "$0"; exit 0 ;;
        --*) echo "Error: unknown flag $1 (see --help)"; exit 1 ;;
        *)  MESSAGE="$1"; shift ;;
    esac
done
[ -z "$MESSAGE" ] && { echo "Error: commit message required (see --help)"; exit 1; }
[ $ALL = 1 ] && [ -n "$PAPER" ] && { echo "Error: --all and --paper do not mix"; exit 1; }
[ $HUB = 1 ] && { [ -n "$PAPER" ] || [ $ALL = 1 ]; } && { echo "Error: --hub runs alone (--all already includes it)"; exit 1; }
[ $WITHHUB = 1 ] && { [ -n "$PAPER" ] || [ $ALL = 1 ] || [ $HUB = 1 ]; } && { echo "Error: --with-hub pairs only with the umbrella push"; exit 1; }

mkdir -p "$HERE/logs"
exec > >(tee -a "$HERE/logs/git_push.log") 2>&1
echo "== $(date '+%Y-%m-%d %H:%M:%S') git_push.sh ${PAPER:+--paper $PAPER --name $PUBNAME} ${DRY:+}$([ $DRY = 1 ] && echo '(dry run)')"

# ---- credentials: .env is gitignored and must stay so ----------------------------------------------
ENV_FILE="$HERE/.env"
[ -f "$ENV_FILE" ] || { echo "FATAL: $ENV_FILE not found (needs GITHUB_TOKEN_KAPIL / GITHUB_TOKEN_GAYTRI)"; exit 1; }
git -C "$HERE" check-ignore -q .env || { echo "FATAL: .env is not gitignored in $HERE; refusing to continue"; exit 1; }
set -a; . "$ENV_FILE"; set +a

case "${ACCOUNT_FLAG:-}" in
    kapil|Kapil|1)   CHOICE=1 ;;
    gaytri|Gaytri|2) CHOICE=2 ;;
    "") echo "Select account:"; echo "1) Kapil"; echo "2) Gaytri"; read -p "Enter choice [1/2]: " CHOICE ;;
    *)  echo "Error: --account must be kapil or gaytri"; exit 1 ;;
esac
if [ "$CHOICE" = "2" ]; then
    USERNAME="GaytriJena"; EMAIL="gaytrijena2000@gmail.com"; NOREPLY="208319684+GaytriJena@users.noreply.github.com"; ACCOUNT="Gaytri"
else
    USERNAME="kapilw25";   EMAIL="kapilw25@gmail.com";       NOREPLY="90255702+kapilw25@users.noreply.github.com"; ACCOUNT="Kapil"
fi
# the chosen account is the commit author only; pushes and API calls always use the owner's token
TOKEN="${!OWNER_TOKEN_VAR}"
[ -n "$TOKEN" ] || { echo "FATAL: $OWNER_TOKEN_VAR (the owner's token) not set in .env"; exit 1; }
echo "commit author: $ACCOUNT ($USERNAME); repos owned by $OWNER"

# ---- helpers ---------------------------------------------------------------------------------------------
api() { curl -s -H "Authorization: token $TOKEN" -H "Accept: application/vnd.github+json" "$@"; }
ensure_repo() {   # ensure_repo <name> <private|public> <may-create 0|1>
    local name="$1" vis="$2" create="${3:-0}" code
    code=$(api -o /dev/null -w '%{http_code}' "https://api.github.com/repos/$OWNER/$name")
    if [ "$code" = "200" ]; then echo "repo $OWNER/$name exists"; return 0; fi
    if [ "$code" != "404" ]; then echo "FATAL: GitHub API returned $code for $OWNER/$name (bad token?)"; return 1; fi
    [ "$create" = 1 ] || { echo "FATAL: $OWNER/$name does not exist and this run may not create repos; nothing pushed"; return 1; }
    [ $DRY = 1 ] && { echo "(dry run) would create $vis repo $OWNER/$name"; return 0; }
    local priv=false; [ "$vis" = "private" ] && priv=true
    code=$(api -o /dev/null -w '%{http_code}' -X POST "https://api.github.com/user/repos" \
           -d "{\"name\":\"$name\",\"private\":$priv,\"auto_init\":false}")
    [ "$code" = "201" ] && echo "created $vis repo $OWNER/$name" || { echo "FATAL: create returned $code"; return 1; }
}
# a key prefix must start a word: 2026-10-12 "task-20241107035558-..." in a paper's md matched sk-[...]{20,}
SECRET_RX='(^|[^A-Za-z0-9])(hf_[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,}|wandb_v1_[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{30,})'
secret_scan() {   # secret_scan <dir>: refuse to push anything credential-shaped among the files git would take
    local hits
    if [ "$(git -C "$1" rev-parse --show-toplevel 2>/dev/null)" = "$1" ]; then   # its own repo, not a folder inside another one
        hits=$(cd "$1" && git ls-files -co --exclude-standard -z | xargs -0 grep -IlE "$SECRET_RX" 2>/dev/null | head -5)
    else
        hits=$(grep -rIlE "$SECRET_RX" --exclude-dir=.git --exclude=.env "$1" 2>/dev/null | head -5)
    fi
    [ -z "$hits" ] || { echo "FATAL: credential-shaped strings found, not pushing:"; echo "$hits"; return 1; }
}
push_dir() {      # push_dir <dir> <repo-name> <message> <author-email>
    local dir="$1" name="$2" msg="$3" email="${4:-$EMAIL}"
    # the export folder sits inside the umbrella's work tree (gitignored); it must be its OWN repo, never the umbrella's index
    [ "$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null)" = "$dir" ] || git -C "$dir" init -q -b main
    git -C "$dir" add -A
    # size gate (owner order 2026-10-12): GitHub's 5 GB repo guideline, gate at REPO_MAX_GB (default 4) and 95 MB a file.
    # A committed file never leaves history, so heavy files are stopped here, before the commit; they belong in the HF bucket.
    local gate
    gate=$(git -C "$dir" diff --cached --name-only -z --diff-filter=AM | (cd "$dir" && python3 -c '
import os, subprocess, sys
fs = [f for f in sys.stdin.buffer.read().decode(errors="replace").split("\0") if f and os.path.isfile(f)]
sz = sorted(((os.path.getsize(f), f) for f in fs), reverse=True)
kib = [l.split()[1] for l in subprocess.run(["git", "count-objects", "-v"], capture_output=True, text=True).stdout.splitlines() if l.startswith("size-pack")]
pack = int(kib[0]) * 1024 if kib else 0
lim = float(os.environ.get("REPO_MAX_GB", "4")) * 1024 ** 3
add = sum(s for s, _ in sz); big = [x for x in sz if x[0] > 95e6]
if big or pack + add > lim:
    print(f"  history {pack / 1024 ** 3:.2f} GB + this commit {add / 1024 ** 3:.2f} GB, gate {lim / 1024 ** 3:.0f} GB; biggest files:")
    for s, f in (big or sz)[:10]: print(f"  {s / 1e6:8.1f} MB  {f}")
'))
    if [ -n "$gate" ]; then
        echo "FATAL: size gate, nothing committed (a committed file never leaves history):"; echo "$gate"
        echo "  heavy files go to the HF bucket: gitignore them, then bash .claude/skills/infra-delete-instance/preflight.sh --sync-box-only"
        git -C "$dir" reset -q; return 1
    fi
    if git -C "$dir" diff --cached --quiet; then
        echo "nothing to commit in $dir"
    elif [ $DRY = 1 ]; then
        echo "(dry run) would commit:"; git -C "$dir" diff --cached --stat | tail -3; git -C "$dir" reset -q
    else
        git -C "$dir" -c user.name="$USERNAME" -c user.email="$email" commit -q -m "$msg" && echo "committed as $USERNAME <$email>: $msg"
    fi
    local url="https://github.com/${OWNER}/${name}.git"
    if git -C "$dir" remote get-url origin >/dev/null 2>&1; then git -C "$dir" remote set-url origin "$url"; else git -C "$dir" remote add origin "$url"; fi
    [ $DRY = 1 ] && { echo "(dry run) would push $dir main -> $url"; return 0; }
    local auth; auth=$(printf '%s:%s' "$OWNER" "$TOKEN" | base64 | tr -d '\n')   # one-shot header, token never in the URL or the remote
    if GIT_TERMINAL_PROMPT=0 git -C "$dir" -c credential.helper= -c "http.extraheader=AUTHORIZATION: basic $auth" push -u origin main 2>&1 \
        | sed -E "s#${TOKEN}#[token]#g; s#basic [A-Za-z0-9+/=]+#basic [redacted]#g"; then
        echo "pushed $dir (author $ACCOUNT) -> https://github.com/$OWNER/$name"
    else   # 2026-09-28: a rejected push used to print "pushed" and "Done"
        echo "FATAL: push to https://github.com/$OWNER/$name was rejected or failed (see above); nothing was published"
        return 1
    fi
}

sync_onto_remote() {   # sync_onto_remote <export-dir> <repo-name>: the export is a fresh snapshot of the paper, so put it on
    # top of whatever the remote already holds (results-only commits, Pages builds), making the push a fast-forward
    local dir="$1" name="$2" auth
    [ "$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null)" = "$dir" ] || git -C "$dir" init -q -b main
    local url="https://github.com/${OWNER}/${name}.git"
    if git -C "$dir" remote get-url origin >/dev/null 2>&1; then git -C "$dir" remote set-url origin "$url"; else git -C "$dir" remote add origin "$url"; fi
    auth=$(printf '%s:%s' "$OWNER" "$TOKEN" | base64 | tr -d '\n')
    if GIT_TERMINAL_PROMPT=0 git -C "$dir" -c credential.helper= -c "http.extraheader=AUTHORIZATION: basic $auth" fetch -q origin main 2>/dev/null; then
        git -C "$dir" reset -q --soft FETCH_HEAD && echo "export placed on top of $OWNER/$name main ($(git -C "$dir" rev-parse --short FETCH_HEAD))"
    fi
}

# ---- lane 2: export one paper and push its public repo -----------------------------------------------------
publish_paper() { # publish_paper <paper-folder> <public-name> <may-create 0|1>
    local paper="$1" pub="$2" create="${3:-0}" out tmp
    [ -d "$HERE/papers/$paper" ] || { echo "FATAL: no folder papers/$paper"; return 1; }
    out="$HERE/exports/$pub"; tmp="$HERE/exports/.tmp_$pub"
    rm -rf "$tmp"
    echo "exporting papers/$paper -> exports/$pub (paperkit gates run here)"
    PYTHONPATH="$HERE/shared" python3 -m paperkit.export "$paper" --out "$tmp" || { echo "FATAL: export of $paper failed its gates; fix and rerun"; rm -rf "$tmp"; return 1; }
    mkdir -p "$out"
    rsync -a --delete --exclude .git "$tmp/" "$out/"; rm -rf "$tmp"   # keep the export repo's history, refresh its files
    secret_scan "$out" || return 1
    ensure_repo "$pub" private "$create" || return 1   # new paper repos start private (decided 2026-09-29)
    [ $DRY = 1 ] || sync_onto_remote "$out" "$pub"
    push_dir "$out" "$pub" "$MESSAGE" "$NOREPLY" || return 1   # paper repos never carry a personal email
    if [ $DRY = 0 ] && ! grep -qs "^$paper $pub\$" "$REGISTRY"; then echo "$paper $pub" >> "$REGISTRY"; echo "registered $paper as public in public_papers.txt"; fi
    echo "Done (public paper repo $pub)"
}
# ---- lane 3: the public docs hub (pages only; every paper repo stays private) ---------------------------------
publish_hub() {
    local out="$HERE/papers/docs" name="${OWNER}.github.io"
    echo "building the docs hub from hub_papers.txt -> papers/docs (paperkit gates run per paper)"
    PYTHONPATH="$HERE/shared" python3 -m paperkit.hub --out "$out" --check || { echo "FATAL: hub build or link check failed; nothing pushed"; return 1; }
    secret_scan "$out" || return 1
    ensure_repo "$name" public 1 || return 1   # the one public repo, pages only (decided 2026-09-30)
    [ $DRY = 1 ] || sync_onto_remote "$out" "$name"
    push_dir "$out" "$name" "$MESSAGE" "$NOREPLY" || return 1
    echo "Done (public docs hub https://$name/dataset-bench-lab/)"
}
if [ $HUB = 1 ]; then publish_hub; exit $?; fi

if [ -n "$PAPER" ]; then
    [ -n "$PUBNAME" ] || { echo "Error: --paper needs --name <public-repo-name>"; exit 1; }
    publish_paper "$PAPER" "$PUBNAME" 1; exit $?
fi

# ---- lane 1: the private umbrella ---------------------------------------------------------------------------
secret_scan "$HERE" || exit 1
ensure_repo "$UMBRELLA" private 0 || exit 1
push_dir "$HERE" "$UMBRELLA" "$MESSAGE" || exit 1
echo "Done (private umbrella)"
if [ $WITHHUB = 1 ]; then publish_hub || exit 1; fi   # the pages are built from what was just pushed

# ---- --all: refresh every paper that is already public ------------------------------------------------------
if [ $ALL = 1 ]; then
    [ -s "$REGISTRY" ] || { echo "no public papers registered in public_papers.txt; nothing more to push"; exit 0; }
    FAILED=""
    while read -r paper pub; do
        [ -z "$paper" ] || [ "${paper#\#}" != "$paper" ] && continue
        publish_paper "$paper" "$pub" 0 || FAILED="$FAILED $paper"
    done < "$REGISTRY"
    [ -s "$HERE/hub_papers.txt" ] && { publish_hub || FAILED="$FAILED docs-hub"; }
    [ -z "$FAILED" ] && echo "Done (--all: umbrella, every registered paper repo, docs hub)" || { echo "Done with failures:$FAILED"; exit 1; }
fi
