#!/usr/bin/env python3
import hashlib, hmac, json, os, sys, urllib.request
from datetime import datetime, timezone

def main():
      name = "Zuraiz Zahoor Ajaz"
      email = "xuraix29@gmail.com"
      resume_link = "https://linkedin.com/in/zuraiz"
      repo_link = os.environ.get("GITHUB_SERVER_URL","https://github.com") + "/" + os.environ.get("GITHUB_REPOSITORY","Zura1z/b12-apply")
      run_id = os.environ.get("GITHUB_RUN_ID","0")
      action_run_link = f"{repo_link}/actions/runs/{run_id}"
      ts = datetime.now(timezone.utc)
      timestamp = ts.strftime('%Y-%m-%dT%H:%M:%S.') + f'{ts.microsecond // 1000:03d}Z'
      payload = {"action_run_link": action_run_link, "email": email, "name": name, "repository_link": repo_link, "resume_link": resume_link, "timestamp": timestamp}
      body = json.dumps(payload, sort_keys=True, separators=(',',':')).encode('utf-8')
      print(f"Payload: {body.decode()}")
      secret = "hello-there-from-b12"
      digest = hmac.new(secret.encode('utf-8'), body, hashlib.sha256).hexdigest()
      signature = f"sha256={digest}"
      print(f"Signature: {signature}")
      req = urllib.request.Request("https://b12.io/apply/submission", data=body, headers={"Content-Type":"application/json","X-Signature-256":signature}, method="POST")
      try:
                with urllib.request.urlopen(req) as resp:
                              result = json.loads(resp.read().decode())
                              print(f"Receipt: {result.get('receipt')}")
      except urllib.request.HTTPError as e:
                print(f"Error {e.code}: {e.read().decode()}")
                sys.exit(1)

  if __name__ == "__main__":
        main()
