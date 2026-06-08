import { useEffect, useState } from 'react'
import RoverCanvas from '../components/RoverCanvas'
import { api } from '../services/api'
import { createTelemetrySocket } from '../services/telemetrySocket'

type LidarScan = {
  angle: number
  distance: number
}

type RoverState = {
  x: number
  y: number
  heading: number
  path: [number, number][]
  lidar?: LidarScan[]
}

type Obstacle = {
  x: number
  y: number
}

export default function RoverDashboard() {
  const [rover, setRover] = useState<RoverState>({
    x: 0,
    y: 0,
    heading: 0,
    path: [[0, 0]] as [number, number][],
  })
  const [obstacles, setObstacles] = useState<Obstacle[]>([])
  const [wsStatus, setWsStatus] = useState<'connecting' | 'connected' | 'disconnected'>('connecting')

  async function sendCommand(command: string) {
    await api.post('/rover/command', {
      command,
    })

    const res = await api.get('/rover/telemetry')
    setRover(res.data)
  }

  useEffect(() => {
    let active = true

    const loadInitialData = async () => {
      try {
        const [worldRes, telemetryRes] = await Promise.all([
          api.get('/world'),
          api.get('/rover/telemetry'),
        ])

        if (!active) {
          return
        }

        setObstacles(worldRes.data.obstacles)
        setRover(telemetryRes.data)
      } catch (err) {
        console.error('Failed to load initial data:', err)
      }
    }

    const telemetrySocket = createTelemetrySocket({
      wsUrl: import.meta.env.VITE_WS_URL,
      onOpen: () => {
        if (!active) {
          return
        }

        console.info('Telemetry websocket connected')
        setWsStatus('connected')
      },
      onMessage: (event) => {
        if (!active) {
          return
        }

        setRover(JSON.parse(event.data))
      },
      onError: (event) => {
        if (!active) {
          return
        }

        console.error('WebSocket error:', event)
        setWsStatus('disconnected')
      },
      onClose: () => {
        if (!active) {
          return
        }

        console.info('Telemetry websocket closed')
        setWsStatus('disconnected')
      },
    })

    void loadInitialData()

    const handleKeyDown = (e: KeyboardEvent) => {
      switch (e.key.toLowerCase()) {
        case 'w':
          void sendCommand('forward')
          break
        case 's':
          void sendCommand('backward')
          break
        case 'a':
          void sendCommand('left')
          break
        case 'd':
          void sendCommand('right')
          break
        case ' ':
          void sendCommand('stop')
          break
      }
    }

    window.addEventListener('keydown', handleKeyDown)

    return () => {
      active = false
      telemetrySocket.close()
      window.removeEventListener('keydown', handleKeyDown)
    }
  }, [])

  return (
    <div>
      <h1>EarthRover-1</h1>

      <RoverCanvas rover={rover} obstacles={obstacles} />
      <div>
        <p>X: {rover.x}</p>
        <p>Y: {rover.y}</p>
        <p>Heading: {rover.heading}</p>
        <p>Connection: {wsStatus}</p>
        <div>
          <h2>LiDAR</h2>
          <p>Rays: {rover.lidar?.length ?? 0}</p>
          <p>
            Closest Object:{' '}
            {rover.lidar?.length
              ? Math.min(...rover.lidar.map((ray) => ray.distance)).toFixed(2)
              : 'N/A'}{' '}
            m
          </p>
        </div>
      </div>
    </div>
  )
}
