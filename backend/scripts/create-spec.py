import argparse
import json
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--backend-env", required=True)
    parser.add_argument("--slack-webhook-url", required=True)

    args = parser.parse_args()

    spec = {
        "containers": {
            "cu": {
                "image": ":cu-container-service-1.backend.latest",
                "environment": {
                    "version": args.version,
                    "backend_env": args.backend_env,
                    "slack_webhook_url": args.slack_webhook_url,
                },
                "ports": {"80": "HTTP"},
            }
        },
        "publicEndpoint": {
            "containerName": "cu",
            "containerPort": 80,
            "healthCheck": {
                "healthyThreshold": 2,
                "unhealthyThreshold": 2,
                "timeoutSeconds": 5,
                "intervalSeconds": 10,
                "path": "/health",
                "successCodes": "200",
            },
        },
    }

    cwd = os.getcwd()
    with open("/".join((cwd, "lightsail-deploy.json")), "w") as f:
        json.dump(spec, f, indent=2)


if __name__ == "__main__":
    main()
