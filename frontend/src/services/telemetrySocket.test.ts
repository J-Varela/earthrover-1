import { afterEach, describe, expect, it, vi } from 'vitest'

import { buildTelemetryWebSocketUrl, createTelemetrySocket } from './telemetrySocket'

class FakeWebSocket {
  static instances: FakeWebSocket[] = []
  static CONNECTING = 0
  static OPEN = 1
  static CLOSING = 2
  static CLOSED = 3

  readonly url: string
  readyState = FakeWebSocket.CONNECTING
  onopen: (() => void) | null = null
  onmessage: ((event: MessageEvent<string>) => void) | null = null
  onerror: ((event: Event) => void) | null = null
  onclose: (() => void) | null = null

  constructor(url: string) {
    this.url = url
    FakeWebSocket.instances.push(this)
  }

  close() {
    this.readyState = FakeWebSocket.CLOSED
    this.onclose?.()
  }

  emitOpen() {
    this.readyState = FakeWebSocket.OPEN
    this.onopen?.()
  }
}

describe('buildTelemetryWebSocketUrl', () => {
  it('uses an explicit public websocket URL when provided', () => {
    expect(
      buildTelemetryWebSocketUrl({
        wsUrl: 'wss://rover.example.com/ws/telemetry',
        windowLocation: { protocol: 'http:', host: 'localhost:5173' },
      }),
    ).toBe('wss://rover.example.com/ws/telemetry')
  })

  it('falls back to the current browser origin websocket path', () => {
    expect(
      buildTelemetryWebSocketUrl({
        windowLocation: { protocol: 'https:', host: 'dashboard.example.com' },
      }),
    ).toBe('wss://dashboard.example.com/ws/telemetry')
  })
})

describe('createTelemetrySocket', () => {
  afterEach(() => {
    FakeWebSocket.instances = []
    vi.useRealTimers()
  })

  it('reconnects after the socket closes unexpectedly', () => {
    vi.useFakeTimers()

    createTelemetrySocket({
      reconnectDelayMs: 500,
      WebSocketImpl: FakeWebSocket as unknown as typeof WebSocket,
      windowLocation: { protocol: 'http:', host: 'localhost:5173' },
    })

    expect(FakeWebSocket.instances).toHaveLength(1)

    FakeWebSocket.instances[0].emitOpen()
    FakeWebSocket.instances[0].close()

    vi.advanceTimersByTime(500)

    expect(FakeWebSocket.instances).toHaveLength(2)
    expect(FakeWebSocket.instances[1].url).toBe('ws://localhost:5173/ws/telemetry')
  })
})
