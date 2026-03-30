"""
Claude Computer Use Demo
Shows how to use Claude's computer use capability with practical examples.
Note: Requires claude-3-5-sonnet and beta header.
"""
import anthropic
import base64
import subprocess
import json
import os
from pathlib import Path

client = anthropic.Anthropic()

def take_screenshot() -> str:
    """Take screenshot and return as base64"""
    try:
        # Linux/Mac
        subprocess.run(["scrot", "/tmp/screenshot.png"], check=True, capture_output=True)
    except FileNotFoundError:
        try:
            subprocess.run(["import", "-window", "root", "/tmp/screenshot.png"], check=True, capture_output=True)
        except Exception:
            # Create a test image if no screenshot tool available
            from PIL import Image, ImageDraw
            img = Image.new('RGB', (1280, 720), color='white')
            draw = ImageDraw.Draw(img)
            draw.text((400, 300), "Computer Use Demo Screen", fill='black')
            img.save("/tmp/screenshot.png")
    
    with open("/tmp/screenshot.png", "rb") as f:
        return base64.standard_b64encode(f.read()).decode()

def run_bash(command: str) -> str:
    """Execute a bash command safely"""
    safe_commands = ["ls", "cat", "echo", "pwd", "date", "python3", "pip"]
    cmd_name = command.strip().split()[0]
    if cmd_name not in safe_commands:
        return f"Command '{cmd_name}' not in allowlist for safety"
    result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
    return result.stdout + result.stderr

def computer_use_task(task: str, max_iterations: int = 10) -> str:
    """Run a computer use task with tool loop"""
    print(f"\n🖥️  Computer Use Task: {task}")
    
    tools = [
        {
            "type": "computer_20241022",
            "name": "computer",
            "display_width_px": 1280,
            "display_height_px": 720,
            "display_number": 1,
        },
        {
            "type": "bash_20241022",
            "name": "bash",
        },
        {
            "type": "text_editor_20241022",
            "name": "str_replace_editor",
        }
    ]
    
    messages = [{"role": "user", "content": task}]
    
    for i in range(max_iterations):
        response = client.beta.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            tools=tools,
            messages=messages,
            betas=["computer-use-2024-10-22"],
        )
        
        print(f"  Iteration {i+1}: stop_reason={response.stop_reason}")
        
        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
            return "Task completed"
        
        tool_calls = [b for b in response.content if b.type == "tool_use"]
        if not tool_calls:
            break
        
        messages.append({"role": "assistant", "content": response.content})
        
        tool_results = []
        for tc in tool_calls:
            print(f"    Tool: {tc.name}({list(tc.input.keys())})")
            
            if tc.name == "computer":
                action = tc.input.get("action")
                if action == "screenshot":
                    screenshot = take_screenshot()
                    result = {
                        "type": "tool_result",
                        "tool_use_id": tc.id,
                        "content": [{
                            "type": "image",
                            "source": {"type": "base64", "media_type": "image/png", "data": screenshot}
                        }]
                    }
                else:
                    result = {"type": "tool_result", "tool_use_id": tc.id, "content": f"Action {action} simulated"}
                tool_results.append(result)
            
            elif tc.name == "bash":
                cmd = tc.input.get("command", "")
                output = run_bash(cmd)
                tool_results.append({"type": "tool_result", "tool_use_id": tc.id, "content": output})
            
            elif tc.name == "str_replace_editor":
                cmd = tc.input.get("command", "")
                path = tc.input.get("path", "")
                tool_results.append({"type": "tool_result", "tool_use_id": tc.id, "content": f"Editor action {cmd} on {path} simulated"})
        
        messages.append({"role": "user", "content": tool_results})
    
    return "Max iterations reached"

def demo_examples():
    """Run several example tasks"""
    examples = [
        "List all Python files in the current directory and tell me what each one does based on its name",
        "Show me the current date and time, then calculate how many days until December 31st",
        "Create a simple Python script that prints 'Hello from Claude Computer Use!' and explain what it does",
    ]
    
    print("=" * 60)
    print("🖥️  Claude Computer Use Demo")
    print("=" * 60)
    
    for i, task in enumerate(examples, 1):
        print(f"\n📋 Example {i}: {task}")
        result = computer_use_task(task, max_iterations=5)
        print(f"\n✅ Result:\n{result}")
        print("-" * 40)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
        result = computer_use_task(task)
        print(f"\nResult: {result}")
    else:
        demo_examples()
