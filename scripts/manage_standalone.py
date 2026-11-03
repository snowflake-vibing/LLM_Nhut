"""
Standalone Background Service Manager - Version 3.0
Cho phép khởi động, kiểm tra và dừng toàn bộ dịch vụ (Telegram Daemon, Continuous Pipeline, Streamlit)
hoàn toàn ĐỘC LẬP ngoài Windows, KHÔNG phụ thuộc vào Antigravity IDE hay Docker Desktop.
"""

import os
import sys
import json
import time
import subprocess
import signal

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PID_FILE = os.path.join(ROOT_DIR, "data", "services.pid")
VENV_PYTHON = os.path.join(ROOT_DIR, "venv", "Scripts", "python.exe")
VENV_PYTHONW = os.path.join(ROOT_DIR, "venv", "Scripts", "pythonw.exe")
VENV_STREAMLIT = os.path.join(ROOT_DIR, "venv", "Scripts", "streamlit.exe")

if not os.path.exists(VENV_PYTHONW):
    VENV_PYTHONW = VENV_PYTHON


def get_running_pids():
    if not os.path.exists(PID_FILE):
        return {}
    try:
        with open(PID_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_pids(pids):
    os.makedirs(os.path.dirname(PID_FILE), exist_ok=True)
    with open(PID_FILE, "w", encoding="utf-8") as f:
        json.dump(pids, f, ensure_ascii=False, indent=2)


def is_pid_alive(pid):
    if not pid:
        return False
    try:
        # Trên Windows dùng tasklist để kiểm tra PID
        res = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True)
        return str(pid) in res.stdout
    except Exception:
        return False


def start_all():
    print("==================================================")
    print("🚀 KHỞI ĐỘNG CÁC DỊCH VỤ CHẠY NGẦM ĐỘC LẬP 24/7")
    print("🎯 Hoàn toàn KHÔNG phụ thuộc Antigravity hay Docker Desktop")
    print("==================================================")

    current_pids = get_running_pids()
    new_pids = {}

    # 1. Telegram Bot Daemon
    tg_pid = current_pids.get("telegram_daemon")
    if tg_pid and is_pid_alive(tg_pid):
        print(f"🤖 [Telegram Daemon] Đang chạy sẵn (PID: {tg_pid}) ✅")
        new_pids["telegram_daemon"] = tg_pid
    else:
        tg_script = os.path.join(ROOT_DIR, "scripts", "telegram_bot_daemon.py")
        p = subprocess.Popen(
            [VENV_PYTHONW, tg_script],
            cwd=ROOT_DIR,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        new_pids["telegram_daemon"] = p.pid
        print(f"🤖 [Telegram Daemon] Đã khởi chạy ngầm thành công (PID: {p.pid}) ✅")

    # 2. Continuous Evolutionary Pipeline
    pipe_pid = current_pids.get("continuous_pipeline")
    if pipe_pid and is_pid_alive(pipe_pid):
        print(f"🌟 [Continuous Pipeline] Đang chạy sẵn (PID: {pipe_pid}) ✅")
        new_pids["continuous_pipeline"] = pipe_pid
    else:
        pipe_script = os.path.join(ROOT_DIR, "scripts", "continuous_dev_pipeline.py")
        p = subprocess.Popen(
            [VENV_PYTHONW, pipe_script],
            cwd=ROOT_DIR,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        new_pids["continuous_pipeline"] = p.pid
        print(f"🌟 [Continuous Pipeline] Đã khởi chạy ngầm thành công (PID: {p.pid}) ✅")

    # 3. Streamlit Citizen Web App
    st_pid = current_pids.get("streamlit_app")
    if st_pid and is_pid_alive(st_pid):
        print(f"🌐 [Streamlit Web App] Đang chạy sẵn tại http://localhost:8501 (PID: {st_pid}) ✅")
        new_pids["streamlit_app"] = st_pid
    else:
        st_script = os.path.join(ROOT_DIR, "app", "main.py")
        p = subprocess.Popen(
            [VENV_PYTHONW, "-m", "streamlit", "run", st_script, "--server.port", "8501", "--server.headless", "true"],
            cwd=ROOT_DIR,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        new_pids["streamlit_app"] = p.pid
        print(f"🌐 [Streamlit Web App] Đã khởi chạy ngầm tại http://localhost:8501 (PID: {p.pid}) ✅")

    save_pids(new_pids)
    print("\n🎉 Tất cả 3 dịch vụ đã chạy độc lập dưới nền hệ điều hành Windows!")
    print("💡 Giờ đây bạn có thể TẮT Antigravity và TẮT Docker Desktop; các dịch vụ vẫn hoạt động 24/7!")


def stop_all():
    print("==================================================")
    print("🛑 DỪNG TẤT CẢ CÁC DỊCH VỤ CHẠY NGẦM")
    print("==================================================")
    current_pids = get_running_pids()
    for name, pid in current_pids.items():
        if pid and is_pid_alive(pid):
            try:
                subprocess.run(["taskkill", "/PID", str(pid), "/F", "/T"], capture_output=True)
                print(f"🛑 Đã dừng dịch vụ '{name}' (PID: {pid}) ✅")
            except Exception as e:
                print(f"⚠️ Không thể dừng {name} (PID: {pid}): {e}")
        else:
            print(f"ℹ️ Dịch vụ '{name}' (PID: {pid}) đã dừng từ trước.")

    save_pids({})
    print("✅ Hoàn tất dừng toàn bộ dịch vụ ngầm.")


def status_all():
    print("==================================================")
    print("ℹ️ KIỂM TRA TRẠNG THÁI DỊCH VỤ ĐỘC LẬP 24/7")
    print("==================================================")
    current_pids = get_running_pids()
    if not current_pids:
        print("🔴 Hiện chưa có dịch vụ nào đang chạy ngầm độc lập.")
        return

    for name, pid in current_pids.items():
        alive = is_pid_alive(pid)
        status_icon = "🟢 Đang chạy (Active)" if alive else "🔴 Đã dừng (Inactive)"
        print(f"• {name:<22}: {status_icon} (PID: {pid})")


if __name__ == "__main__":
    action = sys.argv[1].lower() if len(sys.argv) > 1 else "status"
    if action == "start":
        start_all()
    elif action == "stop":
        stop_all()
    else:
        status_all()
