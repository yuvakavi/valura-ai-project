async def event_stream(generator):
    """
    Convert generator output into SSE format
    """

    async for event in generator:
        yield f"event: {event.get('event')}\n"
        yield f"data: {event.get('data')}\n\n"
