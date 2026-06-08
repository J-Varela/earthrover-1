import { useEffect, useRef } from "react";

type Obstacle = {
  x: number;
  y: number;
};

type LidarScan = {
  angle: number;
  distance: number;
};

type Rover = {
  x: number;
  y: number;
  heading: number;
  path: [number, number][];
  lidar?: LidarScan[];
};

type Props = {
  rover: Rover;
  obstacles: Obstacle[];
};

export default function RoverCanvas({
  rover,
  obstacles,
}: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;

    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const scale = 40;

    // Keep rover centered on canvas
    const roverX = centerX;
    const roverY = centerY;
    const sensingRadius = 60;

    // lidar rays
    if (rover.lidar?.length) {
      rover.lidar.forEach((ray) => {
        const angle = (ray.angle * Math.PI) / 180;
        const endX = roverX + Math.cos(angle) * ray.distance * scale;
        const endY = roverY - Math.sin(angle) * ray.distance * scale;

        ctx.beginPath();
        ctx.moveTo(roverX, roverY);
        ctx.lineTo(endX, endY);
        ctx.strokeStyle = "rgba(0,255,255,0.4)";
        ctx.lineWidth = 1;
        ctx.stroke();
      });
    }
    // path
    const path = rover.path || [];

    if (path.length > 0) {
      ctx.beginPath();
      path.forEach((point, index) => {
        const x = centerX + (point[0] - rover.x) * scale;
        const y = centerY - (point[1] - rover.y) * scale;

        if (index === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });
      ctx.strokeStyle = "rgba(0, 0, 255, 0.6)";
      ctx.lineWidth = 2;
      ctx.stroke();
    }

    // obstacles
    obstacles.forEach((obs) => {
      const x = centerX + (obs.x - rover.x) * scale;
      const y = centerY - (obs.y - rover.y) * scale;
      const distance = Math.hypot(x - roverX, y - roverY);

      ctx.beginPath();
      ctx.arc(x, y, 8, 0, Math.PI * 2);
      ctx.fillStyle = distance <= sensingRadius ? "yellow" : "red";
      ctx.fill();
    });

    // rover
    ctx.beginPath();
    ctx.arc(roverX, roverY, 10, 0, Math.PI * 2);
    ctx.fillStyle = "blue";
    ctx.fill();

    

    
    ctx.beginPath();
    ctx.arc(roverX, roverY, sensingRadius, 0, Math.PI * 2);
    ctx.strokeStyle = "rgba(0,255,0,0.3)";
    ctx.stroke();

    // heading line
    const angle = (rover.heading * Math.PI) / 180;

    const lineX = roverX + Math.cos(angle) * 25;
    const lineY = roverY - Math.sin(angle) * 25;

    ctx.beginPath();
    ctx.moveTo(roverX, roverY);
    ctx.lineTo(lineX, lineY);
    ctx.stroke();
  }, [rover, obstacles]);

  return (
    <canvas
      ref={canvasRef}
      width={800}
      height={600}
      style={{
        border: "1px solid gray",
      }}
    />
  );
}