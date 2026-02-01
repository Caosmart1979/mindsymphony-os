"""
Lightning Tracer - 非侵入式事件追踪器

受 Microsoft Agent Lightning 启发，实现 emit_xxx 风格的追踪接口
核心特性:
1. 零代码侵入（通过装饰器和运行时钩子）
2. 低开销（异步写入，采样控制）
3. 丰富的上下文捕获
4. 与现有 MindSymphony 无缝集成
"""

import time
import uuid
import json
import hashlib
import functools
from typing import Any, Dict, Optional, Callable, List
from dataclasses import dataclass, asdict
from datetime import datetime
from contextvars import ContextVar
from enum import Enum
import threading
import queue


class SpanType(Enum):
    """追踪事件类型"""
    SKILL_INVOCATION = "skill_invocation"
    TOOL_EXECUTION = "tool_execution"
    REASONING_STEP = "reasoning_step"
    USER_INTERACTION = "user_interaction"
    CROSS_SKILL_HANDOFF = "cross_skill_handoff"
    DECISION_POINT = "decision_point"


@dataclass
class Span:
    """追踪事件（Span）数据结构

    类比: OpenTelemetry Span + Lightning 特定字段
    """
    span_id: str
    trace_id: str
    parent_id: Optional[str]

    # 基础信息
    span_type: SpanType
    name: str  # skill_name, tool_name, etc.
    start_time: float
    end_time: Optional[float] = None
    duration_ms: Optional[float] = None

    # 输入输出（存储hash，可选存储完整内容）
    input_hash: Optional[str] = None
    input_data: Optional[str] = None  # 可配置是否存储
    output_hash: Optional[str] = None
    output_data: Optional[str] = None

    # 性能指标
    latency_ms: Optional[float] = None
    token_count: Optional[int] = None

    # 上下文
    metadata: Dict[str, Any] = None
    tags: List[str] = None

    # 状态
    status: str = "ok"  # ok, error, cancelled
    error_message: Optional[str] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.tags is None:
            self.tags = []

    def finish(self, output: Any = None, error: Exception = None):
        """完成 span"""
        self.end_time = time.time()
        self.duration_ms = (self.end_time - self.start_time) * 1000

        if output is not None:
            self.output_data = self._serialize(output)
            self.output_hash = self._hash(self.output_data)

        if error is not None:
            self.status = "error"
            self.error_message = str(error)

    def to_dict(self) -> Dict:
        """序列化为字典"""
        return {
            "span_id": self.span_id,
            "trace_id": self.trace_id,
            "parent_id": self.parent_id,
            "span_type": self.span_type.value,
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_ms": self.duration_ms,
            "input_hash": self.input_hash,
            "input_data": self.input_data,
            "output_hash": self.output_hash,
            "output_data": self.output_data,
            "latency_ms": self.latency_ms,
            "token_count": self.token_count,
            "metadata": self.metadata,
            "tags": self.tags,
            "status": self.status,
            "error_message": self.error_message,
        }

    @staticmethod
    def _serialize(data: Any) -> str:
        """序列化数据"""
        try:
            return json.dumps(data, ensure_ascii=False, default=str)
        except:
            return str(data)

    @staticmethod
    def _hash(data: str) -> str:
        """计算数据哈希"""
        return hashlib.sha256(data.encode()).hexdigest()[:16]


# 当前追踪上下文（线程安全）
_current_trace: ContextVar[Optional[Dict]] = ContextVar('current_trace', default=None)


