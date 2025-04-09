from flask import Flask, request, redirect, jsonify, render_template_string
from urllib.parse import urlencode
import json
import jwt
import datetime
from cryptography.hazmat.primitives import serialization

# === Flask 基础 ===
app = Flask(__name__)

# === 加载配置 ===
import config
TOOL_DOMAIN = config.TOOL_DOMAIN
CLIENT_ID = config.CLIENT_ID
DEPLOYMENT_ID = config.DEPLOYMENT_ID
PLATFORM_PUBLIC_KEY_URL = config.PLATFORM_PUBLIC_KEY_URL
ISSUER = config.ISSUER
AUTH_LOGIN_URL = config.AUTH_LOGIN_URL
AUTH_TOKEN_URL = config.AUTH_TOKEN_URL

# === 加载密钥 ===
with open("keys/private.key", "rb") as f:
    PRIVATE_KEY = f.read()
with open("keys/public.key", "rb") as f:
    PUBLIC_KEY = f.read()

# ============ OIDC 启动：Canvas 发起登录请求 =============
@app.route("/lti/oidc", methods=["POST"])
def oidc_login():
    login_hint = request.form.get("login_hint")
    lti_message_hint = request.form.get("lti_message_hint")
    target_link_uri = request.form.get("target_link_uri")

    if not (login_hint and lti_message_hint and target_link_uri):
        return "Missing parameters", 400

    redirect_uri = f"{AUTH_LOGIN_URL}?" + urlencode({
        "client_id": CLIENT_ID,
        "login_hint": login_hint,
        "lti_message_hint": lti_message_hint,
        "nonce": "some-random-nonce",  # 实际部署应生成随机 nonce
        "prompt": "none",
        "redirect_uri": f"http://{TOOL_DOMAIN}:5000/lti/launch",
        "response_mode": "form_post",
        "response_type": "id_token",
        "scope": "openid"
    })

    return redirect(redirect_uri)

# ============ Launch 启动入口：验证 token 并展示工具 ============
@app.route("/lti/launch", methods=["POST"])
def lti_launch():
    id_token = request.form.get("id_token")
    if not id_token:
        return "Missing ID Token", 400

    try:
        # 只做解码，不验证签名（测试用，正式必须验证）
        decoded = jwt.decode(id_token, options={"verify_signature": False})
    except Exception as e:
        return f"JWT decode error: {str(e)}", 400

    # 展示简易页面（你可以换成真实前端）
    return render_template_string("""
        <h1>Encando 启动成功 ✅</h1>
        <p>用户信息：</p>
        <pre>{{ decoded | tojson(indent=2) }}</pre>
    """, decoded=decoded)

# ============ JWKS 公钥接口 ============
@app.route("/.well-known/jwks.json", methods=["GET"])
def jwks():
    from jwcrypto import jwk
    key = jwk.JWK.from_pem(PRIVATE_KEY)
    return jsonify({"keys": [json.loads(key.export_public())]})

# ============ 运行应用 ============
if __name__ == '__main__':
    app.run(debug=True)