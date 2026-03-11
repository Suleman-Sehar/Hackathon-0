"""
MCP: Error Recovery Handler
Provides retry logic, graceful degradation, and comprehensive logging.
"""

import json
import sys
import os
import time
from datetime import datetime
from pathlib import Path
import traceback

# Configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
LOGS_DIR = Path(__file__).parent.parent.parent / "Logs"

def get_audit_log_path():
    """Get today's audit log path."""
    today = datetime.now().strftime("%Y-%m-%d")
    return LOGS_DIR / f"audit_{today}.json"

def log_action(action, status, details=None, error=None):
    """Log every action to audit file."""
    LOGS_DIR.mkdir(exist_ok=True)
    log_path = get_audit_log_path()
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "status": status,
        "details": details or {},
        "error": str(error) if error else None,
        "traceback": traceback.format_exc() if error and os.environ.get("DEBUG") else None
    }
    
    # Load existing logs
    logs = []
    if log_path.exists():
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except:
            logs = []
    
    logs.append(entry)
    
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

def retry_with_backoff(func, *args, max_retries=MAX_RETRIES, **kwargs):
    """Execute function with retry and exponential backoff."""
    last_error = None
    
    for attempt in range(max_retries):
        try:
            log_action("retry_attempt", "info", {
                "function": func.__name__,
                "attempt": attempt + 1,
                "max_retries": max_retries
            })
            
            result = func(*args, **kwargs)
            
            log_action("retry_success", "success", {
                "function": func.__name__,
                "attempts": attempt + 1
            })
            
            return {"success": True, "result": result, "attempts": attempt + 1}
            
        except Exception as e:
            last_error = e
            log_action("retry_failed", "warning", {
                "function": func.__name__,
                "attempt": attempt + 1,
                "error": str(e)
            })
            
            if attempt < max_retries - 1:
                delay = RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                time.sleep(delay)
    
    # All retries exhausted
    log_action("retry_exhausted", "error", {
        "function": func.__name__,
        "max_retries": max_retries,
        "final_error": str(last_error)
    })
    
    return {
        "success": False,
        "error": str(last_error),
        "attempts": max_retries,
        "traceback": traceback.format_exc()
    }

def graceful_degradation(input_data, available_services):
    """
    When primary service fails, try alternative services.
    Returns first successful result or aggregated errors.
    """
    primary = input_data.get("primary_service")
    fallbacks = input_data.get("fallback_services", [])
    
    results = []
    
    # Try primary first
    if primary in available_services:
        log_action("graceful_degradation", "info", {"trying": primary, "type": "primary"})
        try:
            result = available_services[primary](input_data)
            if result.get("success"):
                return {"success": True, "service": primary, "result": result}
            results.append({"service": primary, "result": result})
        except Exception as e:
            results.append({"service": primary, "error": str(e)})
    
    # Try fallbacks in order
    for fallback in fallbacks:
        if fallback in available_services:
            log_action("graceful_degradation", "info", {"trying": fallback, "type": "fallback"})
            try:
                result = available_services[fallback](input_data)
                if result.get("success"):
                    return {"success": True, "service": fallback, "result": result, "degraded": True}
                results.append({"service": fallback, "result": result})
            except Exception as e:
                results.append({"service": fallback, "error": str(e)})
    
    # All failed
    log_action("graceful_degradation", "error", {
        "all_failed": True,
        "results": results
    })
    
    return {
        "success": False,
        "degraded": True,
        "all_attempts": results,
        "error": "All services failed"
    }

def execute_recovery(input_data):
    """Main recovery execution handler."""
    action = input_data.get("action")
    target_function = input_data.get("function")
    params = input_data.get("params", {})
    
    log_action("recovery_start", "info", {
        "action": action,
        "function": target_function,
        "params": params
    })
    
    # Define available recovery actions
    recovery_actions = {
        "retry": lambda: retry_with_backoff(
            globals().get(target_function, lambda: None),
            **params
        ),
        "degrade": lambda: graceful_degradation(
            input_data,
            input_data.get("available_services", {})
        ),
        "log_error": lambda: log_action(
            "manual_error",
            "error",
            params
        )
    }
    
    if action not in recovery_actions:
        return {
            "success": False,
            "error": f"Unknown recovery action: {action}"
        }
    
    try:
        result = recovery_actions[action]()
        log_action("recovery_complete", "success", {
            "action": action,
            "result": result
        })
        return result
    except Exception as e:
        log_action("recovery_failed", "error", {
            "action": action,
            "error": str(e)
        })
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

def main():
    """Entry point - accepts JSON from stdin."""
    try:
        input_json = sys.stdin.read()
        input_data = json.loads(input_json)
        
        result = execute_recovery(input_data)
        print(json.dumps(result))
        
    except json.JSONDecodeError as e:
        error = {"status": "failed", "error": f"Invalid JSON input: {str(e)}"}
        log_action("recovery", "failed", error)
        print(json.dumps(error))
    except Exception as e:
        error = {"status": "failed", "error": str(e)}
        log_action("recovery", "failed", error)
        print(json.dumps(error))

if __name__ == "__main__":
    main()
