import uvicorn
import argparse


def run():
    parser = argparse.ArgumentParser(description="启动 FastAPI 应用")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址")
    parser.add_argument("--port", type=int, default=8000, help="监听端口")
    parser.add_argument("--reload", action="store_true", help="开发模式热重载")

    args = parser.parse_args()

    print(f"{'='*60}")
    print(f"🚀 启动 FastAPI 应用在 http://{args.host}:{args.port}")
    print(f"📄 接口文档 Swagger: http://{args.host}:{args.port}/docs")
    print(f"{'='*60}")

    uvicorn.run(
        "app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info",
    )


if __name__ == "__main__":
    run()
