#!/usr/bin/env python3
"""Simple X/Twitter posting helper.

Usage:
 python3 ~/clawd/scripts/x_post.py post "你的推文内容"
 python3 ~/clawd/scripts/x_post.py thread "第1条||第2条||第3条"
 python3 ~/clawd/scripts/x_post.py delete <tweet_id>
 python3 ~/clawd/scripts/x_post.py check

Config file:
 ~/clawd/scripts/data/x_fusheng_keys.json
"""

import argparse
import json
import os
import sys
from pathlib import Path

from requests_oauthlib import OAuth1Session

CONFIG_PATH = Path.home() / "clawd" / "scripts" / "data" / "x_fusheng_keys.json"
API_BASE_V2 = "https://api.twitter.com/2"
VERIFY_URL = "https://api.twitter.com/1.1/account/verify_credentials.json"


class XPostError(Exception):
    pass


def _pick(config, keys, env_names=None, required=False, default=None):
    for key in keys:
        value = config.get(key)
        if value:
            return value

    for env_name in (env_names or []):
        value = os.getenv(env_name)
        if value:
            return value

    if required:
        raise XPostError("缺少配置字段: {}".format(" / ".join(keys)))

    return default


def load_config(path=CONFIG_PATH):
    if not path.exists():
        raise XPostError("配置文件不存在: {}".format(path))

    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise XPostError("配置文件 JSON 格式错误: {}".format(exc)) from exc

    resolved = {
        "consumer_key": _pick(
            config,
            ["consumer_key", "api_key"],
            env_names=["X_CONSUMER_KEY", "X_API_KEY", "TWITTER_CONSUMER_KEY", "TWITTER_API_KEY"],
            required=True,
        ),
        "consumer_secret": _pick(
            config,
            ["consumer_secret", "api_key_secret", "api_secret"],
            env_names=[
                "X_CONSUMER_SECRET",
                "X_API_KEY_SECRET",
                "TWITTER_CONSUMER_SECRET",
                "TWITTER_API_KEY_SECRET",
            ],
            required=True,
        ),
        "access_token": _pick(
            config,
            ["access_token"],
            env_names=["X_ACCESS_TOKEN", "TWITTER_ACCESS_TOKEN"],
            required=True,
        ),
        "access_token_secret": _pick(
            config,
            ["access_token_secret"],
            env_names=["X_ACCESS_TOKEN_SECRET", "TWITTER_ACCESS_TOKEN_SECRET"],
            required=True,
        ),
        "bearer_token": _pick(
            config,
            ["bearer_token"],
            env_names=["X_BEARER_TOKEN", "TWITTER_BEARER_TOKEN"],
            required=False,
            default="",
        ),
    }
    return resolved


def make_session(config):
    return OAuth1Session(
        client_key=config["consumer_key"],
        client_secret=config["consumer_secret"],
        resource_owner_key=config["access_token"],
        resource_owner_secret=config["access_token_secret"],
    )


def _request(session, method, url, **kwargs):
    try:
        response = session.request(method=method, url=url, timeout=30, **kwargs)
    except Exception as exc:
        raise XPostError("请求 X API失败: {}".format(exc)) from exc

    if response.status_code >=400:
        try:
            payload = response.json()
        except Exception:
            payload = response.text
        raise XPostError("X API 返回错误 ({}): {}".format(response.status_code, payload))

    if not response.content:
        return {}

    try:
        return response.json()
    except Exception:
        return {"raw": response.text}


def check_account(session):
    payload = _request(
        session,
        "GET",
        VERIFY_URL,
        params={"skip_status": "true", "include_entities": "false"},
    )
    return {
        "id": payload.get("id_str") or payload.get("id"),
        "name": payload.get("name"),
        "screen_name": payload.get("screen_name"),
    }


def post_tweet(session, text, reply_to_id=None):
    text = (text or "").strip()
    if not text:
        raise XPostError("推文内容不能为空")

    body = {"text": text}
    if reply_to_id:
        body["reply"] = {"in_reply_to_tweet_id": str(reply_to_id)}

    payload = _request(session, "POST", API_BASE_V2 + "/tweets", json=body)
    return payload.get("data", {})


def post_thread(session, joined_text):
    parts = [part.strip() for part in joined_text.split("||") if part.strip()]
    if not parts:
        raise XPostError("Thread 内容不能为空")

    posted = []
    previous_id = None
    for part in parts:
        data = post_tweet(session, part, previous_id)
        previous_id = data.get("id")
        posted.append(data)
    return posted


def delete_tweet(session, tweet_id):
    tweet_id = str(tweet_id).strip()
    if not tweet_id:
        raise XPostError("tweet_id不能为空")
    return _request(session, "DELETE", API_BASE_V2 + "/tweets/{}".format(tweet_id))


def build_parser():
    parser = argparse.ArgumentParser(description="X/Twitter 发推工具")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    post_parser = subparsers.add_parser("post", help="发送单条推文")
    post_parser.add_argument("text", help="推文内容")

    thread_parser = subparsers.add_parser("thread", help="按 || 拆分发送 thread")
    thread_parser.add_argument("text", help="形如 第1条||第2条||第3条")

    delete_parser = subparsers.add_parser("delete", help="删除推文")
    delete_parser.add_argument("tweet_id", help="要删除的 tweet id")

    subparsers.add_parser("check", help="只读校验当前凭证")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        config = load_config()
        session = make_session(config)

        if args.command == "check":
            account = check_account(session)
            print("凭证可用")
            print("账号: @{screen_name} ({name})".format(**account))
            print("用户ID: {}".format(account.get("id") or "unknown"))
            return 0

        if args.command == "post":
            data = post_tweet(session, args.text)
            tweet_id = data.get("id")
            print("发推成功")
            print("tweet_id: {}".format(tweet_id))
            print("url: https://x.com/i/web/status/{}".format(tweet_id))
            return 0

        if args.command == "thread":
            items = post_thread(session, args.text)
            print("Thread发送成功，共 {} 条".format(len(items)))
            for idx, item in enumerate(items, start=1):
                print("{}. {}".format(idx, item.get("id")))
            if items:
                print("首条链接: https://x.com/i/web/status/{}".format(items[0].get("id")))
            return 0

        if args.command == "delete":
            result = delete_tweet(session, args.tweet_id)
            print("删除结果: {}".format(json.dumps(result, ensure_ascii=False)))
            return 0

        parser.print_help()
        return 1
    except XPostError as exc:
        print("错误: {}".format(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
