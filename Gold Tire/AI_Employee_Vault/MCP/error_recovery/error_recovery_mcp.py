"""
Error Recovery MCP - Retry Logic and Graceful Degradation
Version: 0.3 Gold Tier
Owner: Suleman AI Employee v0.3

Handles failures with exponential backoff retry and graceful degradation.
Creates human alerts for critical failures.
"""

import json
import sys
import os
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Callable

# Configuration
ROOT_DIR = Path(__file__).parent.parent.parent
LOGS_DIR = ROOT_DIR / "Logs"
PENDING_APPROVAL_DIR = ROOT_DIR / "Pending_Approval"

# Ensure directories exist
LOGS_DIR.mkdir(exist_ok=True)
PENDING_APPROVAL_DIR.mkdir(exist_ok=True)

# Retry configuration
DEFAULT_MAX_RETRIES = 3
BASE_DELAY = 1  # seconds (1s -> 4s -> 16s exponential backoff)


def get_audit_log_path() -> Path:
    """Get today's audit log file path."""
    today = datetime.now().strftime("%Y-%m-%d")
    return LOGS_DIR / f"audit_{today}.json"


def log_action(action: str, status: str, details: Optional[Dict] = None, error: Optional[str] = None):
    """Log every action to audit JSON file."""
    log_path = get_audit_log_path()
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "status": status,
        "details": details or {},
        "error": error
    }
    
    # Load existing logs
    logs = []
    if log_path.exists():
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except (json.JSONDecodeError, IOError):
            logs = []
    
    # Append new entry
    logs.append(entry)
    
    # Save back
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def create_error_alert(action: str, error: str, params: Dict, attempt: int):
    """
    Create an error alert file for human review.
    
    Args:
        action: The action that failed
        error: Error message
        params: Original parameters
        attempt: Number of retry attempts made
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    alert_file = PENDING_APPROVAL_DIR / f"ERROR_ALERT_{action}_{timestamp}.md"
    
    content = f"""# Error Alert - Manual Review Required

**Generated:** {datetime.now().isoformat()}  
**Action:** {action}  
**Retry Attempts:** {attempt}  
**Status:** CRITICAL - Requires Human Intervention

---

## Error Details

```
{error}
```

## Original Parameters

```json
{json.dumps(params, indent=2)}
```

## Stack Trace

```
{traceback.format_exc()}
```

---

## Required Actions

- [ ] Review error cause
- [ ] Fix underlying issue
- [ ] Re-run action manually or approve retry
- [ ] Update this file with resolution

---

