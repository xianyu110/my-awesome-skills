---
name: x-api-publisher
description: Post, thread, verify, and delete content on X/Twitter through the X API using local OAuth credentials. Use when the user wants API-based X publishing, wants to update X credentials, verify account access, or troubleshoot X API posting failures such as permissions or credits issues.
---

# X API Publisher

Use this skill for **API-based** X/Twitter operations with the local credential file.

## Files

- Script: `${SKILL_DIR}/scripts/x_post.py`
- Credential file: `~/clawd/scripts/data/x_fusheng_keys.json`

Do **not** print secrets back into chat.

## Supported actions

###1) Verify credentials
Safe to run without extra confirmation:

```bash
python3 ${SKILL_DIR}/scripts/x_post.py check
```

###2) Post a single tweet
Only publish after the user has **explicitly confirmed** the post.

```bash
python3 ${SKILL_DIR}/scripts/x_post.py post "你的推文内容"
```

###3) Post a thread
Use `||` as the separator between tweets.

```bash
python3 ${SKILL_DIR}/scripts/x_post.py thread "第1条||第2条||第3条"
```

###4) Delete a tweet
Deletion is destructive. Confirm with the user first.

```bash
python3 ${SKILL_DIR}/scripts/x_post.py delete <tweet_id>
```

## Workflow

1. If the user provided new credentials, update `~/clawd/scripts/data/x_fusheng_keys.json`.
2. Run `check` first to confirm the account is reachable.
3. Draft or confirm the tweet/thread text.
4. Only after explicit approval, run `post` or `thread`.
5. Return the final tweet URL or error message.

## Credential format

Expected JSON fields:

```json
{
 "consumer_key": "...",
 "consumer_secret": "...",
 "access_token": "...",
 "access_token_secret": "...",
 "bearer_token": "..."
}
```

## Troubleshooting

###403 oauth1-permissions
The X app is missing write permissions.

Fix:
- Set the X app to **Read and write**
- Regenerate **Access Token** and **Access Token Secret**
- Update the credential JSON

###402 CreditsDepleted
The X API account has no usable credits.

Fix:
- Top up X API credits in the X Developer Console
- Retry the same command after credits are available

### Client Secret only / OAuth2-only credentials
A Client Secret alone is **not enough** for this OAuth1 posting flow.
You still need user-scoped posting credentials, or a complete OAuth2 user-token flow.

## Notes

- This skill is for **API publishing**, not browser automation.
- If API posting is blocked by credits or permissions, explain the exact blocker clearly.
- After a successful post, always return the URL.