class LightningTracer:
    """Lightning Tracer - 非侵入式追踪器

    核心方法:
    - emit_skill_invocation: 追踪技能调用
    - emit_tool_execution: 追踪工具执行
    - emit_user_interaction: 追踪用户交互
    - emit_cross_skill_handoff: 追踪技能交接
    - auto_trace: 装饰器，自动追踪函数

    示例:
        tracer = LightningTracer()

        # 方式1: 显式 emit
        tracer.emit_skill_invocation("my_skill", input_data, output_data)

        # 方式2: 装饰器自动追踪
        @tracer.auto_trace(span_type=SpanType.SKILL_INVOCATION)
        def my_skill(input_data):
            return output_data

        # 方式3: 上下文管理器
        with tracer.span("my_operation", SpanType.TOOL_EXECUTION) as span:
            result = do_something()
            span.set_output(result)
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.enabled = self.config.get('enabled', True)
        self.sampling_rate = self.config.get('sampling_rate', 1.0)
        self.store_full_data = self.config.get('store_full_data', True)
        self.max_queue_size = self.config.get('max_queue_size', 10000)

        # 异步写入队列
        self._queue: queue.Queue = queue.Queue(maxsize=self.max_queue_size)
        self._worker_thread: Optional[threading.Thread] = None
        self._shutdown = False

        # 存储后端（默认内存，可配置为 SQLite）
        self._store = None

        # 统计
        self._stats = {
            "spans_emitted": 0,
            "spans_dropped": 0,
            "spans_stored": 0,
        }

        if self.enabled:
            self._start_worker()

    def _start_worker(self):
        """启动后台写入线程"""
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()

    def _worker_loop(self):
        """后台写入循环"""
        while not self._shutdown:
            try:
                span = self._queue.get(timeout=1.0)
                self._store_span(span)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"[Tracer] Error storing span: {e}")

    def _store_span(self, span: Span):
        """存储 span 到后端"""
        # 延迟初始化存储
        if self._store is None:
            from ..store.core import LightningStore
            self._store = LightningStore()

        try:
            self._store.store_span(span)
            self._stats["spans_stored"] += 1
        except Exception as e:
            print(f"[Tracer] Failed to store span: {e}")
            self._stats["spans_dropped"] += 1

    def _should_sample(self) -> bool:
        """采样决策"""
        if self.sampling_rate >= 1.0:
            return True
        import random
        return random.random() < self.sampling_rate

    def _create_span(
        self,
        name: str,
        span_type: SpanType,
        parent_id: Optional[str] = None,
        input_data: Any = None,
        metadata: Optional[Dict] = None
    ) -> Span:
        """创建新的 span"""
        # 获取当前 trace 上下文
        current_trace = _current_trace.get()
        trace_id = current_trace["trace_id"] if current_trace else str(uuid.uuid4())

        # 序列化输入
        input_str = None
        input_hash = None
        if input_data is not None:
            input_str = Span._serialize(input_data) if self.store_full_data else None
            input_hash = Span._hash(Span._serialize(input_data))

        span = Span(
            span_id=str(uuid.uuid4()),
            trace_id=trace_id,
            parent_id=parent_id,
            span_type=span_type,
            name=name,
            start_time=time.time(),
            input_hash=input_hash,
            input_data=input_str,
            metadata=metadata or {},
        )

        return span

    def emit_skill_invocation(
        self,
        skill_name: str,
        input_data: Any,
        output_data: Any = None,
        latency_ms: Optional[float] = None,
        metadata: Optional[Dict] = None,
        parent_span_id: Optional[str] = None
    ) -> Optional[Span]:
        """发射技能调用事件

        Args:
            skill_name: 技能名称
            input_data: 输入数据
            output_data: 输出数据（可选）
            latency_ms: 延迟（毫秒，可选）
            metadata: 额外元数据
            parent_span_id: 父 span ID

        Returns:
            Span 对象（如果被采样）
        """
        if not self.enabled or not self._should_sample():
            return None

        span = self._create_span(
            name=skill_name,
            span_type=SpanType.SKILL_INVOCATION,
            parent_id=parent_span_id,
            input_data=input_data,
            metadata=metadata
        )

        span.latency_ms = latency_ms

        if output_data is not None:
            span.finish(output=output_data)

        # 异步写入队列
        try:
            self._queue.put_nowait(span)
            self._stats["spans_emitted"] += 1
        except queue.Full:
            self._stats["spans_dropped"] += 1

        return span

    def emit_tool_execution(
        self,
        tool_name: str,
        params: Dict[str, Any],
        result: Any = None,
        latency_ms: Optional[float] = None,
        error: Optional[Exception] = None,
        metadata: Optional[Dict] = None
    ) -> Optional[Span]:
        """发射工具执行事件"""
        if not self.enabled or not self._should_sample():
            return None

        span = self._create_span(
            name=tool_name,
            span_type=SpanType.TOOL_EXECUTION,
            input_data=params,
            metadata=metadata
        )

        span.latency_ms = latency_ms

        if result is not None or error is not None:
            span.finish(output=result, error=error)

        try:
            self._queue.put_nowait(span)
            self._stats["spans_emitted"] += 1
        except queue.Full:
            self._stats["spans_dropped"] += 1

        return span

    def emit_user_interaction(
        self,
        interaction_type: str,  # 'message', 'feedback', 'interruption', etc.
        content: Any,
        sentiment: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Optional[Span]:
        """发射用户交互事件

        用于捕获用户反馈、满意度信号
        """
        if not self.enabled or not self._should_sample():
            return None

        meta = metadata or {}
        meta["interaction_type"] = interaction_type
        if sentiment:
            meta["sentiment"] = sentiment

        span = self._create_span(
            name=f"user_{interaction_type}",
            span_type=SpanType.USER_INTERACTION,
            input_data=content,
            metadata=meta
        )

        span.finish(output={"captured": True})

        try:
            self._queue.put_nowait(span)
            self._stats["spans_emitted"] += 1
        except queue.Full:
            self._stats["spans_dropped"] += 1

        return span

    def emit_cross_skill_handoff(
        self,
        from_skill: str,
        to_skill: str,
        handoff_context: Dict[str, Any],
        metadata: Optional[Dict] = None
    ) -> Optional[Span]:
        """发射技能交接事件

        用于追踪多技能协作流程
        """
        if not self.enabled or not self._should_sample():
            return None

        meta = metadata or {}
        meta["from_skill"] = from_skill
        meta["to_skill"] = to_skill

        span = self._create_span(
            name=f"{from_skill}_to_{to_skill}",
            span_type=SpanType.CROSS_SKILL_HANDOFF,
            input_data=handoff_context,
            metadata=meta
        )

        span.finish()

        try:
            self._queue.put_nowait(span)
            self._stats["spans_emitted"] += 1
        except queue.Full:
            self._stats["spans_dropped"] += 1

        return span

    def auto_trace(
        self,
        span_type: SpanType = SpanType.SKILL_INVOCATION,
        name: Optional[str] = None,
        capture_args: bool = True,
        capture_return: bool = True
    ):
        """装饰器 - 自动追踪函数

        示例:
            @tracer.auto_trace(span_type=SpanType.SKILL_INVOCATION)
            def my_skill(input_data):
                return result

            # 自动发射:
            # - 调用时: span.start
            # - 返回时: span.finish(output=result)
            # - 异常时: span.finish(error=exc)
        """
        def decorator(func: Callable) -> Callable:
            span_name = name or func.__name__

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if not self.enabled or not self._should_sample():
                    return func(*args, **kwargs)

                # 准备输入数据
                input_data = None
                if capture_args:
                    input_data = {
                        "args": args,
                        "kwargs": kwargs
                    }

                # 创建 span
                span = self._create_span(
                    name=span_name,
                    span_type=span_type,
                    input_data=input_data
                )

                # 执行函数
                try:
                    result = func(*args, **kwargs)

                    # 完成 span
                    if capture_return:
                        span.finish(output=result)
                    else:
                        span.finish()

                    # 写入队列
                    try:
                        self._queue.put_nowait(span)
                        self._stats["spans_emitted"] += 1
                    except queue.Full:
                        self._stats["spans_dropped"] += 1

                    return result

                except Exception as e:
                    # 记录异常
                    span.finish(error=e)
                    try:
                        self._queue.put_nowait(span)
                        self._stats["spans_emitted"] += 1
                    except queue.Full:
                        self._stats["spans_dropped"] += 1
                    raise

            return wrapper
        return decorator

    def span(
        self,
        name: str,
        span_type: SpanType,
        metadata: Optional[Dict] = None
    ):
        """上下文管理器 - 手动控制 span 生命周期

        示例:
            with tracer.span("my_op", SpanType.TOOL_EXECUTION) as span:
                result = do_something()
                span.set_output(result)
        """
        return _SpanContext(self, name, span_type, metadata)

    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self._stats.copy()

    def flush(self):
        """刷新队列，等待所有 span 写入"""
        self._queue.join()

    def shutdown(self):
        """关闭 tracer，清理资源"""
        self._shutdown = True
        self.flush()
        if self._worker_thread:
            self._worker_thread.join(timeout=5.0)


class _SpanContext:
    """Span 上下文管理器"""

    def __init__(
        self,
        tracer: LightningTracer,
        name: str,
        span_type: SpanType,
        metadata: Optional[Dict] = None
    ):
        self.tracer = tracer
        self.name = name
        self.span_type = span_type
        self.metadata = metadata
        self.span: Optional[Span] = None

    def __enter__(self) -> Span:
        self.span = self.tracer._create_span(
            name=self.name,
            span_type=self.span_type,
            metadata=self.metadata
        )
        return self.span

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.span:
            self.span.finish(error=exc_val)
            try:
                self.tracer._queue.put_nowait(self.span)
                self.tracer._stats["spans_emitted"] += 1
            except queue.Full:
                self.tracer._stats["spans_dropped"] += 1


# 全局 tracer 实例
_default_tracer: Optional[LightningTracer] = None


def get_tracer(config: Optional[Dict] = None) -> LightningTracer:
    """获取全局 tracer 实例"""
    global _default_tracer
    if _default_tracer is None:
        _default_tracer = LightningTracer(config)
    return _default_tracer