**Assigned To:** System Administrator  
**Priority:** High
"""
    
    with open(alert_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    log_action("error_alert_created", "warning", {
        "file": str(alert_file),
        "action": action
    })
    
    return str(alert_file)


def exponential_backoff_retry(
    func: Callable,
    *args,
    max_retries: int = DEFAULT_MAX_RETRIES,
    base_delay: float = BASE_DELAY,
    action_name: str = "",
    **kwargs
) -> Dict[str, Any]:
    """
    Execute function with exponential backoff retry.
    
    Backoff schedule: 1s -> 4s -> 16s (exponential: base_delay * 4^attempt)
    
    Args:
        func: Function to execute
        *args: Positional arguments for func
        max_retries: Maximum retry attempts
        base_delay: Base delay in seconds
        action_name: Name of action for logging
        **kwargs: Keyword arguments for func
    
    Returns:
        Dict with success status, result or error, and attempt count
    """
    last_error = None
    results = []
    
    for attempt in range(max_retries + 1):  # +1 for initial attempt
        try:
            # Log retry attempt (skip for first attempt)
            if attempt > 0:
                delay = base_delay * (4 ** (attempt - 1))  # 1s -> 4s -> 16s
                log_action(f"{action_name}_retry", "info", {
                    "attempt": attempt,
                    "max_retries": max_retries,
                    "delay_seconds": delay
                })
                time.sleep(delay)
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Log success
            log_action(f"{action_name}", "success", {
                "attempt": attempt + 1,
                "total_attempts": attempt + 1
            })
            
            return {
                "status": "success",
                "result": result,
                "attempts": attempt + 1,
                "retries": attempt
            }
            
        except Exception as e:
            last_error = e
            error_msg = str(e)
            
            # Log failure
            log_action(f"{action_name}_attempt_failed", "warning", {
                "attempt": attempt + 1,
                "error": error_msg
            })
            
            results.append({
                "attempt": attempt + 1,
                "error": error_msg
            })
    
    # All retries exhausted
    error_msg = str(last_error) if last_error else "Unknown error"
    
    log_action(f"{action_name}_failed", "error", {
        "max_retries": max_retries,
        "final_error": error_msg,
        "all_attempts": results
    })
    
    # Create human alert for critical failure
    alert_file = create_error_alert(
        action_name,
        error_msg,
        kwargs.get("params", {}),
        max_retries + 1
    )
    
    return {
        "status": "failed",
        "error": error_msg,
        "attempts": max_retries + 1,
        "retries": max_retries,
        "alert_file": alert_file,
        "all_attempts": results
    }


def graceful_degradation(
    actions: list,
    input_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Try multiple actions/platforms with graceful degradation.
    If one fails, continue with others.
    
    Args:
        actions: List of (action_name, func) tuples
        input_data: Input data for all actions
    
    Returns:
        Dict with partial success info
    """
    results = {
        "successful": [],
        "failed": [],
        "partial_success": False
    }
    
    for action_name, func in actions:
        try:
            log_action(f"graceful_degradation_{action_name}", "info", {
                "status": "attempting"
            })
            
            result = func(input_data)
            
            if isinstance(result, dict) and result.get("status") == "success":
                results["successful"].append({
                    "action": action_name,
                    "result": result
                })
                log_action(f"graceful_degradation_{action_name}", "success", {})
            else:
                results["failed"].append({
                    "action": action_name,
                    "error": result.get("error", "Unknown") if isinstance(result, dict) else str(result)
                })
                log_action(f"graceful_degradation_{action_name}", "error", {
                    "error": result.get("error", "Unknown") if isinstance(result, dict) else str(result)
                })
                
        except Exception as e:
            results["failed"].append({
                "action": action_name,
                "error": str(e)
            })
            log_action(f"graceful_degradation_{action_name}", "error", {
                "error": str(e)
            })
    
    # Determine overall status
    if results["successful"] and results["failed"]:
        results["partial_success"] = True
        results["status"] = "partial_success"
    elif results["successful"]:
        results["status"] = "success"
    else:
        results["status"] = "failed"
    
    return results


def execute_recovery_action(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main execution function for error recovery actions.
    
    Args:
        input_data: JSON with action type and parameters
    
    Returns:
        Dict with recovery result
    """
    action_type = input_data.get("action_type", "")
    params = input_data.get("params", {})
    max_retries = input_data.get("max_retries", DEFAULT_MAX_RETRIES)
    
    log_action("error_recovery_start", "info", {
        "action_type": action_type,
        "max_retries": max_retries
    })
    
    # Handle different recovery action types
    if action_type == "retry_with_backoff":
        # For retry actions, we need the actual function to call
        # This is a placeholder - in practice, you'd map action_type to actual functions
        return {
            "status": "error",
            "error": "retry_with_backoff requires a target function"
        }
    
    elif action_type == "graceful_degradation":
        actions_list = input_data.get("actions", [])
        # Execute with graceful degradation
        return graceful_degradation(actions_list, params)
    
    elif action_type == "log_and_alert":
        # Just log and create alert
        error_msg = params.get("error", "Unknown error")
        alert_file = create_error_alert(
            params.get("action", "unknown"),
            error_msg,
            params,
            0
        )
        return {
            "status": "alert_created",
            "alert_file": alert_file
        }
    
    else:
        return {
            "status": "error",
            "error": f"Unknown recovery action type: {action_type}"
        }


def main():
    """Entry point - reads JSON from stdin and executes recovery action."""
    try:
        # Read input from stdin
        input_text = sys.stdin.read()
        
        if not input_text.strip():
            print(json.dumps({"status": "error", "error": "No input provided"}))
            return
        
        input_data = json.loads(input_text)
        
        # Execute recovery action
        result = execute_recovery_action(input_data)
        
        # Output result as JSON
        print(json.dumps(result, indent=2))
        
    except json.JSONDecodeError as e:
        error_result = {"status": "error", "error": f"Invalid JSON input: {str(e)}"}
        log_action("error_recovery_mcp", "error", error_result)
        print(json.dumps(error_result))
    except Exception as e:
        error_result = {"status": "error", "error": str(e)}
        log_action("error_recovery_mcp", "error", error_result)
        print(json.dumps(error_result))


if __name__ == "__main__":
    main()
