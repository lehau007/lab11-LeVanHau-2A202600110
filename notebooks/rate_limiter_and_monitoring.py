"""
Rate Limiter and Monitoring Implementation for Lab 11
Copy these code blocks into your Jupyter notebook
"""

# ============================================================
# PART 5: RATE LIMITER
# ============================================================

import time
from collections import defaultdict, deque

class RateLimiter:
    """Simple rate limiter using sliding window algorithm."""
    
    def __init__(self, max_requests=10, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.user_requests = defaultdict(deque)
        self.blocked_count = 0
        self.total_count = 0
    
    def is_allowed(self, user_id: str) -> tuple:
        """Check if user is allowed to make a request."""
        self.total_count += 1
        now = time.time()
        user_window = self.user_requests[user_id]
        
        # Remove expired timestamps
        while user_window and user_window[0] < now - self.window_seconds:
            user_window.popleft()
        
        # Check if limit exceeded
        if len(user_window) >= self.max_requests:
            self.blocked_count += 1
            oldest = user_window[0]
            wait_time = int(self.window_seconds - (now - oldest))
            return False, f"Rate limit exceeded. Please wait {wait_time} seconds."
        
        # Allow request
        user_window.append(now)
        return True, "Request allowed"
    
    def get_stats(self) -> dict:
        """Get rate limiter statistics."""
        return {
            "total_requests": self.total_count,
            "blocked_requests": self.blocked_count,
            "block_rate": self.blocked_count / self.total_count if self.total_count > 0 else 0,
            "active_users": len(self.user_requests)
        }


class RateLimitPlugin(base_plugin.BasePlugin):
    """ADK Plugin for rate limiting."""
    
    def __init__(self, max_requests=10, window_seconds=60):
        super().__init__(name="rate_limiter")
        self.limiter = RateLimiter(max_requests, window_seconds)
    
    async def on_user_message_callback(
        self,
        *,
        invocation_context: InvocationContext,
        user_message: types.Content,
    ) -> types.Content | None:
        """Check rate limit before processing message."""
        user_id = invocation_context.user_id if invocation_context else "anonymous"
        
        allowed, message = self.limiter.is_allowed(user_id)
        
        if not allowed:
            return types.Content(
                role="model",
                parts=[types.Part.from_text(text=message)]
            )
        
        return None


# ============================================================
# PART 6: AUDIT & MONITORING
# ============================================================

import json
from datetime import datetime
from dataclasses import dataclass, field, asdict

@dataclass
class AuditEntry:
    """Single audit log entry."""
    timestamp: str
    user_id: str
    session_id: str
    input_text: str
    output_text: str
    blocked_by: list = field(default_factory=list)
    redacted: bool = False
    latency_ms: float = 0.0
    metadata: dict = field(default_factory=dict)


class AuditLogger:
    """Audit logger for tracking all interactions."""
    
    def __init__(self):
        self.entries = []
        self.start_times = {}
    
    def start_request(self, user_id: str, session_id: str, input_text: str):
        """Record start of request."""
        request_id = f"{user_id}_{session_id}_{len(self.entries)}"
        self.start_times[request_id] = time.time()
        return request_id
    
    def end_request(
        self,
        request_id: str,
        user_id: str,
        session_id: str,
        input_text: str,
        output_text: str,
        blocked_by: list = None,
        redacted: bool = False,
        metadata: dict = None
    ):
        """Record end of request."""
        start_time = self.start_times.pop(request_id, time.time())
        latency_ms = (time.time() - start_time) * 1000
        
        entry = AuditEntry(
            timestamp=datetime.now().isoformat(),
            user_id=user_id,
            session_id=session_id,
            input_text=input_text,
            output_text=output_text,
            blocked_by=blocked_by or [],
            redacted=redacted,
            latency_ms=latency_ms,
            metadata=metadata or {}
        )
        
        self.entries.append(entry)
        return entry
    
    def export_json(self, filepath: str = "audit_log.json"):
        """Export audit log to JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(
                [asdict(entry) for entry in self.entries],
                f,
                indent=2,
                ensure_ascii=False
            )
        print(f"✅ Exported {len(self.entries)} entries to {filepath}")
    
    def get_stats(self) -> dict:
        """Get audit statistics."""
        total = len(self.entries)
        blocked = sum(1 for e in self.entries if e.blocked_by)
        redacted = sum(1 for e in self.entries if e.redacted)
        avg_latency = sum(e.latency_ms for e in self.entries) / total if total > 0 else 0
        
        return {
            "total_requests": total,
            "blocked_requests": blocked,
            "redacted_responses": redacted,
            "block_rate": blocked / total if total > 0 else 0,
            "avg_latency_ms": avg_latency,
            "unique_users": len(set(e.user_id for e in self.entries))
        }


class MonitoringSystem:
    """Real-time monitoring and alerting system."""
    
    def __init__(self, audit_logger: AuditLogger):
        self.audit_logger = audit_logger
        self.alerts = []
        self.thresholds = {
            "block_rate": 0.20,
            "avg_latency_ms": 2000,
            "rapid_blocks": 5,
        }
    
    def check_metrics(self):
        """Check metrics and fire alerts if thresholds exceeded."""
        stats = self.audit_logger.get_stats()
        
        print("\n" + "=" * 70)
        print("📊 MONITORING DASHBOARD")
        print("=" * 70)
        
        print(f"\n📈 Current Metrics:")
        print(f"  Total Requests: {stats['total_requests']}")
        print(f"  Blocked: {stats['blocked_requests']} ({stats['block_rate']:.1%})")
        print(f"  Redacted: {stats['redacted_responses']}")
        print(f"  Avg Latency: {stats['avg_latency_ms']:.1f}ms")
        print(f"  Unique Users: {stats['unique_users']}")
        
        alerts_fired = []
        
        if stats['block_rate'] > self.thresholds['block_rate']:
            alert = f"⚠️  HIGH BLOCK RATE: {stats['block_rate']:.1%}"
            alerts_fired.append(alert)
        
        if stats['avg_latency_ms'] > self.thresholds['avg_latency_ms']:
            alert = f"⚠️  HIGH LATENCY: {stats['avg_latency_ms']:.1f}ms"
            alerts_fired.append(alert)
        
        recent_entries = [e for e in self.audit_logger.entries[-20:]]
        recent_blocks = sum(1 for e in recent_entries if e.blocked_by)
        if recent_blocks >= self.thresholds['rapid_blocks']:
            alert = f"⚠️  RAPID BLOCKS: {recent_blocks} blocks detected"
            alerts_fired.append(alert)
        
        if alerts_fired:
            print(f"\n🚨 ALERTS ({len(alerts_fired)}):")
            for alert in alerts_fired:
                print(f"  {alert}")
        else:
            print(f"\n✅ All metrics within normal range")
        
        print("=" * 70)
        
        return alerts_fired
    
    def get_top_blocked_users(self, n=5):
        """Get users with most blocked requests."""
        user_blocks = defaultdict(int)
        for entry in self.audit_logger.entries:
            if entry.blocked_by:
                user_blocks[entry.user_id] += 1
        
        top_users = sorted(user_blocks.items(), key=lambda x: x[1], reverse=True)[:n]
        
        print(f"\n🔍 Top {n} Users with Blocked Requests:")
        for user_id, count in top_users:
            print(f"  {user_id}: {count} blocked")
        
        return top_users
    
    def get_attack_patterns(self):
        """Analyze attack patterns."""
        blocked_entries = [e for e in self.audit_logger.entries if e.blocked_by]
        
        guardrail_counts = defaultdict(int)
        for entry in blocked_entries:
            for guardrail in entry.blocked_by:
                guardrail_counts[guardrail] += 1
        
        print(f"\n🛡️  Blocks by Guardrail Type:")
        for guardrail, count in sorted(guardrail_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {guardrail}: {count}")
        
        return guardrail_counts


class AuditPlugin(base_plugin.BasePlugin):
    """ADK Plugin for audit logging."""
    
    def __init__(self, audit_logger: AuditLogger):
        super().__init__(name="audit_logger")
        self.audit_logger = audit_logger
        self.current_request_id = None
        self.current_input = ""
        self.current_user = "anonymous"
        self.current_session = "unknown"
    
    async def on_user_message_callback(
        self,
        *,
        invocation_context: InvocationContext,
        user_message: types.Content,
    ) -> types.Content | None:
        """Record input."""
        self.current_user = invocation_context.user_id if invocation_context else "anonymous"
        self.current_session = invocation_context.session_id if invocation_context else "unknown"
        
        text = ""
        if user_message and user_message.parts:
            for part in user_message.parts:
                if hasattr(part, 'text') and part.text:
                    text += part.text
        
        self.current_input = text
        self.current_request_id = self.audit_logger.start_request(
            self.current_user, self.current_session, text
        )
        
        return None
    
    async def after_model_callback(
        self,
        *,
        callback_context,
        llm_response,
    ):
        """Record output."""
        text = ""
        if hasattr(llm_response, 'content') and llm_response.content:
            for part in llm_response.content.parts:
                if hasattr(part, 'text') and part.text:
                    text += part.text
        
        if self.current_request_id:
            self.audit_logger.end_request(
                self.current_request_id,
                self.current_user,
                self.current_session,
                self.current_input,
                text
            )
        
        return llm_response


# ============================================================
# USAGE EXAMPLE
# ============================================================

# Create audit logger and monitoring
audit_logger = AuditLogger()
monitoring = MonitoringSystem(audit_logger)

# Create fully protected agent
fully_protected_agent = llm_agent.LlmAgent(
    model="gemini-2.5-flash-lite",
    name="fully_protected_assistant",
    instruction="You are a helpful VinBank assistant."
)

fully_protected_runner = runners.InMemoryRunner(
    agent=fully_protected_agent,
    app_name="fully_protected",
    plugins=[
        RateLimitPlugin(max_requests=10, window_seconds=60),
        InputGuardrailPlugin(),
        OutputGuardrailPlugin(use_llm_judge=False),
        AuditPlugin(audit_logger)
    ]
)

print("✅ Fully protected agent created with all layers!")
