#!/usr/bin/env python3
"""
Ally Orchestrator - 任务编排中心
并行分发任务给多个 ally skills，统一监控和汇总结果
"""
import json
import subprocess
import time
import sys
import os
import signal
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class HiOrchestrator:
    def __init__(self, workspace: Path = Path.home() / ".claude" / "orchestrator"):
        self.workspace = workspace
        self.workspace.mkdir(parents=True, exist_ok=True)

        self.ally_paths = {
            "claude": Path.home() / ".agents/skills/claude-ally",
            "codex": Path.home() / ".agents/skills/codex-ally",
            "tcodex": Path.home() / ".agents/skills/tcodex-ally",
            "gemini": Path.home() / ".agents/skills/gemini-ally",
            "codebuddy": Path.home() / ".agents/skills/codebuddy-ally"
        }

        # 智能任务分配规则
        self.task_type_keywords = {
            "work": ["修复", "fix", "实现", "implement", "bug", "feature", "重构", "refactor",
                     "开发", "develop", "编码", "code", "功能", "function"],
            "think": ["审查", "review", "分析", "analyze", "设计", "design", "评估", "evaluate",
                      "优化", "optimize", "规划", "plan", "架构", "architecture"],
            "execute": ["生成", "generate", "创建", "create", "编写", "write", "脚本", "script",
                       "配置", "config", "工具", "tool", "快速", "quick"],
            "multimodal": ["截图", "screenshot", "图片", "image", "视觉", "visual", "UI",
                          "界面", "interface", "视频", "video"]
        }

        # 默认 ally 映射
        self.default_ally_map = {
            "work": "tcodex",      # 工作任务 → tcodex
            "think": "claude",     # 思考任务 → claude
            "execute": "codex",    # 执行任务 → codex
            "multimodal": "gemini" # 多模态任务 → gemini
        }

    def _infer_ally(self, task: Dict) -> str:
        """智能推断任务应该使用的 ally"""
        # 如果显式指定了 ally，直接使用
        if "ally" in task and task["ally"]:
            return task["ally"]

        # 如果指定了 type，根据 type 选择
        if "type" in task and task["type"] in self.default_ally_map:
            return self.default_ally_map[task["type"]]

        # 根据 prompt 关键词推断
        prompt = task.get("prompt", "").lower()

        # 统计各类型关键词匹配数
        scores = {task_type: 0 for task_type in self.task_type_keywords}
        for task_type, keywords in self.task_type_keywords.items():
            for keyword in keywords:
                if keyword in prompt:
                    scores[task_type] += 1

        # 选择得分最高的类型
        if max(scores.values()) > 0:
            best_type = max(scores, key=scores.get)
            return self.default_ally_map[best_type]

        # 默认使用 codex（执行任务）
        return "codex"

    def dispatch(self, batch_file: Path) -> str:
        """分发任务批次，立即返回"""
        with open(batch_file) as f:
            batch = json.load(f)

        batch_id = batch["batch_name"]
        batch_dir = self.workspace / batch_id
        batch_dir.mkdir(exist_ok=True)

        # 保存批次元数据
        (batch_dir / "batch.json").write_text(json.dumps(batch, indent=2))

        # 并行启动所有任务
        task_pids = []
        for task in batch["tasks"]:
            try:
                pid = self._launch_task(task, batch["project_root"], batch_dir)
                task_pids.append({"task_id": task["id"], "pid": pid, "status": "launched"})
            except Exception as e:
                print(f"⚠️  Failed to launch task {task['id']}: {e}")
                task_pids.append({"task_id": task["id"], "pid": None, "status": "failed", "error": str(e)})

        # 保存 PID 映射
        (batch_dir / "pids.json").write_text(json.dumps(task_pids, indent=2))

        print(f"✅ 任务批次已分发: {batch_id}")
        print(f"📊 总计 {len(batch['tasks'])} 个任务")
        launched = sum(1 for p in task_pids if p["status"] == "launched")
        print(f"🚀 成功启动: {launched} 个任务")
        if launched < len(batch['tasks']):
            print(f"⚠️  启动失败: {len(batch['tasks']) - launched} 个任务")
        print(f"\n🔄 后台执行中，使用以下命令监控：")
        print(f"   python3 {__file__} status {batch_id}")

        return batch_id

    def _launch_task(self, task: Dict, project_root: str, batch_dir: Path) -> int:
        """启动单个任务（后台运行）"""
        # 智能推断 ally
        ally = self._infer_ally(task)
        task_id = task["id"]

        # 记录推断结果
        if "ally" not in task or not task["ally"]:
            print(f"  ℹ️  Task {task_id}: 自动选择 {ally} (基于: {task.get('type', 'prompt分析')})")

        if ally not in self.ally_paths:
            raise ValueError(f"Unknown ally: {ally}")

        ally_path = self.ally_paths[ally]
        bridge_script = ally_path / "scripts" / f"{ally}_bridge.py"

        if not bridge_script.exists():
            raise FileNotFoundError(f"Bridge script not found: {bridge_script}")

        # 构建命令
        cmd = [
            "python3",
            str(bridge_script),
            "--cd", project_root,
            "--PROMPT", task["prompt"]
        ]

        # 添加可选参数
        if task.get("sandbox"):
            cmd.extend(["--sandbox", task["sandbox"]])
        if task.get("session_id"):
            cmd.extend(["--SESSION_ID", task["session_id"]])
        if task.get("skip_git_repo_check"):
            cmd.append("--skip-git-repo-check")
        if task.get("return_all_messages"):
            cmd.append("--return-all-messages")

        # 启动后台进程
        output_file = batch_dir / f"{task_id}.output"
        with open(output_file, "w") as f:
            proc = subprocess.Popen(
                cmd,
                stdout=f,
                stderr=subprocess.STDOUT,
                start_new_session=True
            )

        # 保存任务状态
        status = {
            "task_id": task_id,
            "ally": ally,  # 记录实际使用的 ally
            "inferred": "ally" not in task or not task["ally"],  # 是否为自动推断
            "status": "RUNNING",
            "pid": proc.pid,
            "start_time": datetime.now().isoformat(),
            "output_file": str(output_file),
            "command": " ".join(cmd)
        }
        (batch_dir / f"{task_id}.status").write_text(json.dumps(status, indent=2))

        return proc.pid

    def status(self, batch_id: str, watch: bool = False) -> Dict:
        """查询批次状态"""
        batch_dir = self.workspace / batch_id
        if not batch_dir.exists():
            raise ValueError(f"批次不存在: {batch_id}")

        batch = json.loads((batch_dir / "batch.json").read_text())

        while True:
            # 收集所有任务状态
            statuses = []
            for task in batch["tasks"]:
                status_file = batch_dir / f"{task['id']}.status"
                if status_file.exists():
                    status = json.loads(status_file.read_text())

                    # 检查进程是否还在运行
                    if status.get("pid") and self._is_running(status["pid"]):
                        status["status"] = "RUNNING"
                        # 尝试读取部分输出显示进度
                        output_file = Path(status["output_file"])
                        if output_file.exists():
                            size = output_file.stat().st_size
                            status["output_size"] = f"{size}B"
                    else:
                        # 检查输出文件判断成功/失败
                        output_file = Path(status["output_file"])
                        if output_file.exists():
                            try:
                                output = output_file.read_text()
                                if '"success": true' in output or '"success":true' in output:
                                    status["status"] = "DONE"
                                    # 提取简要结果
                                    try:
                                        result = json.loads(output)
                                        msg = result.get("agent_messages", "")
                                        status["summary"] = msg[:100] + "..." if len(msg) > 100 else msg
                                    except:
                                        status["summary"] = "Completed"
                                elif '"success": false' in output or '"success":false' in output:
                                    status["status"] = "FAILED"
                                    try:
                                        result = json.loads(output)
                                        status["error"] = result.get("error", "Unknown error")[:100]
                                    except:
                                        status["error"] = "Task failed"
                                else:
                                    status["status"] = "UNKNOWN"
                            except Exception as e:
                                status["status"] = "ERROR"
                                status["error"] = str(e)
                        else:
                            status["status"] = "FAILED"
                            status["error"] = "No output file"

                    # 计算持续时间
                    start = datetime.fromisoformat(status["start_time"])
                    duration = (datetime.now() - start).total_seconds()
                    status["duration"] = f"{int(duration)}s"

                    statuses.append(status)
                else:
                    # 任务尚未启动
                    statuses.append({
                        "task_id": task["id"],
                        "ally": task["ally"],
                        "status": "PENDING",
                        "duration": "N/A"
                    })

            result = {
                "batch_id": batch_id,
                "tasks": statuses,
                "summary": self._summarize(statuses)
            }

            if not watch:
                return result

            # Watch mode: 清屏并显示
            os.system('clear')
            self._print_status(result)

            # 检查是否全部完成
            if result["summary"]["running"] == 0 and result["summary"]["pending"] == 0:
                print("\n✅ 所有任务已完成")
                break

            time.sleep(3)

        return result

    def _is_running(self, pid: int) -> bool:
        """检查进程是否运行"""
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

    def _summarize(self, statuses: List[Dict]) -> Dict:
        """汇总状态"""
        done = sum(1 for s in statuses if s["status"] == "DONE")
        running = sum(1 for s in statuses if s["status"] == "RUNNING")
        failed = sum(1 for s in statuses if s["status"] in ["FAILED", "ERROR"])
        pending = sum(1 for s in statuses if s["status"] == "PENDING")
        unknown = sum(1 for s in statuses if s["status"] == "UNKNOWN")

        return {
            "done": done,
            "running": running,
            "failed": failed,
            "pending": pending,
            "unknown": unknown,
            "total": len(statuses)
        }

    def _print_status(self, status: Dict):
        """打印状态表格"""
        print(f"\n📦 Batch: {status['batch_id']}")
        print("━" * 80)
        print(f"{'ID':<15} {'Ally':<10} {'Status':<15} {'Duration':<12} {'Info':<30}")
        print("━" * 80)

        status_emoji = {
            "DONE": "✅ DONE",
            "FAILED": "❌ FAILED",
            "ERROR": "💥 ERROR",
            "RUNNING": "🔄 RUNNING",
            "PENDING": "⏳ PENDING",
            "UNKNOWN": "❓ UNKNOWN"
        }

        for task in status["tasks"]:
            info = ""
            if task["status"] == "RUNNING" and "output_size" in task:
                info = task["output_size"]
            elif task["status"] == "DONE" and "summary" in task:
                info = task["summary"][:30]
            elif task["status"] in ["FAILED", "ERROR"] and "error" in task:
                info = task["error"][:30]

            print(f"{task['task_id']:<15} {task['ally']:<10} "
                  f"{status_emoji.get(task['status'], task['status']):<15} "
                  f"{task.get('duration', 'N/A'):<12} {info:<30}")

        print("━" * 80)
        summary = status["summary"]
        print(f"Overall: {summary['done']} done, {summary['running']} running, "
              f"{summary['failed']} failed, {summary['pending']} pending")
        if summary['unknown'] > 0:
            print(f"         {summary['unknown']} unknown")

    def results(self, batch_id: str, output_file: Optional[Path] = None) -> str:
        """生成结果报告（Markdown）"""
        status = self.status(batch_id)
        batch_dir = self.workspace / batch_id

        lines = [f"# {batch_id} - Results Summary\n"]
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        summary = status["summary"]
        lines.append(f"## ✅ Completed: {summary['done']}/{summary['total']} tasks\n")

        if summary["failed"] > 0:
            lines.append(f"## ⚠️ Failed: {summary['failed']} tasks\n")

        if summary["running"] > 0:
            lines.append(f"## 🔄 Still Running: {summary['running']} tasks\n")

        for task in status["tasks"]:
            lines.append(f"### Task: {task['task_id']} ({task['ally']})\n")

            status_emoji = {
                "DONE": "✅ Success",
                "FAILED": "❌ Failed",
                "ERROR": "💥 Error",
                "RUNNING": "🔄 Running",
                "PENDING": "⏳ Pending",
                "UNKNOWN": "❓ Unknown"
            }
            lines.append(f"**Status:** {status_emoji.get(task['status'], task['status'])}")
            lines.append(f"**Duration:** {task.get('duration', 'N/A')}\n")

            # 读取任务输出
            output_file_path = Path(task.get("output_file", ""))
            if output_file_path.exists():
                try:
                    output_text = output_file_path.read_text()
                    output = json.loads(output_text)

                    if output.get("success"):
                        lines.append("**Output:**")
                        lines.append("```")
                        lines.append(output.get("agent_messages", "No output"))
                        lines.append("```")
                    else:
                        lines.append("**Error:**")
                        lines.append("```")
                        lines.append(output.get("error", "Unknown error"))
                        lines.append("```")
                except json.JSONDecodeError:
                    lines.append("**Raw Output:**")
                    lines.append("```")
                    lines.append(output_text[:500])  # 限制长度
                    if len(output_text) > 500:
                        lines.append("\n... (truncated)")
                    lines.append("```")
                except Exception as e:
                    lines.append(f"**Error reading output:** {e}")
            else:
                lines.append("**Output:** No output file found")

            lines.append("")

        report = "\n".join(lines)

        # 可选：保存到文件
        if output_file:
            output_file.write_text(report)
            print(f"📄 Report saved to: {output_file}")

        return report

    def kill(self, batch_id: str, task_id: Optional[str] = None):
        """终止批次或特定任务"""
        batch_dir = self.workspace / batch_id
        if not batch_dir.exists():
            raise ValueError(f"批次不存在: {batch_id}")

        batch = json.loads((batch_dir / "batch.json").read_text())

        tasks_to_kill = [task_id] if task_id else [t["id"] for t in batch["tasks"]]

        killed = 0
        for tid in tasks_to_kill:
            status_file = batch_dir / f"{tid}.status"
            if status_file.exists():
                status = json.loads(status_file.read_text())
                pid = status.get("pid")

                if pid and self._is_running(pid):
                    try:
                        os.kill(pid, signal.SIGTERM)
                        print(f"🛑 Killed task: {tid} (PID: {pid})")
                        killed += 1
                    except Exception as e:
                        print(f"⚠️  Failed to kill task {tid}: {e}")

        print(f"\n✅ Killed {killed} task(s)")


