#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Publish WeChat content from an article directory.

Usage:
  bash scripts/publish-from-dir.sh --article-dir /path/to/article-dir [--mode article|image-text] [--theme grace] [--submit] [--profile /path/to/profile]

Options:
  --article-dir <path>   Article directory (required)
  --mode <mode>          article | image-text (default: article)
  --theme <name>         Theme for article mode (default: grace)
  --submit               Save as draft
  --profile <dir>        Chrome profile directory
  -h, --help             Show help
EOF
}

ARTICLE_DIR=""
MODE="article"
THEME="grace"
SUBMIT=0
PROFILE_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --article-dir)
      ARTICLE_DIR="${2:-}"
      shift 2
      ;;
    --mode)
      MODE="${2:-}"
      shift 2
      ;;
    --theme)
      THEME="${2:-}"
      shift 2
      ;;
    --submit)
      SUBMIT=1
      shift
      ;;
    --profile)
      PROFILE_DIR="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$ARTICLE_DIR" ]]; then
  echo "Error: --article-dir is required" >&2
  usage >&2
  exit 1
fi

if [[ ! -d "$ARTICLE_DIR" ]]; then
  echo "Error: article directory not found: $ARTICLE_DIR" >&2
  exit 1
fi

case "$MODE" in
  article|image-text)
    ;;
  *)
    echo "Error: --mode must be article or image-text" >&2
    exit 1
    ;;
esac

find_markdown() {
  local dir="$1"
  if [[ -f "$dir/article.md" ]]; then
    printf '%s\n' "$dir/article.md"
    return 0
  fi
  if [[ -f "$dir/index.md" ]]; then
    printf '%s\n' "$dir/index.md"
    return 0
  fi
  find "$dir" -maxdepth 1 -type f -name '*.md' | head -n 1
}

find_images_dir() {
  local dir="$1"
  local candidate
  for candidate in "$dir/images" "$dir/assets" "$dir/img"; do
    if [[ -d "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  return 1
}

MARKDOWN_FILE="$(find_markdown "$ARTICLE_DIR")"
if [[ -z "$MARKDOWN_FILE" ]]; then
  echo "Error: no markdown file found in $ARTICLE_DIR" >&2
  exit 1
fi

IMAGES_DIR=""
if IMAGES_DIR="$(find_images_dir "$ARTICLE_DIR" 2>/dev/null || true)"; then
  :
fi

BASE_DIR="/Users/chinamanor/clawd/skills"
BAOYU_DIR="$BASE_DIR/baoyu-post-to-wechat"
ARTICLE_SCRIPT="$BAOYU_DIR/scripts/wechat-article.ts"
IMAGE_TEXT_SCRIPT="$BAOYU_DIR/scripts/wechat-browser.ts"

if [[ ! -f "$ARTICLE_SCRIPT" || ! -f "$IMAGE_TEXT_SCRIPT" ]]; then
  echo "Error: baoyu-post-to-wechat scripts not found under $BAOYU_DIR" >&2
  exit 1
fi

CMD=(npx -y bun)

if [[ "$MODE" == "article" ]]; then
  CMD+=("$ARTICLE_SCRIPT" --markdown "$MARKDOWN_FILE" --theme "$THEME")
  if [[ $SUBMIT -eq 1 ]]; then
    CMD+=(--submit)
  fi
  if [[ -n "$PROFILE_DIR" ]]; then
    CMD+=(--profile "$PROFILE_DIR")
  fi
else
  if [[ -z "$IMAGES_DIR" ]]; then
    echo "Error: image-text mode requires images/, assets/, or img/ directory" >&2
    exit 1
  fi
  CMD+=("$IMAGE_TEXT_SCRIPT" --markdown "$MARKDOWN_FILE" --images "$IMAGES_DIR")
  if [[ $SUBMIT -eq 1 ]]; then
    CMD+=(--submit)
  fi
  if [[ -n "$PROFILE_DIR" ]]; then
    CMD+=(--profile "$PROFILE_DIR")
  fi
fi

echo "[wechat-draft-pipeline] mode      : $MODE"
echo "[wechat-draft-pipeline] markdown  : $MARKDOWN_FILE"
if [[ -n "$IMAGES_DIR" ]]; then
  echo "[wechat-draft-pipeline] images    : $IMAGES_DIR"
fi
echo "[wechat-draft-pipeline] submit    : $SUBMIT"
echo "[wechat-draft-pipeline] command   : ${CMD[*]}"

"${CMD[@]}"
