"""
Salto APIs - Quick connection test script.
Replace CLIENT_ID, CLIENT_SECRET, and INSTALLATION_NAME with your real credentials.
"""

import grpc
from saltoapis.auth.interceptor import SaltoapisAuthInterceptor
from saltoapis.nebula.user.v1 import user_pb2, user_pb2_grpc

# ─── Configuration ───────────────────────────────────────────────
CLIENT_ID       = "<YOUR_CLIENT_ID>"
CLIENT_SECRET   = "<YOUR_CLIENT_SECRET>"
INSTALLATION_NAME = "<YOUR_INSTALLATION_NAME>"   # e.g. "installations/abc123"
# ─────────────────────────────────────────────────────────────────

def main():
    # 1. Create a secure gRPC channel
    channel = grpc.secure_channel(
        "nebula.saltoapis.com",
        grpc.ssl_channel_credentials()
    )

    # 2. Attach the auth interceptor (handles OAuth2 token refresh automatically)
    intercept_channel = grpc.intercept_channel(
        channel,
        SaltoapisAuthInterceptor(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            scopes=[
                "openid",
                "offline",
                "profile",
                "email",
                "https://saltoapis.com/auth/nebula",
            ],
            discovery_host="account.saltosystems.com",
        ),
    )

    # 3. Create a service stub
    stub = user_pb2_grpc.UserServiceStub(intercept_channel)

    # 4. List users as a connectivity check
    print(f"Connecting to Salto Nebula API...")
    response = stub.ListUsers(
        user_pb2.ListUsersRequest(parent=INSTALLATION_NAME, page_size=10)
    )

    print(f"✅ Connected! Found {len(response.users)} user(s):")
    for user in response.users:
        print(f"  - {user.display_name} ({user.email})")

    channel.close()
    print("Done.")


if __name__ == "__main__":
    main()
