import os
import sys
import subprocess
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CERT_DIR = BASE_DIR / "certificate"
CERT_FILE = CERT_DIR / "localhost+3.pem"
KEY_FILE = CERT_DIR / "localhost+3-key.pem"

REQUIRED_PACKAGES = ["Werkzeug", "pyOpenSSL"]

def check_and_install_packages():
    import importlib
    for pkg in REQUIRED_PACKAGES:
        try:
            importlib.import_module(pkg)
        except ImportError:
            print(f"[INFO] 安装缺失依赖：{pkg}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

def check_certificates():
    if not CERT_FILE.exists() or not KEY_FILE.exists():
        print(f"[ERROR] 证书文件不存在，请使用 mkcert 生成：")
        print(f"mkcert localhost 127.0.0.1 ::1 192.168.x.x")
        sys.exit(1)

def run_https_server(host, port):
    cmd = [
        sys.executable,
        "manage.py",
        "runserver_plus",
        "--cert-file", str(CERT_FILE),
        "--key-file", str(KEY_FILE),
        f"{host}:{port}"
    ]
    print(f"[INFO] 启动 HTTPS 服务：https://{host}:{port}")
    subprocess.call(cmd)

def main():
    parser = argparse.ArgumentParser(description="企业级 Django HTTPS 启动脚本")
    parser.add_argument("--host", default="127.0.0.1", help="绑定的 IP 地址或域名")
    parser.add_argument("--port", default="8000", help="端口号")
    args = parser.parse_args()

    # check_and_install_packages() #自动安装缺少依赖
    check_certificates()
    run_https_server(args.host, args.port)

if __name__ == "__main__":
    main()

# python manage_https.py --host 192.168.10.143 --port 8000
