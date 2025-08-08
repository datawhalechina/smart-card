from functools import wraps
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from .span import get_current_span, Span


class TraceASGIMiddleware:
    """
    用于在 FastAPI 应用中添加追踪功能的 ASGI 中间件。
    示例使用方式:
        app = FastAPI()
        app.add_middleware(TraceASGIMiddleware)
    """

    def __init__(self, app: ASGIApp) -> None:
        """
        初始化 TraceASGIMiddleware 实例。

        :param app: ASGI 应用实例，该中间件将包裹此应用。
        """
        self.app = app

    @staticmethod
    async def my_receive(receive: Receive, span: Span):
        """
        包装原始的 receive 函数，在请求处理前后执行 Span 相关操作。

        :param receive: 原始的 ASGI receive 函数，用于接收请求消息。
        :param span: Span 实例，用于管理请求生命周期中的追踪操作。
        :return: 包装后的异步 receive 函数。
        """
        await span.request_before()

        @wraps(receive)
        async def my_receive():
            """
            包装后的 receive 函数，在接收请求消息后执行 Span 的 request_after 方法。

            :return: 接收到的请求消息。
            """
            message = await receive()
            await span.request_after(message)
            return message

        return my_receive

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        当中间件实例被调用时执行的方法，处理每个传入的请求。

        :param scope: 包含请求信息的 ASGI 范围对象。
        :param receive: 用于接收请求消息的 ASGI receive 函数。
        :param send: 用于发送响应消息的 ASGI send 函数。
        """
        # 如果请求类型不是 HTTP 请求，则直接将请求传递给下一个 ASGI 应用处理
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return

        # 使用上下文管理器获取当前的 Span 实例，并在请求处理完成后自动清理资源
        async with get_current_span(scope) as span:
            # 包装原始的 receive 函数
            handle_outgoing_receive = await self.my_receive(receive, span)

            async def handle_outgoing_request(message: 'Message') -> None:
                """
                包装原始的 send 函数，在发送响应消息前执行 Span 的 response 方法。

                :param message: 要发送的响应消息。
                """
                await span.response(message)
                await send(message)

            # 将处理后的 receive 和 send 函数传递给下一个 ASGI 应用
            await self.app(scope, handle_outgoing_receive, handle_outgoing_request)