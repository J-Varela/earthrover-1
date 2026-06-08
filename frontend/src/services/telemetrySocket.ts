type WindowLocationLike = {
  protocol: string
  host: string
}

type TelemetrySocketEventHandlers = {
  onOpen?: () => void
  onMessage?: (event: MessageEvent<string>) => void
  onError?: (event: Event) => void
  onClose?: () => void
}

type CreateTelemetrySocketOptions = TelemetrySocketEventHandlers & {
  wsUrl?: string
  reconnectDelayMs?: number
  WebSocketImpl?: typeof WebSocket
  windowLocation?: WindowLocationLike
}

export function buildTelemetryWebSocketUrl({
  wsUrl,
  windowLocation = window.location,
}: {
  wsUrl?: string
  windowLocation?: WindowLocationLike
} = {}): string {
  if (wsUrl) {
    return wsUrl
  }

  const wsProtocol = windowLocation.protocol === 'https:' ? 'wss:' : 'ws:'
  return `${wsProtocol}//${windowLocation.host}/ws/telemetry`
}

export function createTelemetrySocket({
  wsUrl,
  reconnectDelayMs = 1000,
  WebSocketImpl = WebSocket,
  windowLocation = window.location,
  onOpen,
  onMessage,
  onError,
  onClose,
}: CreateTelemetrySocketOptions = {}) {
  let socket: WebSocket | null = null
  let reconnectTimer: ReturnType<typeof setTimeout> | null = null
  let closedByClient = false

  const clearReconnectTimer = () => {
    if (reconnectTimer !== null) {
      clearTimeout(reconnectTimer)
      reconnectTimer = null
    }
  }

  const connect = () => {
    const nextSocket = new WebSocketImpl(
      buildTelemetryWebSocketUrl({ wsUrl, windowLocation }),
    )
    socket = nextSocket

    nextSocket.onopen = () => {
      onOpen?.()
    }

    nextSocket.onmessage = (event) => {
      onMessage?.(event as MessageEvent<string>)
    }

    nextSocket.onerror = (event) => {
      onError?.(event)
    }

    nextSocket.onclose = () => {
      onClose?.()
      if (closedByClient) {
        return
      }

      clearReconnectTimer()
      reconnectTimer = setTimeout(connect, reconnectDelayMs)
    }
  }

  connect()

  return {
    close() {
      closedByClient = true
      clearReconnectTimer()
      if (
        socket &&
        (socket.readyState === WebSocketImpl.OPEN ||
          socket.readyState === WebSocketImpl.CONNECTING)
      ) {
        socket.close()
      }
    },
  }
}