def main():
    if len(sys.argv) < 2:
        print("Usage: orchestrator.py {dispatch|status|results|kill|watch} <args>")
        print("\nCommands:")
        print("  dispatch <batch-file>       - 分发任务批次")
        print("  status <batch-id>           - 查看批次状态")
        print("  watch <batch-id>            - 实时监控批次状态")
        print("  results <batch-id> [output] - 生成结果报告")
        print("  kill <batch-id> [task-id]   - 终止批次或特定任务")
        sys.exit(1)

    orchestrator = HiOrchestrator()
    command = sys.argv[1]

    try:
        if command == "dispatch":
            if len(sys.argv) < 3:
                print("Usage: orchestrator.py dispatch <batch-file>")
                sys.exit(1)
            batch_file = Path(sys.argv[2])
            orchestrator.dispatch(batch_file)

        elif command == "status":
            if len(sys.argv) < 3:
                print("Usage: orchestrator.py status <batch-id>")
                sys.exit(1)
            batch_id = sys.argv[2]
            status = orchestrator.status(batch_id)
            orchestrator._print_status(status)

        elif command == "watch":
            if len(sys.argv) < 3:
                print("Usage: orchestrator.py watch <batch-id>")
                sys.exit(1)
            batch_id = sys.argv[2]
            orchestrator.status(batch_id, watch=True)

        elif command == "results":
            if len(sys.argv) < 3:
                print("Usage: orchestrator.py results <batch-id> [output-file]")
                sys.exit(1)
            batch_id = sys.argv[2]
            output_file = Path(sys.argv[3]) if len(sys.argv) > 3 else None
            report = orchestrator.results(batch_id, output_file)
            print(report)

        elif command == "kill":
            if len(sys.argv) < 3:
                print("Usage: orchestrator.py kill <batch-id> [task-id]")
                sys.exit(1)
            batch_id = sys.argv[2]
            task_id = sys.argv[3] if len(sys.argv) > 3 else None
            orchestrator.kill(batch_id, task_id)

        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
